from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.
class CustomUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True)
    avatar = models.ImageField(upload_to='profile/', default='default.png')
    birthday = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=0)

    def str(self):
        return self.username

    class Meta(AbstractUser.Meta):
        pass
