"""Определяет схемы URL для learning_logs."""

from django.urls import path

# Точка приказывает импортировать представления из каталога, в котором находится текущий модуль urls.py
from . import views

# Переменна app_name помогает Django отличить этот файл от отноименных файлов-
# -в других приложениях в проекте.
app_name = 'learning_logs'

# Переменная urlpatterns представляет собой список страниц, которые могут-
# -запрашиваться из приложжения leanring_logs.
urlpatterns = [
    # Домашняя страница.
    path('', views.index, name='index'),
    # Страница со списком всех тем.
    path('topics/', views.topics, name='topics'),
    # Страница с подробной информацией по отдельной теме.
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Страница для добавления новой темы.
    path('new_topic/', views.new_topic, name='new_topic'),
    # Страница для добавления новой записи.
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Страница для редактирования записи.
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]