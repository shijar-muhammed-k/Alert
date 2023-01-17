from django.urls import path
from . import views

urlpatterns = [
    path('', views.check_user, name='check_user'),
    path('create_user', views.create_user, name='create_user'),
    path('login', views.user_login, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register, name='register'),
    path('view', views.viewData, name='view'),
    path('editRecord<id>', views.editRecord, name='editRecord'),
    # path('deleteRecord', views.deleteRecord, name='deleteRecord'),
    path('success<id>', views.success,name='success'),
    path('alert', views.alert, name='alert')
]