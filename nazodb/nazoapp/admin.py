from django.contrib import admin
from .models import RiddleModel, CreatorModel

# Register your models here.
admin.site.register(RiddleModel)
admin.site.register(CreatorModel)