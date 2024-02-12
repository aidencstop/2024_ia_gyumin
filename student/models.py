from django.db import models
from manager.models import CustomUser, University, Major, Category, Activity

# Create your models here.

class Student(models.Model):
    GRADE_CHOICES = [
        (1, 'Grade 1'),
        (2, 'Grade 2'),
        (3, 'Grade 3'),
        (4, 'Grade 4'),
        (5, 'Grade 5'),
        (6, 'Grade 6'),
        (7, 'Grade 7'),
        (8, 'Grade 8'),
        (9, 'Grade 9'),
        (10, 'Grade 10'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    grade = models.IntegerField(choices=GRADE_CHOICES)
    # university = models.CharField(max_length=60, choices=[(university.name, university.name) for university in University.objects.all()])
    university = models.ForeignKey(University, on_delete=models.CASCADE, default=None)
    # major = models.CharField(max_length=60, choices=[(major.name, major.name) for major in Major.objects.all()])
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    activity = models.ManyToManyField(Activity, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=250, null = True)

    def __str__(self):
        return self.user.username


class ActivityExperience(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(default='2000-01-01', null=True, blank=True)
    end_date = models.DateField(default='2000-01-01', null=True, blank=True)
    description = models.TextField(max_length=250, null=True)

    def __str__(self):
        return self.activity.name