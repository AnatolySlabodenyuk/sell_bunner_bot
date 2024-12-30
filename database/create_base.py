from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
import os

from config_data.config import Config, load_config

load_dotenv()
config: Config = load_config()

Base = declarative_base()

engine = create_engine(config.tg_bot.database_url)
Session = sessionmaker(bind=engine)
session = Session()


# модель товара
class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)


# товар в корзине
class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, default=1)
    item = relationship("Item")


# Функция инициализации базы
def initialize_database():
    if not os.path.exists("shop.db"):
        print("Файл базы данных отсутствует. Создаю заново...")
    try:
        Base.metadata.create_all(engine)
        print("База данных и таблицы успешно созданы.")
    except OperationalError as e:
        print(f"Ошибка при создании базы данных: {e}")
    if not session.query(Item).first():
        session.add_all([
            Item(name="Сервер", price=100.0),
            Item(name="Облако", price=150.0),
            Item(name="Amvera", price=200.0)
        ])
        session.commit()
