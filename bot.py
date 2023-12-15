# --------------------------------------------------ИМПОРТЫ-------------------------------------------------------------
import telebot
from telebot.types import (KeyboardButton, ReplyKeyboardMarkup, Message, InlineKeyboardMarkup, InlineKeyboardButton)
from info import AboutMe, AboutCharacter
from dotenv import load_dotenv
import os
import random
# -----------------------------------------------ПОЛУЧЕНИЕ ТОКЕНА-------------------------------------------------------
load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token=token)


# --------------------------------------ПРОВЕРКА ПРИВЕТСТВИЯ/ПРОЩАНИЯ---------------------------------------------------
def check_greet(message):
    greet = ['/start', 'привет', 'прив', 'приветствую', 'здравствуйте', 'здравствуй', 'йоу', 'hello', 'hi']
    for i in greet:
        if i in message.text.lower():
            return True


def check_bye(message):
    bye = ['пока', 'поки', 'до свидания', 'до встречи', 'бай']
    for i in bye:
        if i in message.text.lower():
            return True


# ------------------------------------------------ОСНОВНЫЕ ФУНКЦИИ------------------------------------------------------
@bot.message_handler(commands=['start'])
def starting(message):
    greet = (f'Привет, {message.from_user.first_name}!\n Я бот-визитка.\n'
             f' Я создан для того, чтобы рассказывать миру об интересных существах - людях, '
             f'персонажах из игр, мультиков и т.п. Приятного пользования!\n'
             f'/help - информация о командах')
    img = 'https://i.postimg.cc/cJK9qZr6/photo-5465308694494432771-y.jpg'
    bot.send_photo(message.chat.id, img, greet)


@bot.message_handler(commands=['help'])
def about_bot(message):
    bot.send_message(message.chat.id, 'Что же я могу? К сожалению, я не человек и умею не так много.\n'
                                      'А именно:\n'
                                      '\n'
                                      'Могу разнообразно поприветствовать вас\n'
                                      'Имею неплохую реализацию оценивания персонажа(по-моему скромному'
                                      ' роботовскому мнению)\n'
                                      '/who - покажу, о ком могу рассказать\n'
                                      '/echo - буду отвечать на ваши сообщения таким же сообщением. '
                                      'Работает только с текстом и фото (относится к тем'
                                      ' словам, которые не входят в другие функции бота)\n'
                                      '/rate - позволяет оценить конкретного персонажа\n'
                                      '/my_rates - покажу, как вы оценили моих персонажей\n'
                                      '\n'
                                      'А дальше, в зависимости от вашего выбора, расскажу что-нибудь интересное.')


@bot.message_handler(commands=['who'])
def about_characters(message: Message):
    keyboard = make_characters_names_keyboard()
    text = ('Пока я обладаю информацией только о двух живых существах: \n'
            '1 - Мой Создатель\n'
            '2 - Главный герой из его любимой игры The Forest')
    bot.send_message(message.chat.id, text,
                     reply_markup=keyboard, parse_mode="HTML")


echo_is_on = False


@bot.message_handler(commands=['echo'])
def echo(message):
    ans_echo_keyboard = make_ans_echo_keyboard()
    global echo_is_on
    if echo_is_on:
        bot.send_message(message.chat.id, 'Хотите выключить режим эхо?', reply_markup=ans_echo_keyboard)
    else:
        bot.send_message(message.chat.id, 'Хотите включить режим эхо? (с фото тоже работает)',
                         reply_markup=ans_echo_keyboard)
# ------------------------------------------ПРИВЕТСТВИЕ/ПРОЩАНИЕ--------------------------------------------------------


@bot.message_handler(content_types=['text'], func=check_greet)
def greeting(message):
    # одно из привествий связано со временем
    import datetime

    def check_time():
        current_time = datetime.datetime.now().time()
        if current_time < datetime.time(12):
            return f'Доброе утро, {message.from_user.first_name}!'
        elif current_time < datetime.time(18):
            return f'Добрый день, {message.from_user.first_name}!'
        else:
            return f'Добрый вечер, {message.from_user.first_name}!'

    greet_time = check_time()
    bot_greets = ['Привет-привет!', f'Здравствуйте, {message.from_user.first_name}!', 'Приветики-пистолетики!',
                  f'Приветсвую, {message.from_user.first_name}!',
                  f'Здравья желаю, товарищ, {message.from_user.first_name}!', greet_time]
    rand_greet = random.choice(bot_greets)
    bot.send_message(message.chat.id, rand_greet)


@bot.message_handler(content_types=['text'], func=check_bye)
def farewell(message):
    bye = (f'До встречи, {message.from_user.first_name}! Если захотите еще раз услышать об интересных людях, '
           f'я всегда к вашим услугам.')
    bot.send_message(message.chat.id, bye)


# ----------------------------------------------------ОЦЕНКИ------------------------------------------------------------
rating_is_on = False
rates = {'Мой Создатель': '0',
         'Главный Герой': '0'}
current_rate = 0
current_char = ''
rate = ''


