import asyncio
import logging
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_TOKEN, ADMIN_ID, CHARACTERS, USER_CHARACTER_MAPPING

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def is_admin(user_id):
    return user_id == ADMIN_ID

def get_character_for_user(user_id, username, first_name):
    if user_id == ADMIN_ID:
        return "Пико Пикович"
    
    if username:
        username_with_at = f"@{username}"
        if username_with_at in USER_CHARACTER_MAPPING:
            return USER_CHARACTER_MAPPING[username_with_at]
    
    if first_name and first_name in USER_CHARACTER_MAPPING:
        return USER_CHARACTER_MAPPING[first_name]
    
    return None

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    if message.chat.type == "private":
        await message.answer(
            "👋 **Привет! Я ролевой бот Пико Пиковича!**\n\n"
            "📱 **Доступные команды:**\n"
            "• /role - 🎭 Моя роль\n"
            "• /ping - 🏓 Проверка работы\n"
            "• /help - 📖 Все команды\n\n"
            "🎭 **Бот работает 24/7 на сервере!**"
        )
    else:
        await message.answer(
            f"🎭 **Ролевой бот Пико Пиковича**\n\n"
            f"✅ Бот активирован в чате!\n"
            f"💡 Используйте /help для списка команд\n"
            f"🎬 Модераторы: /start_rp для начала ролевой"
        )

@dp.message(Command("ping"))
async def ping_cmd(message: types.Message):
    start_time = datetime.now()
    msg = await message.answer("🏓 Понг...")
    end_time = datetime.now()
    ping_time = (end_time - start_time).total_seconds() * 1000
    
    await msg.edit_text(f"🏓 **Понг!**\n⏱ Время: `{ping_time:.2f}ms`\n✅ Бот работает 24/7!")

@dp.message(Command("role"))
async def my_role_cmd(message: types.Message):
    user_role = get_character_for_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name
    )
    
    if user_role:
        role_data = CHARACTERS[user_role]
        await message.answer(
            f"🎭 **ВАША РОЛЬ:** {user_role}\n"
            f"📝 **Амплуа:** {role_data['role']}\n"
            f"ℹ️ **Описание:** {role_data['desc']}"
        )
    else:
        await message.answer(
            "❌ **У вас нет назначенной роли!**\n\n"
            "📞 Обратитесь к @PicoFromTheVoid"
        )

@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    user_id = message.from_user.id
    user_status = "👤 Игрок"
    
    if is_admin(user_id):
        user_status = "👑 Главный администратор"
    
    help_text = (
        f"🎭 **Ролевой бот Пико Пиковича**\n\n"
        f"🔑 **Ваш статус:** {user_status}\n\n"
        f"**🎮 Основные команды:**\n"
        f"• /start - 🏠 Начало\n"
        f"• /role - 🎭 Моя роль\n"
        f"• /ping - 🏓 Проверка работы\n"
        f"• /help - 📖 Эта справка\n\n"
        f"**⚡ Модераторские команды:**\n"
        f"• /start_rp - 🎬 Начать ролевую\n"
        f"• /stop_rp - 🛑 Завершить ролевую\n\n"
        f"📞 **Поддержка:** @PicoFromTheVoid"
    )
    
    await message.answer(help_text)

@dp.message(Command("start_rp"))
async def start_rp_cmd(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Только администратор может запускать ролевые!")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎭 Начать ролевую", callback_data="start_rp")]
    ])
    
    await message.answer(
        "🎭 **НАЧАТЬ РОЛЕВУЮ**\n\n"
        "Готовы начать приключение?\n"
        "Нажмите кнопку ниже!",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "start_rp")
async def start_rp_callback(callback: types.CallbackQuery):
    await callback.answer("🎬 Ролевая началась!")
    await callback.message.answer(
        "🎭 **РОЛЕВАЯ НАЧАЛАСЬ!**\n\n"
        "Присоединяйтесь к своим ролям!\n"
        "Бот работает в режиме 24/7!"
    )

async def main():
    logger.info("🚀 Бот Пико Пиковича запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
