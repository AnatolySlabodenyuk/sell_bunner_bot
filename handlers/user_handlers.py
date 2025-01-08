from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from keyboards.base_kb import base_kb
from lexicon.base_commands_enum import BaseCommandsEnum
from lexicon.buttons_enum import ButtonsEnum
from lexicon.products_enum import ProductsEnum
from aiogram.fsm.context import FSMContext
from state.status_class import Form
from database.example_table import session, Item, CartItem
from database.tables import Cart, add_data_in_cart_table, clear_cart_table
from keyboards.inline_kb import ProductsCallbackFactory, BannerTypesCallbackFactory, BannerSizeCallbackFactory, create_products_inline_kb, create_bunner_types_inline_kb, create_tarpaulin_densities_inline_kb, create_bunner_size_inline_kb
import prettytable as pt


router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    """
    Этот хэндлер срабатывает на команду /start
    """
    await clear_cart_table()
    await message.answer(
        text=BaseCommandsEnum.start.value,
        reply_markup=base_kb
    )


@router.message(F.text == ButtonsEnum.restart.value)
async def process_restart_button(message: Message):
    """
    Этот хэндлер срабатывает на кнопку restart_button
    """
    await clear_cart_table()
    await message.answer(
        text=BaseCommandsEnum.start.value,
        reply_markup=base_kb
    )


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    """
    Этот хэндлер срабатывает на команду /help
    """
    await message.answer(
        text=BaseCommandsEnum.help_text.value,
        reply_markup=base_kb
    )


@router.message(F.text == ButtonsEnum.help.value)
async def process_help_button(message: Message):
    """
    Этот хэндлер срабатывает на кнопку help_button
    """
    await message.answer(
        text=BaseCommandsEnum.help_text.value,
        reply_markup=base_kb
    )


# # Этот хэндлер срабатывает на кнопку 'Показать каталог товаров' - не таблица
# @router.message(F.text == ButtonsEnum.catalog.value)
# async def process_catalog_button(message: Message):
#     items = session.query(Item).all()
#     if items:
#         text = 'Каталог товаров:\n'
#         for item in items:
#             text += f'{item.name} - {item.price:.2f} RUB\n'
#         text += '\nВведите название товара, чтобы добавить его в корзину.'
#     else:
#         text = 'Каталог пуст.'

#     await message.answer(
#         text=text,
#         reply_markup=base_kb
#     )


# @router.message(F.text == ButtonsEnum.catalog.value)
# async def process_catalog_button(message: Message):
#     """
#     Этот хэндлер срабатывает на кнопку 'Показать каталог товаров' - таблица
#     """
#     table = pt.PrettyTable(['Товар', 'Цена'])
#     table.align['Товар'] = 'l'
#     table.align['Цена'] = 'r'
#
#     items = session.query(Item).all()
#     data = []
#     if items:
#         for item in items:
#             data.append((item.name, item.price))
#
#         for symbol, price in data:
#             table.add_row([symbol, f'{price:.2f} RUB'])
#     else:
#         table = pt.PrettyTable(['Товар', 'Цена'])
#
#     await message.answer(
#         text=f'Каталог товаров\n'
#         f'<pre>{table}</pre>\n'
#         f'Введите название товара, чтобы добавить его в корзину',
#         reply_markup=base_kb
#     )

@router.message(F.text == ButtonsEnum.catalog.value)
async def process_catalog_button(message: Message):
    """
    Этот хэндлер срабатывает на кнопку 'Показать каталог товаров'
    """
    await message.answer(
        text='Выбери товар',
        reply_markup=await create_products_inline_kb()
    )


@router.callback_query(ProductsCallbackFactory.filter())
async def inline_products_button_press(
    callback: CallbackQuery,
    callback_data: ProductsCallbackFactory
):
    """
    Этот хэндлер срабатывает на выбор продукта
    """
    if callback_data.product_name == ProductsEnum.banners.value:
        await callback.message.answer(
            text='Выбери качество баннера',
            reply_markup=await create_bunner_types_inline_kb()
        )
        await callback.answer()

    elif callback_data.product_name == ProductsEnum.tarpaulin.value:
        await callback.message.answer(
            text='Выбери плотность Тарпаулина',
            reply_markup=await create_tarpaulin_densities_inline_kb()
        )
        await callback.answer()

    elif callback_data.product_name == ProductsEnum.camouflage_network.value:
        await callback.message.answer(
            text='Еще делаю'
        )
        await callback.answer(text='Еще в работе')

    else:
        await callback.message.answer(
            text='Что-то пошло не так'
        )
        await callback.answer()


