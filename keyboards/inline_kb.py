from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.create_base import get_name_from_table
from aiogram.filters.callback_data import CallbackData


class ProductsCallbackFactory(CallbackData, prefix="products"):
    product_name: str


class BannerTypesCallbackFactory(CallbackData, prefix="banner"):
    bunner_type: str | None
    is_back: bool


class TarpaulinDensitiesCallbackFactory(CallbackData, prefix="tarpaulin"):
    tarpaulin_density: str | None
    is_back: bool


async def create_products_inline_kb(width: int) -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры с продукцией "на лету"
    """
    products_kb_builder = InlineKeyboardBuilder()
    buttons_list: list[InlineKeyboardButton] = []

    product_name_list = await get_name_from_table()

    for product_name in product_name_list:
        buttons_list.append(
            InlineKeyboardButton(
                text=product_name,
                callback_data=ProductsCallbackFactory(
                    product_name=product_name
                ).pack()
            )
        )

    products_kb_builder.row(*buttons_list, width=width)

    return products_kb_builder.as_markup()


async def create_bunner_types_inline_kb() -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры с продукцией "на лету"
    """
    banner_kp_builder = InlineKeyboardBuilder()
    bunner_type_list = ['Китай', 'Европа']

    for bunner_type in bunner_type_list:
        banner_kp_builder.button(
            text=bunner_type,
            callback_data=BannerTypesCallbackFactory(
                bunner_type=bunner_type,
                is_back=False
            )
        )
    banner_kp_builder.button(
        text='Назад',
        callback_data=BannerTypesCallbackFactory(
            bunner_type=None,
            is_back=True
        )
    )
    banner_kp_builder.adjust(2)

    return banner_kp_builder.as_markup()


async def create_tarpaulin_densities_inline_kb() -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры с плотностью тарпаулина "на лету"
    """
    tarpaulin_densities_kb_builder = InlineKeyboardBuilder()
    density_list = [60, 90, 120, 150, 180, 220, 280]

    for density in density_list:
        tarpaulin_densities_kb_builder.button(
            text=str(density),
            callback_data=TarpaulinDensitiesCallbackFactory(
                tarpaulin_density=str(density),
                is_back=False
            )
        )

    tarpaulin_densities_kb_builder.button(
        text='Назад',
        callback_data=TarpaulinDensitiesCallbackFactory(
            tarpaulin_density=None,
            is_back=True
        )
    )

    tarpaulin_densities_kb_builder.adjust(1)

    return tarpaulin_densities_kb_builder.as_markup()
