from flask import Flask, request
import db  # MODIFIED: Replaced sqlite3 with db for asyncpg pooling
from telegram import Bot
from telegram import Update, InlineKeyboardMarkup, ChatMember, InlineKeyboardButton
from telegram.constants import ParseMode
import asyncio
import functions

app = Flask(__name__)

TOKEN = '8004725012:AAGJAkWMb9rEtZxMdGmU2S2PZ93i2M21UCo'

bot = Bot(token = TOKEN)

async def correct(user_id, text) :
    await bot.send_message(chat_id = user_id, text =text )

async def edit(message_id, text , reply_markup = None) : 
    await bot.edit_message_text(chat_id = '-1002549216386' ,parse_mode = ParseMode.MARKDOWN_V2 , message_id = message_id, text =text  , reply_markup = reply_markup)

async def unlinked(text) :  
    message = await bot.send_message(chat_id = '-1002499320415', text = text , parse_mode= ParseMode.MARKDOWN_V2)
    return message.message_id

# --- MODIFIED: Start of new async DB functions to replace sqlite3 blocks ---

async def db_find_request(trans_id):
    pool = await db.get_db_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow('SELECT request_id, user_id,  status, message_id , credit_price FROM topup_requests WHERE trans_id = $1', trans_id)

async def db_process_request(user_id, amount, request_id):
    pool = await db.get_db_pool()
    async with pool.acquire() as conn:
        # Using a transaction to ensure all updates succeed or none do.
        async with conn.transaction():
            old_user_data = await conn.fetchrow('SELECT balance, name, username FROM users WHERE id = $1 FOR UPDATE', user_id)
            old_balance, name, username = old_user_data
            
            new_balance = old_balance + amount
            await conn.execute('UPDATE users SET balance = $1 WHERE id = $2', new_balance, user_id)
            await conn.execute("UPDATE topup_requests SET status = 'مقبول', amount_added = $1 WHERE request_id = $2", amount, request_id)
    return old_balance, name, username, new_balance

async def db_create_unlinked_request(amount, trans_id):
    pool = await db.get_db_pool()
    async with pool.acquire() as conn:
        # Use RETURNING to get the new ID, as a replacement for lastrowid
        request_id = await conn.fetchval('''
            INSERT INTO topup_requests (amount_added, trans_id, status, timestamp, topup_type)
            VALUES ($1, $2, 'طلب تلقائي بانتظار الربط', NOW(), 'سيرياتيل كاش')
            RETURNING request_id
        ''', int(amount), int(trans_id))
    return request_id

async def db_update_unlinked_message_id(message_id, request_id):
    pool = await db.get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute('UPDATE topup_requests SET message_id = $1 WHERE request_id = $2', message_id, request_id)

# --- End of new async DB functions ---


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@app.route('/receive-sms', methods=['POST'])
def receive_sms():

    sms_data = request.json
    message = sms_data['message']

    if message.startswith('تم تعبئة') : 
        print(message)
        without_first = message[31:]
        amount = without_first.split('ل.س')[0]
        print(amount)
        id = without_first.split('رقم العملية ')[1]
    else :
        print(message)
        without_first = message[15:]
        print(without_first)
        amount = without_first.split(' ل.س')[0]
        print(amount)
        id = without_first.split('هو ')[1]
        print(id)

    # MODIFIED: Replaced the first sqlite3 block
    result = loop.run_until_complete(db_find_request(int(id)))

    if result :
        request_id, user_id, status, message_id , credit = result
        if status == 'في الانتظار' :
            
            syrian = amount
            amount_to_add = round(int(amount) / credit , 2)

            # MODIFIED: Replaced the second sqlite3 block
            old_balance, name, username, new_balance = loop.run_until_complete(db_process_request(user_id, amount_to_add, request_id))
            
            text = (f"تم الموافقة على طلب شحن الرصيد رقم {request_id} وشحن رصيدك بقيمة {amount_to_add} ✅")
            
            button = functions.create_telegram_check_button(user_id)
            edit_text = (
                                               f"تم التحقق من العملية بالرقم : `{request_id}`\n"
                                                f"الرقم التعريفي للمستخدم : `{user_id}` \n"
                                                f"الاسم : {functions.escape_markdown_v2(name)}\n"
                                                f"المعرف : @{functions.escape_markdown_v2(username)}\n\n"
                                                f"الطريقة :سيرياتيل كاش\n"
                                                f"رقم عملية التحويل : `{functions.escape_markdown_v2(id)}` \n"
                                                f"المبلغ بالسوري : {functions.escape_markdown_v2(syrian)}\n"
                                                f"المبلغ المضاف : {functions.escape_markdown_v2(amount_to_add)}\n"
                                                f"الرصيد قبل الإضافة : {functions.escape_markdown_v2(old_balance)}\n"
                                                f"الرصيد بعد الإضافة : {functions.escape_markdown_v2(new_balance)}"
            )

            loop.run_until_complete(correct(user_id, text))
            loop.run_until_complete(edit(message_id, edit_text , button))
    else :
        # MODIFIED: Replaced the third sqlite3 block (INSERT)
        request_id = loop.run_until_complete(db_create_unlinked_request(int(amount), int(id)))
        
        text = (
                f"عملية شحن غير مربوطة بطلب بعد : \n\n"
                f"رقم العملية : `{request_id}`\n"
                f"رقم عملية التحويل :  `{id}` \n"
                f"المبلغ :  `{amount}` ")

        message_id = loop.run_until_complete(unlinked(text))

        # MODIFIED: Replaced the fourth sqlite3 block (UPDATE)
        loop.run_until_complete(db_update_unlinked_message_id(message_id, request_id))

    return "SMS received", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)