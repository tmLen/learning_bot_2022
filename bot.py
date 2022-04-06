import logging

from random import randint
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
# Updater - компонент отвечающий за обмен данными с сервером Телеграм
# CommandHandler - компонет отвечающий за обрабтку комманд
# MessageHandler - обработчик сообщений
# Filters - фильтры для сообщений

import settings

# старт логирования
logging.basicConfig(filename='bot.log', level=logging.INFO)

#функция которая выводит приветствие пользователю при команде /start
def greet_user(update, context):
    update.message.reply_text(f'Добрый день!')

def talk_to_me(update, context):
    text = update.message.text
    update.message.reply_text(text)

def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Ваше число {user_number}, моё число {bot_number}, вы выиграли!'
    elif user_number == bot_number:
        message = f'Ваше число {user_number}, моё число {bot_number}, ничья'
    else:
        message = f'Ваше число {user_number}, моё число {bot_number}, вы проиграли! ха ха'
    
    return message


def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = f'Введите целое число'
    else:
        message = 'Введите число'
    update.message.reply_text(message)

def main():
    #создаем апдейтер
    mybot = Updater(settings.API_KEY, use_context=True)

    #добавляем диспетчер    
    dp = mybot.dispatcher

    #добавление обрабоки команды /start
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    #включаем полинг
    mybot.start_polling()
    #включаем бесконечный цикл
    mybot.idle()


if __name__ == '__main__':
    main()

