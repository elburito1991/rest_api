# Python Flask Rest Api
---

Programmed by elburito1991@gmail.com

Пример того, как может быть написан на языке `Python` Rest Api, c использованием микрофреймворка `Flask`.

В программе описаны CRUD операции для создания и хранения учетных данных  в БД посредством `PostgreSQL`.

Тестирование производилось при помощи платформы `API POSTMAN`


### 🖥 Локальная установка проекта
1. Скопируйте данный репозиторий: `git clone <this repo's remote url>`
2. Задайте директорию: `cd rest_api`
3. Создайте виртуальное окружение для этого проекта и активируйте его :
```
python -m venv venv
venv\Scripts\activate
```
4. Установите библиотеки: `pip install -r requirements.txt`
5. Создайте базу данных с именем `db`
6. Инициализируйте и установите миграцию данных в БД
```
flask db init
flask db migrate
flask db upgrade
```
7. Запустите приложение `app.py`

### 🔗 Пример работы [приложения](https://documenter.getpostman.com/view/25638777/2s93CUJVjA)