@bot.message_handler(commands=['rate'])
def rating(message):
    keyboard = make_characters_names_keyboard()
    bot.send_message(message.chat.id, 'Какого персонажа вы хотите оценить: ', reply_markup=keyboard)
    global rating_is_on
    rating_is_on = True


@bot.message_handler(commands=['my_rates'])
def my_rates(message):
    bot.send_message(message.chat.id, 'Предоставляю вам ваши оценки:')
    for char, char_rate in rates.items():
        if char_rate == '0':
            bot.send_message(message.chat.id, f'У персонажа "{char}" пока нет оценки.')
        else:
            bot.send_message(message.chat.id, f'Персонаж "{char}" имеет оценку {char_rate}.')


def isfloat(message):
    new_msg = message.text.replace(',', '.')
    try:
        float(new_msg)
    except ValueError:
        return False
    return True


@bot.message_handler(content_types=['text'], func=isfloat)
def rate_with_nums(message):
    global rate
    rate = message.text
    if current_char in rates.keys():
        if rate in ['1', '2', '3', '4', '5']:
            ans_rate_keyboard = make_ans_rate_keyboard()
            bot.send_message(message.chat.id, f'Вы хотите поставить оценку персонажу "{current_char} "?',
                             reply_markup=ans_rate_keyboard)
        else:
            bot.send_message(message.chat.id, 'Кажется, вы отправили неверное число.'
                                              ' Если вы хотите оценить персонажа, '
                                              'то отправьте цифру от 1 до 5.')
    else:
        bot.send_message(message.chat.id, 'Кажется, вы отправили число. Если вы хотите оценить персонажа, '
                                          'то сначала выберите его через команду  /rate, а потом'
                                          ' отправьте цифру от 1 до 5.')


# ----------------------------------------------------------------------------------------------------------------------
# все, что будет, если пользователь напишет имя персонажа


characters = {'Мой Создатель': AboutMe,
              'Главный Герой': AboutCharacter}
about_me = ['возраст', 'хобби', 'интересы', 'история', 'проекты']
about_character = ['возраст', 'хобби', 'интересы', 'история']
character = ''


@bot.message_handler(content_types=['text'], func=lambda message: message.text.title() in characters.keys())
def talk_about(message):
    global rating_is_on  # если пользователь до этого написал /rate, то выведется меню оценивания
    if rating_is_on:
        inline_kb = make_rating_keyboard()
        bot.send_message(message.chat.id, 'Оцените персонажа от 1 до 5 (цифру можно написать):', reply_markup=inline_kb)
        global current_char
        current_char = message.text.title()
        rating_is_on = False
    else:  # иначе выведется меню информации о персонаже
        global character
        character = message.text.title()
        new_ans = characters[character].tell_about()
        pic = characters[character].get_photo()
        bot.send_photo(message.chat.id, pic, new_ans)
        options_keyboard = make_characters_options_keyboard()
        bot.send_message(message.chat.id, 'Что бы вы хотели обо мне узнать?', reply_markup=options_keyboard)
# ----------------------------------------------------------------------------------------------------------------------
# кнопка для возвращения обратно в меню персонажей


@bot.message_handler(content_types=['text'],
                     func=lambda message: message.text.lower() == 'вернуться к списку персонажей')
def back(message):
    keyboard = make_characters_names_keyboard()
    bot.send_message(message.chat.id, 'О ком бы вы хотели узнать?', reply_markup=keyboard)
# ----------------------------------------------------------------------------------------------------------------------
# вывод информации о персонаже в зависимости от категории


def check_option(message):
    for i in about_me:
        if i in message.text.lower():
            return True


@bot.message_handler(content_types=['text'], func=check_option)
def about(message):
    ans = message.text.lower()

    try:
        characters[character]
    except KeyError:
        keyboard = make_characters_names_keyboard()
        bot.send_message(message.chat.id, 'Вы пока еще не выбрали ни одного персонажа.'
                         ' Выберите, чтобы узнать информацию о нем:', reply_markup=keyboard)
    else:
        new_ans = 'что-то там'  # это для PEP8
        if 'возраст' in ans:
            new_ans = characters[character].about_age()
        if 'хобби' in ans:
            new_ans = characters[character].about_hobbies()
        if 'интересы' in ans:
            new_ans = characters[character].about_interests()
        if 'история' in ans and character != 'Главный Герой':
            new_ans = characters[character].about_history()
        if 'история' in ans and character == 'Главный Герой':
            new_ans = characters[character].about_history()
            keyboard = InlineKeyboardMarkup()  # решил не выносить в отдельную функцию, т.к здесь всего 1 кнопка
            btn = InlineKeyboardButton('Посмотреть трейлер игры (youtube)', url='https://youtu.be/8KXfxHujIAA')
            keyboard.add(btn)
            bot.send_message(message.chat.id, new_ans, reply_markup=keyboard)
        elif 'проекты' not in ans:
            bot.send_message(message.chat.id, new_ans)
        if character == 'Мой Создатель' and 'проекты' in ans:
            keyboard = InlineKeyboardMarkup()  # решил не выносить в отдельную функцию, т.к здесь всего 1 кнопка
            btn = InlineKeyboardButton('Фильтр фотографий', url='https://github.com/NikkyBricky/Photo-Filting')
            keyboard.add(btn)
            new_ans = characters[character].about_projects()
            bot.send_message(message.chat.id, new_ans, reply_markup=keyboard)


