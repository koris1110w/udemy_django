from .models import RiddleModel, CreatorModel, ReviewModel
from .forms import UserForm, FilterListForm, ReviewForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.db.models import Q, Avg

def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

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

def topfunc(request):
    data = RiddleModel.objects.order_by("created_at").all()
    ranking_list = data.order_by('rating').reverse()[0:5]
    page_obj = data[0:10]
    context = {
        'ranking_list': ranking_list,
        'page_obj': page_obj,
    }
    return render(request, 'top.html', context)

# @login_required
def listfunc(request):
    # 検索のときはGETで取得します。
    form = FilterListForm(request.GET or None)

    # object_list = RiddleModel.objects.all()
    data = RiddleModel.objects.order_by("id").all()
    ranking_list = data.order_by('rating').reverse()[0:5]

    if form.is_valid():
        name = form.cleaned_data['name']
        type = form.cleaned_data['type']
        time = form.cleaned_data['time']
        level = form.cleaned_data['level']
        order = form.cleaned_data['order']

        filter_kwargs = {}
        if type:
            filter_kwargs["type__in"] = type
        if time:
            filter_kwargs['time__in'] = time
        if level:
            filter_kwargs['level__in'] = level

        data = data.filter(**filter_kwargs)
        
        if name:
            data = data.filter(Q(name__icontains=name)|Q(description__icontains=name))

        if order:
            data = data.order_by(order).reverse()

    page_cnt = 2 #一画面あたり10コ表示する
    onEachSide = 2 #選択ページの両側には3コ表示する
    onEnds = 2 #左右両端には2コ表示する
    paginater = Paginator(data, page_cnt)
    page = int(request.GET.get('page', 1)) # 表示したいページ
    page_obj = paginater.get_page(page)
    page_list = page_obj.paginator.get_elided_page_range(page, on_each_side=onEachSide, on_ends=onEnds)

    context = {
        'ranking_list': ranking_list,
        'page_obj': page_obj,
        'page_list': page_list,
        'form': form
    }
    return render(request, 'list.html', context)

def detailfunc(request, pk):
    form = ReviewForm(request.POST)
    object = get_object_or_404(RiddleModel, pk=pk)
    try:
        reviewed = ReviewModel.objects.filter(user=request.user, riddle=object)
    except:
        reviewed = None
    context = {
        'object': object,
        'form': form,
        'reviewed': reviewed,
    }
    if reviewed != []:
        if form.is_valid():
            rating = form.cleaned_data['rating']
            rating_story = form.cleaned_data['rating_story']
            rating_gimmick = form.cleaned_data['rating_gimmick']
            rating_sukkiri = form.cleaned_data['rating_sukkiri']
            rating_level = form.cleaned_data['rating_level']
            
            try:
                review = ReviewModel.objects.create(user=request.user, riddle=object, rating=rating, rating_story=rating_story, rating_gimmick=rating_gimmick, rating_sukkiri=rating_sukkiri, rating_level=rating_level)
                object.rating = ReviewModel.objects.filter(riddle=object).aggregate(Avg("rating"))["rating__avg"]
                object.rating_story = ReviewModel.objects.filter(riddle=object).aggregate(Avg("rating_story"))["rating_story__avg"]
                object.rating_gimmick = ReviewModel.objects.filter(riddle=object).aggregate(Avg("rating_gimmick"))["rating_gimmick__avg"]
                object.rating_sukkiri = ReviewModel.objects.filter(riddle=object).aggregate(Avg("rating_sukkiri"))["rating_sukkiri__avg"]
                object.rating_level = ReviewModel.objects.filter(riddle=object).aggregate(Avg("rating_level"))["rating_level__avg"]
                object.save()
                return render(request, 'detail.html', context)
            except IntegrityError:
                return render(request, 'detail.html', context)

    return render(request, 'detail.html', context)

def goodfunc(request, pk):
    object = RiddleModel.objects.get(pk=pk)
    object.good += 1
    object.save()
    return redirect('detail', pk=pk)

def playingfunc(request, pk):
    object = RiddleModel.objects.get(pk=pk)
    object.playings += 1
    object.save()
    return redirect(object.url)

def bookmarkfunc(request, pk):
    object = RiddleModel.objects.get(pk=pk)
    # アクセスしたユーザーをbookmarksに追加する
    object.bookmarks.add(request.user)
    object.save()
    return redirect('detail', pk=pk)

def removebookmarkfunc(request, pk):
    object = RiddleModel.objects.get(pk=pk)
    # アクセスしたユーザーをbookmarksに追加する
    object.bookmarks.remove(request.user)
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