from django.urls import path, include
from .views import *

app_name = 'main'

urlpatterns = [
    path('', main, name='main'),
    path('services/', ServiceListView.as_view(), name='services'),
    path('photo/', PhotosList.as_view(), name='photo'),
    path('about/', about, name='about'),
    path('contact/', contact_view, name='contact'),
    path('user/', include([
        path('login/', LoginUser.as_view(), name='login'),
        path('logout/', logout_user, name='logout'),
        path('<str:username>', profile, name='profile'),
        path('<str:username>/<int:order_id>/', order_detail, name='order_detail'),
    ])),
]