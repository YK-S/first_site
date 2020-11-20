from django.contrib import admin
from vote import models
# Register your models here.
admin.site.register(models.Item)
admin.site.register(models.Vote)
admin.site.register(models.User)