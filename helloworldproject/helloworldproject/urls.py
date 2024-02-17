from django.contrib import admin
from django.urls import path, include
from .views import helloworldfunction, helloworldClass

urlpatterns = [
    path('admin/', admin.site.urls),
    path('helloworld/', helloworldfunction),
    path('helloworld2/', helloworldClass.as_view()),
    path('helloapp/', include('helloworldapp.urls'))
]
