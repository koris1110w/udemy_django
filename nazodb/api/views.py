from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from nazoapp.models import RiddleModel


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