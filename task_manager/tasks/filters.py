import django_filters
from .models import Tasks
from django import forms


class TasksFilter(django_filters.FilterSet):
    self_task = django_filters.BooleanFilter(method='user_is_creator',
                                             widget=forms.CheckboxInput)

    def user_is_creator(self, queryset, name, value):
        if value:
            return queryset.filter(creator=self.request.user)
        return queryset

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'label', 'self_task']
        filter_overrides = {
            django_filters.BooleanFilter: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }
