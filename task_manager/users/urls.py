from django.urls import path
from . import views


urlpatterns = [
    path('', views.UserList.as_view(), name='users'),
    path('create/', views.RegisterView.as_view(), name='register'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(),
         name='update_user'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(),
         name='delete_user'),
]
