from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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
        permissions = [('view_statistics', 'View extra statistics')]


@receiver(post_save, sender=CustomUser)
def save_user(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='Users'))
