import asyncio
import time
import os
import groq
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import Command
from aiogram import Router, F,Bot, Dispatcher

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot_funcs import get_home, find_crypto, get_tomorrow_hometask, MyStates, bd_to_xlsx
from db_config import *
from config import Settings

settings = Settings()
bot = Bot(token=settings.token)
dp = Dispatcher()
router = Router()
dp.include_router(router)



@router.message(Command('start'))
async def welcome(message):
    new_engine = create_async_engine('sqlite+aiosqlite:///23dcp.db')
    print('Someone is here')  #чекаю заходы
    print(message.from_user.username)
    print(message.from_user.id)
    print(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
    idtg = message.from_user.id
    username = message.from_user.username
    date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

    builder = ReplyKeyboardBuilder()
    builder.button(text="английский")
    builder.button(text='все дз на завтра')
    builder.button(text='педагогика,психология')
    builder.button(text='бел,рус.язык,культура речи и лингвистика')
    builder.button(text='мед.подготовка и анатомия')
    builder.button(text='история, ибг, астрономия')
    builder.adjust(3,2)
    await message.answer('''короче это бот с дз для имбицилов из 23 дцп. все категории предметов расположены 
на кнопках клавиатуры, тыкай че надо и выбирай предмет. команды:\n /talktogpt - диалог с гпт\n /stoptalking - завершить диалог с гпт\n /bebebe - пасхалка\n /excel_file - конвертация дз в ексель файл''', reply_markup= builder.as_markup(resize_keyboard=True))
    list_of_data = [idtg,username,date]
    session = async_sessionmaker(bind=new_engine, expire_on_commit=False)
    async with session() as session:
        async with session.begin():
            session.add(DebilBase(idtg=list_of_data[0], user=list_of_data[1], time=list_of_data[2]))
            await session.commit()
    print('ок\nвсе добавлено')
    # await picking(message)



@router.message(Command('megalodon'))
async def megalodon(message:Message, state: FSMContext):
    if message.chat.id == 1257829157:
        await message.answer('напиши юзернейм')
        await state.set_state(MyStates.waiting_for_list)
    else:
        await message.answer('отказано')
        await bot.send_message(1257829157, 'кто то пытался подглядеть')



@router.message(Command('bebebe'))
async def crypto(message):
    usd = find_crypto()[0]
    button = [[InlineKeyboardButton(text="давай в евро",callback_data='eur',style='primary')]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)
    await message.answer( f'Курс биткоина в долларах на текущую дату: {usd}', reply_markup=keyboard)

@router.message(Command('excel_file'))
async def hw_to_excel(message):
    file_path = bd_to_xlsx()
    excel_file = FSInputFile(file_path)
    await message.answer_document(excel_file)
    os.remove(file_path)



@router.message(Command('talktogpt'))
async def talktogpt(message:Message,state:FSMContext):
    await state.set_state(MyStates.speaking_to_gpt)
    await message.answer(text='задай вопрос')


@router.message(Command('stoptalking'))
async def stop_gpt(message: Message, state: FSMContext):
    await state.clear()
    await get_home(message)



@router.callback_query(F.data == 'eur')
async def eur(callback: CallbackQuery):
    euro = find_crypto()[1]
    await callback.message.answer( f'Курс биткоина в евро на текущую дату: {euro}')

@router.message(MyStates.waiting_for_list)
async def list_of_users(message: Message, state: FSMContext):
    username = message.text
    engine = create_async_engine('sqlite+aiosqlite:///23dcp.db')
    session = async_sessionmaker(bind=engine,expire_on_commit=False)
    async with session() as session:
        async with session.begin():
            users_finding = await session.execute(select(DebilBase).where (DebilBase.user == username))
            users = users_finding.scalars()
            if users:
                visits = ''
                for i in users:
                    visits += f'{i.user}, {i.idtg}, {i.time}\n'
                    print(visits)
                await bot.send_message(1257829157 ,text=visits)
            else:
                await message.answer('нет данных')
    await state.clear()

@router.message(MyStates.waiting_for_subject)
async def get_hometask(message:Message, state: FSMContext):
    await bot.send_chat_action(message.chat.id, 'typing')
    print('ok')
    engine = create_async_engine('sqlite+aiosqlite:///23dcp.db')
    session = async_sessionmaker(bind=engine,expire_on_commit=False)
    print('yeee')
    async with session() as session:
        async with session.begin():
            try:
                subject_finding = await session.execute(select(HW).where(HW.name == message.text))
                subject = subject_finding.scalar()
                if subject is None:
                    await  message.answer('или ничего не задавали, или админ долбоебка')
                else:
                    hw = f'дз: {subject.task} на {subject.deadline}'
                    await message.answer(hw)
            except Exception:
                await message.answer('не найдено')
        print('ok\nвсе отправлено')
    await state.clear()

    await get_home(message)


@router.message(MyStates.speaking_to_gpt)
async def gpt_talks(message):
    prompt = message.text
    client = groq.Groq(api_key=settings.api_key)
    try:
        response = client.chat.completions.create(model='llama-3.3-70b-versatile', messages=[{'role': 'user', 'content': prompt}], temperature=0.7)
        print(response)
        await message.answer(response.choices[0].message.content)
    except:
        await message.answer('ошибка блен')



@router.message(F.text)
async def choose_subject(message:Message, state:FSMContext):
    if message.text == 'английский':
        builder = ReplyKeyboardBuilder()
        builder.button(text='пуипр')
        builder.button(text='фонетика')
        builder.button(text='грамматика')
        builder.adjust(3,1)
        await bot.send_message(message.chat.id, 'выбери предмет', reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(MyStates.waiting_for_subject)
        # await get_hometask(message)
    elif message.text == 'все дз на завтра':
        await get_tomorrow_hometask(message)
    elif message.text == 'педагогика,психология':
        builder = ReplyKeyboardBuilder()
        builder.button(text='педагогика')
        builder.button(text='психология')
        builder.adjust(2,1)
        await bot.send_message(message.chat.id, 'выбери предмет', reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(MyStates.waiting_for_subject)
        # await get_hometask(message)
    elif message.text == 'бел,рус.язык,культура речи и лингвистика':
        builder = ReplyKeyboardBuilder()
        builder.button(text='бел.язык')
        builder.button(text='рус.язык')
        builder.button(text='культура речи')
        builder.button(text='лингвистика')
        builder.adjust(2,2)
        await bot.send_message(message.chat.id, 'выбери предмет', reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(MyStates.waiting_for_subject)
        # await get_hometask(message)
    elif message.text == 'мед.подготовка и анатомия':
        builder = ReplyKeyboardBuilder()
        builder.button(text='мед.подготовка')
        builder.button(text='анатомия')
        builder.adjust(2,1)
        await bot.send_message(message.chat.id, 'выбери предмет', reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(MyStates.waiting_for_subject)
        # await get_hometask(message)
    elif message.text == 'история, ибг, астрономия':
        builder = ReplyKeyboardBuilder()
        builder.button(text='история')
        builder.button(text='ибг')
        builder.button(text='астрономия')
        builder.adjust(2,1)
        await bot.send_message(message.chat.id, 'выбери предмет', reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(MyStates.waiting_for_subject)
        # await get_hometask(message)
    elif message.text.count('/') > 1:
        if message.chat.id == 1257829157:
            await message.answer( 'очередное дз')
            new_task, name, new_deadline = map(str, message.text.split('/'))
            print (new_task, name, new_deadline)
            engine =create_async_engine('sqlite+aiosqlite:///23dcp.db')
            session = async_sessionmaker(bind=engine,expire_on_commit=False)
            try:
                async with session() as session:
                    async with session.begin():
                        find = await session.execute(select(HW).where(HW.name == name))
                        if find:
                            find_smth = find.scalar()
                            find_smth.deadline = new_deadline
                            find_smth.task = new_task
                            await message.answer('добавлено')
                        else:
                            session.add(HW(name=name, task=new_task, deadline=new_deadline))
                            await session.commit()
                            await message.answer("что-то новенькое/nдобавлено ")
            except Exception:
                await bot.send_message(message.chat.id, 'error')
        else:
            await bot.send_message(message.chat.id, 'отвали')
    else:
        await get_hometask(message,state)


if __name__ == "__main__":
    async def main():
        await create_all_tables()
        await dp.start_polling(bot)
    asyncio.run(main())


