# --------------------------------------------------ИМПОРТЫ-------------------------------------------------------------
import telebot
from telebot.types import (KeyboardButton, ReplyKeyboardMarkup, Message, InlineKeyboardMarkup, InlineKeyboardButton)
from info import AboutMe, AboutCharacter
from dotenv import load_dotenv
import os
import random
import json
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
def save_to_js():
    with open('user_data.json', 'w', encoding='utf8') as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)


def load_from_js():
    try:
        with open('user_data.json', 'r+', encoding='utf8') as f:
            data = json.load(f)
    except Exception:
        data = {}
    return data


user_data = load_from_js()


@bot.message_handler(commands=['start'])
@bot.message_handler(content_types=['text'], func=lambda message: 'Кто Я' in message.text.title())
def starting(message):
    keyboard = make_main_menu_keyboard()
    greet = (f'Привет, {message.from_user.first_name}!\n Я бот-визитка.\n'
             f' Я создан для того, чтобы рассказывать миру об интересных существах - людях, '
             f'персонажах из игр, мультиков и т.п. Приятного пользования!\n')
    img = 'https://i.postimg.cc/cJK9qZr6/photo-5465308694494432771-y.jpg'
    bot.send_photo(message.chat.id, img, greet, reply_markup=keyboard)
    user_id = f'{message.from_user.id}'
    if user_id not in user_data:
        user_data[user_id] = {}
        user_data[user_id]['echo_is_on'] = False
        user_data[user_id]['rates'] = {'Мой Создатель': '0',
                                       'Главный Герой': '0'}

        save_to_js()


@bot.message_handler(commands=['help'])
@bot.message_handler(content_types=['text'], func=lambda message: 'Обо Мне' in message.text.title())
def about_bot(message):
    bot.send_message(message.chat.id, 'Что же я могу? К сожалению, я не человек и умею не так много.\n'
                                      'А именно:\n'
                                      '\n'
                                      'Могу разнообразно поприветствовать вас\n'
                                      'Имею неплохую реализацию оценивания персонажа(по-моему скромному'
                                      ' роботовскому мнению)\n'
                                      '/start (Запуск) - главная информация о боте\n'
                                      '/help (Помощь) - опишу свои основные функции\n'
                                      '/who (О персонажах) - покажу, о ком могу рассказать\n'
                                      '/echo (Эхо-мод) - буду отвечать на ваши сообщения таким же сообщением. '
                                      'Работает только с текстом и фото (относится к тем'
                                      ' словам, которые не входят в другие функции бота)\n'
                                      '/rate (Оценить персонажа) - позволяет оценить конкретного персонажа\n'
                                      '/my_rates (Мои оценки )- покажу, как вы оценили моих персонажей\n'
                                      '\n'
                                      'А дальше, в зависимости от вашего выбора, расскажу что-нибудь интересное.')


@bot.message_handler(commands=['who'])
@bot.message_handler(content_types=['text'], func=lambda message: 'О Персонажах' in message.text.title())
def about_characters(message: Message):
    user_id = f'{message.from_user.id}'
    keyboard = make_characters_names_keyboard()
    text = ('Пока я обладаю информацией только о двух живых существах: \n'
            '1 - Мой Создатель\n'
            '2 - Главный герой из его любимой игры The Forest')
    bot.send_message(message.chat.id, text,
                     reply_markup=keyboard, parse_mode="HTML")
    # сделано для того, чтобы при последовательном выборе команд /rate и /who и затем при выборе одного из персонажей
    # в итоге отображалась информация о нем, а не запрос на оценку
    user_data[user_id]['rating_is_on'] = False

    save_to_js()


@bot.message_handler(commands=['echo'])
@bot.message_handler(content_types=['text'], func=lambda message: 'Эхо-Мод' in message.text.title())
def echo(message):
    user_id = f'{message.from_user.id}'
    ans_echo_keyboard = make_ans_echo_keyboard()
    load_from_js()
    if user_data[user_id]['echo_is_on']:
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
@bot.message_handler(commands=['rate'])
@bot.message_handler(content_types=['text'], func=lambda message: 'Оценить Персонажа' in message.text.title())
def rating(message):
    user_id = f'{message.from_user.id}'
    keyboard = make_characters_names_keyboard()
    bot.send_message(message.chat.id, 'Какого персонажа вы хотите оценить: ', reply_markup=keyboard)
    load_from_js()
    user_data[user_id]['rating_is_on'] = True
    save_to_js()


