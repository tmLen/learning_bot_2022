
from email.message import Message
import logging
from mailbox import MaildirMessage
from setuptools import Command
#импорт клавиатуры для бота
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, ConversationHandler
# Updater - компонент отвечающий за обмен данными с сервером Телеграм
# CommandHandler - компонет отвечающий за обрабтку комманд
# MessageHandler - обработчик сообщений
# Filters - фильтры для сообщений
# ConversationHandler - обработчик отвечающий за диалоги 

import settings
from handlers import greet_user, guess_number, send_cat_picture, user_coordinates, talk_to_me, check_user_photo
from questionnaire import (questionnaire_start, questionnaire_name, questionnaire_rating, questionnaire_comment, questionnaire_skip, 
                            questionnaire_dont_know)

# старт логирования
logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    #создаем апдейтер
    mybot = Updater(settings.API_KEY, use_context=True)

    #добавляем диспетчер    
    dp = mybot.dispatcher

    questionnaire = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Заполнить анкету)$'), questionnaire_start)
        ],
        states={
            'name': [MessageHandler(Filters.text, questionnaire_name)],
            'rating': [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), questionnaire_rating)],
            'comment': [
                CommandHandler('skip', questionnaire_skip), 
                MessageHandler(Filters.text, questionnaire_comment)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location | Filters.poll, questionnaire_dont_know)
        ]
    )

    # добавлеине обработки хендлера для диалогов
    dp.add_handler(questionnaire)
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