
import logging
from mailbox import MaildirMessage
#импорт клавиатуры для бота
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
# Updater - компонент отвечающий за обмен данными с сервером Телеграм
# CommandHandler - компонет отвечающий за обрабтку комманд
# MessageHandler - обработчик сообщений
# Filters - фильтры для сообщений

import settings
from handlers import greet_user, guess_number, send_cat_picture, user_coordinates, talk_to_me, check_user_photo

# старт логирования
logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    #создаем апдейтер
    mybot = Updater(settings.API_KEY, use_context=True)

    #добавляем диспетчер    
    dp = mybot.dispatcher

    #добавление обрабоки команд /start /guess  /cat
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))

    #добавление обрабокти текстовых сообщений пользователя
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    #включаем полинг
    mybot.start_polling()
    #включаем бесконечный цикл
    mybot.idle()


if __name__ == '__main__':
    main()