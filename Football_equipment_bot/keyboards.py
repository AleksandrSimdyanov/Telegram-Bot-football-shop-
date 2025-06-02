from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           ReplyKeyboardMarkup,
                           KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
import app.database.requests as rq

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Каталог 🗂"), KeyboardButton(text="Корзина 🛍")],
        [KeyboardButton(text="Заказы 📦"), KeyboardButton(text="Помощь 🆘")]
    ], resize_keyboard=True
)

async def types_kb(back=True):
    builder = InlineKeyboardBuilder()
    types = await rq.get_types()
    for type in types:
        button = InlineKeyboardButton(text=type.ru_name, callback_data=f"type_{type.id}")
        builder.row(button)
    if back:
        builder.row(InlineKeyboardButton(text="⏪Вернуться", callback_data="back_menu"))
    return builder.as_markup()

async def products_kb(type_id, back=True):
    builder = InlineKeyboardBuilder()
    products = await rq.get_products(type_id)
    for product in products:
        button = InlineKeyboardButton(text=product.name, callback_data=f"product_{product.id}")
        builder.row(button)
    if back:
        builder.row(InlineKeyboardButton(text="⏪Вернуться", callback_data="back_section"))
    return builder.as_markup()

async def buy_kb(product_id):
    product = await rq.get_product_by_id(product_id)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Купить-1шт-{product.price} рублей", callback_data=f"indicate_{product.id}")]
        ]
    )
    return kb

async def size_kb(product_id):
    builder = InlineKeyboardBuilder()
    product = await rq.get_product_by_id(product_id)
    sizes = product.size.split(", ")
    for size in sizes:
        button = InlineKeyboardButton(text=size, callback_data=f"buy_{product.id}_{size}")
        builder.add(button)
    builder.row(InlineKeyboardButton(text="⏪Вернуться", callback_data="back_section"))
    return builder.as_markup()

async def new_buy_kb(product_id, us_id, quantity, size):
    product = await rq.get_product_by_id(product_id)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Купить-{size} размер-{product.price} рублей", callback_data=f"buy_{product.id}_{size}")],
            [InlineKeyboardButton(text="➖", callback_data=f"minus_{product_id}_{size}"), InlineKeyboardButton(text=f"{quantity} шт.", callback_data="count"), InlineKeyboardButton(text="➕", callback_data=f"plus_{product_id}_{size}")],
            [InlineKeyboardButton(text=f"Корзина ({await rq.get_sum_cart_by_user_id(us_id)} рублей)", callback_data=f"cart_{us_id}")],
        ]
    )
    return kb

make_order_kb =  InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Сделать заказ", callback_data=f"order")]
        ]
    )
pay_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="СБП")],
        [KeyboardButton(text="Банковская карта")],
        [KeyboardButton(text="Наличные")]
    ], resize_keyboard=True
)

phone_number_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Контакт", request_contact=True)]
    ], resize_keyboard=True
)

yes_no_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
    ], resize_keyboard=True
)

async def order_kb(orders):
    builder = InlineKeyboardBuilder()
    for order in orders:
        builder.add(InlineKeyboardButton(text=f"Заказ № {order.id} - {order.status}", callback_data=f"order_{order.id}"))
        builder.adjust(1)
    return builder.as_markup()

async def appeal_kb(appeal_id):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Ответить", callback_data=f"appeal_{appeal_id}")]
        ]
    )
    return kb