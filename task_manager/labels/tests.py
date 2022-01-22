from django.test import TestCase
from task_manager.users.models import CustomUser
from task_manager.labels.models import Labels
from django.urls import reverse


class LabelTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        CustomUser.objects.create_user(**self.credentials)

    def create_label(self):
        return Labels.objects.create(name='test_label')

    def test_create_label(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
        response = self.client.post('/labels/create/', {'name': 'test_label'})
        self.assertEqual(Labels.objects.count(), 1)

    def test_update_label(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
        label = self.create_label()
        response = self.client.post(reverse('update_label',
                                    kwargs={'pk': label.id}),
                                    {'name': 'test_label1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('labels'))
        label.refresh_from_db()
        self.assertEqual(label.name, 'test_label1')

    def test_delete_label(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
        label = self.create_label()
        self.assertEqual(Labels.objects.count(), 1)
        response = self.client.post(reverse('delete_label',
                                            kwargs={'pk': label.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('labels'))
        self.assertEqual(Labels.objects.count(), 0)
