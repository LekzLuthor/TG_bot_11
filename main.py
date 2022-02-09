import telebot
from telebot import types
import datetime
import random

from data.music import *
from data.film_parser import parser, img_installer

TOKEN = '5169770075:AAGPtGFOXMfTwVw8JwYIEWurX4pyXdLBNbA'
PASS = '24.05.2020'
bot = telebot.TeleBot(TOKEN)
accepted_chats = []
try:
    with open('chats_id_base.txt', 'r') as f:
        accepted_chats = [int(i) for i in f.readline().split(';') if i != '']
except FileNotFoundError:
    accepted_chats = []
print(accepted_chats)

music_mode = False
bad_mood_mode = False
cinematic_mode = False


# morning=1, day=2, evening=3, night=0
def time_of_day():
    current_date_time = datetime.datetime.now()
    current_time = current_date_time.time()
    hour = int(str(current_time)[:2])
    if 5 <= hour <= 11:
        return 1
    if 12 <= hour <= 17:
        return 2
    if 18 <= hour <= 0:
        return 3
    if 1 <= hour <= 4:
        return 0


@bot.message_handler(commands=['pass'])
def get_pass_mess(message):
    if message.chat.id not in accepted_chats:
        if message.text == f'/pass {PASS}':
            accepted_chats.append(message.chat.id)
            with open('chats_id_base.txt', 'a') as file:
                file.write(f'{message.chat.id};')
            print(accepted_chats)

            bot.send_message(
                message.chat.id, 'Рад тебя видеть, солнышко'
            )
        else:
            bot.send_message(
                message.chat.id, 'Этот бот только для одного человека. Подтвердите свою личность.'
            )
    else:
        bot.send_message(
            message.chat.id, 'Ты уже подтвердила свою личность'
        )


@bot.message_handler(func=lambda message: message.chat.id not in accepted_chats, commands=['start'])
def accepted_checker(message):
    bot.send_message(message.chat.id, 'Этот бот только для одного человека. Подтвердите свою личность.')


@bot.message_handler(commands=['start'])
def start_message(message):
    time_code = time_of_day()

    if time_code == 0:
        day_time = 'Доброй ночи'
    elif time_code == 1:
        day_time = 'Доброе утро'
    elif time_code == 2:
        day_time = 'Добрый день'
    else:
        day_time = 'Добрый вечер'

    # создание доп клавиатуры
    markup = types.ReplyKeyboardMarkup()
    item1 = types.KeyboardButton("🙉Хочу музычки")
    item2 = types.KeyboardButton('😎Хочу фильмец')
    item3 = types.KeyboardButton('😿Мне грустно')
    item4 = types.KeyboardButton('Пока не знаю чего хочу')
    markup.add(item1, item2, item3, item4)
    bot.send_message(
        message.chat.id,
        f'{day_time}, Анастасия, начнём?)',
        parse_mode='html',
        reply_markup=markup
    )


@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(
        message.chat.id,
        '''
        список команд: \n
        \"/start\" - начать работу \n
        \"/pass + пароль\" - ввод пароля
        '''
    )


