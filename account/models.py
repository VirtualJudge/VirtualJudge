from django.db import models


class UserProfile(models.Model):
    accepted_problem_number = models.IntegerField(default=0)
    submission_number = models.IntegerField(default=0)


class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=200)
    real_name = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=254, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    reset_password_token = models.CharField(max_length=40, null=True)
    active_account_token = models.CharField(max_length=40, null=True)
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
