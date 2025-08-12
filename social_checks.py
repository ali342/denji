import db  # MODIFIED: Replaced sqlite3
from telegram import Bot

import time
import json
import asyncio
import requests
import functions

from telegram.constants import ParseMode

TOKEN = '8004725012:AAGJAkWMb9rEtZxMdGmU2S2PZ93i2M21UCo'
# TOKEN = '7718105050:AAFDSOl-EE4axZ7FO51J4YlFDq9OXvSpANg' # my test

bot = Bot(token = TOKEN)

async def send(user_id, text) :
    await bot.send_message(chat_id = user_id, text =text )

async def accepted(text , reply_markup = None) :
    await bot.send_message(chat_id = '-1002879904667', text =text , reply_markup = reply_markup , parse_mode= ParseMode.MARKDOWN_V2 )

async def rejected(text) :
    await bot.send_message(chat_id = '-1002849483030', text =text , parse_mode= ParseMode.MARKDOWN_V2 )

async def partial(text , reply_markup = None) :
    await bot.send_message(chat_id = '-1002822978724', text =text , reply_markup = reply_markup , parse_mode= ParseMode.MARKDOWN_V2)

# --- MODIFIED: Start of new async DB helper functions ---

async def db_process_social_completed(order_id):
    """Processes a completed social order within a single transaction."""
    pool = await db.get_db_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            req_data = await conn.fetchrow('SELECT request_id, user_id, app, service, amount, link, price FROM social_requests WHERE auto_id = $1', order_id)
            if not req_data: return None
            
            request_id, user_id, app, offer, amount, link, price = req_data

            await conn.execute("UPDATE social_requests SET status = 'مقبول' WHERE auto_id = $1", order_id)
            
            user_data = await conn.fetchrow('SELECT name, username FROM users WHERE id = $1 FOR UPDATE', user_id)
            name, username = user_data
            
            await conn.execute("UPDATE users SET total_spent = total_spent + $1 WHERE id = $2", price, user_id)
            
            return request_id, user_id, app, offer, amount, link, price, name, username

async def db_process_social_canceled(order_id):
    """Processes a canceled social order, refunding the user in a single transaction."""
    pool = await db.get_db_pool()
    async with pool.acquire() as conn:
        req_data = await conn.fetchrow('SELECT request_id, user_id, app, service, amount, link, price, refunded FROM social_requests WHERE auto_id = $1', order_id)
        if not req_data: return None, False
        
        # If already refunded, do nothing.
        if req_data['refunded']: return None, True

        request_id, user_id, app, offer, amount, link, price = req_data['request_id'], req_data['user_id'], req_data['app'], req_data['service'], req_data['amount'], req_data['link'], req_data['price']

        async with conn.transaction():
            await conn.execute("UPDATE social_requests SET status = 'مرفوض' WHERE auto_id = $1", order_id)
            
            user_data = await conn.fetchrow('SELECT name, username FROM users WHERE id = $1 FOR UPDATE', user_id)
            name, username = user_data

            # Refund user and get new balance
            await conn.execute("UPDATE users SET balance = balance + $1 WHERE id = $2", price, user_id)
            new_balance = await conn.fetchval('SELECT balance FROM users WHERE id = $1', user_id)

            # Update the request with refund details
            await conn.execute('UPDATE social_requests SET balance_after_refund = $1, refunded = $2 WHERE request_id = $3', new_balance, price, request_id)
            
            return (request_id, user_id, app, offer, amount, link, price, name, username), False

