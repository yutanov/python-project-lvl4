from django.test import TestCase, Client
from task_manager.users.models import CustomUser
from django.urls import reverse


class RegisterCase(TestCase):

    def test_register(self):
        c = Client()
        response = c.post('/users/create/', {'first_name': 'test',
                                             'last_name': 'test',
                                             'username': 'test',
                                             'password1': 'test',
                                             'password2': 'test'})
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        c = Client()
        c.post('/users/create/', {'first_name': 'test',
                                  'last_name': 'test',
                                  'username': 'test',
                                  'password1': 'test',
                                  'password2': 'test'})
        response = c.post('/login/', {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 302)


class UpdateDeleteCase(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        CustomUser.objects.create_user(**self.credentials)

    def test_update(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
        response = self.client.post('/users/1/update/', {'first_name': 'test',
                                                         'last_name': 'test',
                                                         'username': 'test',
                                                         'password1': 'test',
                                                         'password2': 'test'})
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/login/', {'username': 'test',
                                                'password': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_delete(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
        response = self.client.post('/users/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users'))
        response = self.client.post('/login/', {'username': 'testuser',
                                                'password': 'secret'})
        self.assertEqual(response.status_code, 200)
