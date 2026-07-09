from django.conf import settings
from django.db import models


class EmailConfirmationCode(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='email_confirmation_code')
    code = models.CharField(max_length=6)
    def __str__(self):
        return f"{self.user.username} - {self.code}"