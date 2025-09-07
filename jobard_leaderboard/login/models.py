from django.contrib.auth.models import AbstractUser
from django.db import models
from leaderboard.models import Driver

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='users', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email