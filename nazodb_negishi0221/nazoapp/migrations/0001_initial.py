# Generated by Django 5.0.2 on 2024-02-18 00:49

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreatorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('image', models.FileField(upload_to='')),
                ('url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RiddleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('image', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('web', 'WEB'), ('line', 'LINE')], max_length=10)),
                ('time', models.IntegerField()),
                ('level', models.CharField(choices=[('easy', '初級'), ('normal', '中級'), ('hard', '上級')], max_length=10)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('release_date', models.DateField()),
                ('end_date', models.DateField()),
                ('url', models.CharField(max_length=255)),
                ('good', models.IntegerField()),
                ('read', models.IntegerField()),
                ('readtext', models.TextField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nazoapp.creatormodel')),
            ],
        ),
    ]
