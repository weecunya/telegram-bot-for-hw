from sqlalchemy import select
from telebot import types
import time
from db_config import DebilBase
from telebot.async_telebot import AsyncTeleBot
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from db_config import DebilBase
from config import Settings
import requests
from db_config import HW

settings = Settings()

bot = AsyncTeleBot(settings.token)


async def get_home(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('английский\n(первая подгруппа)')
    btn2 = types.KeyboardButton('все дз на завтра')
    btn3 = types.KeyboardButton('педагогика,\nпсихология')
    markup.row(btn1, btn2, btn3)
    btn5 = types.KeyboardButton('бел,рус.язык,культура речи и лингвистика')
    btn4 = types.KeyboardButton('мед.подготовка и анатомия')
    btn6 = types.KeyboardButton('история, ибг, астрономия')
    markup.row(btn4, btn5, btn6)
    await bot.send_message(message.chat.id, 'выбрать еще', reply_markup = markup)
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


async def get_tomorrow_hometask(message):
    await bot.send_chat_action(message.chat.id, 'typing')
    tomorrow = get_tomorrow_date()
    engine = create_async_engine('sqlite+aiosqlite:///23dcp.db')
    session = async_sessionmaker(bind=engine,expire_on_commit=False)
    async with session() as session:
        async with session.begin():
            try:
                hw_finding = await session.execute(select(HW).where(HW.deadline == tomorrow))
                hw = hw_finding.scalar().all()
                if not hw is None:
                    for h in hw:
                        home = f'{h.name}: {h.task}\n'
                        await bot.send_message(message.chat.id, home)
                    print('ok\nвсе отправлено')
                else:
                    await bot.send_message(message.chat.id, 'или ничего не задавали, или админ долбоебка')
            except Exception:
                await bot.send_message(message.chat.id,'не найдено')

async def bebebe(message):
    username = message.text
    engine = create_async_engine('sqlite+aiosqlite:///23dcp.db')
    session = async_sessionmaker(bind=engine,expire_on_commit=False)
    async with session() as session:
        async with session.begin():
            users_finding = await session.execute(select(DebilBase).where (DebilBase.user == username))
            users = users_finding.scalar().all()
            visits: str = ''
            if users is not None:
                for i in users:
                    visits += f'{i.user}, {i.idtg}, {i.time}\n'
                print(visits)
                await bot.send_message(settings.id_telegram, visits)
            else:
                await bot.send_message(message.chat.id, 'нет данных')


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