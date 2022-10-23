from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
import requests
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
import datetime
from magazine import models
from magazine.forms import BargainingForms, ProfileForms
from faker import Faker



def exchange(request):
    response = requests.get(url='https://api.exchangerate-api.com/v4/latest/USD').json()
    currencies = response.get('rates')

    if request.method == 'GET':
        context = {
            'currencies': currencies
        }

        return render(request=request, template_name='front/converter.html', context=context)

    if request.method == 'POST':
        from_amount = float(request.POST.get('from-amount'))
        from_curr = request.POST.get('from-curr')
        to_curr = request.POST.get('to-curr')

        converted_amount = round((currencies[to_curr] / currencies[from_curr]) * float(from_amount), 2)

        context = {
            'from_curr': from_curr,
            'to_curr': to_curr,
            'from_amount': from_amount,
            'currencies': currencies,
            'converted_amount': converted_amount
        }

        return render(request=request, template_name='front/converter.html', context=context)


def home(request):
    return render(request=request, template_name='front/base.html')


# def fake_create_user(request):
#     for _ in range(100):
#         fake_user.delay()
#     return redirect('/')
#
#
# def fake_create_posts(request):
#     for u in User.objects.all():
#         for _ in range(1000):
#             fake_post.delay(u.id)
#     return redirect('/')


def profile(request, user_name):
    try:
        p = int(request.GET.get('p', 1))
    except ValueError:
        p = 1

    try:
        user_profile = models.Profile.objects.get(user__username=user_name)
        posts = models.Companies.objects.filter(user__username=user_name).order_by('-date')
        pages = Paginator(posts, 100)
        return render(
            request,
            'registration/profile.html',
            {
                'profile': user_profile,
                'posts': pages.page(p),
                'page': p,
                'num_pages': int(pages.num_pages)
            }
        )

    except (User.DoesNotExist, models.Profile.DoesNotExist):
        return redirect('home')


def post(request, post_id):
    try:
        user_post = models.Companies.objects.get(id=post_id)
        author = user_post.user.username
        return render(request, 'front/user_post.html', {'post': user_post, 'user': author})
    except models.Companies.DoesNotExist:
        return HttpResponseNotFound(request)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = models.Companies
    form_class = BargainingForms
    template_name = 'front/create_post.html'

    def form_valid(self, form):
        r = super().form_valid(form)
        self.object.user = self.request.user
        self.object.save()
        return r


class PostShowView(ListView):
    model = models.Companies
    paginate_by = 100
    template_name = 'front/posts.html'
    context_object_name = 'posts'
    ordering = ('-date',)
    page_kwarg = 'p'

    def get_queryset(self):
        if self.request.GET.get('d'):
            date = datetime.datetime.strptime(self.request.GET['d'], '%Y-%m-%d')
            date_to = date + datetime.timedelta(days=1)
            date_query = (Q(date__gte=date) & Q(date__lt=date_to))
        else:
            date_query = Q()

        if self.request.GET.get('s'):
            s = self.request.GET['s']
            q1 = models.Companies.objects.filter(
                date_query & Q(title__contains=s) & ~Q(content__contains=s)
            ).order_by('-date')
            q2 = models.Companies.objects.filter(
                date_query & ~Q(title__contains=s) & Q(content__contains=s)
            ).order_by('-date')

            q = q1 | q2

        else:
            q = models.Companies.objects.filter(date_query).order_by('-date').all().values('id', 'title', 'user', 'date', 'companies', 'comments' )
        return q


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = models.Companies
    form_class = BargainingForms
    success_url = '/posts/{id}'
    template_name = 'front/update.html'
    permission_denied_message = 'Нет доступа к редактированию данного поста!'

    def test_func(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        post_user_id = models.Companies.objects.filter(id=pk).values('user_id').first()['user_id']
        return self.request.user.id == post_user_id


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Companies
    success_url = '/'


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = models.Companies
    form_class = ProfileForms
    template_name = 'registration/profile_create.html'

    def form_valid(self, form):
        r = super().form_valid(form)
        self.object.user = self.request.user
        self.object.save()
        return r