@router.callback_query(BannerTypesCallbackFactory.filter())
async def inline_banner_types_button_press(
    callback: CallbackQuery,
    callback_data: BannerTypesCallbackFactory
):
    """
    Этот хэндлер срабатывает на выбор типа баннера
    """
    if callback_data.bunner_type == 'Китай':
        await callback.message.answer(
            text='Выбери размер',
            reply_markup=await create_bunner_size_inline_kb(banner_type='Китай')
        )
        await callback.answer()
    elif callback_data.bunner_type == 'Европа':
        await callback.message.answer(
            text='Выбери размер',
            reply_markup=await create_bunner_size_inline_kb(banner_type='Европа')
        )
        await callback.answer()
    else:
        await callback.message.answer(
            text='Что-то пошло не так'
        )
        await callback.answer()


@router.callback_query(BannerSizeCallbackFactory.filter())
async def inline_bunner_size_price_button_press(
    callback: CallbackQuery,
    callback_data: BannerSizeCallbackFactory
):
    """
    Этот хэндлер срабатывает на выбор размера баннера
    """
    await add_data_in_cart_table(
        product_name=callback_data.products_name,
        callback_message=callback
    )


# @router.message(F.text == ButtonsEnum.add_to_cart.value)
# async def process_add_to_cart_button(message: Message, state: FSMContext):
#     """
#     Этот хэндлер срабатывает на кнопку 'Добавить товар в корзину'
#     """
#     await state.set_state(Form.state_status)
#     await state.update_data(state_status='busy')
#     await message.answer(text=BaseCommandsEnum.add_to_cart.value)


# @router.message(Form.state_status)
# async def add_to_cart(message: Message, state: FSMContext):
#     """
#     Этот хэндлер срабатывает на ввод товаров от пользователя
#     """
#     item_name = message.text.capitalize().strip()
#     item = session.query(Item).filter_by(name=item_name).first()
#     if item:
#         cart_item = (
#             session.query(CartItem).filter_by(
#                 user_id=message.from_user.id,
#                 item_id=item.id
#             )
#             .first()
#         )
#         if cart_item:
#             cart_item.quantity += 1
#         else:
#             cart_item = CartItem(
#                 user_id=message.from_user.id,
#                 item_id=item.id,
#                 quantity=1
#             )
#             session.add(cart_item)
#         session.commit()
#         await message.answer(f"Товар '{item_name}' добавлен в корзину.")
#         await state.clear()
#     else:
#         await message.answer("Товар не найден. Пожалуйста, введите корректное название товара.")


# @router.message(F.text == ButtonsEnum.cart.value)
# async def view_cart(message: Message):
#     """
#     Этот хэндлер срабатывает на кнопку 'Показать содержимое вашей корзины'
#     """
#     cart_items = session.query(CartItem).filter_by(
#         user_id=message.from_user.id).all()
#     if cart_items:
#         text = f'Ваша корзина:\n'
#         total = 0
#         for cart_item in cart_items:
#             item_total = cart_item.quantity * cart_item.item.price
#             text += f'{cart_item.item.name} - {cart_item.quantity} шт. - {item_total:.2f} RUB\n'
#             total += item_total
#         text += f'\nИтого: {total:.2f} RUB\n'
#         text += f'\nВведите /checkout для оформления заказа.'
#     else:
#         text = 'Ваша корзина пуста.'
#     await message.answer(text)


@router.message(F.text == ButtonsEnum.cart.value)
async def view_cart(message: Message):
    """
    Этот хэндлер срабатывает на кнопку 'Показать содержимое вашей корзины'
    """
    cart_items = session.query(Cart).filter_by(
        user_id=message.from_user.id).all()

    if cart_items:
        text = f'Ваша корзина:\n'
        total = 0
        for cart_item in cart_items:
            item_total = cart_item.quantity * cart_item.item.price
            text += f'{cart_item.item.product_name} - {
                cart_item.quantity} шт. - {item_total:.2f} RUB\n'
            total += item_total
        text += f'\nИтого: {total:.2f} RUB\n'
        text += f'\nОформление заказа еще в работе 😅.'
    else:
        text = 'Ваша корзина пуста.'
    await message.answer(f'{text}')


# # счет на оплату
# @router.message(F.text == ButtonsEnum.checkout.value)
# async def checkout(message: Message):
#     cart_items = session.query(CartItem).filter_by(
#         user_id=message.from_user.id).all()
#     if cart_items:
#         title = "Оплата заказа"
#         description = "Оплата товаров из вашей корзины"
#         payload = "Custom-Payload"
#         currency = "RUB"
#         prices = [
#             LabeledPrice(
#                 f"{item.item.name} ({item.quantity} шт.)", int(
#                     item.item.price * 100 * item.quantity)
#             )
#             for item in cart_items
#         ]
#         await context.bot.send_invoice(
#             chat_id=update.message.chat_id,
#             title=title,
#             description=description,
#             payload=payload,
#             provider_token=payment_provider_token,
#             currency=currency,
#             prices=prices,
#             start_parameter="test-payment"
#         )
#     else:
#         await update.message.reply_text("Ваша корзина пуста")