async def db_process_social_partial(order_id, remained_from_api):
    """Processes a partially completed order, refunding the difference in a single transaction."""
    pool = await db.get_db_pool()
    async with pool.acquire() as conn:
        req_data = await conn.fetchrow('SELECT request_id, user_id, app, service, amount, link, price, refunded FROM social_requests WHERE auto_id = $1', order_id)
        if not req_data: return None, True
        
        # If already refunded, do nothing.
        if req_data['refunded']: return None, True

        request_id, user_id, app, offer, amount, link, price = req_data['request_id'], req_data['user_id'], req_data['app'], req_data['service'], req_data['amount'], req_data['link'], req_data['price']
        
        remain_percent = int(remained_from_api) / amount
        must_refund = round(float(price * remain_percent), 2)

        async with conn.transaction():
            await conn.execute("UPDATE social_requests SET status = 'مقبول جزئيا' WHERE auto_id = $1", order_id)
            
            user_data = await conn.fetchrow('SELECT name, username FROM users WHERE id = $1 FOR UPDATE', user_id)
            name, username = user_data

            # Refund user and get new balance
            await conn.execute("UPDATE users SET balance = balance + $1 WHERE id = $2", must_refund, user_id)
            new_balance = await conn.fetchval('SELECT balance FROM users WHERE id = $1', user_id)

            # Update the request with refund details
            await conn.execute('UPDATE social_requests SET balance_after_refund = $1, refunded = $2, remained = $3 WHERE request_id = $4', new_balance, must_refund, int(remained_from_api), request_id)

            return (request_id, user_id, app, offer, amount, link, price, name, username, must_refund), False

# --- End of new async DB helper functions ---

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

