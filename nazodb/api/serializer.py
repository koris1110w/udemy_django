from rest_framework import serializers
from nazoapp.models import RiddleModel

class RiddleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiddleModel
        fields = "__all__"
        read_only_fields = ('id',)