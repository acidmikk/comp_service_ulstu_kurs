from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from itertools import chain
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from .models import *
from .forms import ContactForm, LoginUserForm


# Create your views here.


class PhotosList(ListView):
    model = Photo
    template_name = 'comp_service/photos.html'
    paginate_by = 5
    context_object_name = 'photos'

    def get_queryset(self):
        return Photo.objects.all().order_by('-published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')

        try:
            photos = paginator.page(page)
        except PageNotAnInteger:
            # Если страница не является целым числом, поставим первую страницу
            photos = paginator.page(1)
        except EmptyPage:
            # Если страница находится за пределами доступного диапазона, поставим последнюю страницу
            photos = paginator.page(paginator.num_pages)

        context['object_list'] = photos
        return context


def main(request):
    return render(request, 'comp_service/main.html')


def about(request):
    if request.method == 'GET':
        form = ContactForm()
    elif request.method == 'POST':
        # если метод POST, проверим форму и отправим письмо
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['mess']
            recepients = [settings.EMAIL_HOST_USER]
            send_mail(name + ' -- ' + email, message, settings.EMAIL_HOST_USER, recepients)
            return redirect('main:about')
    return render(request, 'comp_service/about.html', {'form': form})


class ServiceListView(ListView):
    model = Service
    template_name = 'comp_service/services.html'
    context_object_name = 'services'


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'comp_service/service_detail.html'
    context_object_name = 'service'


def contact_view(request):
    # если метод GET, вернем форму
    if request.method == 'GET':
        form = ContactForm()
    elif request.method == 'POST':
        # если метод POST, проверим форму и отправим письмо
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['mess']
            recepients = [settings.EMAIL_HOST_USER]
            send_mail(name + ' -- ' + email, message, settings.EMAIL_HOST_USER, recepients)
            return redirect('main:main')
    else:
        return HttpResponse('Неверный запрос.')
    return render(request, 'comp_service/contact.html', {'form': form})


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'comp_service/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('main:main')


@login_required
def logout_user(request):
    logout(request)
    return redirect('main:main')


@login_required
def order_detail(request, username, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Проверяем доступ к заказу
    if not can_view_order(request.user, order):
        # Обработка случая, когда доступ запрещен
        return redirect('main:main')
    return render(request, 'comp_service/order_detail.html', {'order': order,
                                                              'username': username})


@login_required
def profile(request, username):
    profile_user = User.objects.get(username=username)
    context = {'user': profile_user,
               'orders': Order.objects.filter(user=request.user)}
    if not can_view_profile(request.user, profile_user):
        # Обработка случая, когда доступ запрещен
        return redirect('main:main')
    return render(request, 'comp_service/profile.html', context)


def can_view_order(user, order):
    return user.is_authenticated and (user == order.user or user.is_staff)


def can_view_profile(user, profile_user):
    return user.is_authenticated and (user == profile_user or user.is_staff)