# отправка ботом сообщения на любое не подходящее под другие декораторы смс
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio'])
def turn_on_echo_mode(message):
    global echo_is_on
    if echo_is_on:

        if message.photo:  # проверяем, что отправил пользователь
            fileid = message.photo[-1].file_id
            file_info = bot.get_file(fileid)
            downloaded_file = bot.download_file(file_info.file_path)

            bot.send_photo(message.chat.id, photo=downloaded_file)
        elif message.text:   # проверяем, что отправил пользователь
            bot.send_message(message.chat.id, message.text)
        else:
            bot.send_message(message.chat.id, 'Я пока не знаю, как работать с такой формулировкой сообщения.\n'
                                              'Если хотите узнать о доступных функциях, напишите /help')
    else:
        bot.send_message(message.chat.id, 'Я пока не знаю, как работать с такой формулировкой сообщения.\n'
                                          'Если хотите узнать о доступных функциях, напишите /help')


# -----------------------------------------------------КЛАВИАТУРЫ-------------------------------------------------------
def make_characters_names_keyboard():
    char_buttons = [KeyboardButton(char_name) for char_name in characters.keys()]
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(*char_buttons)
    return markup


def make_characters_options_keyboard():
    button_back = KeyboardButton('Вернуться к списку персонажей')
    if character != 'Главный Герой':
        char_buttons = [KeyboardButton(char_option) for char_option in about_me]
    else:
        char_buttons = [KeyboardButton(char_option) for char_option in about_character]
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(*char_buttons).add(button_back)
    return markup


def make_rating_keyboard():
    rate_keyboard = InlineKeyboardMarkup(row_width=5)
    btn1 = InlineKeyboardButton('1', callback_data='1')
    btn2 = InlineKeyboardButton('2', callback_data='2')
    btn3 = InlineKeyboardButton('3', callback_data='3')
    btn4 = InlineKeyboardButton('4', callback_data='4')
    btn5 = InlineKeyboardButton('5', callback_data='5')
    rate_keyboard.add(btn1, btn2, btn3, btn4, btn5)
    return rate_keyboard


def make_ans_rate_keyboard():
    ans_markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Да', callback_data='yes')
    btn2 = InlineKeyboardButton('Нет', callback_data='no')
    ans_markup.add(btn1, btn2)
    return ans_markup


def make_ans_echo_keyboard():
    ans_markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Да', callback_data='Yes')
    btn2 = InlineKeyboardButton('Нет', callback_data='No')
    ans_markup.add(btn1, btn2)
    return ans_markup


# -------------------------------------------РЕАЛИЗАЦИЯ КНОПОК----------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def save_rate(call):
    global rate
    global current_rate, current_char
    if call.data in ['1', '2', '3', '4', '5']:
        rates[current_char] = call.data
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Получил вашу оценку ({call.data}) для персонажа "{current_char}"',
                              reply_markup=None)
        bot.send_message(call.message.chat.id, 'Спасибо за вашу оценку!\n'
                                               'Посмотреть свои оценки вы можете, используя команду /my_rates')
    if call.data == 'yes':
        rates[current_char] = rate
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Получил вашу оценку ({rate}) для персонажа "{current_char}"', reply_markup=None)
        rate = ''
        bot.send_message(call.message.chat.id, 'Спасибо за вашу оценку!\n'
                                               'Посмотреть свои оценки вы можете, используя команду /my_rates')
    if call.data == 'no':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Хорошо! Если хотите увидеть мой функционал, напишите /help или '
                                   'нажмите на кнопку "меню" в левом углу окна сообщения', reply_markup=None)
    global echo_is_on
    if call.data == 'Yes':
        if echo_is_on:
            echo_is_on = False
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Хорошо! Если хотите увидеть мой функционал, напишите /help или '
                                       'нажмите на кнопку "меню" в левом углу окна сообщения', reply_markup=None)
        else:
            echo_is_on = True
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Функция "Эхо" включена! Чтобы выключить ее, напишите команду /echo еще раз и'
                                       ' положительно ответьте на вопрос.',
                                  reply_markup=None)
    if call.data == 'No':
        if echo_is_on:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Оставляю функцию "Эхо" включенной. Чтобы выключить ее, '
                                       'напишите команду /echo еще раз и положительно ответьте на вопрос.',
                                  reply_markup=None)

        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Хорошо! Функция "Эхо" выключена.'
                                       ' Если хотите увидеть мой функционал, напишите /help или '
                                       'нажмите на кнопку "меню" в левом углу окна сообщения', reply_markup=None)
# ----------------------------------------------------------------------------------------------------------------------


bot.polling()  # начало работы
