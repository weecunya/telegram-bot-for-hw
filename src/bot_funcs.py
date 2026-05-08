import sqlite3
from sqlalchemy import select
import time
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import Settings
import requests
from db_config import HW
from aiogram import Router,Bot, Dispatcher
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
import pandas



settings = Settings()
router = Router()
dp = Dispatcher()
bot = Bot(token=settings.token)
dp.include_router(router)


class MyStates(StatesGroup):
    waiting_for_subject = State()
    speaking_to_gpt = State()
    waiting_for_list = State()

async def get_home(message):
    builder = ReplyKeyboardBuilder()
    builder.button(text="английский")
    builder.button(text="все дз на завтра")
    builder.button(text="педагогика,психология")
    builder.button(text="бел,рус.язык,культура речи и лингвистика")
    builder.button(text="мед.подготовка и анатомия")
    builder.button(text="история, ибг, астрономия")
    builder.adjust(3,3)
    await bot.send_message(message.chat.id, 'выбрать еще', reply_markup = builder.as_markup(resize_keyboard=True))
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
    tomorrow = str(get_tomorrow_date())
    print(tomorrow)
    engine = create_async_engine('sqlite+aiosqlite:///23dcp.db')
    session = async_sessionmaker(bind=engine,expire_on_commit=False)
    async with session() as session:
        async with session.begin():
            try:
                hw_finding = await session.execute(select(HW).where(HW.deadline == tomorrow))
                if hw_finding:
                    hw = hw_finding.scalars().all()
                    print(hw)
                    for h in hw:
                        home = f'{h.name}: {h.task}\n'
                        await message.answer(home)
                    print('ok\nвсе отправлено')
                    if len(hw) == 0:
                         await message.answer('или ничего не задавали, или админ долбоебка')
                else:
                    await message.answer('не найдено')
            except Exception:
                await message.answer('не найдено')

def bd_to_xlsx():
    conn = sqlite3.connect('23dcp.db')
    df = pandas.read_sql('SELECT * FROM homework', conn)
    # df.to_excel('homework.xlsx', index=False)
    with pandas.ExcelWriter('homework.xlsx') as writer:
        df.to_excel(writer, sheet_name='homework', index=False)
        worksheet = writer.sheets['homework']
        worksheet.column_dimensions['A'].width = 5
        worksheet.column_dimensions['B'].width = 40
        worksheet.column_dimensions['C'].width = 40
        worksheet.column_dimensions['D'].width = 20
    conn.close()
    return 'homework.xlsx'


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

