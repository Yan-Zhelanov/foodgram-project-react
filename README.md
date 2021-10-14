# Foodgram
Это сервис для публикаций и обмена рецептами.
Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное, в покупки, скачивать список покупок. Неавторизованным пользователям доступна регистрация, авторизация, просмотр рецептов других пользователей.

![example workflow](https://github.com/Yan-Zhelanov/foodgram-project-react/actions/workflows/foodgram_workflow.yaml/badge.svg)


## Стек технологий
Python 3.9.7, Django 3.2.7, Django REST Framework, PostgreSQL.

## Установка
Создайте файл `.env` в директории `/backend/` с содержанием:
```
SECRET_KEY=любой_секретный_ключ_на_ваш_выбор
DEBUG=False
ALLOWED_HOSTS=*,или,ваши,хосты,через,запятые,без,пробелов
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=пароль_к_базе_данных_на_ваш_выбор
DB_HOST=db
DB_PORT=5432
```

#### Установите и запустите проект:
1. Перейдите в директорию `/infra/`
```bash
cd ./infra/
```
2. Запустите docker compose:
```bash
docker-compose up -d
```
3. Примените миграции:
```bash
docker-compose exec backend python manage.py migrate
```
4. Создайте администратора:
```bash
docker-compose exec backend python manage.py createsuperuser
```
5. Соберите статику:
```bash
docker-compose exec backend python manage.py collectstatic
```
6. Заполните базу начальными данными:
```bash
docker-compose exec backend python manange.py loaddata fixtures.json
```

## Как импортировать дату из своего csv файла?
1. Заходим в shell:
```bash
docker-compose exec backend python manage.py shell
```

2. Импортируем нужные модели:
```python
from recipes.models import Ingredient, Tags
```

3. Импортируем скрипт:
```python
from scripts.import_data import create_models
```

4. Запускаем скрипт с тремя параметрами:

`file_path` — путь до вашего csv файла,

`model` — класс модели из импортированных ранее,

`print_errors` — нужно ли распечатать каждую ошибку подробно? (```True or False```)

Пример:
```python
create_models('../data/ingredients.csv', Ingredient, True)
```

## Сайт
Сайт доступен по ссылке:
[http://foodgram.ddns.net/](http://foodgram.ddns.net/)

## Документация
Чтобы открыть документацию локально, запустите сервер и перейдите по ссылке:
[http://127.0.0.1/api/docs/](http://127.0.0.1/api/docs/)

Или же заходите на мой сервер:
[http://foodgram.ddns.net/api/docs/](http://foodgram.ddns.net/api/docs/)

