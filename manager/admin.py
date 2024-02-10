from django.contrib import admin
from .models import University, Major, Category, Activity, CustomUser
# Register your models here.

admin.site.register(University)
admin.site.register(Major)
admin.site.register(Category)
admin.site.register(Activity)
admin.site.register(CustomUser)