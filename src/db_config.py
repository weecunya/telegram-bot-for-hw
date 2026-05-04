from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Model(DeclarativeBase):
    pass

class DebilBase(Model):
    __tablename__ = 'debilki'
    id: Mapped[int] = mapped_column(primary_key=True)
    idtg: Mapped[int]
    user: Mapped[str]
    time: Mapped[str]


class HW(Model):
    __tablename__ = 'homework'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    task: Mapped[str | None]
    deadline: Mapped[str | None]


    # class DebilBase(Base):
    #     __tablename__ = 'debilki'
    #     id = Column(Integer, primary_key=True)
    #     idtg = Column(Integer)
    #     user = Column(String(30))
    #     time = Column(String(30))
    #
    #
    # class HW(Base):
    #     __tablename__ = 'homework'
    #     id = Column(Integer, primary_key=True)
    #     name = Column(String(30))
    #     task = Column(String(30))
    #     deadline = Column(String(30))



