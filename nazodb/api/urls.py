from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("", views.APIHelloView.as_view(), name="api_hello"),
    path("bookmark/<int:pk>/", views.APIBookMarkView.as_view(), name="api_bookmark"),
    path('ranking/', views.APIRankingView.as_view(), name='api_ranking'),
    path('riddle_list/', views.APIRiddleListView.as_view(), name='api_list'),
]