## Проект «API для YaMDb»

### Описание:

Проект YaMDb собирает отзывы пользователей на произведения.

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Список категорий может быть расширен.
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
Добавлять произведения, категории и жанры может только администратор.

Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку; из пользовательских оценок формируется рейтинг произведения.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Технологии:

Python 3.7

Django 3.2

### Запуск проекта:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Guten-Edd/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -3.7 -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
cd api_yamdb/
```

```
python manage.py migrate
```

Выполнить загрузку информации в базу данных:

```
python manage.py csv_import
```

Запустить проект:

```
python manage.py runserver
```

Документация доступна по адресу:

```
http://127.0.0.1:8000/redoc/
```

### Авторы:
[Эдуард Соловьев](https://github.com/Guten-Edd)

[Елена Посохова](https://github.com/Elenka-Posohova)

[Иван Филиппов](https://www.linkedin.com/in/iffilippov/)

<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" width="50" height="50"/>
