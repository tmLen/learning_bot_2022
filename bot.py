# Updater - компонент отвечающий за обмен данными с сервером Телеграм
# CommandHandler - компонет отвечающий за обрабтку комманд

from telegram.ext import CommandHandler, Updater

key = '5217524414:AAHNL_XsbLKgkqZcTd-Bl41xKLFRNIzMqYI'

#функция которая выводит приветствие пользователю при команде /start
def greet_user(update, context):
    print('hello!')

def main():
    #создаем апдейтер
    mybot = Updater(key, use_context=True)

    #добавляем диспетчер    
    dp = mybot.dispatcher

    #добавление обрабоки команды /start
    dp.add_handler(CommandHandler('start', greet_user))

    #включаем полинг
    mybot.start_polling()
    #включаем бесконечный цикл
    mybot.idle()

main()

