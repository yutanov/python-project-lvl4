from django.test import TestCase
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Statuses
from django.urls import reverse


class LabelTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        CustomUser.objects.create_user(**self.credentials)

    def create_status(self):
        return Statuses.objects.create(name='test_status')

    def test_create_status(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
        response = self.client.post('/statuses/create/',
                                    {'name': 'test_status'})
        self.assertEqual(Statuses.objects.count(), 1)

    def test_update_status(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
        status = self.create_status()
        response = self.client.post(reverse('update_status',
                                    kwargs={'pk': status.id}),
                                    {'name': 'test_status1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('statuses'))
        status.refresh_from_db()
        self.assertEqual(status.name, 'test_status1')

    def test_delete_status(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
        status = self.create_status()
        self.assertEqual(Statuses.objects.count(), 1)
        response = self.client.post(reverse('delete_status',
                                    kwargs={'pk': status.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('statuses'))
        self.assertEqual(Statuses.objects.count(), 0)
