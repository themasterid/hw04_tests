# hw04_tests - Протестируйте проект Yatube, спринт 5 в Яндекс.Практикум

## Спринт 5 - Протестируйте проект Yatube

### hw04_tests - Протестируйте проект Yatube Яндекс.Практикум.

Покрытие тестами проекта Yatube из спринта 4 Питон-разработчика бекенда Яндекс.Практикум.
Все что нужно, это покрыть тестами проект, в учебных целях.
Стек:
- django-debug-toolbar 2.2
- django 2.2.28
- pytest-django 3.8.0
- pytest-pythonpath 0.7.3
- pytest 5.3.5
- requests 2.22.0
- six 1.14.0
- sorl-thumbnail 12.6.3
- mixer 7.1.2

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
python -m venv venv
```

Активируем виртуальное окружение:

```bash
source venv/Scripts/activate
```

> Для деактивации виртуального окружения выполним (после работы):
> ```bash
> deactivate
> ```

Устанавливаем зависимости:

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Применяем миграции:

```bash
python yatube/manage.py makemigrations
```
```bash
python yatube/manage.py migrate
```

Создаем супер пользователя:

```bash
python yatube/manage.py createsuperuser
```

При желании делаем коллекцию статики:

```bash
python yatube/manage.py collectstatic
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

====================================================== test session starts =======================================================
platform win32 -- Python 3.9.7, pytest-6.2.5, py-1.10.0, pluggy-0.13.1 -- ...hw03_forms\venv\Scripts\python.exe
django: settings: yatube.settings (from ini)
rootdir: ...\hw03_forms, configfile: pytest.ini, testpaths: tests/
plugins: Faker-12.0.0, django-3.8.0, pythonpath-0.7.3
collected 20 items

tests/test_paginator.py::TestGroupPaginatorView::test_group_paginator_view_get PASSED                                       [  5%]
tests/test_paginator.py::TestGroupPaginatorView::test_group_paginator_not_in_context_view PASSED                            [ 10%]
tests/test_paginator.py::TestGroupPaginatorView::test_index_paginator_not_in_view_context PASSED                            [ 15%]
tests/test_paginator.py::TestGroupPaginatorView::test_index_paginator_view PASSED                                           [ 20%]
tests/test_paginator.py::TestGroupPaginatorView::test_profile_paginator_view PASSED                                         [ 25%]
tests/test_about.py::TestTemplateView::test_about_author_tech PASSED                                                        [ 30%]
tests/test_auth_urls.py::TestAuthUrls::test_auth_urls PASSED                                                                [ 35%]
tests/test_create.py::TestCreateView::test_create_view_get PASSED                                                           [ 40%]
tests/test_create.py::TestCreateView::test_create_view_post PASSED                                                          [ 45%]
tests/test_homework.py::TestPost::test_post_create PASSED                                                                   [ 50%]
tests/test_homework.py::TestGroup::test_group_create PASSED                                                                 [ 55%]
tests/test_homework.py::TestGroupView::test_group_view PASSED                                                               [ 60%]
tests/test_post.py::TestPostView::test_post_view_get PASSED                                                                 [ 65%]
tests/test_post.py::TestPostEditView::test_post_edit_view_get PASSED                                                        [ 70%]
tests/test_post.py::TestPostEditView::test_post_edit_view_author_get PASSED                                                 [ 75%]
tests/test_post.py::TestPostEditView::test_post_edit_view_author_post PASSED                                                [ 80%]
tests/test_profile.py::TestProfileView::test_profile_view_get PASSED                                                        [ 85%]
tests/test_homework.py::TestPost::test_post_model PASSED                                                                    [ 90%]
tests/test_homework.py::TestPost::test_post_admin PASSED                                                                    [ 95%]
tests/test_homework.py::TestGroup::test_group_model PASSED                                                                  [100%]

======================================================= 20 passed in 1.96s =======================================================
```

Запускаем проект:

```bash
python yatube/manage.py runserver localhost:80
```

После чего проект будет доступен по адресу http://localhost/

Заходим в http://localhost/admin и создаем группы и записи.
После чего записи и группы появятся на главной странице.

Автор: [Дмитрий Клепиков](https://github.com/themasterid) :+1:
