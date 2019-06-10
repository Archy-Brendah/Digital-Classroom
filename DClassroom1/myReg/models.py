from django.db import models
from django.utils import timezone

user=models.ForeignKey('auth.User',on_delete=models.CASCADE)
# Create your models here.
