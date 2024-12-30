import enum


class ButtonsEnum(enum.Enum):
    restart = 'Перезапустить бота'
    help = 'Инструкция'
    catalog = 'Показать каталог товаров'
    add_to_cart = 'Добавить товар в корзину'
    cart = 'Показать содержимое вашей корзины'
    checkout = 'Оформить заказ'