@bot.message_handler(commands=['my_rates'])
@bot.message_handler(content_types=['text'], func=lambda message: 'Мои Оценки' in message.text.title())
def my_rates(message):
    user_id = f'{message.from_user.id}'
    load_from_js()
    bot.send_message(message.chat.id, 'Предоставляю вам ваши оценки:')
    for char, char_rate in user_data[user_id]['rates'].items():
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
    user_id = f'{message.from_user.id}'
    load_from_js()
    user_data[user_id]['current_rate'] = message.text
    save_to_js()
    if 'current_rate_char' in user_data[user_id].keys():
        if user_data[user_id]['current_rate'] in ['1', '2', '3', '4', '5']:
            ans_rate_keyboard = make_ans_rate_keyboard()
            bot.send_message(message.chat.id, 'Вы хотите поставить оценку персонажу ' +
                             user_data[user_id]['current_rate_char'] + '?', reply_markup=ans_rate_keyboard)
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


@bot.message_handler(content_types=['text'], func=lambda message: message.text.title() in characters.keys())
def talk_about(message):
    user_id = f'{message.from_user.id}'
    load_from_js()
    # если пользователь до этого написал /rate, то выведется меню оценивания
    if user_data[user_id]['rating_is_on']:
        inline_kb = make_rating_keyboard()
        bot.send_message(message.chat.id, 'Оцените персонажа от 1 до 5 (цифру можно написать):', reply_markup=inline_kb)
        user_data[user_id]['current_rate_char'] = message.text.title()
        save_to_js()
    else:  # иначе выведется меню информации о персонаже
        user_data[user_id]['current_about_character'] = message.text.title()
        save_to_js()
        new_ans = characters[user_data[user_id]['current_about_character']].tell_about()
        pic = characters[user_data[user_id]['current_about_character']].get_photo()
        bot.send_photo(message.chat.id, pic, new_ans)
        options_keyboard = make_characters_options_keyboard(message)
        bot.send_message(message.chat.id, 'Что бы вы хотели обо мне узнать?', reply_markup=options_keyboard)
# ----------------------------------------------------------------------------------------------------------------------
# кнопка для возвращения обратно в меню персонажей или в главное меню


@bot.message_handler(content_types=['text'],
                     func=lambda message: message.text.lower() == 'вернуться к списку персонажей')
def back_to_characters(message):
    keyboard = make_characters_names_keyboard()
    bot.send_message(message.chat.id, 'О ком бы вы хотели узнать?', reply_markup=keyboard)


@bot.message_handler(content_types=['text'],
                     func=lambda message: message.text.lower() == 'вернуться в главное меню')
def back_to_menu(message):
    user_id = f'{message.from_user.id}'
    load_from_js()
    keyboard = make_main_menu_keyboard()
    bot.send_message(message.chat.id, 'Что вам угодно?', reply_markup=keyboard)
    user_data[user_id]['rating_is_on'] = False
    save_to_js()
# ----------------------------------------------------------------------------------------------------------------------
# вывод информации о персонаже в зависимости от категории


def check_option(message):
    for i in about_me:
        if i in message.text.lower():
            return True


@bot.message_handler(content_types=['text'], func=check_option)
def about(message):
    user_id = f'{message.from_user.id}'
    load_from_js()
    ans = message.text.lower()

    try:
        characters[user_data[user_id]['current_about_character']]
    except KeyError:
        keyboard = make_characters_names_keyboard()
        bot.send_message(message.chat.id, 'Вы пока еще не выбрали ни одного персонажа.'
                         ' Выберите, чтобы узнать информацию о нем:', reply_markup=keyboard)
    else:
        new_ans = 'что-то там'  # это для PEP8
        if 'возраст' in ans:
            new_ans = characters[user_data[user_id]['current_about_character']].about_age()
        if 'хобби' in ans:
            new_ans = characters[user_data[user_id]['current_about_character']].about_hobbies()
        if 'интересы' in ans:
            new_ans = characters[user_data[user_id]['current_about_character']].about_interests()
        if 'история' in ans and user_data[user_id]['current_about_character'] != 'Главный Герой':
            new_ans = characters[user_data[user_id]['current_about_character']].about_history()
        if 'история' in ans and user_data[user_id]['current_about_character'] == 'Главный Герой':
            new_ans = characters[user_data[user_id]['current_about_character']].about_history()
            keyboard = InlineKeyboardMarkup()  # решил не выносить в отдельную функцию, т.к здесь всего 1 кнопка
            btn = InlineKeyboardButton('Посмотреть трейлер игры (youtube)', url='https://youtu.be/8KXfxHujIAA')
            keyboard.add(btn)
            bot.send_message(message.chat.id, new_ans, reply_markup=keyboard)
        elif 'проекты' not in ans:
            bot.send_message(message.chat.id, new_ans)
        if user_data[user_id]['current_about_character'] == 'Мой Создатель' and 'проекты' in ans:
            keyboard = InlineKeyboardMarkup()  # решил не выносить в отдельную функцию, т.к здесь всего 1 кнопка
            btn = InlineKeyboardButton('Мой github', url='https://github.com/NikkyBricky/')
            keyboard.add(btn)
            new_ans = characters[user_data[user_id]['current_about_character']].about_projects()
            bot.send_message(message.chat.id, new_ans, reply_markup=keyboard)


