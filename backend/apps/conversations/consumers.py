import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        qs = dict(
            pair.split('=', 1) for pair in
            self.scope['query_string'].decode().split('&')
            if '=' in pair
        )
        self.user = await self._get_user(qs.get('token', ''))
        if not self.user:
            await self.close()
            return

        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']

        if not await self._is_participant():
            await self.close()
            return

        self.group = f'chat_{self.conversation_id}'
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group'):
            await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data.get('message', '').strip()
        if not text:
            return

        msg = await self._save_message(text)
        await self.channel_layer.group_send(self.group, {
            'type': 'chat_message',
            'payload': {
                'id': msg.id,
                'sender_id': str(self.user.id),
                'content_text': msg.content_text,
                'is_read': False,
                'created_at': msg.created_at.isoformat(),
            },
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['payload']))

    @database_sync_to_async
    def _get_user(self, token):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            payload = AccessToken(token)
            return User.objects.get(id=payload['user_id'])
        except Exception:
            return None

    @database_sync_to_async
    def _is_participant(self):
        from .models import Conversation
        try:
            conv = Conversation.objects.get(id=self.conversation_id)
            return self.user in (conv.user_one, conv.user_two)
        except Conversation.DoesNotExist:
            return False

    @database_sync_to_async
    def _save_message(self, text):
        from .models import Conversation, Message
        conv = Conversation.objects.get(id=self.conversation_id)
        msg = Message.objects.create(conversation=conv, sender=self.user, content_text=text)
        conv.last_message_at = timezone.now()
        conv.save(update_fields=['last_message_at'])
        return msg
