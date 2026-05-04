import time
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
import requests
from requests.exceptions import ConnectionError
from telebot import types
#from random import choice
import telebot
from sqlalchemy.ext.declarative import declarative_base

#from sqlalchemy.orm import mapped_column
#from sqlalchemy.orm import Mapped


Base = declarative_base()


class DebilBase(Base):
    __tablename__ = 'debilki'
    id = Column(Integer, primary_key=True)
    idtg = Column(Integer)
    user = Column(String(30))
    time = Column(String(30))


class HW(Base):
    __tablename__ = 'homework'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    task = Column(String(30))
    deadline = Column(String(30))


engine = create_engine('sqlite:///23dcp.db', echo=True)
#def table_make():
Base.metadata.create_all(engine)

TOKEN = '8593444978:AAHltrFyLi_Es-h7ZNxWbWiyCCAN5KruJqI'
bot = telebot.TeleBot(TOKEN)
# API_TOKEN = '''sk-proj-kM63ox-R7r5UkxcSnpx53bRHute10SdITW8bc-LvVuFGQJw0EdJyFxFWj8YAhsTECegk
# GwDDnpT3BlbkFJPOhd-2isarurQYQnjz2DJlfaqFfJnu2hPo7eJyoCdh0XzI8pLrqEJB0Ael9UI27mJL0YYweUQA'''


@bot.message_handler(commands=['start'])
def welcome(message):
    print('Someone is here')  #чекаю заходы
    print(message.from_user.username)
    print(message.from_user.id)
    print(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))

    idtg = message.from_user.id
    username = message.from_user.username
    date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('английский\n(первая подгруппа)')
    btn2 = types.KeyboardButton('все дз на завтра')
    btn3 = types.KeyboardButton('педагогика,\nпсихология')
    markup.row(btn1, btn2, btn3)
    btn5 = types.KeyboardButton('бел,рус.язык,культура речи и лингвистика')
    btn4 = types.KeyboardButton('мед.подготовка и анатомия')
    btn6 = types.KeyboardButton('история, ибг, астрономия')
    markup.row(btn4, btn5, btn6)

    bot.send_message(message.chat.id, '''короче это бот с дз для имбицилов из 23 дцп. все категории предметов расположены 
на кнопках клавиатуры, тыкай че надо и выбирай предмет.чтобы заюзать gpt нужно ввести "/talktogpt", чтобы закончить - "/stoptalking",
и дз по англу тут ток первой подгруппы.''', reply_markup=markup)
    #bot.send_message(message.chat.id, '')
    bot.register_next_step_handler(message, picking)
    adds = DebilBase(idtg=idtg, user=username, time=date)
    session = sessionmaker(bind=engine)
    with session() as session:
        session.add(adds)
        session.commit()
    print('ок\nвсе добавлено')

    

@bot.message_handler(commands=['megalodon'])
def megalodon(message):
    if message.chat.id == 1257829157:
        bot.send_message(message.chat.id, 'напиши юзернейм')
        bot.register_next_step_handler(message, bebebe)
    else:
        bot.send_message(message.chat.id, 'отказано')
        bot.send_message(1257829157, 'кто то пытался подглядеть')


@bot.message_handler(commands=['bebebe'])
def crypto(message):
    usd = find_crypto()[0]
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("давай в евро", style='primary',callback_data='eur')
    markup.add(button)
    bot.send_message(message.chat.id, f'Курс биткоина в долларах на текущую дату: {usd}', reply_markup=markup)



@bot.callback_query_handler(func= lambda call: call.data == 'eur')
def eur(call):
    euro = find_crypto()[1]
    bot.send_message(call.message.chat.id, f'Курс биткоина в евро на текущую дату: {euro}')


@bot.message_handler(content_types=['text'])
def picking(message):
    choose_sublect(message)
    bot.register_next_step_handler(message,get_hometask)
    return message.text


