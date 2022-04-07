from telegram import ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from utils import main_keyboard

def questionnaire_start(update, context):
    update.message.reply_text(
        'Привет, как вас зовут?',
        reply_markup=ReplyKeyboardRemove()
    )
    return 'name'

def questionnaire_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text('Пожалуйста введите Имя и фамилию')
        return 'name'
    else:
        context.user_data['questionnaire'] = {'name': user_name}

        reply_keyboard = [['1', '2', '3', '4', '5']]
        update.message.reply_text(
            'Пожалуйста оцените бота от 1 до 5',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return 'rating'

def questionnaire_rating(update, context):
    context.user_data['questionnaire']['rating'] = int(update.message.text)
    update.message.reply_text('Напишите комментарий или нажмите /skip чтобы пропустить')
    return 'comment'


def format_questionnaire(questionnaire):

    user_text = f'''<b>Имя Фамилия:</b> {questionnaire["name"]}
    <b>Оценка:</b> {questionnaire["rating"]}
    '''
    if 'comment' in questionnaire:
        user_text += f'<b>Комментарий:</b> {questionnaire["comment"]}'

    return user_text

def questionnaire_comment(update, context):
    context.user_data['questionnaire']['comment'] = update.message.text
    update.message.reply_text(
        format_questionnaire(context.user_data['questionnaire']), 
        reply_markup=main_keyboard(), 
        parse_mode=ParseMode.HTML
    )
    return ConversationHandler.END

def questionnaire_skip(update, context):
    update.message.reply_text(
        format_questionnaire(context.user_data['questionnaire']), 
        reply_markup=main_keyboard(), 
        parse_mode=ParseMode.HTML
    )
    return ConversationHandler.END

def questionnaire_dont_know(update, context):
    update.message.reply_text('Я вас не понимаю')