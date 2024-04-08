from django_filters import rest_framework as filters
from django.db.models import Q
from nazoapp import models

class RiddleFilter(filters.FilterSet):
    type = filters.MultipleChoiceFilter(choices=models.TYPE_SET)
    time = filters.MultipleChoiceFilter(choices=models.TIME_SET)
    level = filters.MultipleChoiceFilter(choices=models.LEVEL_SET)
    word = filters.CharFilter(method='wordFilter') 

    class Meta:
        model = models.RiddleModel
        fields = ['type','time','level','word',]

    def wordFilter(self,queryset,name,value):
        #ここでOR検索を入れる。fieldsのcustomerNameに入ってきた値を利用
        return queryset.filter(Q(name__icontains=value)|Q(description__icontains=value))