# Foodgram
Cервис для публикаций и обмена рецептами.

Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное, в покупки, скачивать список покупок. Неавторизованным пользователям доступна регистрация, авторизация, просмотр рецептов других пользователей.

![Foodgram Workflow](https://github.com/Yan-Zhelanov/foodgram-project-react/actions/workflows/foodgram_workflow.yaml/badge.svg)


## Стек технологий
Python 3.9.7, Django 3.2.7, Django REST Framework 3.12, PostgresQL, Docker, Yandex.Cloud.

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

#### Установка Docker
Для запуска проекта вам потребуется установить Docker и docker-compose.

Для установки на ubuntu выполните следующие команды:
```bash
sudo apt install docker docker-compose
```

Про установку на других операционных системах вы можете прочитать в [документации](https://docs.docker.com/engine/install/) и [про установку docker-compose](https://docs.docker.com/compose/install/).

#### Разные версии конфигураций
В папке `/server/` и `/infra/` лежат два фалйа: `docker-compose.yml` и `nginx.conf`.
Если вы планируете запускать проект локально, пользуйтесь конфигурационными файлами из второй папки,
если же вы планируете запускать проект на сервере, то скопируйте на сервер файлы из одноимённой папки.

### Пример установки и запуска проекта локально:
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
4. Заполните базу начальными данными (необязательно):
```bash
docker-compose exec backend python manange.py loaddata ../data/fixtures.json
```
5. Создайте администратора:
```bash
docker-compose exec backend python manage.py createsuperuser
```
6. Соберите статику:
```bash
docker-compose exec backend python manage.py collectstatic
```

### Установка проекта на ваш сервер
1. Скопируйте файлы из папки `/server/` на ваш сервер:
```bash
scp -r data/ <username>@<server_ip>:/home/<username>/
```
2. Зайдите на сервер и настройте `server_name` в конфиге nginx на ваше доменное имя:
```bash
vim nginx.conf
```
3. Создайте в той же папке `.env` файл, как было показано в самом начале.
4. Запуск и миграции выполняются теми же командами, что и локально. Если вы хотите загрузить какие-либо данные, чтобы заполнить ими базу данных, не забудьте скопировать и их, как показано в пункте №1.

## Как импортировать данные из своего csv файла?
Для начала убедитесь, что первая строчка вашего csv файла совпадает с названиями полей в модели. Если на первой строчке нет названия полей или они неправильные, исправьте, прежде чем приступать к импортированию.
### Импортирование с помощью скрипта
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

#### Админ-панель
Логин: `admin@gmail.com`
Пароль: `eLfxYjQghJdtHrBfLvbYrB5548`

## Документация к API
Чтобы открыть документацию локально, запустите сервер и перейдите по ссылке:
[http://127.0.0.1/api/docs/](http://127.0.0.1/api/docs/)

Так же документация доступна на сервере:
[http://foodgram.ddns.net/api/docs/](http://foodgram.ddns.net/api/docs/)

