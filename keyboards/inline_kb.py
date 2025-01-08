from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.example_table import get_name_from_item_table
from database.tables import get_banner_size_and_price_from_products_table, get_banner_name_from_products_table
from lexicon.products_enum import ProductsEnum
from aiogram.filters.callback_data import CallbackData


class ProductsCallbackFactory(CallbackData, prefix="products"):
    product_name: str


class BannerTypesCallbackFactory(CallbackData, prefix="banner_type"):
    bunner_type: str | None
    is_back: bool


class BannerSizeCallbackFactory(CallbackData, prefix="banner_size_price"):
    products_name: str | None
    is_back: bool


class TarpaulinDensitiesCallbackFactory(CallbackData, prefix="tarpaulin"):
    tarpaulin_density: str | None
    is_back: bool


# async def create_products_inline_kb(width: int) -> InlineKeyboardMarkup:
#     """
#     Функция для формирования инлайн-клавиатуры с продукцией из базы
#     """
#     products_kb_builder = InlineKeyboardBuilder()
#     buttons_list: list[InlineKeyboardButton] = []

#     product_name_list = await get_name_from_table()

#     for product_name in product_name_list:
#         buttons_list.append(
#             InlineKeyboardButton(
#                 text=product_name,
#                 callback_data=ProductsCallbackFactory(
#                     product_name=product_name
#                 ).pack()
#             )
#         )

#     products_kb_builder.row(*buttons_list, width=width)

#     return products_kb_builder.as_markup()


async def create_products_inline_kb() -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры с продукцией
    """
    products_kb_builder = InlineKeyboardBuilder()
    products_list = [product.value for product in ProductsEnum]

    for product in products_list:
        products_kb_builder.button(
            text=product,
            callback_data=ProductsCallbackFactory(
                product_name=product
            )
        )

    products_kb_builder.adjust(len(products_list) - 1)

    return products_kb_builder.as_markup()


async def create_bunner_types_inline_kb() -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры с типом баннеров
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
    banner_kp_builder.adjust(len(bunner_type_list))

    return banner_kp_builder.as_markup()


async def create_bunner_size_inline_kb(banner_type: str) -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры с ценой на баннера из базы
    """
    bunner_size_kb_builder = InlineKeyboardBuilder()
    buttons_list: list[InlineKeyboardButton] = []

    banner_names_list = await get_banner_name_from_products_table(banner_type)

    # for bunner_size_data in bunner_size_data_list:
    #     buttons_list.append(
    #         InlineKeyboardButton(
    #             text=f'Размер {bunner_size_data[0]
    #                            } - {bunner_size_data[1]} р.',
    #             callback_data=BannerSizePriceCallbackFactory(
    #                 banner_size=bunner_size_data[0],
    #                 is_back=False
    #             ).pack()
    #         )
    #     )

    for products_name in banner_names_list:
        buttons_list.append(
            InlineKeyboardButton(
                text=f'{products_name}',
                callback_data=BannerSizeCallbackFactory(
                    products_name=products_name,
                    is_back=False
                ).pack()
            )
        )

    buttons_list.append(
        InlineKeyboardButton(
            text='Назад',
            callback_data=BannerSizeCallbackFactory(
                products_name=None,
                is_back=True
            ).pack()
        )
    )

    bunner_size_kb_builder.row(*buttons_list, width=1)

    return bunner_size_kb_builder.as_markup()


async def create_tarpaulin_densities_inline_kb() -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры с плотностью тарпаулина
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
