from glob import glob #для доступа к файлам
from random import choice

from utils import get_smile, main_keyboard, play_random_numbers

#функция которая выводит приветствие пользователю при команде /start
def greet_user(update, context):
    smile = get_smile(context.user_data)

    update.message.reply_text(
        f'Здравствуй, пользователь {smile}!',
        reply_markup = main_keyboard()
    )

#функция кторая возвращает пользователю текст который он ввел и добавляет смайл
def talk_to_me(update, context):
    text = update.message.text
    smile = get_smile(context.user_data)
    update.message.reply_text(f'{text} {smile}', reply_markup = main_keyboard())

# функция которая вызывает игру в числа с пользователем
def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = f'Введите целое число'
    else:
        message = 'Введите число'
    update.message.reply_text(message, reply_markup = main_keyboard())

# функция отправляет изображение кта в чат
def send_cat_picture(update, context):
    # выбираем все файлы из папки images с названием содержащим cat
    # выбираем из них случайное
    # отправляем в чат
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)

    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))

#функция которая обрабатывает коориднаты пользователя
def user_coordinates(update, context):
    smile = get_smile(context.user_data)
    coord = update.message.location

    update.message.reply_text(
        f'Ваши координаты {coord} {smile}',
        reply_markup = main_keyboard()
    )