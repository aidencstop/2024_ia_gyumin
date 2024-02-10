from django.db import models
from manager.models import CustomUser
# Create your models here.

class Counselor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)