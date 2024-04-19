from django_filters import rest_framework as filters
from django.db.models import Q
from web import models

FILTER_SET = (
    ("created_at", "新着順"),
    ("rating", "評価順"),
    ("playings", "プレイ数順"),
    ("level", "難易度順"),
)

class RiddleFilter(filters.FilterSet):
    type = filters.MultipleChoiceFilter(choices=models.TYPE_SET)
    time = filters.MultipleChoiceFilter(choices=models.TIME_SET)
    level = filters.MultipleChoiceFilter(choices=models.LEVEL_SET)
    word = filters.CharFilter(method='wordFilter')
    order = filters.CharFilter(method='order')

    class Meta:
        model = models.RiddleModel
        fields = ['type','time','level','word',]

    def wordFilter(self,queryset,name,value):
        #ここでOR検索を入れる。fieldsのcustomerNameに入ってきた値を利用
        return queryset.filter(Q(name__icontains=value)|Q(description__icontains=value))
    
    def order(self,queryset,name,value):
        return queryset.order_by(value)
