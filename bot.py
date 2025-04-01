import os

import pandas as pd
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from db import init_db, parse_prices, save_to_db

load_dotenv()


async def start(update: Update, context):
    """Обработчик команды /start."""

    await update.message.reply_text(
        '📁 Отправьте Excel-файл с данными в формате:\n'
        'title | url | xpath\n\n'
        'Пример файла: https://example.com/example.xlsx'
    )


async def handle_file(update: Update, context):
    """Обработчик загрузки файла."""

    file = await update.message.document.get_file()
    file_path = 'temp.xlsx'
    await file.download_to_drive(file_path)

    try:
        df = pd.read_excel(file_path)

        if not all(col in df.columns for col in ['title', 'url', 'xpath']):
            raise ValueError(
                '❌ Неверный формат файла! Убедитесь, что есть колонки: title, url, xpath.'
            )

        save_to_db(df)
        await update.message.reply_text('✅ Данные сохранены!')

        averages = parse_prices()
        if averages:
            await update.message.reply_text(
                '🔍 Средние цены:\n' + '\n'.join(averages)
            )

    except Exception as e:
        await update.message.reply_text(f'❌ Ошибка: {str(e)}')

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


def main():
    """Запуск бота."""

    init_db()
    app = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.run_polling()


if __name__ == '__main__':
    main()
