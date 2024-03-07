from django.contrib import admin
from .models import RiddleModel, CreatorModel, ReviewModel

# Register your models here.
admin.site.register(RiddleModel)
admin.site.register(CreatorModel)
admin.site.register(ReviewModel)