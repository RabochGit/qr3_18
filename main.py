import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6395527947:AAFocv0mOM60nwQmv3VcAxqgo7RnA05Bs7E",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    descr = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Создать задачу"  # Можно менять текст
text_button_1 = "_Сегодня_"  # Можно менять текст
text_button_2 = "_Завтра_"  # Можно менять текст
text_button_3 = "Info и *полезные ссылочки*"  # Можно менять текст

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    ),
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)



@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Приветствую вас! Я ваш личный помощник в организации времени. Меня зовут Савва. <br> Моя задача - помочь вам структурировать ваш день и достичь большей продуктивности. <br> Вы можете использовать меня, чтобы создавать задачи, устанавливать напоминания и следить за своим расписанием. <br> Я всегда здесь, чтобы помочь вам в этом. <br> Если у вас возникнут вопросы или нужна помощь, не стесняйтесь обращаться. <br> Давайте начнем работу! Чем я могу вам помочь сегодня?',  # Можно менять текст
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Супер! Напиши название задачи')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер! Добавь описание задачи')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.descr, message.chat.id)


@bot.message_handler(state=PollState.descr)
def descr(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['descr'] = message.text
    bot.send_message(message.chat.id, 'Записал!', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Держи список задач на сегодня:", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Держи список задач на завтра:", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Привет! Я - Савва, ваш личный помощник в организации времени. Управляйте своим расписанием проще и продуктивнее. Создавайте задачи, устанавливайте напоминания, просматривайте свое расписание. Давайте начнем работу! <br> Полезные ссылочки тут: <br> [Видео по тайм-менеджменту] (https://youtu.be/YH01ldFrVRo?si=fh1rWjkpjPDLOIYW) <br> [Крутая статья от Умскула] (https://umschool.net/journal/issledovaniya/issledovanie-tajm-menedzhment-vypusknikov-pri-podgotovke-k-ekzamenam/) <br> [Красивый планер] (https://ru.pinterest.com/pin/214484000996367658/)")  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()