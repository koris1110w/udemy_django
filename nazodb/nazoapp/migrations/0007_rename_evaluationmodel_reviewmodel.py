# Generated by Django 5.0.2 on 2024-03-07 13:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nazoapp', '0006_evaluationmodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EvaluationModel',
            new_name='ReviewModel',
        ),
    ]
