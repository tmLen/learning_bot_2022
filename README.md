# Проект tmlen_bot
tmlen_bot - бот для телеграм, который нужен чтобы вспомнить принципы работы с ботами


## Установка
1. Клонируйте репозиторий с github
2. Создайте виртуальное окружение
3. Установите зависимости `pip install -r requirements.txt`
4. Создайте файл `settings.py` 
5. Впишите в settings.py переменные 
```
API_KEY = 'api-ключ от телеграм бота '
CLARIFAI_API_KEY = 'api ключ бота clarifai'
USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']

```
6. Запустите бота командой `python bot.py`