# отправка ботом сообщения на любое не подходящее под другие декораторы смс
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio'])
def turn_on_echo_mode(message):
    user_id = f'{message.from_user.id}'
    if user_data[user_id]['echo_is_on']:

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
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(*char_buttons).add('Вернуться в главное меню')
    return markup


def make_characters_options_keyboard(message):
    user_id = f'{message.from_user.id}'
    load_from_js()
    button_back = KeyboardButton('Вернуться к списку персонажей')
    if user_data[user_id]['current_about_character'] != 'Главный Герой':
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


def make_main_menu_keyboard():
    menu_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add('Кто я? 🙊', 'Обо мне 🤖',
                                                                             'Эхо-мод 🦜', 'О персонажах 📝',
                                                                             'Оценить персонажа #⃣ ', 'Мои оценки 📊')

    return menu_markup
# -------------------------------------------РЕАЛИЗАЦИЯ КНОПОК----------------------------------------------------------


@bot.callback_query_handler(func=lambda call: True)
def save_rate(call):
    user_id = f'{call.from_user.id}'
    load_from_js()
    if call.data in ['1', '2', '3', '4', '5']:
        user_data[user_id]['rates'][user_data[user_id]['current_rate_char']] = call.data
        save_to_js()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Получил вашу оценку ({call.data}) для персонажа "' +
                              user_data[user_id]['current_rate_char'] + '"', reply_markup=None)
        bot.send_message(call.message.chat.id, 'Спасибо за вашу оценку!\n'
                                               'Посмотреть свои оценки вы можете в разделе "Мои оценки" или, '
                                               'используя команду /my_rates')
    if call.data == 'yes':
        user_data[user_id]['rates'][user_data[user_id]['current_rate_char']] = user_data[user_id]['current_rate']
        save_to_js()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Получил вашу оценку ({user_data[user_id]['current_rate']}) для персонажа '
                              f'"{user_data[user_id]['current_rate_char']}"', reply_markup=None)
        bot.send_message(call.message.chat.id, 'Спасибо за вашу оценку!\n'
                                               'Посмотреть свои оценки вы можете в разделе "Мои оценки" или, '
                                               'используя команду /my_rates')
    if call.data == 'no':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Хорошо! Если хотите увидеть мой функционал, перейдите в раздел "Обо мне" '
                                   'или используйте команду /help', reply_markup=None)
    if call.data == 'Yes':
        if user_data[user_id]['echo_is_on']:
            user_data[user_id]['echo_is_on'] = False
            save_to_js()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Хорошо! Если хотите увидеть мой функционал, перейдите в раздел "Обо мне" '
                                       'или используйте команду /help', reply_markup=None)
        else:
            user_data[user_id]['echo_is_on'] = True
            save_to_js()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Функция "Эхо" включена! Чтобы выключить ее, используйте кнопку "Эхо-мод" или'
                                       ' команду /echo еще раз и положительно ответьте на вопрос.', reply_markup=None)
    if call.data == 'No':
        if user_data[user_id]['echo_is_on']:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Оставляю функцию "Эхо" включенной. Чтобы выключить ее, '
                                       'используйте кнопку "Эхо-мод" или команду '
                                       '/echo еще раз и положительно ответьте на вопрос.',
                                  reply_markup=None)

        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Хорошо! Функция "Эхо" выключена.'
                                       ' Если хотите увидеть мой функционал, перейдите в раздел "Обо мне" '
                                       'или используйте /help', reply_markup=None)
# ----------------------------------------------------------------------------------------------------------------------


bot.infinity_polling() # начало работы
