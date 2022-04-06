from emoji import emojize
from glob import glob #для доступа к файлам
import logging
from random import choice, randint
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
# Updater - компонент отвечающий за обмен данными с сервером Телеграм
# CommandHandler - компонет отвечающий за обрабтку комманд
# MessageHandler - обработчик сообщений
# Filters - фильтры для сообщений

import settings

# старт логирования
logging.basicConfig(filename='bot.log', level=logging.INFO)

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        user_data['emoji'] = emojize(smile, language='alias')
    return user_data['emoji']

#функция которая выводит приветствие пользователю при команде /start
def greet_user(update, context):
    smile = get_smile(context.user_data)
    update.message.reply_text(f'Здравствуй, пользователь {smile}!')

def talk_to_me(update, context):
    text = update.message.text
    smile = get_smile(context.user_data)
    update.message.reply_text(f'{text} {smile}')

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

def send_cat_picture(update, context):
    # выбираем все файлы из папки images с названием содержащим cat
    # выбираем из них случайное
    # отправляем в чат
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)

    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))

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
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    #включаем полинг
    mybot.start_polling()
    #включаем бесконечный цикл
    mybot.idle()


if __name__ == '__main__':
    main()

