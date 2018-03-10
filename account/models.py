from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class UserManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, username):
        return self.get(**{f"{self.model.USERNAME_FIELD}__iexact": username})


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=200)

    nick_name = models.CharField(max_length=30, null=True)
    real_name = models.CharField(max_length=30, null=True)

    create_time = models.DateTimeField(auto_now_add=True, null=True)

    reset_password_token = models.CharField(max_length=40, null=True)
    active_account_token = models.CharField(max_length=40, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'user'
        ordering = ('id',)
