from django.db import models
from django.urls import reverse


class Statuses(models.Model):
    name_len = 100
    name = models.CharField(max_length=name_len)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        verbose_name = 'status'
        verbose_name_plural = 'statuses'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('statuses')
