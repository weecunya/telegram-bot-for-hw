from requests.exceptions import ConnectionError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from bot_funcs import get_home, find_crypto,bebebe, get_tomorrow_hometask
from db_config import *
from src.config import Settings
import time
import asyncio

settings = Settings()
bot = AsyncTeleBot(settings.token)


@bot.message_handler(commands=['start'])
async def welcome(message):
    new_engine = create_async_engine('sqlite+aiosqlite:///23dcp.db')

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
    await bot.send_message(message.chat.id, '''короче это бот с дз для имбицилов из 23 дцп. все категории предметов расположены 
на кнопках клавиатуры, тыкай че надо и выбирай предмет.чтобы заюзать gpt нужно ввести "/talktogpt", чтобы закончить - "/stoptalking",
и дз по англу тут ток первой подгруппы.''', reply_markup=markup)
    list_of_data = [idtg,username,date]
    session = async_sessionmaker(bind=new_engine, expire_on_commit=False)
    async with session() as session:
        async with session.begin():
            session.add(DebilBase(idtg=list_of_data[0], user=list_of_data[1], time=list_of_data[2]))
            await session.commit()
    print('ок\nвсе добавлено')
    # await picking(message)



@bot.message_handler(commands=['megalodon'])
async def megalodon(message):
    if message.chat.id == 1257829157:
        await bot.send_message(message.chat.id, 'напиши юзернейм')
        await bebebe(message)
    else:
        await bot.send_message(message.chat.id, 'отказано')
        await bot.send_message(1257829157, 'кто то пытался подглядеть')



@bot.message_handler(commands=['bebebe'])
async def crypto(message):
    usd = find_crypto()[0]
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("давай в евро", style='primary',callback_data='eur')
    markup.add(button)
    await bot.send_message(message.chat.id, f'Курс биткоина в долларах на текущую дату: {usd}', reply_markup=markup)



@bot.callback_query_handler(func= lambda call: call.data == 'eur')
async def eur(call):
    euro = find_crypto()[1]
    await bot.send_message(call.message.chat.id, f'Курс биткоина в евро на текущую дату: {euro}')



@bot.message_handler(content_types=['text'])
async def choose_subject(message):
    if message.text == 'английский\n(первая подгруппа)':
        markup = types.ReplyKeyboardMarkup()
        butt1 = types.KeyboardButton('пуипр')
        butt2 = types.KeyboardButton('фонетика')
        butt3 = types.KeyboardButton('грамматика')
        markup.row(butt1, butt2)
        markup.row(butt3)
        await bot.send_message(message.chat.id, 'выбери предмет', reply_markup=markup)
        # await get_hometask(message)
    elif message.text == 'все дз на завтра':
        await get_tomorrow_hometask(message)
    elif message.text == 'педагогика,\nпсихология':
        markup2 = types.ReplyKeyboardMarkup()
        butt12 = types.KeyboardButton('педагогика')
        butt22 = types.KeyboardButton('психология')
        markup2.row(butt12, butt22)
        await bot.send_message(message.chat.id, 'выбери предмет', reply_markup=markup2)
        # await get_hometask(message)
    elif message.text == 'бел,рус.язык,культура речи и лингвистика':
        markup3 = types.ReplyKeyboardMarkup()
        butt13 = types.KeyboardButton('бел.язык')
        butt23 = types.KeyboardButton('рус.язык')
        butt33 = types.KeyboardButton('культура речи')
        butt43 = types.KeyboardButton('лингвистика')
        markup3.row(butt13, butt23)
        markup3.row(butt33, butt43)
        await bot.send_message(message.chat.id, 'выбери предмет', reply_markup=markup3)
        # await get_hometask(message)
    elif message.text == 'мед.подготовка и анатомия':
        markup4 = types.ReplyKeyboardMarkup()
        butt14 = types.KeyboardButton('мед.подготовка')
        butt24 = types.KeyboardButton('анатомия')
        markup4.row(butt14, butt24)
        await bot.send_message(message.chat.id, 'выбери предмет', reply_markup=markup4)
        # await get_hometask(message)
    elif message.text == 'история, ибг, астрономия':
        markup5 = types.ReplyKeyboardMarkup()
        butt15 = types.KeyboardButton('история')
        butt25 = types.KeyboardButton('ибг')
        butt35 = types.KeyboardButton('астрономия')
        markup5.row(butt15, butt25)
        markup5.row(butt35)
        await bot.send_message(message.chat.id, 'выбери предмет', reply_markup=markup5)
        # await get_hometask(message)
    elif message.text.count('/') > 1:
        if message.chat.id == 1257829157:
            await bot.send_message(message.chat.id, 'очередное дз')
            new_task, name, new_deadline = map(str, message.text.split('/'))
            print (new_task, name, new_deadline)
            engine =create_async_engine('sqlite+aiosqlite:///23dcp.db')
            session = async_sessionmaker(bind=engine,expire_on_commit=False)
            try:
                async with session() as session:
                    async with session.begin():
                        if not name in HW:
                            print('okey')
                            session.add(HW(name=name, task = new_task, deadline = new_deadline))
                            await session.commit()
                        else:
                            print('moo')
                            find = await session.execute(select(HW).where(HW.name == name))
                            find_smth = find.scalar().first()
                            find_smth.deadline = new_deadline
                            find_smth.task = new_task

            except Exception:
                await bot.send_message(message.chat.id, 'error')
        else:
            await bot.send_message(message.chat.id, 'отвали')
        # await get_hometask(message)
    else:
        await get_hometask(message)




@bot.message_handler(content_types=['text'])
async def get_hometask(message):
    await bot.send_chat_action(message.chat.id, 'typing')
    print('ok')
    engine = create_async_engine('sqlite+aiosqlite:///23dcp.db')
    session = async_sessionmaker(bind=engine,expire_on_commit=False)
    print('yeee')
    async with session() as session:
        async with session.begin():
            try:
                subject_finding = await session.execute(select(HW).where(HW.name == message.text))
                subject = subject_finding.scalar().first()
                if subject is None:
                    print('nonono')
                    await  bot.send_message(message.chat.id, 'или ничего не задавали, или админ долбоебка')
                else:
                    hw = f'дз: {subject.task} на {subject.deadline}'
                    await bot.send_message(message.chat.id, hw)
            except Exception:
                await bot.send_message(message.chat.id,'не найдено')
        print('ok\nвсе отправлено')

    await get_home(message)


while True:
    try:
        asyncio.run(bot.polling())
    except ConnectionError as e:
        time.sleep(5)
        continue


