from django.contrib import admin

# Зарегистрируйте здесь ваши модели.
from .models import Topic, Entry # '.models' означает, что нужно искать models.py в одном каталоге с admin.py.

# Сообщает Django, что управление моделями должно осуществляться через административный сайт.
admin.site.register(Topic)
admin.site.register(Entry)
