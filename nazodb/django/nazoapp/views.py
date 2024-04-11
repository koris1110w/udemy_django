from django.views.decorators.csrf import csrf_exempt

from .models import RiddleModel, CreatorModel, ReviewModel
from .forms import LoginForm, FilterListForm, ListFilterForm, ReviewForm, UserCreateForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm, EmailChangeForm
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView, FormView
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Q, Avg
from django.template.loader import render_to_string

User = get_user_model()

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

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'login.html'

class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'top.html'

class UserCreate(CreateView):
    """ユーザー仮登録"""
    template_name = 'user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('mail_template/create/subject.txt', context)
        message = render_to_string('mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('user_create_done')


class UserCreateDone(TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'user_create_done.html'


class UserCreateComplete(TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()

class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'password_change_done.html'

class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'mail_template/password_reset/subject.txt'
    email_template_name = 'mail_template/password_reset/message.txt'
    template_name = 'password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'password_reset_complete.html'

class EmailChange(LoginRequiredMixin, FormView):
    """メールアドレスの変更"""
    template_name = 'email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string('mail_template/email_change/subject.txt', context)
        message = render_to_string('mail_template/email_change/message.txt', context)
        send_mail(subject, message, None, [new_email])

        return redirect('email_change_done')


class EmailChangeDone(LoginRequiredMixin, TemplateView):
    """メールアドレスの変更メールを送ったよ"""
    template_name = 'email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin, TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""
    template_name = 'email_change_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)

# def signupfunc(request):
#     form = UserForm(request.POST)  
#     if form.is_valid():  
#         username = form.cleaned_data['username']  
#         password = form.cleaned_data['password']
#         try:
#             user = User.objects.create_user(username, '', password)
#             return render(request, 'signup.html', {})
#         except IntegrityError:
#             return render(request, 'signup.html', {"error":'このユーザーはすでに登録されています'})
#     else:
#         return render(request, 'signup.html', {})

# def loginfunc(request):
#     form = UserForm(request.POST)  
#     if form.is_valid():  
#         username = form.cleaned_data['username']  
#         password = form.cleaned_data['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('list')
#         else:
#             return render(request, 'login.html', {})
#     else:
#         return render(request, 'login.html', {})

# def logoutfunc(request):
#     logout(request)
#     return redirect('login')

# def mypagefunc(request):
#     object_list = RiddleModel.objects.filter(bookmarks=request.user.pk)
#     return render(request, 'mypage.html', {'object_list': object_list})

# def topfunc(request):
#     data = RiddleModel.objects.order_by("created_at").all()
#     ranking_list = data.order_by('rating').reverse()[0:5]
#     page_obj = data[0:10]
#     context = {
#         'ranking_list': ranking_list,
#         'page_obj': page_obj,
#     }
#     return render(request, 'top.html', context)

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
        'form': form,

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

# def creatorfunc(request, pk):
#     creator = get_object_or_404(CreatorModel, pk=pk)
#     object_list = RiddleModel.objects.filter(creator=creator)
#     return render(request, 'creator.html', {'creator': creator ,'object_list': object_list})

class TopView(ListView):
    template_name = 'top.html'
    queryset = RiddleModel.objects.order_by("created_at").all()[0:10]
    context_object_name = "page_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ranking_list"] = RiddleModel.objects.order_by("rating").reverse()[0:10]
        return context

class MyPageView(ListView):
    template_name = 'mypage.html'
    context_object_name = "page_obj"

    def get_queryset(self):
        return RiddleModel.objects.filter(bookmarks=self.request.user.pk)
    

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
    context_object_name = "creator"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_obj"] = RiddleModel.objects.filter(creator=kwargs['object'])
        return context

class TestView(TemplateView):
    template_name = 'test.html'

@csrf_exempt
def bookmark_request(request, pk):
    object = get_object_or_404(RiddleModel, pk=pk)

    if not request.user in object.bookmarks.all():
        object.bookmarks.add(request.user)
        object.save()
        return JsonResponse({'status': 'success', 'is_add': True}, status=200)
    else:
        object.bookmarks.remove(request.user)
        object.save()
        return JsonResponse({'status': 'success', 'is_add': False}, status=200)

