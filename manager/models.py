from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Major(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('counselor', 'Counselor'),
    ]

    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=60)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['name', 'role']
    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def get_by_natural_key(self):
        return (self.username,)
    

class Manager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)