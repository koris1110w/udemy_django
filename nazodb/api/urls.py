from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("", views.APIHelloView.as_view(), name="hello"),
    path("bookmark/<int:pk>/", views.APIBookMarkView.as_view(), name="bookmark"),
    path('ranking/', views.APIRankingView.as_view(), name='ranking'),
]