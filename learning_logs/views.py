from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Создайте здесь свои представления.

def index(request):
    """Домашняя страница приложения Learning Log."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Выводит список тем."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')

    # Определяем контекст, который будет передаваться шаблону
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Выводит одну тему и все ее записи."""
    topic = Topic.objects.get(id=topic_id)
    # Проверка того, что тема принадлежит текущему пользователю.
    # Рефакторинг.
    check_topic_owner(topic, request.user)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Определяет новую тему."""
    if request.method != 'POST':
        # Данные не отправлялись, создается пустая форма.
        form = TopicForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = TopicForm(data=request.POST)
        # Функция is_valid() проверяет, что все обязательные поля были заполнены-
        # -а введенные данные соответствуют типам полей(например ограничение длины).
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # Используем функцию redirect() для перенаправления браузера-
            # -на страницу topics
            return redirect('learning_logs:topics')
        
    # Вывести пустую или недействительную форму.
    context = {'form': form}
    # Страница строится на базе шаблона new_topic.html.
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме."""
    topic = Topic.objects.get(id=topic_id)

    # Проверка того, что тема принадлежит текущему пользователю.
    # Рефакторинг.
    check_topic_owner(topic, request.user)

    if request.method != 'POST':
        # Данные не отправлялись, создается пустая форма.
        form = EntryForm
    else:
        # Отправлены данные POST, обработать данные.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # При вызове save() мы включаем аргумент commit=False, чтобы создать-
            # -новый объект записи и сохранить его в new_entry, но не сохраняя пока в БД.
            new_entry = form.save(commit=False)
            # Присваиваем атрибуду topic объекта new_entry тему, прочитанную-
            # -из БД.
            new_entry.topic = topic
            # Поэтому запись сохраняется в БД с правильно ассоциированной темой.
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    # Вывести пустую или недействительную форму.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись."""
    # Сначала получаем объект записи, который нужно изменить-
    # -и тему, связанную с этой записью.
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # Проверка того, что тема принадлежит текущему пользователю.
    # Рефакторинг.
    check_topic_owner(topic, request.user)

    if request.method != 'POST':
        # Исходный запрос, форма заполняется данными текущей записи-
        # -пользователь видит свои данные и может отредактировать их.
        form = EntryForm(instance=entry)
    else:
        # Отправка данных POST, обработать данные.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
        
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


def check_topic_owner(topic, user):
    """
    Проверка того, что тема принадлежит текущему пользователю.
    """
    if topic.owner != user:
        raise Http404    