from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .managers import UserManager


class User(AbstractBaseUser):
    """
    用户
    """
    username = models.CharField("账号", max_length=64, unique=True)
    email = models.EmailField("邮箱", null=True, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    is_active = models.BooleanField("是否有效", default=True)
    is_admin = models.BooleanField("是否为管理员", default=False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
