import os
import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# from telegram import Update, LabeledPrice
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, PreCheckoutQueryHandler, ContextTypes

from config_data.config import Config, load_config
from database.example_table import initialize_example_database
from database.tables import initialize_products_table
from handlers import user_handlers

logger = logging.getLogger(__name__)


async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
               "[%(asctime)s] - %(name)s - %(message)s")

    # Выводим в консоль информацию о начале запуска бота
    logger.info("Starting bot")

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    await initialize_example_database()
    await initialize_products_table()

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Настраиваем кнопку Menu
    # await set_main_menu(bot)

    # Регистриуем роутеры в диспетчере
    # dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)
    # dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())


# # приветственное сообщение
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Добро пожаловать в наш магазин! Введите /catalog для просмотра товаров.")


# # список доступных команд
# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     help_text = (
#         "Доступные команды:\\n"
#         "/start - Начать работу с ботом\\n"
#         "/help - Показать это меню помощи\\n"
#         "/catalog - Показать каталог товаров\\n"
#         "/cart - Показать содержимое вашей корзины\\n"
#         "/checkout - Оформить заказ\\n"
#         "Просто отправьте название товара, чтобы добавить его в корзину."
#     )
#     await update.message.reply_text(help_text)


# # список товаров из базы
# async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     items = session.query(Item).all()
#     if items:
#         message = "Каталог товаров:\\n"
#         for item in items:
#             message += f"{item.name} - {item.price:.2f} RUB\\n"
#         message += "\\nВведите название товара, чтобы добавить его в корзину."
#     else:
#         message = "Каталог пуст."
#     await update.message.reply_text(message)


# # добавление товара в корзину
# async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     item_name = update.message.text.strip()
#     item = session.query(Item).filter_by(name=item_name).first()
#     if item:
#         cart_item = (
#             session.query(CartItem).filter_by(
#                 user_id=update.message.chat_id,
#                 item_id=item.id
#             )
#             .first()
#         )
#         if cart_item:
#             cart_item.quantity += 1
#         else:
#             cart_item = CartItem(
#                 user_id=update.message.chat_id,
#                 item_id=item.id,
#                 quantity=1
#             )
#             session.add(cart_item)
#         session.commit()
#         await update.message.reply_text(f"Товар '{item_name}' добавлен в корзину.")
#     else:
#         await update.message.reply_text("Товар не найден. Пожалуйста, введите корректное название товара.")


# # отображение корзины
# async def view_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     cart_items = session.query(CartItem).filter_by(
#         user_id=update.message.chat_id).all()
#     if cart_items:
#         message = "Ваша корзина:\\n"
#         total = 0
#         for cart_item in cart_items:
#             item_total = cart_item.quantity * cart_item.item.price
#             message += f"{cart_item.item.name} - {
#                 cart_item.quantity} шт. - {item_total:.2f} RUB\\n"
#             total += item_total
#         message += f"\\nИтого: {total:.2f} RUB"
#         message += "\\nВведите /checkout для оформления заказа."
#     else:
#         message = "Ваша корзина пуста."
#     await update.message.reply_text(message)


# # счет на оплату
# async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     cart_items = session.query(CartItem).filter_by(
#         user_id=update.message.chat_id).all()
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


# # подтверждение оплаты
# async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.pre_checkout_query
#     if query.invoice_payload != "Custom-Payload":
#         await query.answer(ok=False, error_message="Что-то пошло не так...")
#     else:
#         await query.answer(ok=True)


# # обработчик успешного платежа
# async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     session.query(CartItem).filter_by(user_id=update.message.chat_id).delete()
#     session.commit()
#     await update.message.reply_text("Спасибо за покупку! Ваш заказ был успешно оформлен.")


# if __name__ == '__main__':
#     initialize_database()
#     app = Application.builder().token(telegram_token).build()

#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CommandHandler("help", help_command))
#     app.add_handler(CommandHandler("cart", view_cart))
#     app.add_handler(CommandHandler("checkout", checkout))
#     app.add_handler(MessageHandler(
#         filters.TEXT & ~filters.COMMAND, add_to_cart))
#     app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
#     app.add_handler(MessageHandler(
#         filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

#     # Запуск бота
#     app.run_polling()
