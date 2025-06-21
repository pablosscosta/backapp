# backup_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('executar/', views.executar_backup, name='executar_backup'),
]
