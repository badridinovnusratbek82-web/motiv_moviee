from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '8120006600:AAHuMXlrOx17hs742p25cEltLNyvVbj1uao'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- BIR NECHTA KANALLAR RO‘YXATI ---
CHANNELS = ['@motiv_moviee']


# --- Obuna tekshiruvchi funksiya ---
async def check_subscription(user_id):
    not_joined = []
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                not_joined.append(channel)
        except:
            not_joined.append(channel)
    return not_joined


# --- Inline tugmalar yasash ---
def subscribe_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    for ch in CHANNELS:
        kb.add(InlineKeyboardButton(f"📢 {ch} kanaliga obuna bo‘lish", url=f"https://t.me/{ch.replace('@','')}"))
    kb.add(InlineKeyboardButton("✅ Tekshirish", callback_data="check_subscribe"))
    return kb


# --- /start komandasi ---
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    not_joined = await check_subscription(user_id)

    if not_joined:
        await message.answer(
            "👋 Salom! Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:",
            reply_markup=subscribe_keyboard()
        )
    else:
        await message.answer("🎬 Kino kodini yuboring...")


# --- Tekshirish tugmasi bosilganda ---
@dp.callback_query_handler(lambda c: c.data == 'check_subscribe')
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    not_joined = await check_subscription(user_id)

    if not_joined:
        await bot.answer_callback_query(callback_query.id, "🚫 Hali hamma kanallarga obuna bo‘lmagansiz!", show_alert=True)
    else:
        await callback_query.message.delete()
        await bot.send_message(user_id, "✅ Rahmat! Endi kino kodini yuborishingiz mumkin.")


# --- Kino kodi yuborganda ---
@dp.message_handler(lambda msg: msg.text.isdigit())
async def get_post_by_id(message: types.Message):
    user_id = message.from_user.id
    not_joined = await check_subscription(user_id)

    if not_joined:
        await message.answer("⚠️ Avval barcha kanallarga obuna bo‘ling!", reply_markup=subscribe_keyboard())
        return

    message_id = int(message.text)
    try:
        await bot.forward_message(
            chat_id=message.chat.id,
            from_chat_id=CHANNELS[0],  # asosiy kanal
            message_id=message_id
        )
        await message.answer("✅ Kino topildi")
    except Exception as e:
        await message.answer("⚠️ Noto‘g‘ri kod!")


# --- /help komandasi ---
@dp.message_handler(commands=['help'])
async def help_cmd(message: types.Message):
    text = (
        "🤖 Sizga qanday yordam bera olaman?\n\n"
        "Agar muammo yoki savolingiz bo‘lsa, quyidagi admin bilan bog‘laning 👇\n\n"
        "👨‍💻 Admin: @nusratbek123"
    )
    await message.answer(text)


# --- /about komandasi ---
@dp.message_handler(commands=['about'])
async def about_cmd(message: types.Message):
    text = (
        "🌟 **Bot haqida**\n\n"
        "🎬 Ushbu bot orqali siz kinolar kodini yuborib, kanalimizdagi postni osongina topishingiz mumkin.\n"
        "🔒 Faqat kanal a'zolari uchun mo‘ljallangan.\n\n"
        "📢 Kanal: @motiv_moviee\n"
        "👨‍💻 Dasturchi: @nusratbek123\n"
        "📅 Versiya: 1.0"
    )
    await message.answer(text, parse_mode='Markdown')


if __name__ == '__main__':
    print("🤖 Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)