@bot.message_handler(content_types=['text'])
def message_render(message):
    global music_mode
    global bad_mood_mode
    global cinematic_mode
    if message.chat.type == 'private':
        print(message.text)

        # MUSIC MAIN
        if message.text == '🙉Хочу музычки':
            music_mode = True

            markup = types.ReplyKeyboardMarkup()
            item1 = types.KeyboardButton("Хочу гулять одна в наушниках")
            item2 = types.KeyboardButton('Хочу прыгать по комнате и орать')
            item3 = types.KeyboardButton('Ничего не хочу')
            item4 = types.KeyboardButton('К тебе хочу')
            item5 = types.KeyboardButton('Спец раздел')  # !!!!!!
            item6 = types.KeyboardButton('Я передумала...')
            markup.add(item1, item2, item3, item4, item5, item6)

            bot.send_message(
                message.chat.id, f'Что по настроению?',
                reply_markup=markup
            )

        # FILMS MAIN
        if message.text == '😎Хочу фильмец':
            cinematic_mode = True

            markup = types.ReplyKeyboardMarkup()
            item1 = types.KeyboardButton("Хочу в кино")
            item2 = types.KeyboardButton('Хочу сериал')
            item3 = types.KeyboardButton('Хочу фильм')
            item4 = types.KeyboardButton('Я передумала...')
            markup.add(item1, item2, item3, item4)

            bot.send_message(
                message.chat.id, f'Что именно ты хочешь?',
                reply_markup=markup
            )

        # BAD MOOD MAIN
        if message.text == '😿Мне грустно':
            bad_mood_mode = True

            markup = types.ReplyKeyboardMarkup()
            item1 = types.KeyboardButton("Родители творят дичь")
            item2 = types.KeyboardButton('Неудачный день...')
            item3 = types.KeyboardButton('Просто нет настроения')
            item4 = types.KeyboardButton('К тебе хочу')
            item5 = types.KeyboardButton('Стало лучше..)')
            markup.add(item1, item2, item3, item4, item5)

            bot.send_message(
                message.chat.id, f'Что случилось?',
                reply_markup=markup
            )

        # MUSIC MODE TREE
        if music_mode:
            if message.text == 'Хочу гулять одна в наушниках':  # 1
                track_numbs = [random.randint(1, len(first)) for i in range(5)]
                for i in range(5):
                    bot.send_message(
                        message.chat.id, f'{first[track_numbs[i]]}'
                    )

            if message.text == 'Хочу прыгать по комнате и орать':  # 2
                track_numbs = [random.randint(1, len(second)) for i in range(5)]
                for i in range(5):
                    bot.send_message(
                        message.chat.id, f'{second[track_numbs[i]]}'
                    )

            if message.text == 'Ничего не хочу':  # 3
                track_numbs = [random.randint(1, len(third)) for i in range(5)]
                for i in range(5):
                    bot.send_message(
                        message.chat.id, f'{third[track_numbs[i]]}'
                    )

            if message.text == 'К тебе хочу':  # 4
                track_numbs = [random.randint(1, len(fourth)) for i in range(5)]
                for i in range(5):
                    bot.send_message(
                        message.chat.id, f'{fourth[track_numbs[i]]}'
                    )

            # Возвращение в главное меню
            if message.text == 'Я передумала...':
                music_mode = False
                markup = types.ReplyKeyboardMarkup()
                item1 = types.KeyboardButton("🙉Хочу музычки")
                item2 = types.KeyboardButton('😎Хочу фильмец')
                item3 = types.KeyboardButton('😿Мне грустно')
                item4 = types.KeyboardButton('Пока не знаю чего хочу')
                markup.add(item1, item2, item3, item4)
                bot.send_message(
                    message.chat.id,
                    f'Ладно...',
                    reply_markup=markup
                )

        # FILMS MODE TREE
        if cinematic_mode:
            if message.text == 'Хочу в кино':
                headlines, description, time = parser(1)
                img_installer()
                bot.send_message(
                    message.chat.id,
                    f'Вот что сейчас в кино:'
                )
                for i in range(len(headlines)):
                    bot.send_message(
                        message.chat.id,
                        f'{headlines[i]}'
                        f'{description[i]}'
                        f'{time[i]}'

                    )
            if message.text == 'Хочу сериал':
                pass
            if message.text == 'Хочу фильм':
                pass
            if message.text == 'Я передумала...':
                cinematic_mode = False

        # BAD MOOD MODE TREE
        if bad_mood_mode:
            if message.text == 'Родители опять творят дичь':
                pass
            if message.text == 'Неудачный день...':
                pass
            if message.text == 'Просто нет настроения':
                pass
            if message.text == 'К тебе хочу':
                pass

            # Возвращение в главное меню
            if message.text == 'Стало лучше..)':
                bad_mood_mode = False


if __name__ == '__main__':
    bot.polling(non_stop=True)
