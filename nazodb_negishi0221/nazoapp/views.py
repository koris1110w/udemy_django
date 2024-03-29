from .models import RiddleModel, CreatorModel
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

def signupfunc(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.create_user(username, '', password)
            return render(request, 'signup.html', {})
        except IntegrityError:
            return render(request, 'signup.html', {"error":'このユーザーはすでに登録されています'})
    return render(request, 'signup.html', {})

def loginfunc(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return render(request, 'login.html', {})
    else:
        return render(request, 'login.html', {})
    
def logoutfunc(request):
    logout(request)
    return redirect('login')

# @login_required
def listfunc(request):
    object_list = RiddleModel.objects.all()
    return render(request, 'list.html', {'object_list': object_list})

def detailfunc(request, pk):
    object = get_object_or_404(RiddleModel, pk=pk)

    # アクセスしてきたユーザーを既読に追加する
    object.users.add(request.user)
    object.save()

    # 既読のユーザーを取り出してきて数を数える
    read_count = object.users.all().count()
    context = {
        'object': object,
        'read_count': read_count
    }
    return render(request, 'detail.html', context)

def goodfunc(request, pk):
    object = RiddleModel.objects.get(pk=pk)
    object.good += 1
    object.save()
    return redirect('detail', pk=pk)

def readfunc(request, pk):
    object = RiddleModel.objects.get(pk=pk)
    username = request.user.get_username()
    if username in object.readtext:
        return redirect('detail', pk=pk)
    else:
        object.read += 1
        object.readtext = object.readtext + ' ' + username
        object.save()
        return redirect('detail', pk=pk)

class RiddleList(ListView):
    template_name = 'list.html'
    model = RiddleModel

class RiddleDetail(DetailView):
    template_name = 'detail.html'
    model = RiddleModel

class RiddleCreate(CreateView):
    template_name = 'create.html'
    model = RiddleModel
    fields = "__all__"
    success_url = reverse_lazy('list')

class RiddleDelete(DeleteView):
    template_name = 'delete.html'
    model = RiddleModel
    success_url = reverse_lazy('list')

class RiddleUpdate(UpdateView):
    template_name = 'update.html'
    model = RiddleModel
    fields = '__all__'
    success_url = reverse_lazy('list')

class CreatorDetail(DetailView):
    template_name = 'creator.html'
    model = CreatorModel


#根岸修正