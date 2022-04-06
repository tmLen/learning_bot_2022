import logging
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
    print('pressed /start!')
    update.message.reply_text(f'Добрый день!')

def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def main():
    #создаем апдейтер
    mybot = Updater(settings.API_KEY, use_context=True)

    #добавляем диспетчер    
    dp = mybot.dispatcher

    #добавление обрабоки команды /start
    dp.add_handler(CommandHandler('start', greet_user))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    #включаем полинг
    mybot.start_polling()
    #включаем бесконечный цикл
    mybot.idle()


if __name__ == '__main__':
    main()