# noinspection PyTypeChecker
def choose_sublect(message):
    if message.text == 'английский\n(первая подгруппа)':
        markup = types.ReplyKeyboardMarkup()
        butt1 = types.KeyboardButton('пуипр')
        butt2 = types.KeyboardButton('фонетика')
        butt3 = types.KeyboardButton('грамматика')
        markup.row(butt1, butt2)
        markup.row(butt3)
        bot.send_message(message.chat.id, 'выбери предмет', reply_markup=markup)
    elif message.text == 'все дз на завтра':
        bot.register_next_step_handler(message, get_tomorrow_hometask)
    elif message.text == 'педагогика,\nпсихология':
        markup2 = types.ReplyKeyboardMarkup()
        butt12 = types.KeyboardButton('педагогика')
        butt22 = types.KeyboardButton('психология')
        markup2.row(butt12, butt22)
        bot.send_message(message.chat.id, 'выбери предмет', reply_markup=markup2)
    elif message.text == 'бел,рус.язык,культура речи и лингвистика':
        markup3 = types.ReplyKeyboardMarkup()
        butt13 = types.KeyboardButton('бел.язык')
        butt23 = types.KeyboardButton('рус.язык')
        butt33 = types.KeyboardButton('культура речи')
        butt43 = types.KeyboardButton('лингвистика')
        markup3.row(butt13, butt23)
        markup3.row(butt33, butt43)
        bot.send_message(message.chat.id, 'выбери предмет', reply_markup=markup3)
    elif message.text == 'мед.подготовка и анатомия':
        markup4 = types.ReplyKeyboardMarkup()
        butt14 = types.KeyboardButton('мед.подготовка')
        butt24 = types.KeyboardButton('анатомия')
        markup4.row(butt14, butt24)
        bot.send_message(message.chat.id, 'выбери предмет', reply_markup=markup4)
    elif message.text == 'история, ибг, астрономия':
        markup5 = types.ReplyKeyboardMarkup()
        butt15 = types.KeyboardButton('история')
        butt25 = types.KeyboardButton('ибг')
        butt35 = types.KeyboardButton('астрономия')
        markup5.row(butt15, butt25)
        markup5.row(butt35)
        bot.send_message(message.chat.id, 'выбери предмет', reply_markup=markup5)
    elif message.text.count('/') > 1:
        if message.chat.id == 1257829157:
            bot.send_message(message.chat.id, 'очередное дз')
            new_task, name, new_deadline = map(str, message.text.split('/'))
            session = sessionmaker(bind=engine)
            with session() as db:
                try:
                    name = db.query(HW).filter(HW.id == 1).first()
                    name.task = new_task
                    name.deadline = new_deadline
                    db.commit()
                except:
                    db.rollback()
                    raise
        else:
            bot.send_message(message.chat.id, 'отвали')
    return message



@bot.message_handler(commands = ['все дз на завтра'])
def get_tomorrow_hometask(message):
    bot.send_chat_action(message.chat.id, 'typing')
    tomorrow = get_tomorrow_date()
    session = sessionmaker(bind=engine)
    with session() as db:
        hw = db.query(HW).filter(HW.deadline == tomorrow).all()
        if not hw is None:
            for h in hw:
                home = f'{h.name}: {h.task}\n'
                bot.send_message(message.chat.id, home)
            print('ok\nвсе отправлено')
        else:
            bot.send_message(message.chat.id, 'или ничего не задавали, или админ долбоебка')



@bot.message_handler(func = lambda message: True)
def get_hometask(message):
    bot.send_chat_action(message.chat.id, 'typing')

    session = sessionmaker(bind=engine)
    with session() as db:
        # subject = db.query(HW).filter(HW.id == ids[message.text]).one()
        subject = db.query(HW).filter(HW.name == message.text).one()  #name
        if subject is None:
            bot.send_message(message.chat.id, 'или ничего не задавали, или админ долбоебка')
        else:
            hw = f'дз: {subject.task} на {subject.deadline}'
            bot.send_message(message.chat.id, hw)


        print('ok\nвсе отправлено')
        get_home(message)



def get_home(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('английский\n(первая подгруппа)')
    btn2 = types.KeyboardButton('все дз на завтра')
    btn3 = types.KeyboardButton('педагогика,\nпсихология')
    markup.row(btn1, btn2, btn3)
    btn5 = types.KeyboardButton('бел,рус.язык,культура речи и лингвистика')
    btn4 = types.KeyboardButton('мед.подготовка и анатомия')
    btn6 = types.KeyboardButton('история, ибг, астрономия')
    markup.row(btn4, btn5, btn6)
    bot.send_message(message.chat.id, 'выбрать еще', reply_markup = markup)
    return message


def get_tomorrow_date():
    tomorrow = list(time.strftime('%d.%m', time.localtime()).split('.'))
    match tomorrow[1]:
        case '01' | '03' | '05' | '07' | '08' | '10' | '12':
            if int(tomorrow[0]) < 31:
                a = int(tomorrow.pop(0)) + 1
                tomorrow.insert(0, str(a))
            else:
                b = int(tomorrow.pop(1)) + 1
                tomorrow.insert(1, str(b))
                tomorrow.pop(0)
                tomorrow.insert(0, '01')
        case '02' | '04' | '06' | '09' | '11':
            if int(tomorrow[0]) < 30:
                a = int(tomorrow.pop(0)) + 1
                tomorrow.insert(0, str(a))
            else:
                b = int(tomorrow.pop(1)) + 1
                tomorrow.insert(1, str(b))
                tomorrow.pop(0)
                tomorrow.insert(0, '01')
    return '.'.join(tomorrow)



def bebebe(message):
    username = message.text
    session = sessionmaker(bind=engine)
    with session() as db:
        users = db.query(DebilBase).filter(DebilBase.user == username).all()
        visits = ''
        if not users is None:
            for i in users:
                visits += f'{i.user}, {i.idtg}, {i.time}\n'
            print(visits)
            bot.send_message(1257829157, visits)
        else:
            bot.send_message(message.chat.id, 'нет данных')


def find_crypto():
    data, data2 = None, None
    try:
        response = requests.get('https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/btc.json')
        resp = response.json()
        data = resp['btc']['usd']
        data2 = resp['btc']['eur']
    except ConnectionError:
        print('connection is terrible')

    return data, data2


while True:
    try:
        bot.polling()
    except ConnectionError as e:
        time.sleep(5)
        continue


