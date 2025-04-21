from django.db import models
from django.contrib.auth.models import User
from blogs.models import Category

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    categories = models.ManyToManyField(Category, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
