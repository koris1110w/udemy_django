from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()
TYPE_SET = (
    ("web", "WEB"),
    ("line", "LINE"),
)
TIME_SET = (
    ("10", "〜15分"),
    ("30", "15分〜45分"),
    ("60", "45分〜90分"),
    ("120", "90分〜180分"),
    ("300", "180分〜"),
)
LEVEL_SET = (
    ('easy', "初級"),
    ('normal', "中級"),
    ('hard', "上級"),
)

class CreatorModel(models.Model):
    name = models.CharField(max_length=120)
    image = models.FileField()
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class RiddleModel(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='')
    description = models.TextField()
    type = models.CharField(choices=TYPE_SET, max_length=10)
    time = models.CharField(choices=TIME_SET, max_length=10)
    level = models.CharField(choices=LEVEL_SET, max_length=10)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    release_date = models.DateField()
    end_date = models.DateField()
    creator = models.ForeignKey(CreatorModel, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    bookmarks = models.ManyToManyField(User, verbose_name="ブックマークユーザー", blank=True)
    playings = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name