from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.create_base import get_name_from_table
from aiogram.filters.callback_data import CallbackData


class ProductsCallbackFactory(CallbackData, prefix="product"):
    product_name: str


async def create_inline_kb(width: int) -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры на лету
    """
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    product_name_list = await get_name_from_table()

    for product_name in product_name_list:
        buttons.append(
            InlineKeyboardButton(
                text=product_name,
                callback_data=ProductsCallbackFactory(
                    product_name=product_name
                ).pack()
            )
        )

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()
