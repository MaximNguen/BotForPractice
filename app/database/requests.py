from sqlalchemy import select, BigInteger, text

from app.database.models import async_session
from app.database.models import User, Menu, Food, Orders, Cart

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
    
async def get_carts():
    async with async_session() as session:
        all_id = []
        all_carts = await session.scalars(select(Cart))
        for cart in all_carts:
            all_id.append(str(cart.tg_id))
        return all_id

async def get_carts_name(id):
    async with async_session() as session:
        all_name = []
        all_carts = await session.scalars(select(Cart).where(Cart.tg_id == id))
        for cart in all_carts:
            all_name.append(str(cart.name))
        return all_name
        
async def get_carts_price(id):
    async with async_session() as session:
        all_price = []
        all_carts = await session.scalars(select(Cart).where(Cart.tg_id == id))
        for cart in all_carts:
            all_price.append(int(cart.price))
        return all_price
    
async def get_carts_size(id):
    async with async_session() as session:
        all_size = []
        all_carts = await session.scalars(select(Cart).where(Cart.tg_id == id))
        for cart in all_carts:
            all_size.append(str(cart.size))
        return all_size
    
async def get_carts_add(id):
    async with async_session() as session:
        all_add = []
        all_carts = await session.scalars(select(Cart).where(Cart.tg_id == id))
        for cart in all_carts:
            all_add.append(str(cart.add))
        return all_add

async def add_food_to_cart(tg_id, name_food, price_food, size_food, add_food):
    async with async_session() as session:
        session.add(Cart(tg_id=tg_id, name=name_food, price=price_food, size=size_food, add=add_food))
        await session.commit()

async def delete_cart_foods(id):
    async with async_session() as session:
        await session.execute(text(f"DELETE FROM carts WHERE tg_id = {id}"))
        await session.commit()