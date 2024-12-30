from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.buttons_enum import ButtonsEnum

# ------- Создаем клавиатуру через ReplyKeyboardBuilder -------
# Создаем кнопки
button_restart: KeyboardButton = KeyboardButton(
    text=ButtonsEnum.restart.value
)


button_help: KeyboardButton = KeyboardButton(
    text=ButtonsEnum.help.value
)

button_catalog: KeyboardButton = KeyboardButton(
    text=ButtonsEnum.catalog.value
)

button_add_to_cart: KeyboardButton = KeyboardButton(
    text=ButtonsEnum.add_to_cart.value
)

button_cart: KeyboardButton = KeyboardButton(
    text=ButtonsEnum.cart.value
)

button_checkout: KeyboardButton = KeyboardButton(
    text=ButtonsEnum.checkout.value
)


# Инициализируем билдер для клавиатуры с кнопками:
base_kb_builder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=1 (количество кнопок в ряду)
base_kb_builder.row(
    button_restart,
    button_help,
    button_catalog,
    button_add_to_cart,
    button_cart,
    button_checkout,
    width=1
)

# Создаем клавиатуру с кнопками:
base_kb: ReplyKeyboardMarkup = base_kb_builder.as_markup(
    # one_time_keyboard=True,
    resize_keyboard=True
)
