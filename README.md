# Zuzyublik Telegram Bot

Этот бот позволяет пользователю загружать Excel-файл с данными для парсинга сайтов с товарами (зюзюбликами). После загрузки бот:

- Считывает Excel с помощью pandas
- Выводит первые строки таблицы обратно пользователю
- Сохраняет данные в базу данных SQLite
- Выполняет парсинг сайтов, извлекает цены с помощью xpath и выводит среднюю цену по каждому сайту

Бот доступен в тг по нику @ZuzyublikBot

## Требования

- Python 3.8+
- Установленные зависимости (см. файл requirements.txt)

## Установка

1. Склонируйте репозиторий:

```
git clone git@github.com:TeenCreek/zuzyublik_bot.git
```

2. Создайте файл **.env** в корневой директории и добавьте в него ваш Telegram Bot Token:

```
TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН_ТУТ
```

3. Установите зависимости:

```
pip install -r requirements.txt
```

## Запуск

Запустите бота командой:

```
python bot.py
```

Бот начнёт опрос обновлений и будет готов принимать файлы.
