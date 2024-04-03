from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from nazoapp.models import RiddleModel
from . import serializer
from . import pagination


class APIHelloView(APIView):
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        return Response(status=200, data={
            "あいさつ": "hello"
        })

    def post(self, *args, **kwargs):

        return Response(status=200, data={
            "あいさつ": "Bye"
        })

class APIBookMarkView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        return Response(status=200, data={
            "あいさつ": "hello"
        })

    def post(self, *args, **kwargs):
        pk = kwargs.get('pk')
        object = get_object_or_404(RiddleModel, pk=pk)

        if not self.request.user in object.bookmarks.all():
            object.bookmarks.add(self.request.user)
            object.save()
            return Response({'status': 'success', 'is_add': True}, status=200)
        else:
            object.bookmarks.remove(self.request.user)
            object.save()
            return Response({'status': 'success', 'is_add': False}, status=200)


class APIRankingView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = RiddleModel.objects.order_by('rating').reverse()[0:5]
    serializer_class = serializer.RiddleSerializer

    # pagination_class = pagination.StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        # フィルター条件の取得
        type = request.GET.get('type')
        if type:
            queryset = RiddleModel.objects.filter(type=type)
        else:
            queryset = RiddleModel.objects.all()

        return Response(data=serializer.RiddleSerializer(instance=queryset, many=True).data, status=200)