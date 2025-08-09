from flask import Flask, request
import sqlite3
from telegram import Bot

from telegram import Update, InlineKeyboardMarkup, ChatMember, InlineKeyboardButton

from telegram.constants import ParseMode

import asyncio

import functions

app = Flask(__name__)

TOKEN = '8004725012:AAGJAkWMb9rEtZxMdGmU2S2PZ93i2M21UCo'


# request = Request(connect_timeout = 20, read_timeout = 20)
bot = Bot(token = TOKEN)

async def correct(user_id, text) :
    await bot.send_message(chat_id = user_id, text =text )

async def edit(message_id, text , reply_markup = None) : 
    await bot.edit_message_text(chat_id = '-1002549216386' ,parse_mode = ParseMode.MARKDOWN_V2 , message_id = message_id, text =text  , reply_markup = reply_markup)




async def unlinked(text) :  
    message = await bot.send_message(chat_id = '-1002499320415', text = text , parse_mode= ParseMode.MARKDOWN_V2)
    return message.message_id




loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@app.route('/receive-sms', methods=['POST'])
def receive_sms():

    # Extract data from the request


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

    

    with sqlite3.connect('denji.db') as conn :
        cursor = conn.cursor()

        cursor.execute('SELECT request_id, user_id,  status, message_id , credit_price FROM topup_requests WHERE trans_id = ?' ,(id,))
        result = cursor.fetchone()

    if result :
        request_id, user_id, status, message_id , credit = result
        if status == 'في الانتظار' :

            with sqlite3.connect('denji.db') as conn :
                cursor = conn.cursor()

                cursor.execute('SELECT balance , name , username FROM users WHERE id = ?',(user_id,))
                old_user_data = cursor.fetchone()
                old_balance , name , username = old_user_data
                syrian = amount
                amount = round(int(amount) / credit , 2)
                new_balance = old_balance + amount

                cursor.execute('UPDATE users SET balance = ? WHERE id = ?',(new_balance ,user_id))


                cursor.execute('''UPDATE topup_requests SET status = 'مقبول' , amount_added = ? WHERE request_id = ? ''', (amount,request_id))
                conn.commit()

            text = (
                                               f"تم الموافقة على طلب شحن الرصيد رقم {request_id} وشحن رصيدك بقيمة {amount} ✅")
            
            button = functions.create_telegram_check_button(user_id)
            edit_text = (
                                               f"تم التحقق من العملية بالرقم : `{request_id}`\n"
                                                f"الرقم التعريفي للمستخدم : `{user_id}` \n"
                                                f"الاسم : {functions.escape_markdown_v2(name)}\n"
                                                f"المعرف : @{functions.escape_markdown_v2(username)}\n\n"
                                                f"الطريقة :سيرياتيل كاش\n"
                                                f"رقم عملية التحويل : `{functions.escape_markdown_v2(id)}` \n"
                                                f"المبلغ بالسوري : {functions.escape_markdown_v2(syrian)}\n"
                                                f"المبلغ المضاف : {functions.escape_markdown_v2(amount)}\n"
                                                f"الرصيد قبل الإضافة : {functions.escape_markdown_v2(old_balance)}\n"
                                                f"الرصيد بعد الإضافة : {functions.escape_markdown_v2(new_balance)}"
            )

            loop.run_until_complete(correct(user_id, text))
            
            loop.run_until_complete(edit(message_id, edit_text , button))
            
        

    else :
        with sqlite3.connect('denji.db') as conn :
            cursor = conn.cursor()
            cursor.execute('''
                        INSERT INTO topup_requests (amount_added, trans_id, status, timestamp, topup_type)
                        VALUES (?, ? , 'طلب تلقائي بانتظار الربط', datetime('now') , 'سيرياتيل كاش'  )
                    ''', (int(amount), int(id)))
            request_id = cursor.lastrowid
            conn.commit()

        
        text = (
                f"عملية شحن غير مربوطة بطلب بعد : \n\n"
                f"رقم العملية : `{request_id}`\n"
                f"رقم عملية التحويل :  `{id}` \n"
                f"المبلغ :  `{amount}` ")

        message_id = loop.run_until_complete(unlinked(text))

        
        
        with sqlite3.connect('denji.db') as conn :
            cursor = conn.cursor()
            cursor.execute('UPDATE topup_requests SET message_id = ? WHERE request_id = ?',(message_id,request_id))
            conn.commit()

        


    return "SMS received", 200





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)