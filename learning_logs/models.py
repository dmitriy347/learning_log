from django.db import models
from django.contrib.auth.models import User

# Создайте здесь свои модели.

class Topic(models.Model): # Класс Topic наследует от Model (родительского класса, включенного в Django).
    """Тема, которую изучает пользователь"""
    # CharField - блок данных, состоящий из символов, т.е. текст с именами, заголовками и т.п.
    # Сообщаем Django, что резервируем 200 символов.
    text = models.CharField(max_length=200)

    # DateTimeField - блок данных для хранения даты и времени.
    # Аргумент auto_now_add=True - приказывает Django автоматически присвоить-
    # -этому атрибуту текущую дату и время каждый раз, когда польщователь создает новую тему.
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Необходимо сообщить Django какой атрибут должен использоваться-
    # -по умолчанию при вводе информации о теме.
    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.text


class Entry(models.Model):
    """Информация, изученная пользователем по теме."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField() # здесь не требуется ограничение длины
    date_added = models.DateTimeField(auto_now_add=True)

    # Класс Meta вкладывается в класс Entry
    # Он хранит доп. инф. по управлению моделью, в данном случае он позволяе-
    # -задать спец. атрибут, который приказывает Django испольщовать форму-
    # -множественного числа Entries при обращении более чем к одной записи
    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Возвращает строковое представление модели."""
        if len(self.text) <= 50:
            return self.text
        else:
            return f"{self.text[:50]}..."