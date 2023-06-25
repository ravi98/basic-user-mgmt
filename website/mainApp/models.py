from typing import Optional, Any

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):

    def create_user(self, username: str, email: Optional[str], password: Optional[str], **extra_fields: Any):
        user=self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        default_group=Group.objects.get(name='default')
        print(f"saving in user manager, {default_group.name}, {default_group.permissions.all()}")
        user.save(using=self._db)
        default_group.user_set.add(user)

        return user
    
    # def create_superuser(self, username: str, email: Optional[str], password: Optional[str], **extra_fields: Any):
    #     user=self.model(username=username, email=self.normalize_email(email), **extra_fields)
    #     user.set_password(password)
    #     user.is_staff=True
    #     user.is_superuser=True
    #     mod_group=Group.objects.get(name='mod')
    #     user.save(using=self._db)
    #     mod_group.user_set.add(user)

    #     return user
        

class User(AbstractUser):
    objects=CustomUserManager()

    def __str__(self):
        return self.get_full_name()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
