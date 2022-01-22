from django.db import models
from django.urls import reverse
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels


class Tasks(models.Model):
    name_len = 100
    desc_len = 500
    name = models.CharField(max_length=name_len)
    description = models.TextField(max_length=desc_len, blank=True)
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT)
    executor = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                                 related_name="task_executor", null=True,
                                 blank=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                                related_name="task_created_by")
    label = models.ManyToManyField(Labels, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        verbose_name = 'task'
        verbose_name_plural = 'tasks'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tasks')
