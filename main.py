import telebot
from telebot import types
import datetime
import random

from data.music import *
from data.films import *
from data.film_parser import parser, img_installer, clear_logs

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
wanna_to_you_mode = False


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
            bot.send_message(
                message.chat.id,
                f'Ты можешь ввести /help для вывода списка команд'
                f'Если ты введешь команду /start то появится основное меню'
            )
            bot.send_message(
                738718406,
                'NEW USER DETECTED'
            )
        else:
            bot.send_message(
                message.chat.id, 'Этот бот только для одного человека. Подтвердите свою личность.'
            )
    else:
        bot.send_message(
            message.chat.id, 'Ты уже подтвердила свою личность'
        )


@bot.message_handler(func=lambda message: message.chat.id not in accepted_chats,
                     commands=['start', 'pass', 'send_sms', 'escape'])
def accepted_checker(message):
    bot.send_message(message.chat.id, 'Этот бот только для одного человека. Подтвердите свою личность.')


@bot.message_handler(commands=['send_sms'])
def send_mess_to_me_checker(message):
    bot.send_message(
        738718406,
        f'{message.text.replace("/send_sms", "")}'
    )
    bot.send_message(
        message.chat.id,
        'сообщение отправленно'
    )


@bot.message_handler(commands=['escape'])
def escape_from_all(message):
    global music_mode
    global bad_mood_mode
    global cinematic_mode
    global wanna_to_you_mode
    music_mode = False
    bad_mood_mode = False
    cinematic_mode = False
    wanna_to_you_mode = False
    clear_logs()

    markup = types.ReplyKeyboardMarkup()
    item1 = types.KeyboardButton("🙉Хочу музычки")
    item2 = types.KeyboardButton('😎Хочу фильмец')
    item3 = types.KeyboardButton('😿Мне грустно')
    item4 = types.KeyboardButton('Хочу провести время с тобой👉👈')
    item5 = types.KeyboardButton('Пока не знаю чего хочу')
    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(
        message.chat.id,
        f'Выход в главное меню...',
        reply_markup=markup
    )


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
    item4 = types.KeyboardButton('Хочу провести время с тобой👉👈')
    item5 = types.KeyboardButton('Пока не знаю чего хочу')
    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(
        message.chat.id,
        f'{day_time}, солнышко, начнём?)',
        parse_mode='html',
        reply_markup=markup
    )
    bot.send_message(
        message.chat.id,
        f'Ты можешь ввести /help для вывода списка команд'
        f'Если ты введешь команду /start то появится основное меню'
    )


