from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from src.db_config import HW

#
# Base = declarative_base()           #adds = DebilBase(idtg=idtg,user=username,time=date)
#
#
# class HW(Base):
#     __tablename__ = 'homework'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(30))
#     task = Column(String(30))
#     deadline = Column(String(30))




def fill_the_table():

    sub1 = HW(name = 'пуипр', task = 'упр3д стр141,упр4д стр142', deadline = '20.02')
    sub2 = HW(name = 'ибг', task = 'таблица', deadline = '20.02')
    sub3 = HW(name = 'педагогика', task = 'схема принципов', deadline = '23.02')
    sub4 = HW(name = 'лингвистика', task = 'подг к ср', deadline = '23.02')
    sub5 = HW(name = 'бел.язык', task = 'упр10(фотка)', deadline = '24.02')
    sub6 = HW(name = 'культура речи', task = 'сленг родителей(объясн.+аналог)', deadline = '24.02')
    sub7 = HW(name = 'грамматика', task = '', deadline = '')
    sub8 = HW(name = 'фонетика', task = '', deadline = '')
    sub9 = HW(name = 'анатомия', task = '', deadline = '')
    sub10 = HW(name = 'мед.подготовка', task = '', deadline = '')
    sub11= HW(name = 'рус.язык', task = '', deadline = '')
    sub12= HW(name = 'астрономия', task = '', deadline = '')
    sub13= HW(name = 'история', task = '', deadline = '')
    sub14= HW(name = 'психология', task = '', deadline = '')

    list_of_hw = [sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,sub9,sub10,sub11,sub12,sub13,sub14]

    return list_of_hw