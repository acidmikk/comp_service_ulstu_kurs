from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Order
# Create your tests here.


class CompServiceTestCase(TestCase):
    def setUp(self):
        # Создаем пользователя для тестирования
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Создаем заказ для тестирования
        self.order = Order.objects.create(user=self.user, status='created')

    def test_order_detail_view(self):
        # Аутентификация пользователя
        self.client.login(username='testuser', password='testpassword')
        # Получение URL для представления order_detail с использованием параметра order_id
        url = reverse('main:order_detail', args=['testuser', self.order.pk])
        # Отправка GET-запроса
        response = self.client.get(url)
        # Проверка, что ответ имеет статус 200
        self.assertEqual(response.status_code, 200)
        # Проверка, что в ответе содержится информация о заказе
        self.assertContains(response, f"Детали заказа #{self.order.id}")

    def test_profile_view(self):
        # Аутентификация пользователя
        self.client.login(username='testuser', password='testpassword')
        # Получение URL для представления profile
        url = reverse('main:profile', args=['testuser'])
        # Отправка GET-запроса
        response = self.client.get(url)
        # Проверка, что ответ имеет статус 200
        self.assertEqual(response.status_code, 200)
        # Проверка, что в ответе содержится информация о профиле
        self.assertContains(response, "testuser")
