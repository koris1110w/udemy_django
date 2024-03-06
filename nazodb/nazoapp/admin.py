from django.contrib import admin
from .models import RiddleModel, CreatorModel, EvaluationModel

# Register your models here.
admin.site.register(RiddleModel)
admin.site.register(CreatorModel)
admin.site.register(EvaluationModel)