@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(
        message.chat.id,
        '''
        список команд: \n
        \"/start\" - начать работу \n
        \"/pass + пароль\" - ввод пароля
        \"/escape\" - выход из всех разделов в главное меню
        \"/send_sms + сообщение - отправить мне сообщение\"
        '''
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'films_comedy':
                bot.send_message(
                    call.message.chat.id,
                    f'{comedy[random.randint(1, len(comedy))]}'
                )

            if call.data == 'films_melodramma':
                bot.send_message(
                    call.message.chat.id,
                    f'{moralshina[random.randint(1, len(moralshina))]}'
                )

            if call.data == 'films_thriller':
                bot.send_message(
                    call.message.chat.id,
                    f'{thrillers[random.randint(1, len(thrillers))]}'
                )
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Хочу какой-нибудь фильмец', reply_markup=None)
    except Exception as e:
        print(repr(e))


@bot.message_handler(content_types=['text'])
def message_render(message):
    global music_mode
    global bad_mood_mode
    global cinematic_mode
    global wanna_to_you_mode
    if message.chat.type == 'private':
        print(message.text)

        if message.text == 'Пока не знаю чего хочу':
            bot.send_message(
                message.chat.id,
                f'Тогда ты можешь написать мне и я помогу тебе с этой проблемой))\n'
                f't-do.ru/alekzluthor'
            )

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
            item2 = types.KeyboardButton('Хочу сериальчик')
            item3 = types.KeyboardButton('Хочу какой-нибудь фильмец')
            item4 = types.KeyboardButton('Я передумала...')
            markup.add(item1, item2, item3, item4)

            bot.send_message(
                message.chat.id, f'Что именно ты хочешь?',
                reply_markup=markup
            )

        # WANNA TO YOU MODE MAIN
        if message.text == 'Хочу провести время с тобой👉👈':
            wanna_to_you_mode = True

            markup = types.ReplyKeyboardMarkup()
            item1 = types.KeyboardButton("Хочу погулять с тобой")
            item2 = types.KeyboardButton('Хочу с тобой в кино')
            item3 = types.KeyboardButton('Хочу вместе посмотреть фильм в дискордике')
            item4 = types.KeyboardButton('Хочу поиграть в лигу')
            item5 = types.KeyboardButton('Просто хочу поговорить')
            item6 = types.KeyboardButton('Обратно в меню')
            markup.add(item1, item2, item3, item4, item5, item6)

            bot.send_message(
                message.chat.id,
                f'Что именно хочешь, солнце?',
                reply_markup=markup
            )

        # BAD MOOD MAIN
        if message.text == '😿Мне грустно':
            bad_mood_mode = True
            bot.send_message(
                738718406,
                f'!BAD_MOOD_TRIGGER'
            )

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

        # WANNA TO YOU TREE
        if wanna_to_you_mode:
            if message.text == 'Хочу погулять с тобой':
                bot.send_message(
                    message.chat.id,
                    f'Понял тебя\n'
                    f'Саше уже отправленно уведомление, жди его под своим окном)',
                    parse_mode='html'
                )
                bot.send_message(
                    738718406,
                    f'!WANNA TO YOU: Настя хочет погулять'
                )

            if message.text == 'Хочу с тобой в кино':
                bot.send_message(
                    message.chat.id,
                    f'Понял принял\n'
                    f'Саше уже отправленно уведомление, а пока ты можешь посмотреть что сейчас есть в кино\n'
                    f'Для этого зайди в раздел "😎Хочу фильмец" -> "Хочу в кино"',
                    parse_mode='html'
                )
                bot.send_message(
                    738718406,
                    f'!WANNA TO YOU: Настя хочет в кино'
                )

            if message.text == 'Хочу вместе посмотреть фильм в дискордике':
                bot.send_message(
                    message.chat.id,
                    f'Уииии\n'
                    f'Я уже отправил Саше уведомление, а пока ты можешь выбрать фильм который хочешь посмотреть\n'
                    f'Для этого зайди в раздел "😎Хочу фильмец" -> "Хочу фильм"',
                    parse_mode='html'
                )
                bot.send_message(
                    738718406,
                    f'!WANNA TO YOU: Настя хочет вместе посмотреть фильм в дискорде'
                )

            if message.text == 'Хочу поиграть в лигу':
                bot.send_message(
                    message.chat.id,
                    f'Вау)\n'
                    f'Хорошо, я передам Саше, увидимся в лиге)',
                    parse_mode='html'
                )
                bot.send_message(
                    738718406,
                    f'!WANNA TO YOU: Настя хочет в лигу'
                )

            if message.text == 'Просто хочу поговорить':
                bot.send_message(
                    message.chat.id,
                    f'Ты моё солнце\n'
                    f'Скоро позвоню тебе, но если я туплю можешь сделать это тут:\n'
                    f'+79514735636\n'
                    f't-do.ru/alekzluthor\n',
                    parse_mode='html'
                )
                bot.send_message(
                    738718406,
                    f'!WANNA TO YOU: Настя хочет поговорить'
                )

            if message.text == 'Обратно в меню':
                wanna_to_you_mode = False

                markup = types.ReplyKeyboardMarkup()
                item1 = types.KeyboardButton("🙉Хочу музычки")
                item2 = types.KeyboardButton('😎Хочу фильмец')
                item3 = types.KeyboardButton('😿Мне грустно')
                item4 = types.KeyboardButton('Хочу провести время с тобой👉👈')
                item5 = types.KeyboardButton('Пока не знаю чего хочу')
                markup.add(item1, item2, item3, item4, item5)

                bot.send_message(
                    message.chat.id,
                    f'Я надеюсь ты выходишь, потому что что-то выбрала\n'
                    f'В любом случае спасибо что заглянула\n'
                    f'Люблю тебя солнышко, увидимся',
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
                item4 = types.KeyboardButton('Хочу провести время с тобой👉👈')
                item5 = types.KeyboardButton('Пока не знаю чего хочу')
                markup.add(item1, item2, item3, item4, item5)
                bot.send_message(
                    message.chat.id,
                    f'Ладно...',
                    reply_markup=markup
                )

        # FILMS MODE TREE
        if cinematic_mode:

            if message.text == 'Хочу в кино':
                bot.send_message(
                    message.chat.id,
                    f'Подожди секундочку...'
                )
                img_installer()
                headlines, description, time = parser(1)
                new_time = []
                for i in time:
                    j = i.replace("\n", " ")
                    j = j[2:]
                    new_time.append(j)
                bot.send_message(
                    message.chat.id,
                    f'Вот что сейчас в кино:'
                )
                for i in range(len(headlines)):
                    with open(f"/pythonProject1/data/posters/{i}.jpg", 'rb') as poster:
                        bot.send_photo(
                            message.chat.id,
                            poster,
                            caption=f'{headlines[i]}'
                                    f'{description[i]}'
                                    f'Время сеансов:\n'
                                    f'{new_time[i]}',
                            parse_mode='HTML'
                        )

            if message.text == 'Хочу какой-нибудь фильмец':
                inline_markup = types.InlineKeyboardMarkup(row_width=3)
                item1 = types.InlineKeyboardButton('Комедию', callback_data='films_comedy')
                item2 = types.InlineKeyboardButton('Мелодрамму', callback_data='films_melodramma')
                item3 = types.InlineKeyboardButton('Триллер', callback_data='films_thriller')
                inline_markup.add(item1, item2, item3)
                bot.send_message(
                    message.chat.id,
                    f'Какой жанр?',
                    reply_markup=inline_markup
                )

            if message.text == 'Хочу сериальчик':
                bot.send_message(
                    message.chat.id,
                    f'Вот рандомный сериальчик\n'
                    f'{serials[random.randint(1, len(serials))]}'
                )

            if message.text == 'Я передумала...':
                cinematic_mode = False
                clear_logs()
                markup = types.ReplyKeyboardMarkup()
                item1 = types.KeyboardButton("🙉Хочу музычки")
                item2 = types.KeyboardButton('😎Хочу фильмец')
                item3 = types.KeyboardButton('😿Мне грустно')
                item4 = types.KeyboardButton('Хочу провести время с тобой👉👈')
                item5 = types.KeyboardButton('Пока не знаю чего хочу')
                markup.add(item1, item2, item3, item4, item5)
                bot.send_message(
                    message.chat.id,
                    f'Хорошо',
                    reply_markup=markup
                )

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
                markup = types.ReplyKeyboardMarkup()
                item1 = types.KeyboardButton("🙉Хочу музычки")
                item2 = types.KeyboardButton('😎Хочу фильмец')
                item3 = types.KeyboardButton('😿Мне грустно')
                item4 = types.KeyboardButton('Хочу провести время с тобой👉👈')
                item5 = types.KeyboardButton('Пока не знаю чего хочу')
                markup.add(item1, item2, item3, item4, item5)
                bot.send_message(
                    message.chat.id,
                    f'Я рад, солнышко',
                    reply_markup=markup
                )


if __name__ == '__main__':
    bot.polling(non_stop=True)
