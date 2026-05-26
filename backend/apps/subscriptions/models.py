from django.db import models
from django.conf import settings


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    # -1 means unlimited
    contact_views_allowed = models.IntegerField(default=0)
    can_initiate_chat = models.BooleanField(default=False)

    class Meta:
        db_table = 'subscription_plans'

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name='user_subscriptions',
    )
    starts_at = models.DateTimeField()
    # Indexed — daily cron job queries this to downgrade expired accounts
    expires_at = models.DateTimeField(db_index=True)
    contact_views_used = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'user_subscriptions'

    def is_active(self):
        from django.utils import timezone
        return self.expires_at > timezone.now()

    def __str__(self):
        return f'{self.user} — {self.plan.name}'
