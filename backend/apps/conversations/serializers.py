from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.UUIDField(source='sender.id', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender_id', 'content_text', 'is_read', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'other_user', 'last_message', 'unread_count', 'last_message_at']

    def get_other_user(self, obj):
        me = self.context['request'].user
        other = obj.user_two if obj.user_one == me else obj.user_one
        try:
            p = other.profile
            return {
                'id': str(other.id),
                'name': f'{p.first_name} {p.last_name}',
                'photo': p.profile_pic_url or None,
                'city': p.city or '',
            }
        except Exception:
            return {'id': str(other.id), 'name': 'Unknown', 'photo': None, 'city': ''}

    def get_last_message(self, obj):
        msg = obj.messages.order_by('-created_at').first()
        if not msg:
            return None
        return {
            'text': msg.content_text,
            'created_at': msg.created_at,
            'sender_id': str(msg.sender_id),
        }

    def get_unread_count(self, obj):
        me = self.context['request'].user
        return obj.messages.filter(is_read=False).exclude(sender=me).count()
