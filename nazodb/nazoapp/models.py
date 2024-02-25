from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
User = get_user_model()

class CreatorModel(models.Model):
    name = models.CharField(max_length=120)
    image = models.FileField()
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class RiddleModel(models.Model):
    TYPE_SET = (
        ("web", "WEB"),
        ("line", "LINE"),
    )
    LEVEL_SET = (
        ('easy', "初級"),
        ('normal', "中級"),
        ('hard', "上級"),
    )
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='')
    description = models.TextField()
    type = models.CharField(choices=TYPE_SET, max_length=10)
    time = models.IntegerField()
    level = models.CharField(choices=LEVEL_SET, max_length=10)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    release_date = models.DateField()
    end_date = models.DateField()
    creator = models.ForeignKey(CreatorModel, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    # good =models.IntegerField(null=True, blank=True, default=0)
    # read =models.IntegerField(null=True, blank=True, default=0)
    # readtext =models.TextField(null=True, blank=True, default='')
    bookmarks = models.ManyToManyField(User, verbose_name="ブックマークユーザー", blank=True)
    playings = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name