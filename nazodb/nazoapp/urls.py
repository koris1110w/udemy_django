from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done/', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('email/change/', views.EmailChange.as_view(), name='email_change'),
    path('email/change/done/', views.EmailChangeDone.as_view(), name='email_change_done'),
    path('email/change/complete/<str:token>/', views.EmailChangeComplete.as_view(), name='email_change_complete'),
    # path('signup/', views.signupfunc, name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('top/', views.TopView.as_view(), name='top'),
    path('list/', views.listfunc, name='list'),
    # path('list/', RiddleList.as_view(), name='list'),
    path('detail/<int:pk>', views.detailfunc, name='detail'),
    # path('detail/<int:pk>', RiddleDetail.as_view(), name='detail'),
    path('create/', views.RiddleCreate.as_view(), name='create'),
    path('delete/<int:pk>', views.RiddleDelete.as_view(), name='delete'),
    path('update/<int:pk>', views.RiddleUpdate.as_view(), name='update'),
    path('good/<int:pk>', views.goodfunc, name='good'),
    path('playing/<int:pk>', views.playingfunc, name='playing'),
    path('creator/<int:pk>', views.CreatorDetail.as_view(), name='creator'),
    path('bookmark/<int:pk>', views.bookmarkfunc, name='bookmark'),
    path('removebookmark/<int:pk>', views.removebookmarkfunc, name='removebookmark'),
    path('mypage/', views.MyPageView.as_view(), name='mypage'),
    path('test/', views.TestView.as_view(), name='test'),


    # 非同期通信
    path('api/v1/bookmark/<int:pk>/', views.bookmark_request, name="api_bookmark")
]
