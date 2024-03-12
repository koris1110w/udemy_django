from django.contrib import admin
from django.urls import path
from .views import signupfunc, loginfunc, topfunc, listfunc, logoutfunc, detailfunc, goodfunc, playingfunc, creatorfunc, bookmarkfunc, removebookmarkfunc, mypagefunc, RiddleList, RiddleDetail, RiddleCreate, RiddleDelete, RiddleUpdate

urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('logout', logoutfunc, name='logout'),
    path('top/', topfunc, name='top'),
    path('list/', listfunc, name='list'),
    # path('list/', RiddleList.as_view(), name='list'),
    path('detail/<int:pk>', detailfunc, name='detail'),
    # path('detail/<int:pk>', RiddleDetail.as_view(), name='detail'),
    path('create/', RiddleCreate.as_view(), name='create'),
    path('delete/<int:pk>', RiddleDelete.as_view(), name='delete'),
    path('update/<int:pk>', RiddleUpdate.as_view(), name='update'),
    path('good/<int:pk>', goodfunc, name='good'),
    path('playing/<int:pk>', playingfunc, name='playing'),
    path('creator/<int:pk>', creatorfunc, name='creator'),
    path('bookmark/<int:pk>', bookmarkfunc, name='bookmark'),
    path('removebookmark/<int:pk>', removebookmarkfunc, name='removebookmark'),
    path('mypage/', mypagefunc, name='mypage'),
]
