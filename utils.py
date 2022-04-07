import base64
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc, service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

from emoji import emojize
from random import choice, randint
from telegram import ReplyKeyboardMarkup, KeyboardButton  

import settings

def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Ваше число {user_number}, моё число {bot_number}, вы выиграли!'
    elif user_number == bot_number:
        message = f'Ваше число {user_number}, моё число {bot_number}, ничья'
    else:
        message = f'Ваше число {user_number}, моё число {bot_number}, вы проиграли! ха ха'
    
    return message

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        user_data['emoji'] = emojize(smile, language='alias')
    return user_data['emoji']

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Прислать котика', KeyboardButton('Мои координаты', request_location=True)]
    ])


# используя clarifai определяем есть ли на картинке кошка или нет
def check_response_for_object(response, object_name):
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == object_name and concept.value >= 0.90:
                return True
    else:
        print(f'Ошибка распознавания картинки, {response.outputs[0].status.details}')

    return False

def has_object_on_image(file_name, object_name):
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization',  f'Key {settings.CLARIFAI_API_KEY}'),)
    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)
    
    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs = [
            resources_pb2.Input(
                data=resources_pb2.Data(image=image)
            )
        ]
    )

    response = app.PostModelOutputs(request, metadata=metadata)
    return check_response_for_object(response, object_name)



if __name__ == '__main__':
    print(has_object_on_image('images/cat1.jpeg', 'cat'))
    print(has_object_on_image('images/no cat.jpeg', 'cat'))
    print(has_object_on_image('images/no cat.jpeg', 'dog'))


