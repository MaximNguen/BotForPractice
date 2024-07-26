from sqlalchemy import select

from app.database.models import async_session
from app.database.models import User, Menu, Food, Orders

async def set_user(tg_id:int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
            
async def add_order(real_time, user_tg_id, user_name, user_number, user_address, user_comment, user_order, user_price):
    async with async_session() as session:
        session.add(Orders(time=real_time, tg_id=user_tg_id, name=user_name, number=user_number, address=user_address, comment=user_comment, order=user_order, price=user_price))
        await session.commit()

async def get_menu():
    async with async_session() as session:
        return await session.scalars(select(Menu))
    
async def get_foods():
    async with async_session() as session:
        return await session.scalars(select(Food))
    