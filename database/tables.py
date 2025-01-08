from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
from config_data.config import Config, load_config
from aiogram.types import Message, CallbackQuery
import os

load_dotenv()
config: Config = load_config()

Base = declarative_base()

engine = create_engine(config.tg_bot.database_url)
Session = sessionmaker(bind=engine)
session = Session()


class Products(Base):
    """
    Размеры баннера
    """
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    banner_type = Column(String, nullable=False)
    size = Column(String, nullable=False)
    product_name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)


async def initialize_products_table():
    """
    Функция инициализации базы баннеров 
    """
    os.path.join('')
    if not os.path.join(os.getcwd(), 'shop.db'):
        print('Файл базы данных отсутствует. Создаю заново...')
    try:
        Base.metadata.create_all(engine)
        print('База данных и таблицы успешно созданы.')
    except OperationalError as e:
        print(f'Ошибка при создании базы данных: {e}')
    if not session.query(Products).first():
        session.add_all([
            Products(
                banner_type='Китай',
                size='3x6',
                product_name='Китай - 3x6',
                price=100.0
            ),
            Products(
                banner_type='Китай',
                size='4x6',
                product_name='Китай - 4x6',
                price=200.0
            ),
            Products(
                banner_type='Европа',
                size='3x6',
                product_name='Европа - 3x6',
                price=150.0
            ),
            Products(
                banner_type='Европа',
                size='4x6',
                product_name='Европа - 4x6',
                price=300.0
            ),
        ])
        session.commit()


async def get_banner_size_and_price_from_products_table(banner_type: str):
    """
    Функция для получения данных из таблицы Products.
    :return: Список кортежей из размера и цены на баннер.
    """
    try:
        data = session.query(Products.size, Products.price).filter(
            Products.banner_type == banner_type).all()
        return data
    except Exception as e:
        print(f'Ошибка при получении данных: {e}')
        return []


async def get_banner_name_from_products_table(banner_type: str):
    """
    Функция для названия баннера из таблицы Products.
    :return: Список из названий баннеров.
    """
    try:
        product_names = session.query(Products.product_name).filter(
            Products.banner_type == banner_type).all()
        return [product_name[0] for product_name in product_names]
    except Exception as e:
        print(f'Ошибка при получении данных: {e}')
        return []


class Cart(Base):
    """
    Товар в корзине (нового образца)
    """
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, default=1)
    item = relationship('Products')


async def add_data_in_cart_table(product_name: str, callback_message: CallbackQuery):
    new_product = session.query(Products).filter_by(
        product_name=product_name).first()
    if new_product:
        new_cart = (
            session.query(Cart).filter_by(
                user_id=callback_message.from_user.id,
                product_id=new_product.id
            )
            .first()
        )
        if new_cart:
            new_cart.quantity += 1
        else:
            new_cart = Cart(
                user_id=callback_message.from_user.id,
                product_id=new_product.id,
                quantity=1
            )
            session.add(new_cart)
        session.commit()
        await callback_message.message.answer(f'Товар\n"<b>{product_name}</b>"\nдобавлен в корзину')
    else:
        await callback_message.message.answer('Товар не найден. Пожалуйста, введите корректное название товара.')

    await callback_message.answer(text='🎉')


async def clear_cart_table():
    """
    Функция для удаления всех записей из таблицы cart.
    """
    try:
        session.query(Cart).delete()  # Удаляем все записи из таблицы Cart
        session.commit()  # Применяем изменения
        print("Корзина очищена.")
    except OperationalError as e:
        session.rollback()  # Откатываем изменения при ошибке
        print(f"Ошибка при очистке корзины': {e}")
    finally:
        session.close()  # Закрываем сессию
