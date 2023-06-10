
![Изображение](https://yastatic.net/q/logoaas/v2/Яндекс.svg?circle=white&color=fff&first=black) ![Изображение](https://yastatic.net/q/logoaas/v2/Практикум.svg?color=fff)

# Foodgram

![workflow](https://github.com/oisaev/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

### Описание
Учебный проект Яндекс Практикум.

«Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

### Адрес проекта
```
http://practicum.isaev.es/
```

### Интерфейс администратора
```
http://practicum.isaev.es/admin/
email: admin@admin.admin
password: admin
```

### Технологии
- Python 3.9
- Django 3.2
- DRF

### Локальное развертывание
Клонируйте репозиторий:
```
git clone git@github.com:oisaev/foodgram-project-react.git
```
Перед развертыванием проекта необходимо в директории **infra** создать и заполнить **.env** файл по следующему шаблону:
```
SECRET_KEY='p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs' # секретный ключ Django (установите свой)
DEBUG=False # режим отладки Django
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
Далее, в той же директории **infra** выполнить команду для сборки контейнеров и их запуска:
```
docker-compose up -d --build
```
Зайти в контейнер backend'а:
```
В Windows:
winpty docker exec -it foodgram_backend bash
```
```
В Linux:
docker exec -it foodgram_backend bash
```
Выполнить миграции:
```
python manage.py migrate
```
Создать суперпользователя:
```
python manage.py createsuperuser
```
Загрузить теги и ингредиенты:
```
python manage.py upload_data
```
Проект станет доступным по локальному адресу.

### Автор
Студент Яндекс Практикум программы Python-разработчик плюс, когорта 19+
Олег Исаев
