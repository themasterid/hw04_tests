# hw04_tests - Протестируйте проект Yatube, спринт 5 в Яндекс.Практикум

## Спринт 5 - Протестируйте проект Yatube

### hw04_tests - Протестируйте проект Yatube Яндекс.Практикум.

Покрытие тестами проекта Yatube из спринта 4 Питон-разработчика бекенда Яндекс.Практикум.
Все что нужно, это покрыть тестами проект, в учебных целях.

Стек (обновить):
 + Python 3.12
 + asgiref==3.8.1
 + certifi==2025.1.31
 + charset-normalizer==3.4.1
 + django==5.1.6
 + django-debug-toolbar==5.0.1
 + django-environ==0.12.0
 + faker==12.0.1
 + idna==3.10
 + iniconfig==2.0.0
 + mixer==7.2.2
 + packaging==24.2
 + pillow==11.1.0
 + pluggy==1.5.0
 + pytest==8.3.4
 + pytest-django==4.9.0
 + pytest-pythonpath==0.7.3
 + python-dateutil==2.9.0.post0
 + requests==2.32.3
 + six==1.17.0
 + sorl-thumbnail==12.11.0
 + sqlparse==0.5.3
 + urllib3==2.3.0

### Настройка и запуск на ПК

Клонируем проект:

```bash
git clone https://github.com/themasterid/hw04_tests.git
```

или

```bash
git clone git@github.com:themasterid/hw04_tests.git
```

Переходим в папку с проектом:

```bash
cd hw04_tests
```

Устанавливаем виртуальное окружение:

```bash
uv venv
```

Активируем виртуальное окружение:

```bash
source .venv/bin/activate
```

> Для деактивации виртуального окружения выполним (после работы):
> ```bash
> deactivate
> ```

Устанавливаем зависимости:

```bash
uv pip install -r requirements.txt
```

Применяем миграции:

```bash
python3 yatube/manage.py makemigrations
python3 yatube/manage.py migrate
```

Создаем супер пользователя:

```bash
python3 yatube/manage.py createsuperuser
```

При желании делаем коллекцию статики:

```bash
python3 yatube/manage.py collectstatic
```

Предварительно сняв комментарий с:
```bash
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

И закомментировав: 
```bash
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

Иначе получим ошибку: You're using the staticfiles app without having set the STATIC_ROOT setting to a filesystem path.

В папку с проектом, где файл settings.py добавляем файл .env куда прописываем наши параметры:

```bash
SECRET_KEY='Ваш секретный ключ'
ALLOWED_HOSTS='127.0.0.1, localhost'
DEBUG=True
```

Не забываем добавить в .gitingore файлы:

```bash
.env
.venv
```

Для запуска тестов выполним:

```bash
pytest
```

Получим:

```bash

pytest
ОТРЕДАКТИРОВАТЬ ПОСЛЕ УСТРАНЕНИЯ
FAILED tests/test_create.py::TestCreateView::test_create_view_get - AssertionError: Проверьте, чт...
FAILED tests/test_homework.py::TestGroupView::test_group_view - AssertionError: Отредактируйте HT...
FAILED tests/test_post.py::TestPostEditView::test_post_edit_view_author_get - AssertionError: Про...
============================ 3 failed, 17 passed, 33 warnings in 2.98s ============================ 
```

Запускаем проект:

```bash
python3 yatube/manage.py runserver localhost:80
```

После чего проект будет доступен по адресу http://localhost/

Заходим в http://localhost/admin и создаем группы и записи.
После чего записи и группы появятся на главной странице.

Автор: [Дмитрий Клепиков](https://github.com/themasterid) :+1:
