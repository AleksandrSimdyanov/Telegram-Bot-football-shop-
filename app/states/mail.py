from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.database.requests as rq

mail_router = Router()

class Mail(StatesGroup):
    mail = State()

@mail_router.message((F.text == "/mailing") & (F.from_user.id == 835168779))
async def mailing_cmd(message: Message, state: FSMContext):
    await message.answer("Введите сообщение для рассылки")
    await state.set_state(Mail.mail)

@mail_router.message(Mail.mail)
async def send_mail(message: Message, state: FSMContext, bot: Bot):
    mail = message.text
    users = await rq.get_all_users()
    for user in users:
        try:
            await bot.send_message(user.tg_id, mail)
        except Exception:
            continue
    await state.clear()
    await message.answer("Рассылка отправлена")