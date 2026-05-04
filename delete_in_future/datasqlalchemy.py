#from bot import engine,HW
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine  #select
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HW(Base):
    __tablename__ = 'homework'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    task = Column(String(30))
    deadline = Column(String(30))


engine = create_engine('sqlite:///23dcp.db', echo=True)
Base.metadata.create_all(engine)


def delete_subject():
    session = sessionmaker(bind=engine)
    with session() as db:
        odd = db.query(HW).filter(HW.id == 2).all()
        db.delete(odd)
        db.commit()
    return delete_subject()




#adds = HW(name='педагогика',task='схема принципов',deadline='23.02')
#Session = sessionmaker(bind=engine)
#with Session() as session:
#session.add(adds)
#session.commit()


#def update(new_object: HW, session):
#	session.merge(new_object)


#def get_by_name(name: str, session) -> list[HW]:
#statement = select(HW).where(HW.name == name)
#db_object = session.scalars(statement).one()
#return db_object


#def get_by_date(deadline: str, session) -> str:
#statement = select(HW).where(HW.deadline == deadline)
#db_object = session.scalars(statement).all()
#object_to = ','.join(db_object)
#return object_to


#adds = DebilBase(idtg=idtg,user=username,time=date)

#class HW(Base):
#__tablename__ = 'homework'
#id = Column(Integer,primary_key=True)
#name = Column(String(30))
#task = Column(String(30))
#deadline = Column(String(30))
