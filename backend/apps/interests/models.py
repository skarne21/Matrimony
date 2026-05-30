from django.db import models
from django.conf import settings


class InterestStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ACCEPTED = 'accepted', 'Accepted'
    DECLINED = 'declined', 'Declined'
    WITHDRAWN = 'withdrawn', 'Withdrawn'


class Interest(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_interests',
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_interests',
    )
    status = models.CharField(
        max_length=15,
        choices=InterestStatus.choices,
        default=InterestStatus.PENDING,
    )
    message = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'interests'
        # Prevents a user from sending more than one interest to the same person
        unique_together = [('sender', 'receiver')]

    def __str__(self):
        return f'{self.sender} → {self.receiver} ({self.status})'
