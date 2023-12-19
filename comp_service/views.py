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
from django.views.generic import ListView, CreateView
from django.conf import settings
from django.contrib import messages

from .models import *
from .forms import ContactForm, LoginUserForm


# Create your views here.


class PhotosList(ListView):
    model = Photo
    queryset = Photo.objects.all()
    template_name = 'comp_service/photos.html'
    paginate_by = 12
    context_object_name = 'photo'

    def get_queryset(self):
        return Photo.objects.all().order_by('-created_at')

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
    context = {}
    return render(request, 'comp_service/main.html', context)


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


def logout_user(request):
    logout(request)
    return redirect('main:login')


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'comp_service/order_detail.html', {'order': order})


@login_required
def profile(request, username):
    context = {'user': User.objects.get(username=username),
               'orders': Order.objects.filter(user=request.user)}
    return render(request, 'comp_service/profile.html', context)