print('social_checks.py started')
while True :
    try :
        with open('side.json' , 'r' , encoding='utf-8') as f :
            data = json.load(f)
        
        requests_list = data['social_pending']
        to_remove = []

        for order_id in requests_list :
            time.sleep(4)
            try:
                params = {
                    'key' : 'dab3fac7cde4ca03f835688b83789674',
                    'action' : 'status',
                    'order' : order_id
                }
                response = requests.get("https://smmparty.com/api/v2", params=params, timeout=10).json()
                print(response)
                status = response['status']

                if status == 'Completed':
                    # MODIFIED: Replaced all sqlite3 blocks with a single atomic function call
                    result = loop.run_until_complete(db_process_social_completed(order_id))
                    if not result: continue
                    
                    request_id, user_id, app, offer, amount, link, price, name, username = result
                    
                    # ... Notification logic remains the same ...
                    view = {"Tik Tok":'Tik tok - تيك توك 🖤', 'FaceBook':'FaceBook - فيسبوك 💙', 'Instagram':'Instagram - انستاغرام 💜'}
                    imoji = {'متابعين بدون ضمان':'متابعين بدون ضمان 👤❌', 'متابعين ضمان سنة':'متابعين ضمان سنة 👤✅', 'لايكات':'لايكات 👍', 'مشاهدات':'مشاهدات ▶️'}
                    text = f"تم تنفيذ طلبك رقم {request_id} لشحن {view[app]} \nالخدمة : {imoji[offer]}\nالكمية : {amount}\nالرابط : {link}\nشكرا لاستخدامكم متجر Denji ❤"
                    loop.run_until_complete(send(user_id, text))

                    button = functions.create_refill_button(request_id, order_id) if offer == 'متابعين ضمان سنة' else None
                    done_text = f"عملية ناجحة : \n\nرقم العملية : `{request_id}` \nرقم الطلب في الموقع : `{order_id}` \nالتطبيق : {functions.escape_markdown_v2(app)}\nالخدمة : {functions.escape_markdown_v2(offer)}\nالكمية : {functions.escape_markdown_v2(amount)}\nالرابط : {functions.escape_markdown_v2(link)}\nالسعر : {functions.escape_markdown_v2(price)}\nالمستخدم : `{user_id}`\nالاسم : {functions.escape_markdown_v2(name)} \nالمعرف : @{functions.escape_markdown_v2(username)}"
                    loop.run_until_complete(accepted(done_text, button))
                    to_remove.append(order_id)

                elif status == 'Canceled':
                    # MODIFIED: Replaced all sqlite3 blocks with a single atomic function call
                    result, already_refunded = loop.run_until_complete(db_process_social_canceled(order_id))
                    if already_refunded:
                        to_remove.append(order_id)
                        continue
                    if not result: continue

                    request_id, user_id, app, offer, amount, link, price, name, username = result

                    # ... Notification logic remains the same ...
                    view = {"Tik Tok":'Tik tok - تيك توك 🖤', 'FaceBook':'FaceBook - فيسبوك 💙', 'Instagram':'Instagram - انستاغرام 💜'}
                    imoji = {'متابعين بدون ضمان':'متابعين بدون ضمان 👤❌', 'متابعين ضمان سنة':'متابعين ضمان سنة 👤✅', 'لايكات':'لايكات 👍', 'مشاهدات':'مشاهدات ▶️'}
                    text = f"لم نتمكن من تنفيذ طلبك رقم {request_id} لشحن {view[app]} \nالخدمة : {imoji[offer]}\nالكمية : {amount}\nالرابط : {link}\nتم إعادة المبلغ المدفوع \nيرجى التواصل مع الدعم @Mohammed_sn"
                    loop.run_until_complete(send(user_id, text))
                    
                    done_text = f"عملية فاشلة : \n\nرقم العملية : `{request_id}`\nرقم الطلب في الموقع : `{order_id}`\nالتطبيق : {functions.escape_markdown_v2(app)}\nالخدمة : {functions.escape_markdown_v2(offer)}\nالكمية : {functions.escape_markdown_v2(amount)}\nالرابط : {functions.escape_markdown_v2(link)}\nالسعر : {functions.escape_markdown_v2(price)}\nالمستخدم : `{user_id}`\nالاسم : {functions.escape_markdown_v2(name)} \nالمعرف : @{functions.escape_markdown_v2(username)}"
                    loop.run_until_complete(rejected(done_text))
                    to_remove.append(order_id)

                elif status == 'Partial':
                    remained = int(response['remains'])
                    # MODIFIED: Replaced all sqlite3 blocks with a single atomic function call
                    result, already_refunded = loop.run_until_complete(db_process_social_partial(order_id, remained))
                    if already_refunded:
                        to_remove.append(order_id)
                        continue
                    if not result: continue
                    
                    request_id, user_id, app, offer, amount, link, price, name, username, must_refund = result

                    # ... Notification logic remains the same ...
                    view = {"Tik Tok":'Tik tok - تيك توك 🖤', 'FaceBook':'FaceBook - فيسبوك 💙', 'Instagram':'Instagram - انستاغرام 💜'}
                    imoji = {'متابعين بدون ضمان':'متابعين بدون ضمان 👤❌', 'متابعين ضمان سنة':'متابعين ضمان سنة 👤✅', 'لايكات':'لايكات 👍', 'مشاهدات':'مشاهدات ▶️'}
                    text = f"لم نتمكن من تنفيذ طلبك رقم {request_id} لشحن {view[app]} بشكل كامل \nالخدمة : {imoji[offer]}\nالكمية : {amount}\nالرابط : {link}\nمتبقي : {remained} \nتم إعادة {must_refund} $ \nيرجى التواصل مع الدعم @Mohammed_sn"
                    loop.run_until_complete(send(user_id, text))

                    button = functions.create_refill_button(request_id, order_id) if offer == 'متابعين ضمان سنة' else None
                    done_text = f"عملية مكتملة جزئيا : \n\nرقم العملية : `{request_id}`\nرقم الطلب في الموقع : `{order_id}`\nالتطبيق : {functions.escape_markdown_v2(app)}\nالخدمة : {functions.escape_markdown_v2(offer)}\nالكمية : {functions.escape_markdown_v2(amount)}\nالرابط : {functions.escape_markdown_v2(link)}\nالسعر : {functions.escape_markdown_v2(price)}\nمتبقي : {functions.escape_markdown_v2(remained)}\nالمبلغ المعاد : {functions.escape_markdown_v2(must_refund)}\nالمستخدم : `{user_id}`\nالاسم : {functions.escape_markdown_v2(name)} \nالمعرف : @{functions.escape_markdown_v2(username)}"
                    loop.run_until_complete(partial(done_text, button))
                    to_remove.append(order_id)

            except Exception as e:
                print(f"Error processing order_id {order_id}: {e}")
                continue

        if to_remove:
            with open('side.json', 'r+', encoding='utf-8') as f:
                data = json.load(f)
                current_pending = data.get('social_pending', [])
                data['social_pending'] = [p for p in current_pending if p not in to_remove]
                f.seek(0)
                json.dump(data, f)
                f.truncate()
    
    except Exception as e:
        print(f"Error in main loop: {e}")
            
    time.sleep(10)