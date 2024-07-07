from sqlalchemy import select

from app.database.models import async_session
from app.database.models import User, Menu, Item

async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
            
async def get_menu():
    async with async_session() as session:
        return await session.scalars(select(Menu))
    
async def get_menu_item(menu_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.id == menu_id))