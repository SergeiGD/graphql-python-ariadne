# GraphQL hotel

## Навигация
- [Описание проекта](#описание-проекта)
- [Документация](#документация)
- [Инструкция по запуску](#инструкция-по-запуску)

## Описание проекта
Проект создан в учебных целях для ознакомления с технологией graphQL

В данном проекте реализована система управления отелем. Пользователи может просматривать каталог категорий номеров и скидки на них, добавлять интересующие их предложения в корзину и затем создавать на них заказы. Администраторы могут управлять списоком категорий, номеров, фотографий номеров, скидок, тегов, заказов, клиентов, других сотрудников и групп пользователей

**Структура проекта**

Резольверы, схема graphql, юнионы и прочие сопутствующие graphql вещи хранятся в каталоге [ariadne_graphql](./app/ariadne_graphql).

Основная бизнес-логика хранится в модуле [hotel_business_module](https://github.com/SergeiGD/hotel_business_module). В моделях сосредоточена только логика хранения данных (описание таблиц и валидаторы), взаимодействие c происходит по шаблону TableGateway, для всех основных моделей есть свой класс [gateway](https://github.com/SergeiGD/hotel_business_module/tree/main/gateways), в котором хранится логика обработки данных и основные use-cases приложения. 

**Использованые технологии:**
- python 3.10
- ariadne 0.18
- SQLAlchemy 2.0
- uvicorn
- PostgreSQL

## Документация
Документация postman доступна по следующей ссылке: https://documenter.getpostman.com/view/25226558/2s93XsXRDG#intro

Со всех схемой graphQL можно ознакомиться в этом файле: [sdl.gql](./sdl.gql)

## Инструкция по запуску:
1. Находясь в папке с проектом создайте .env файл со следующим содержанием:
```bash
DB_NAME=ваше имя базы данных
DB_USER=ваш логин к базе данных
DB_PASSWORD=ваш пароль к базе данных
DB_PORT=ваш порт для базы данных (должен быть свободен)
SECRET_KEY=ваш произвольный секретный ключ (указывать не обязательно)
EMAIL_USER=ваш адрес эл. почты, откуда будут отправляться письма
EMAIL_PASSWORD=пароль от эл. почты
EMAIL_HOST=сервер отправителя писем (по умолчанию smtp.yandex.com)
```
Пример:
```bash
DB_NAME=graphql
DB_USER=user
DB_PASSWORD=passwd
DB_PORT=5454
EMAIL_USER=myauthmanager@ya.ru
EMAIL_PASSWORD=mdskmfkmerw32kklas
```

2) Соберите и запустите контейнеры:
```
docker-compose up --build
```
3) Для создания суперпользователя, после запуска контейнеров выполните скрипт [create_superuser.sh](./create_superuser.sh), который первым аргументом принимает адрес эл. почты, а вторым пароль. Пример:
```
./create_superuser.sh admin@gmail.com password123
```

Приложение будет достпуно по адресу http://127.0.0.1:8000/graphql

P.S. убедитесь, что у Вас открыт 5000 порт и не забудьте провести клонирование вместе с подмодулями (флаг --recurse-submodules)
