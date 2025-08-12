import json
# import sqlite3 # MODIFIED: sqlite3 is no longer used in this file.

from telegram import Update, InlineKeyboardMarkup, ChatMember, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes, \
    CallbackQueryHandler
from telegram.constants import ParseMode

import functions, keyboards, handlers, db
from collections import defaultdict
from time import time
import logging
from uuid import uuid4
import html
import traceback
from io import BytesIO

logger = logging.getLogger()

from asyncio import Lock
from weakref import WeakValueDictionary

# TOKEN = '8104378989:AAEywJ79v-ABya3X091P3vAOcVIc2aEuJa0' # denji test
TOKEN = '7718105050:AAFDSOl-EE4axZ7FO51J4YlFDq9OXvSpANg' # my test
# TOKEN = '8004725012:AAGJAkWMb9rEtZxMdGmU2S2PZ93i2M21UCo' # main denji

OWNER_ID = '5349543151'
# OWNER_ID = '5363898935'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['status'] = None
    user_id = update.effective_user.id
    
    with open('side.json', 'r') as f:
        blocked_list = json.load(f)['blocked_list']
    if str(user_id) in blocked_list:
        await update.message.reply_text("تم حظرك من قبل الدعم❌")
        return

    if await functions.check_membership(update, context):
        username = update.effective_user.username if update.effective_user.username else "NONE"
        name = update.message.from_user.full_name
        
        # --- MODIFIED: Replaced all sqlite3 code with a single asyncpg block ---
        pool = await db.get_db_pool()
        async with pool.acquire() as conn:
            # Check if the user exists
            exist = await conn.fetchrow('SELECT * FROM users WHERE id = $1', user_id)

            if not exist:
                await context.bot.send_message(
                    chat_id='-1002500174412',
                    text=f'مستخدم جديد : 🎉\n\n'
                         f'الاسم : {functions.escape_markdown_v2(name)}\n'
                         f'المعرف : @{functions.escape_markdown_v2(username)}\n'
                         f'ايدي الحساب : `{functions.escape_markdown_v2(user_id)}` ',
                    parse_mode=ParseMode.MARKDOWN_V2,
                    reply_markup=functions.create_telegram_check_button(user_id)
                )
            
            # Insert the user if they don't exist. ON CONFLICT is the PostgreSQL equivalent of INSERT OR IGNORE.
            await conn.execute(
                'INSERT INTO users (id, username, name) VALUES ($1, $2, $3) ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, username = EXCLUDED.username',
                user_id, username, name
            )

            # Fetch the user's balance and points
            data = await conn.fetchrow(
                'SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)), total_spent FROM users WHERE id = $1',
                user_id
            )
            balance, points = data
        # --- End of modification ---

        chat_type = update.message.chat.type
        if chat_type != 'group':
            if str(update.message.from_user.id) == OWNER_ID:
                await update.message.reply_text("أهلا بالسيد denji", reply_markup=keyboards.owner_keyboard)
            else:
                await update.message.reply_text(
                    f' *مرحبا بك سيد {functions.escape_markdown_v2(update.message.from_user.full_name)} في بوت denji sms 🤍* 🔥 \n\n'
                    f"*الرقم التعريفي :* `{user_id}` \n\n"
                    f"*الرصيد :* *{functions.escape_markdown_v2(balance)}* $\n\n"
                    f"*النقاط :* {functions.escape_markdown_v2(points)}",
                    reply_markup=keyboards.main_keyboard,
                    parse_mode='MarkdownV2'
                )
    else:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('القناة الرئيسية', url='https://t.me/+eqt5wlTNNjVhNTRk')],
            [InlineKeyboardButton('قناة التفعيلات', url='https://t.me/+JKioOpVhfIphNDRk')]
        ])
        await update.message.reply_text(
            'الرجاء الاشتراك بالقنوات لمتابعة أخبار المتجر واستخدام البوت ',
            reply_markup=keyboard
        )

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Exception while handling an update:", exc_info=context.error)
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    bytes_io = BytesIO()
    bytes_io.write(message.encode())
    bytes_io.seek(0)
    await context.bot.send_document('-1002668654788', document=bytes_io, filename=f"logs_{str(uuid4())}.html")
    try:
        await context.bot.send_message(chat_id='-1002668654788', text=message, parse_mode=ParseMode.HTML)
    except Exception:
        pass

user_locks = WeakValueDictionary()

def get_user_lock(user_id: int) -> Lock:
    lock = user_locks.get(user_id)
    if lock is None:
        lock = Lock()
        user_locks[user_id] = lock
    return lock

class SafeCallbackQueryHandler(CallbackQueryHandler):
    def __init__(self, callback, **kwargs):
        super().__init__(self._wrap(callback), **kwargs)

    @staticmethod
    def _wrap(button):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = update.effective_user
            if user is None:
                return await button(update, context)
            async with get_user_lock(user.id):
                await button(update, context)
        return wrapper

async def on_startup(app):
    await db.get_db_pool()

async def on_shutdown(app):
    await db.close_db_pools()

if __name__ == '__main__':
    print('starting...')
    app = Application.builder().token(TOKEN).post_init(on_startup).post_shutdown(on_shutdown).concurrent_updates(True).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('account', functions.get_account))
    app.add_handler(CommandHandler('syr', functions.change_syr))
    app.add_handler(CommandHandler('rec', functions.record))
    
    app.add_handler(MessageHandler(filters.PHOTO, handlers.handle_photo))
    app.add_handler(SafeCallbackQueryHandler(handlers.button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_messages))

    # Errors
    app.add_error_handler(error)

    print('polling..')
    app.run_polling(poll_interval=1)