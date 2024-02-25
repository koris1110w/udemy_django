from .models import RiddleModel, CreatorModel
from .forms import UserForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

def signupfunc(request):
    form = UserForm(request.POST)  
    if form.is_valid():  
        username = form.cleaned_data['username']  
        password = form.cleaned_data['password']
        try:
            user = User.objects.create_user(username, '', password)
            return render(request, 'signup.html', {})
        except IntegrityError:
            return render(request, 'signup.html', {"error":'このユーザーはすでに登録されています'})
    else:
        return render(request, 'signup.html', {})

def loginfunc(request):
    form = UserForm(request.POST)  
    if form.is_valid():  
        username = form.cleaned_data['username']  
        password = form.cleaned_data['password']
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

def mypagefunc(request):
    object_list = RiddleModel.objects.filter(bookmarks=request.user.pk)
    return render(request, 'mypage.html', {'object_list': object_list})

# @login_required
def listfunc(request):
    object_list = RiddleModel.objects.all()
    return render(request, 'list.html', {'object_list': object_list})

def detailfunc(request, pk):
    object = get_object_or_404(RiddleModel, pk=pk)
    return render(request, 'detail.html', {'object': object})

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

def bookmarkfunc(request, pk):
    object = RiddleModel.objects.get(pk=pk)
    # アクセスしたユーザーをbookmarksに追加する
    object.bookmarks.add(request.user)
    object.save()
    return redirect('detail', pk=pk)

def creatorfunc(request, pk):
    creator = get_object_or_404(CreatorModel, pk=pk)
    object_list = RiddleModel.objects.filter(creator=creator)
    return render(request, 'creator.html', {'creator': creator ,'object_list': object_list})

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