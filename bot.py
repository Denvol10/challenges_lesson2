from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings
import ephem
import time

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

# Создадим функцию greet_user
def greet_user(bot, update): # bot - экземпляр нашего бота, с помощью него даем команды, update - сообщение от telegram
    text = 'Данный бот предназначен для вывода информации о текущем положении планет\
    введите команду в формате /planet "название планеты на английском", например\
    /planet Mars. Для вывода информации о следующем полнолунии введите команду /next_full_moon "дата в формате years/month/day",\
    напимер /next_full_moon 2019/05/26. Для вывода информации о следующем полнолунии относительно сегодня введите команду\
    /next_full_moon today'
    print(text)
    update.message.reply_text(text)

# Создаем функцию talk_to_me:
def talk_to_me(bot, update):
    user_text = 'Привет {}! Ты написал: {}'.format(update.message.chat.first_name, update.message.text)
    logging.info('User: %s, Chat id: %s, Message: %s', update.message.chat.username,
                update.message.chat.id, update.message.text)
    update.message.reply_text(user_text)

# Создадим функцию, которая показывает в каком созвездии находится планета, используя модуль ephem
def constell_panet(bot, update):
    planet = update.message.text.split()[-1]
    now_date = time.strftime('%Y/%m/%d')
    print(planet, now_date)
    if planet == 'Mercury':
        ep_planet = ephem.Mercury(now_date)
    elif planet == 'Venus':
        ep_planet = ephem.Venus(now_date)
    elif planet == 'Mars':
        ep_planet = ephem.Mars(now_date)
    elif planet == 'Jupiter':
        ep_planet = ephem.Jupiter(now_date)
    elif planet == 'Saturn':
        ep_planet = ephem.Saturn(now_date)
    elif planet == 'Uranus':
        ep_planet = ephem.Uranus(now_date)
    elif planet == 'Neptune':
        ep_planet = ephem.Neptune(now_date)
    else:
        print('Ввод неверный')
    const = ephem.constellation(ep_planet)
    print(const)
    user_text_const = f'Планета {planet} сегодня находится в созвездии {const}'
    print(user_text_const)
    update.message.reply_text(user_text_const)

def word_count(bot, update):
    text = update.message.text[10:]
    text_list = text.split()
    # проверка на пустой ввод
    if text_list == []:
        print('Пустой ввод введите текст')
    print(text_list)
    count = 0
    for word in text_list:
        # проверка на то что слово состоит из букв
        if word.isalpha():
            count += 1
        # если после слова есть знак препинания
        elif word[:-1].isalpha():
            count += 1
        # если слово в кавычках или скобках
        elif word[1:-1].isalpha():
            count += 1
    print(f'{count} слова')

def nextFullMoon(bot, update):
    date = update.message.text.split()[-1]
    if date == 'today':
        date = time.strftime('%Y/%m/%d')
    delimiter1 = '-'
    delimiter2 = '/'
    if len(date) == 10 and ((date.find(delimiter1) == 4 and date.rfind(delimiter1) == 7) or ((date.find(delimiter2) == 4 and date.rfind(delimiter2) == 7))):
        date_moon = ephem.next_full_moon(date)
        date_moon_text = f'Следующее полнолуние {date_moon}'
    else:
        print('Введите дату в правильном формате!')
        update.message.reply_text('Введите дату в правильном формате!')
    print(date_moon_text)
    update.message.reply_text(date_moon_text)



# Тело бота, объявляем функцию main()
def main():
    # создаем переменную для взаимодействия с ботом
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    # текст в логе при запуске бота
    logging.info('Bot starts')

    # создание объекта принимающие входящие сообщения и передающий их дальше (обработчик команд)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user)) # 'start' - команда в telegram, greet_user - название функции (любое)

    # добавление команды в бота, которая принимает на вход название планеты
    dp.add_handler(CommandHandler('planet', constell_panet))

    # добавление команды в бота, которая считает количество слов в предложении
    dp.add_handler(CommandHandler('wordcount', word_count))

    # добавление команды в бота, которая принимает на вход дату для следующего полнолуния
    dp.add_handler(CommandHandler('next_full_moon', nextFullMoon))

    # хэндлер для перехвата текстовых сообщений пользователя
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    # обращаться к телеграмм и проверять наличие сообщений
    mybot.start_polling()

    # mybot будет работать до принудительной остановки
    mybot.idle()

# делаем вызов функции main(), запускаем бота
main()