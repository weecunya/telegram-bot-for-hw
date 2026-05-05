from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select


class Model(DeclarativeBase):
    pass

class DebilBase(Model):
    __tablename__ = 'debilki'
    id: Mapped[int] = mapped_column(primary_key=True)
    idtg: Mapped[int]
    user: Mapped[str]
    time: Mapped[str]

list_of_subjects = ['пуипр',"грамматика","фонетика","педагогика","психология","бел.язык","рус.язык","культура речи","лингвистика",
                    "мед.подготовка","анатомия","история","ибг","астрономия"]

class HW(Model):
    __tablename__ = 'homework'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None]
    task: Mapped[str | None]
    deadline: Mapped[str | None]

async def create_all_tables():
    engine = create_async_engine('sqlite+aiosqlite:///23dcp.db')
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    session = async_sessionmaker(engine, expire_on_commit=False)
    async with session() as session:
        async with session.begin():
            for i in list_of_subjects:
                result = await session.execute(select(HW))
                if not result.scalars() in list_of_subjects:
                    session.add(HW(name=i, task = '-', deadline = '-'))
                else:
                    await session.rollback()




