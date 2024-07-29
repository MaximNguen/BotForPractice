from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine 

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    
class Menu(Base):
    __tablename__ = "menu"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    
class Food(Base):
    __tablename__ = "foods"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(15))
    price: Mapped[int] = mapped_column()
    size: Mapped[str] = mapped_column(String(10))
    add: Mapped[str] = mapped_column(String(50))

class Orders(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[str] = mapped_column(String(50))
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(30))
    number: Mapped[str] = mapped_column(String(30))
    address: Mapped[str] = mapped_column(String(100))
    comment: Mapped[str] = mapped_column(String(500))
    order: Mapped[str] = mapped_column(String(500))
    price: Mapped[str] = mapped_column(String(7))
    
class Cart(Base):
    __tablename__ = "carts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(15))
    price: Mapped[int] = mapped_column()
    size: Mapped[str] = mapped_column(String(10))
    add: Mapped[str] = mapped_column(String(50))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)