from django.db import models
from django.contrib.auth.models import User
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
    ('1', "初級"),
    ('2', "中級"),
    ('3', "上級"),
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
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    rating_story = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    rating_gimmick = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    rating_sukkiri = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    rating_level = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    release_date = models.DateField()
    end_date = models.DateField()
    creator = models.ForeignKey(CreatorModel, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    bookmarks = models.ManyToManyField(User, verbose_name="ブックマークユーザー", blank=True)
    playings = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateField()

    def __str__(self):
        return self.name
    
class ReviewModel(models.Model):
    user = models.ForeignKey(User, verbose_name="投稿者", on_delete=models.CASCADE)
    riddle = models.ForeignKey(RiddleModel, verbose_name="謎", on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    rating_story = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    rating_gimmick = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    rating_sukkiri = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    rating_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])