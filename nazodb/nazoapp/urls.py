from django.contrib import admin
from django.urls import path
from .views import signupfunc, loginfunc, listfunc, logoutfunc, detailfunc, goodfunc, readfunc, creatorfunc, bookmarkfunc, RiddleList, RiddleDetail, RiddleCreate, RiddleDelete, RiddleUpdate

urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('logout', logoutfunc, name='logout'),
    path('list/', listfunc, name='list'),
    # path('list/', RiddleList.as_view(), name='list'),
    path('detail/<int:pk>', detailfunc, name='detail'),
    # path('detail/<int:pk>', RiddleDetail.as_view(), name='detail'),
    path('create/', RiddleCreate.as_view(), name='create'),
    path('delete/<int:pk>', RiddleDelete.as_view(), name='delete'),
    path('update/<int:pk>', RiddleUpdate.as_view(), name='update'),
    path('good/<int:pk>', goodfunc, name='good'),
    path('read/<int:pk>', readfunc, name='read'),
    path('creator/<int:pk>', creatorfunc, name='creator'),
    path('bookmark/<int:pk>', bookmarkfunc, name='bookmark'),
]
