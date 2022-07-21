![workflow](https://github.com/DD477/foodgram-project-react/actions/workflows/main.yml/badge.svg)

  ## Проект Foodgram
Дипломный проект "Продвинутый помошник" курса "Python-разработчик плюс". На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
    
 Backend:
  <p>
  
  [Dmitry Dobrodeev](https://github.com/DD477)
  
  </p>
  
  Frontend:
  
  [Яндекс.Практикум](https://github.com/yandex-praktikum/foodgram-project-react)
  



## Оглавление

* [Использованные технологии](#использованные-технологии)
* [Необходимый софт](#необходимый-софт)
* [Как запустить проект](#как-запустить-проект)
* [Использование](#использование)


## Использованные технологии
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

[К оглавлению](#оглавление) ↑

## Необходимый софт
- [Python](https://www.python.org/) 3.8.10 или выше
- [Docker](https://www.docker.com/) 4.10.1
- [Docker Compose](https://docs.docker.com/compose/) 3.9

## Как запустить проект:
- Клонировать репозиторий 
   ```sh
   git clone https://github.com/DD477/foodgram-project-react.git
   ```
- Перейти в папку с проектом
   ```sh
   cd foodgram-project-react
   ```
- Cоздать и активировать виртуальное окружение
   ```sh
   python3 -m venv venv
   ```
   ```sh
   source venv/bin/activate
   ```
- Обновить менеджер пакетов (pip)
   ```sh
   pip install --upgrade pip
   ```
- Установить зависимости из файла requirements.txt
   ```sh
   pip install -r ./backend/requirements.txt
   ```
- В папке `infra` создать файл `.env` - в нем будут храниться переменные окружения для проекта. Пример содержимого ниже:

  ```sh
  SECRET_KEY=SECRET_KEY
  DB_ENGINE=django.db.backends.postgresql
  POSTGRES_DB=postgres
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres
  DB_HOST=db
  DB_PORT=5432
  PGADMIN_DEFAULT_EMAIL=admin@admin.ru
  PGADMIN_DEFAULT_PASSWORD=admin
  ```
- Запустите docker-compose
  ```sh
  docker-compose up
  ```
   
[К оглавлению](#оглавление) ↑

## Использование
- После запуска контейнеров, сайт будет доступен по адресу http://localhost/
- Спецификация API будет доступна http://localhost/api/docs/
* [Для удобства работы с приложением, можно воспользоваться панелью администрирования по адресу /admin](http://foodgramproject.ddns.net/admin/)
* ```sh
  Логин: admin
  Пароль: admin
  ```

[К оглавлению](#оглавление) ↑

### Лицензия:
- MIT
