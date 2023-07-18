from django.contrib.auth import get_user_model
from django.db import models

Client = get_user_model()


class Match(models.Model):
    initiator = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='confirmers',
    )
    confirmer = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='initiators'
    )
    is_accepted = models.BooleanField(default=False)
    is_declined = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Совпадения'
        verbose_name = 'Совпадение'
        constraints = [
            models.UniqueConstraint(
                fields=['initiator', 'confirmer'],
                name='unique_initiator_confirmer'
            )
        ]

    def __str__(self):
        return f'{self.initiator} - {self.confirmer}'
