from telegram import Update, InlineKeyboardMarkup, ChatMember, InlineKeyboardButton

from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes, \
    CallbackQueryHandler

from telegram.constants import ParseMode


import requests 

import aiohttp


import functions, keyboards
import time
 
import json
import sqlite3

import random
import string

characters = string.ascii_letters + string.digits

# OWNER_ID = '5349543151'
OWNER_ID = '5363898935'

def get_gv(var) :
    with open('side.json' , 'r' , encoding='utf-8') as file :
        data = json.load(file)
    return data.get(var)

buttons_ids = {}



general_lists = {}






min_amount_texts = {
            'متابعين بدون ضمان 👤❌' : 'متابع',
            'متابعين ضمان سنة 👤✅' : 'متابع' ,
            'لايكات 👍' : 'لايك' , 
            'مشاهدات ▶️' : 'مشاهدة'
        }



def get_json(file_name) : 
    with open(file_name , 'r' , encoding='utf-8')as file :
        data = json.load(file)
    return data

def update_json(file_name , data) : 
    with open(file_name , 'w' , encoding='utf-8')as file :
        json.dump(data,file)
    
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    option = query.data
    user_id = query.from_user.id
    if not option.startswith(('lion:' , 'lioncode:' , 'viotp:' , 'viotpcode:' , 'العرض المفعل' , 'dropsms:', 'dropsmscode:' , 'smslive:' , 'smslivecode:', 'socialconf:')) :
        await query.answer()
    context.user_data['status'] = None

    
    

    with open('side.json' , 'r') as f :
        blocked_list = json.load(f)['blocked_list']
    if str(user_id) in blocked_list :
        await context.bot.send_message(chat_id = user_id, text = "تم حظرك من قبل الدعم❌")
        return
    
    if not functions.ON and str(user_id) != OWNER_ID :
        await context.bot.send_message(chat_id = user_id, text = "البوت متوقف مؤقتا ⏳")
        return
    
    name = query.from_user.full_name
    username = query.from_user.username
    
    
    if option == 'سجل الشراء' :
        context.user_data['status'] = 'normal'
        conn = functions.connect_db()
        cursor = conn.cursor()
        cursor.execute('''SELECT request_id , user_id , app , country , number , server , provider , status , timestamp , price , CAST(ROUND(balance_before, 2) AS DECIMAL(10,2)) ,  CAST(ROUND(balance_after, 2) AS DECIMAL(10,2)) ,  CAST(ROUND(balance_after_refund, 2) AS DECIMAL(10,2)) , code , auto_id , (STRFTIME('%s', end_time) - STRFTIME('%s', 'now')) FROM item_requests WHERE user_id = ?''',(user_id,))
        result = cursor.fetchall()
        
        if result :
            if len(result) > 8 :
                result = result[-8:]
            for order in result :
                request_id , user_id , app , country , number , server , provider , status , timestamp , price , balance_before , balance_after , balance_after_refund , code , auto_id , rest_seconds = order
                try :
                    if rest_seconds == None :
                        rest_seconds = -1

                    time_left = ''
                    if rest_seconds > 0 :
                        rest_minutes = rest_seconds // 60
                        rest_seconds = rest_seconds % 60
                        if rest_seconds < 10 :
                            rest_seconds = f"0{rest_seconds}"
                        time_left = f'{rest_minutes}:{rest_seconds}'

                    
                    new_names_dict = {
                        'مفعل' : 'جارية ⏳',
                        'منتهية' : 'مكتملة ✅',
                        'ملغية' : 'ملغية ❌'
                    }
                    await context.bot.send_message(chat_id = user_id , 
                                                   text = f"رقم الطلب : `{request_id}`\n\n"
                                                   f"الرقم : `{functions.escape_markdown_v2(number)}`\n"
                                                   f"التطبيق : {functions.escape_markdown_v2(app)}\n"
                                                   f"الدولة : {functions.escape_markdown_v2(country)}\n"
                                                   f"الكود : `{functions.escape_markdown_v2(code) if code else 'لايوجد'}`\n"
                                                   f"الوقت المتبقي : {functions.escape_markdown_v2(time_left) if time_left != '' else '0'}\n"
                                                    f"الحالة : {new_names_dict[status]}\n"
                                                    f"التاريخ : {functions.escape_markdown_v2(timestamp)}" , parse_mode = ParseMode.MARKDOWN_V2)
                except :
                    None
        else :
            try :
                await context.bot.send_message(chat_id = user_id, text = "ليس لديك طلبات شراء أرقام مسجلة")
            except :
                None
        
        cursor.execute('''SELECT request_id , user_id , app , service , amount , link , status , timestamp , price , refunded , remained  FROM social_requests WHERE user_id = ?''',(user_id,))
        result = cursor.fetchall()
        conn.close()
        if result :
            if len(result) > 8 :
                result = result[-8:]
            for order in result :
                request_id , user_id , app , service , amount , link , status , timestamp , price , refunded , remained = order
                try :
                    

                    
                    new_names_dict = {
                        'في الانتظار' : 'جارية ⏳',
                        'مقبول' : 'مكتملة ✅',
                        'مقبول جزئيا' : 'مكتملة جزئيا ⚪',
                        'مرفوض' : 'مرفوضة ❌'

                    }
                    if not refunded :
                        await context.bot.send_message(chat_id = user_id , 
                                                text = f"رقم الطلب : `{request_id}`\n\n"
                                                f"التطبيق : `{functions.escape_markdown_v2(app)}`\n"
                                                f"الخدمة : {functions.escape_markdown_v2(service)}\n"
                                                f"الكمية : {functions.escape_markdown_v2(amount)}\n"
                                                f"الرابط : {functions.escape_markdown_v2(link)}\n"
                                                f"السعر : {functions.escape_markdown_v2(price)} $\n\n"
                                                    f"الحالة : {new_names_dict[status]}\n"
                                                    f"التاريخ : {functions.escape_markdown_v2(timestamp)}" , parse_mode = ParseMode.MARKDOWN_V2)
                    else :
                        await context.bot.send_message(chat_id = user_id , 
                                                    text = f"رقم الطلب : `{request_id}`\n\n"
                                                    f"التطبيق : `{functions.escape_markdown_v2(app)}`\n"
                                                    f"الخدمة : {functions.escape_markdown_v2(service)}\n"
                                                    f"الكمية : {functions.escape_markdown_v2(amount)}\n"
                                                    f"الرابط : {functions.escape_markdown_v2(link)}\n"
                                                    f"السعر : {functions.escape_markdown_v2(price)} $\n\n"
                                                    f"الحالة : {new_names_dict[status]}\n"
                                                    f"الكمية المتبقية : {functions.escape_markdown_v2(remained)} \n"
                                                    f"المبلغ المعاد : {functions.escape_markdown_v2(refunded)} $ \n"
                                                    f"التاريخ : {functions.escape_markdown_v2(timestamp)}" , parse_mode = ParseMode.MARKDOWN_V2)
                except :
                    None
        else :
            try :
                await context.bot.send_message(chat_id = user_id, text = "ليس لديك طلبات تواصل اجتماعي مسجلة")
            except :
                None

    elif option == 'سجل الإيداع' :
        context.user_data['status'] = 'normal'
        result = await functions.get_topup_record(user_id) 
        if result :
            if len(result) > 15 :
                result = result[-15:]
            for order in result :
                request_id , user_id , amount_sent , credit , amount_added , trans_id , old_balance, new_balance,  status , timestamp , topup_type , photo_file_id , message_id   = order

                try :
                    new_names_dict = {
                        'في الانتظار' : 'في الانتظار ⏳',
                        'مقبول' : 'مقبول ✅',
                        'مرفوض' : 'مرفوض ❌'
                    }
                    await context.bot.send_message(chat_id = user_id , 
                                                   text = f"رقم الطلب : {request_id}\n\n"
                                                    f"النوع : {topup_type}\n"
                                                    f"المبلغ المطلوب : {amount_sent}\n"
                                                    f"سعر ال $ : {credit}\n"
                                                    f"المبلغ المضاف : {amount_added}\n"
                                                    f"رقم العملية : {trans_id}\n\n"

                                                    f"الحالة : {new_names_dict[status]}\n"
                                                    f"التاريخ : {timestamp}" )
                except :
                    None
        else :
            try :
                await context.bot.send_message(chat_id = user_id, text = "ليس لديك طلبات شحن مسجلة")
            except :
                None
                

    elif option == 'شحن الرصيد' :
        context.user_data['status'] = 'normal'
        await query.edit_message_text( text = "اختر الطريقة" , reply_markup = keyboards.topup_methods)
        
    elif option == 'سيرياتيل كاش' :
        context.user_data['topup method'] = option
        keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('رجوع' , callback_data = f"شحن الرصيد")
                        ]
                    ]
                )
        await query.edit_message_text(text = f"1 $ \\= {get_gv('syr_credit')} ل\\.س \n\n"
                                      f"يرجى التحويل على أحد الأرقام التالية \n\n"
                                      f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\- \n\n"
                                      f"{get_gv('syr')}\n"
                                      f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\- \n\n"
                                       f"تحويل يدوي حصرا ثم إرسال رقم عملية التحويل" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup = keyboard)
        context.user_data['status'] = 'waiting topup id'
        
    
    
    
    elif option.startswith('msr:') :
        await query.edit_message_text(text= "⏳")
        
        #method , trans_id , amount = option.split(':')[1:]
        buttons_id = option.split(':')[1]
        method , trans_id , amount , credit = buttons_ids[buttons_id].split(':')

        amount = int(amount)
        credit = int(credit)

        with sqlite3.connect('denji.db') as conn :
            cursor = conn.cursor()
            cursor.execute('SELECT status , message_id , amount_added , request_id  FROM topup_requests WHERE trans_id = ?',(trans_id,))
            result = cursor.fetchone()

        
        if result :
            status, message_id , amount_added , request_id  = result
            if status == 'طلب تلقائي بانتظار الربط' :
                with sqlite3.connect('denji.db') as conn :
                    cursor = conn.cursor()

                    cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) , name , username FROM users WHERE id = ?',(user_id,))
                    balance , name , username = cursor.fetchone()

                    amount_added = round(amount_added / credit   , 2)


                    cursor.execute(''' UPDATE topup_requests SET status = 'مقبول' , user_id = ? , amount_sent = ? , amount_added = ? , credit_price = ? , balance_before = ? , balance_after = ?  WHERE trans_id = ? ''', (user_id, amount, amount_added , credit, balance , balance + amount_added , trans_id))
                    conn.commit()

                    

                    cursor.execute('UPDATE users SET balance = balance + ROUND(?, 2) WHERE id = ?' , (amount_added, user_id))
                    conn.commit()
                
                
                await query.edit_message_text(text =f"تم الموافقة على طلب شحن الرصيد رقم {request_id} وشحن رصيدك بقيمة {amount_added} ✅")
                
                button = functions.create_telegram_check_button(user_id)
                await context.bot.edit_message_text(chat_id = '-1002499320415' , message_id = message_id, 
                                                    text = f"تم التحقق من العملية بالرقم : {request_id}\n"
                                                    f"الرقم التعريفي للمستخدم : `{user_id}` \n"
                                                    f"الاسم : {functions.escape_markdown_v2(name)}\n"
                                                    f"المعرف : @{functions.escape_markdown_v2(username)}\n\n"
                                                    f"الطريقة :سيرياتيل كاش\n"
                                                    f"رقم عملية التحويل : `{functions.escape_markdown_v2(trans_id)}` \n"
                                                    f"المبلغ المضاف : {functions.escape_markdown_v2(amount_added)}\n"
                                                    f"الرصيد قبل الإضافة : {functions.escape_markdown_v2(balance)}\n"
                                                    f"الرصيد بعد الإضافة : {functions.escape_markdown_v2(balance + amount_added)}" , reply_markup = button , parse_mode = ParseMode.MARKDOWN_V2)

            else :
                await query.edit_message_text(text = f"{query.message.text}\n\n"
                                              f"هذه العملية موجودة مسبقا بالرقم : {request_id} ❌")
        
        else :
        
            with sqlite3.connect('denji.db') as conn :
                try :
                    cursor = conn.cursor()
                    cursor.execute('''INSERT INTO topup_requests (user_id, amount_sent , trans_id , status , timestamp , topup_type , credit_price ) 
                                VALUES (? , ? , ? , 'في الانتظار' , datetime('now') , ? , ?)
                    ''' , (user_id, amount , trans_id, method , credit))
                    request_id = cursor.lastrowid
                    conn.commit()   

                    must_added = round(amount / credit , 2)

                    keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('موافقة', callback_data = f'acms:{user_id}:{must_added}:{request_id}'),
                            InlineKeyboardButton('رفض', callback_data = f'rejms:{user_id}:{request_id}')
                        ]
                    ]
                )
                        
                    message = await context.bot.send_message(chat_id = '-1002549216386' , text = 
                        f"عملية إيداع جديدة بالرقم : `{request_id}` \n\n"
                        f"النوع : {method}\n"
                        f"رقم العملية : `{trans_id}`\n"
                        f"المبلغ المرسل : {amount}\n"
                        f"سعر ال $ : {credit} \n"
                        f"اسم المستخدم : {functions.escape_markdown_v2(query.from_user.full_name)}\n"
                        f"المعرف : @{functions.escape_markdown_v2(query.from_user.username)}\n"
                        f"الرقم التعريفي : `{user_id}`" , reply_markup = keyboard , parse_mode = ParseMode.MARKDOWN_V2)

                    message_id = message.message_id

                    cursor.execute('UPDATE topup_requests SET message_id = ? WHERE request_id = ?',(message_id, request_id))

                    

                except :
                    conn.rollback()
                    await query.message.reply_text(text= "حدث خطأ ما ")
                    return
                    
            await query.edit_message_text(text = f"{query.message.text}\n\n"
                                            f"تم استلام طلبك يرجى الانتظار للتأكيد ⏳")
            
    elif option == 'cancle' :
        await query.edit_message_text('تم إلغاء العملية❌')
        
        
    elif option.startswith('acms:') :
        user_id, must_added, request_id = option.split(':')[1:]
        must_added = float(must_added)
        with sqlite3.connect('denji.db') as conn :
            cursor = conn.cursor()

            cursor.execute('SELECT status FROM topup_requests WHERE request_id = ?',(request_id,))
            status = cursor.fetchone()[0]

            if status != 'في الانتظار' :
                await query.edit_message_text(text = f"{query.message.text}\n\n"
                                              f"تم تنفيذ هذا الطلب مسبقا ")

                return

            cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) FROM users WHERE id = ?' , (user_id,))
            data = cursor.fetchone()
            old_balance = data[0]

            cursor.execute('UPDATE users SET balance = balance + ROUND(?, 2) WHERE id = ?' , (must_added,user_id))
            conn.commit()

             
            cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) FROM users WHERE id = ?' , (user_id,))
            data = cursor.fetchone()
            new_balance = data[0]

            cursor.execute('''UPDATE topup_requests SET status = 'مقبول' , amount_added = ? , balance_before = ?, balance_after = ? WHERE request_id = ? ''', (must_added,old_balance , new_balance , request_id))
        
        await query.edit_message_text(text = f"{query.message.text}\n\n"
                                      f"تم إضافة الرصيد ✔\n\n"
                                      f"الرصيد قبل الإضافة : {old_balance}\n"
                                      f"المبلغ المضاف : {must_added}\n"
                                      f"الرصيد الجديد : {new_balance}")
        
        await context.bot.send_message(chat_id = user_id, text = 
        f"تم الموافقة على طلب شحن الرصيد رقم {request_id} وشحن رصيدك بقيمة {must_added} ✔")

    elif option.startswith('rejms:') :
        user_id , request_id = option.split(':')[1:]

        with sqlite3.connect('denji.db') as conn :
            cursor = conn.cursor()
            cursor.execute('''UPDATE topup_requests SET status = 'مرفوض' WHERE request_id = ? ''', (request_id,))
            conn.commit()

        await query.edit_message_text(text= f"{query.message.text}\n\n"
        f"تم رفض العملية ❌")

        await context.bot.send_message(chat_id = user_id , text = 
        f"تم رفض طلبك لشحن الرصيد رقم {request_id} ❌")
        
        
    elif option == 'حسابي' :
        context.user_data['status'] = 'normal'
        name, balance, total_spent = await functions.account(user_id)
        await context.bot.send_message(chat_id = user_id, text = f"*اسم المستخدم : *{functions.escape_markdown_v2(name)}\n\n"
                                        f"*الرقم التعريفي :* `{user_id}` \n\n"
                                        f"*الرصيد :* *{functions.escape_markdown_v2(balance)}* $\n\n"
                                        f"*النقاط :* {functions.escape_markdown_v2(total_spent)}" ,
                                        parse_mode = ParseMode.MARKDOWN_V2 , 
                                        reply_markup = keyboards.my_account)

    
    elif option == 'الدعم' :
        context.user_data['status'] = 'normal'
        await context.bot.send_message(chat_id = user_id, text = f"للتواصل مع الدعم يرجى طرح مشكلتك باختصار\n\n"
                                       f"[Denji sms admin](tg://user?id={OWNER_ID})" , parse_mode = 'MarkdownV2')
        
    


    elif option == 'بايير' : 
        keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('رجوع' , callback_data = f"شحن الرصيد")
                        ]
                    ]
                )
        await query.edit_message_text(text = f'طريقة الإيداع : بايير\n'
                                          f"يرجى الإرسال على العنوان التالي ثم إرسال لقطة شاشة للعملية \n\n"
                                          f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\- \n\n"
                                          f"`{functions.escape_markdown_v2(get_gv('payeer'))}`\n\n"
                                          f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\- \n\n"
                                          f" 1 $ \\= {functions.escape_markdown_v2(get_gv('pay_credit'))} PAYEER USD" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup = keyboard)
        context.user_data['status'] = 'waiting payeer screen shot'



    elif option == 'photo cancle' :
        context.user_data['status'] = None
        await query.edit_message_caption(caption = 'تم إلغاء العملية❌')
        
    elif option.startswith('pay:') :
        await query.edit_message_caption(caption = '⏳')
        amount , credit = option.split(':')[1:]
        amount = float(amount)
        credit = float(credit)

        conn = functions.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
                    INSERT INTO topup_requests (user_id, amount_sent, status, timestamp, topup_type , photo_file_id , credit_price)
                    VALUES (?, ? , 'في الانتظار', datetime('now') , 'بايير' , ? , ? )
                ''', (user_id, amount   , photo_files_ids[user_id] , credit))
        request_id = cursor.lastrowid
        conn.commit()
        conn.close()
        must_added = round(amount / credit , 2)
        keyboard = [
                [
                    InlineKeyboardButton("✅ تأكيد", callback_data=f"notappay:{user_id}:{must_added}:{request_id}"),
                    InlineKeyboardButton("❌ رفض", callback_data=f"notrejpay:{user_id}:{must_added}:{request_id}")
                ]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_photo(chat_id = '-1002608105558' , photo = photo_files_ids[user_id] , caption = f"طلب إيداع بايير : \n\n"
                                       f"رقم العملية : {request_id}\n"
                                       f"الرقم التعريفي : `{user_id}` \n"
                                       f"الاسم : {functions.escape_markdown_v2(query.from_user.first_name)} {functions.escape_markdown_v2(query.from_user.last_name if query.from_user.last_name else '')} \n"
                                       f"اسم المستخدم : @{functions.escape_markdown_v2(query.from_user.username if query.from_user.username else '')} \n"
                                       f"المبلغ المرسل : {functions.escape_markdown_v2(amount)} \n"
                                       f"سعر ال $ : {functions.escape_markdown_v2(credit)}"
                                       ,
                                       parse_mode= ParseMode.MARKDOWN_V2 ,
                                       reply_markup = reply_markup)

        await query.edit_message_caption(
                                            caption = f" {query.message.caption} \n\n"
                                             f"تم استلام طلبك يرجى الانتظار للتأكيد ⏳" 
                                             , reply_markup = None)
        








    # sham cash

    elif option == 'شام كاش' : 
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('ليرة سورية' , callback_data = f"شام كاش ليرة سوربة"),
                    InlineKeyboardButton('دولار' , callback_data = f"شام كاش دولار")
                ],
                [
                    InlineKeyboardButton('رجوع' , callback_data = f"شحن الرصيد")
                ]
            ]
        )
        await query.message.reply_text("اختر العملة ", reply_markup = keyboard)

                
    elif option == 'شام كاش ليرة سوربة' : 
        keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('رجوع' , callback_data = f"شحن الرصيد")
                        ]
                    ]
                )
        await query.edit_message_text(text = f'طريقة الإيداع : شام كاش ليرة سوربة\n'
                                          f"يرجى الإرسال على العنوان التالي ثم إرسال لقطة شاشة للعملية \n\n"
                                          f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\- \n\n"
                                          f"`{functions.escape_markdown_v2(get_gv('sham_cash_syr'))}`\n\n"
                                          f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\- \n\n"
                                          f" 1 $ \\= {functions.escape_markdown_v2(get_gv('sham_cash_syr_credit'))} ل\\.س" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup = keyboard)
        context.user_data['status'] = 'waiting sham cash syrian screen shot'

    

    elif option == 'شام كاش دولار' : 
        keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('رجوع' , callback_data = f"شحن الرصيد")
                        ]
                    ]
                )
        await query.edit_message_text(text = f'طريقة الإيداع : شام كاش دولار\n'
                                          f"يرجى الإرسال على العنوان التالي ثم إرسال لقطة شاشة للعملية \n\n"
                                          f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\- \n\n"
                                          f"`{functions.escape_markdown_v2(get_gv('sham_cash_dol'))}`\n\n"
                                          f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\- \n\n"
                                          f" 1 $ \\= {functions.escape_markdown_v2(get_gv('sham_cash_dol_credit'))} ل\\.س" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup = keyboard)
        context.user_data['status'] = 'waiting sham cash dollar screen shot'



   
        
    elif option.startswith('shamcash:') :
        await query.edit_message_caption(caption = '⏳')
        amount , credit = option.split(':')[1:]
        amount = float(amount)
        credit = float(credit)

        conn = functions.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
                    INSERT INTO topup_requests (user_id, amount_sent, status, timestamp, topup_type , photo_file_id , credit_price)
                    VALUES (?, ? , 'في الانتظار', datetime('now') , 'شام كاش' , ? , ? )
                ''', (user_id, amount   , photo_files_ids[user_id] , credit))
        request_id = cursor.lastrowid
        conn.commit()
        conn.close()
        must_added = round(amount / credit , 2)
        keyboard = [
                [
                    InlineKeyboardButton("✅ تأكيد", callback_data=f"notappay:{user_id}:{must_added}:{request_id}"),
                    InlineKeyboardButton("❌ رفض", callback_data=f"notrejpay:{user_id}:{must_added}:{request_id}")
                ]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_photo(chat_id = '-1002817477353' , photo = photo_files_ids[user_id] , caption = f"طلب إيداع شام كاش : \n\n"
                                       f"رقم العملية : {request_id}\n"
                                       f"الرقم التعريفي : `{user_id}` \n"
                                       f"الاسم : {functions.escape_markdown_v2(query.from_user.first_name)} {functions.escape_markdown_v2(query.from_user.last_name if query.from_user.last_name else '')} \n"
                                       f"اسم المستخدم : @{functions.escape_markdown_v2(query.from_user.username if query.from_user.username else '')} \n"
                                       f"المبلغ المرسل : {functions.escape_markdown_v2(amount)} \n"
                                       f"سعر ال $ : {functions.escape_markdown_v2(credit)}"
                                       ,
                                       parse_mode= ParseMode.MARKDOWN_V2 ,
                                       reply_markup = reply_markup)

        await query.edit_message_caption(
                                            caption = f" {query.message.caption} \n\n"
                                             f"تم استلام طلبك يرجى الانتظار للتأكيد ⏳" 
                                             , reply_markup = None)

    
    
    elif option.startswith('notappay:'):
        user_id , must_added, request_id = option.split(':')[1:]
        try :
            must_added = float(must_added)
        except :
            conn = functions.connect_db()
            cursor = conn.cursor()

            cursor.execute('''
                    UPDATE topup_requests 
                    SET status = 'مقبول'
                    WHERE request_id = ?
                ''', ( request_id,))
            
            conn.commit()
            conn.close()
            await query.edit_message_caption(caption = f" {query.message.caption} \n\n"
                                            f"هناك مشكلة في المبلغ المدخل يرجى إضافة الرصيد يدويا " ,
                                       reply_markup = None )
            return


        
        
        conn = functions.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) FROM users WHERE id = ?' , (user_id,))
        data = cursor.fetchone()
        old_balance = data[0]

        cursor.execute('UPDATE users SET balance = balance + ROUND(?, 2) WHERE id = ?' , (must_added,user_id))
        conn.commit()

             
        cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) FROM users WHERE id = ?' , (user_id,))
        data = cursor.fetchone()
        new_balance = data[0]

        cursor.execute('''UPDATE topup_requests SET status = 'مقبول' , amount_added = ? , balance_before = ?, balance_after = ? WHERE request_id = ? ''', (must_added,old_balance , new_balance , request_id))
        
        
        
        conn.commit()
        conn.close()

        await query.edit_message_caption(caption = f" {query.message.caption} \n\n"
                                            f"تم تحديث رصيد المستخدم ✔ \n"
                                            f"الرصيد قبل الإضافة : {old_balance}\n"
                                             f"تم إضافة {must_added}\n"
                                              f"الرصيد بعد الإضافة : {new_balance}" ,
                                       reply_markup = None )
        
        await context.bot.send_message(chat_id=user_id, text = f"تم شحن رصيدك بمقدار {must_added} ✔")

        

    elif option.startswith('notrejpay:') :
        user_id , must_added, request_id = option.split(':')[1:]
        conn = functions.connect_db()
        cursor = conn.cursor()

        cursor.execute('''
                UPDATE topup_requests
                SET status = 'مرفوض'
                WHERE request_id = ? ''' , (request_id,))

        conn.commit()
        conn.close()
        await context.bot.send_message(chat_id=user_id, text = f"تم رفض طلب شحن رصيدك رقم {request_id} إذا كنت تظن أن هناك مشكلة ما \n رجاء تواصل مع الدعم\n\n"
                                       f"[Denji sms admin](tg://user?id={OWNER_ID})" , parse_mode = ParseMode.MARKDOWN_V2)

        await query.edit_message_caption(caption = f" {query.message.caption} \n\n"
                                            f"تم رفض العملية ❌ " ,
                                       reply_markup = None )
        

    


    


    elif option == 'USDT' : 
        keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('رجوع' , callback_data = f"شحن الرصيد")
                        ]
                    ]
                )
        
        bep20 = get_gv('bep20')
        coinex = get_gv('coinex')
        await query.edit_message_text(text = f'طريقة الإيداع : USDT \n'
                                          f"يرجى الإرسال على العنوان التالي ثم إرسال لقطة شاشة للعملية \n\n"
                                          f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\- \n\n"
                                          f"BEP\\-20 : \n\n"
                                          f"`{functions.escape_markdown_v2(bep20)}`\n\n"
                                          f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\- \n\n"
                                          f"COINEX : \n\n"
                                          f"`{functions.escape_markdown_v2(coinex)}`\n\n"
                                          f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\- \n\n"
                                          f" 1 $ \\= 1 USDT" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup = keyboard)
        context.user_data['status'] = 'waiting usdt screen shot'



    elif option == 'photo cancle' :
        context.user_data['status'] = None
        await query.edit_message_caption(caption = 'تم إلغاء العملية❌')
        
    elif option.startswith('usdt:') :
        await query.edit_message_caption(caption = '⏳')
        amount , credit = option.split(':')[1:]
        amount = float(amount)
        credit = float(credit)

        conn = functions.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
                    INSERT INTO topup_requests (user_id, amount_sent, status, timestamp, topup_type , photo_file_id , credit_price)
                    VALUES (?, ? , 'في الانتظار', datetime('now') , 'USDT' , ? , ? )
                ''', (user_id, amount   , photo_files_ids[user_id] , credit))
        request_id = cursor.lastrowid
        conn.commit()
        conn.close()
        must_added = round(amount / credit , 2)
        keyboard = [
                [
                    InlineKeyboardButton("✅ تأكيد", callback_data=f"notappay:{user_id}:{must_added}:{request_id}"),
                    InlineKeyboardButton("❌ رفض", callback_data=f"notrejpay:{user_id}:{must_added}:{request_id}")
                ]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_photo(chat_id = '-1002501666631' , photo = photo_files_ids[user_id] , caption = f"طلب إيداع USDT : \n\n"
                                       f"رقم العملية : {request_id}\n"
                                       f"الرقم التعريفي : `{user_id}` \n"
                                       f"الاسم : {functions.escape_markdown_v2(query.from_user.first_name)} {functions.escape_markdown_v2(query.from_user.last_name if query.from_user.last_name else '')} \n"
                                       f"اسم المستخدم : @{functions.escape_markdown_v2(query.from_user.username if query.from_user.username else '')} \n"
                                       f"المبلغ المرسل : {functions.escape_markdown_v2(amount)} \n"
                                       f"سعر ال $ : {functions.escape_markdown_v2(credit)}"
                                       ,
                                       parse_mode= ParseMode.MARKDOWN_V2 ,
                                       reply_markup = reply_markup)

        await query.edit_message_caption(
                                            caption = f" {query.message.caption} \n\n"
                                             f"تم استلام طلبك يرجى الانتظار للتأكيد ⏳" 
                                             , reply_markup = None)
        

    
    # binance


    elif option == 'binance' : 
        keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('رجوع' , callback_data = f"شحن الرصيد")
                        ]
                    ]
                )
        
        address = get_gv('binance')
        
        await query.edit_message_text(text = f'طريقة الإيداع : Binance \n'
                                          f"يرجى الإرسال على العنوان التالي ثم إرسال لقطة شاشة للعملية \n\n"
                                          f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\- \n\n"
                                          f"`{functions.escape_markdown_v2(address)}`\n\n"
                                          f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\- \n\n"
                                          f" 1 $ \\= 1 USDT" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup = keyboard)
        context.user_data['status'] = 'waiting binance screen shot'



        
    elif option.startswith('binconf:') :
        await query.edit_message_caption(caption = '⏳')
        amount , credit = option.split(':')[1:]
        amount = float(amount)
        credit = float(credit)

        conn = functions.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
                    INSERT INTO topup_requests (user_id, amount_sent, status, timestamp, topup_type , photo_file_id , credit_price)
                    VALUES (?, ? , 'في الانتظار', datetime('now') , 'Binance' , ? , ? )
                ''', (user_id, amount   , photo_files_ids[user_id] , credit))
        request_id = cursor.lastrowid
        conn.commit()
        conn.close()
        must_added = round(amount / credit , 2)
        keyboard = [
                [
                    InlineKeyboardButton("✅ تأكيد", callback_data=f"notappay:{user_id}:{must_added}:{request_id}"),
                    InlineKeyboardButton("❌ رفض", callback_data=f"notrejpay:{user_id}:{must_added}:{request_id}")
                ]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_photo(chat_id = '-1002489054350' , photo = photo_files_ids[user_id] , caption = f"طلب إيداع Binance : \n\n"
                                       f"رقم العملية : {request_id}\n"
                                       f"الرقم التعريفي : `{user_id}` \n"
                                       f"الاسم : {functions.escape_markdown_v2(query.from_user.first_name)} {functions.escape_markdown_v2(query.from_user.last_name if query.from_user.last_name else '')} \n"
                                       f"اسم المستخدم : @{functions.escape_markdown_v2(query.from_user.username if query.from_user.username else '')} \n"
                                       f"المبلغ المرسل : {functions.escape_markdown_v2(amount)} \n"
                                       f"سعر ال $ : {functions.escape_markdown_v2(credit)}"
                                       ,
                                       parse_mode= ParseMode.MARKDOWN_V2 ,
                                       reply_markup = reply_markup)

        await query.edit_message_caption(
                                            caption = f" {query.message.caption} \n\n"
                                             f"تم استلام طلبك يرجى الانتظار للتأكيد ⏳" 
                                             , reply_markup = None)
        

    
        

    elif option == 'الخدمات' : 
        await query.edit_message_text(text= 'اختر الخدمة : ',  reply_markup = keyboards.service_keyboard)
    
    elif option == 'Telegram' :
        
        lion_data = get_json('lion_bot.json')
        real_available = lion_data['available_countries']
        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]
        
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{lion_data['names'][code]} | {lion_data['prices'][code]} $" , callback_data = f"lion:{code}:{lion_data['prices'][code]}"))
            
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"الخدمات")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        conn = functions.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) FROM users WHERE id = ?',(user_id,))
        data = cursor.fetchone()
        balance = data[0]
        await query.edit_message_text(text = f'رصيدك : `{functions.escape_markdown_v2(balance)}` $\n\n'
                                      'اختر الدولة : ' , reply_markup = keyboard , parse_mode = ParseMode.MARKDOWN_V2)

    elif option.startswith('keyboard:') :
        key = option.split(':')[1]
        if key in general_lists :
            keyboard = InlineKeyboardMarkup(general_lists[key])
            await query.edit_message_text(text = 'اختر الدولة : ' , reply_markup = keyboard)
        else :
            await query.edit_message_text(text = 'تم تحديث البوت يرجى إعادة البدء من start' )


    
    elif option.startswith('lion:') :
        code , price = option.split(':')[1:]
        price = float(price)

        msg      = query.message
        orig_txt = msg.text or msg.caption
        orig_kb  = msg.reply_markup  

        await query.edit_message_text('جار شراء الرقم...⏳')

        lion_data = get_json('lion_bot.json')
        if price != lion_data['prices'][code] :
            await query.answer('تم تحديث الأسعار يرجى إعادة الطلب ' , show_alert = True)
            await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
            return

        conn = functions.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) , active_offers_id FROM users WHERE id = ?',(user_id,))
        data = cursor.fetchone()
        balance , active_offers  = data


        if price > balance :
            conn.close()
            await query.answer('ليس لديك رصيد كافي لإتمام العملية ❌' , show_alert = True)
            await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
            return
        
        new_balance = balance - price

        try :
            lion_data = get_json('lion_bot.json')
            api_token = lion_data['api_token']

            url = f'https://TG-Lion.net?action=getNumber&apiKey={api_token}&YourID={OWNER_ID}&country_code={code}'


            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        response = await response.json()  
            except aiohttp.ClientError as e:
                response = {'status' : False}
                print(f"An error occurred: {e}")
                

            if response['status'] == 'ok' :
                number = response['Number']
                cursor.execute('''INSERT INTO item_requests (user_id , app , country , number , status , timestamp , price , balance_before , balance_after , provider) 
                               VALUES (? , ? , ? , ? , ? , datetime('now') , ? , ? ,? , ?)
                               ''', (user_id , 'Telegram' , lion_data['names'][code] , number , 'مفعل' , price , balance , new_balance , 'Lion' ))
                
                request_id = cursor.lastrowid
                conn.commit()

                if active_offers :
                    active_offers += f":{request_id}"
                else :
                    active_offers = f"{request_id}"

                cursor.execute('UPDATE users SET balance = ROUND(?, 2) , active_offers_id = ? WHERE id = ?',(new_balance, active_offers, user_id))
                conn.commit()

                

                button = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('طلب الكود' , callback_data = f"lioncode:{request_id}")
                        ]
                    ]
                )

                try :
                    await context.bot.send_message(chat_id = '-1002537720561' , text = f"عملية شراء رقم {request_id} : \n\n"
                                                   f"الرقم : `{functions.escape_markdown_v2(number)}` \n"
                                                   f"الدولة : {functions.escape_markdown_v2(lion_data['names'][code])} \n"
                                                   f"السعر : {functions.escape_markdown_v2(price)}\n"
                                                   f"تطبيق تيليغرام \n\n"
                                                   f"المستخدم : `{user_id}`\n"
                                                   f"الاسم : {functions.escape_markdown_v2(name)}\n"
                                                   f"المعرف : @{functions.escape_markdown_v2(username)}" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup= functions.create_telegram_check_button(user_id))
                except Exception as e :
                    print(e)
                await query.edit_message_text(text='تم شراء العرض بنجاح : \n'
                                              f'رقم العملية : `{request_id}`\n'
                                              f"الرقم : `{functions.escape_markdown_v2(number)}`\n"
                                              f"الدولة : {functions.escape_markdown_v2(lion_data['names'][code])}\n"
                                              f"التطبيق : تيليغرام\n"
                                              f'يرجى النقر على الزر للحصول على كود التفعيل ✅' , reply_markup = button , parse_mode = ParseMode.MARKDOWN_V2)
                await query.answer('تم شراء العرض بنجاح ✅')

            else :
                if response['status'] == 'error' and response['message'] == 'Insufficient balance' :
                    await context.bot.send_message(chat_id = OWNER_ID , text = "انتهى رصيدك في بوت ليون ❌❌❌")
                
                print(response)
                await query.message.reply_text(text='لا يوجد أرقام في هذا السيرفر حاليا 💔' )
                await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
                await query.answer()
        except Exception as e :
            print('in lion buy   ' , e)
            await query.message.reply_text(text='لا يوجد أرقام في هذا السيرفر حاليا 💔' )
            
            await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
            await query.answer()

        conn.close()
    

    elif option.startswith('lioncode:') :
        request_id = option.split(':')[1]

        conn = functions.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT active_offers_id FROM users WHERE id = ?' , (user_id,))
        data = cursor.fetchone()
        active_offers = data[0]
        active_offers = active_offers.split(":")

        if request_id not in active_offers :
            conn.close()
            await query.answer('تم الانتهاء من هذا العرض ❌' , show_alert = True)
            return


        cursor.execute('SELECT number , country , timestamp , price FROM item_requests WHERE request_id = ?' , (request_id,))
        data = cursor.fetchone()
        number , country , date , price = data

        lion_data = get_json('lion_bot.json')
        api_token = lion_data['api_token']

        url = f'https://TG-Lion.net?action=getCode&number={number}&apiKey={api_token}&YourID={OWNER_ID}'

        try :
            

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response = await response.json()  
            

            if response['code']  :
                code = response['code']
                password = response['pass']
                await query.edit_message_text(text = f"*تم استلام الكود بنجاح* ☑️\n\n"
                                              f"*» الرقم :* `{functions.escape_markdown_v2(number)}`\n"
                                              f"*» الكود :* `{functions.escape_markdown_v2(code)}`\n"
                                              f"*» كلمة السر :* `{functions.escape_markdown_v2(password)}`\n\n"
                                               f"*إضغط على الكود للنسخ* 🌸" , parse_mode = ParseMode.MARKDOWN_V2)
                await query.answer()

                logged_out = await functions.logout_lion(number , api_token , OWNER_ID)
                if not logged_out :
                    await context.bot.send_message(chat_id = OWNER_ID , text = f"حدثت مشكلة أثناء تسجيل الخروج من الرقم : {number}")

                active_offers.remove(request_id)
                nactive = ''
                for i in range(len(active_offers)) :
                    n = active_offers[i]
                    if i == 0 :
                        nactive += f"{n}"
                    else :
                        nactive += f":{n}"

                if nactive == '' :
                    nactive = None
                cursor.execute('UPDATE users SET active_offers_id = ? , total_spent = ROUND(total_spent + ? , 2)  WHERE id = ?',(nactive , price ,user_id))
                conn.commit()

                cursor.execute('''UPDATE item_requests SET status = 'منتهية' , code = ? WHERE request_id = ? ''' , (code, request_id))
                conn.commit()

                try :
                    await context.bot.send_message(chat_id = '-1002689252952' , text = f"طلب كود لعملية الشراء رقم  {request_id} : \n\n"
                                                   f"الرقم : `{functions.escape_markdown_v2(number)}` \n"
                                                   f"الدولة : *{functions.escape_markdown_v2(country)}*\n"
                                                   f"السعر : *{functions.escape_markdown_v2(price)}*\n"
                                                   f"الكود : {functions.escape_markdown_v2(code)}\n"
                                                   f"كلمة السر : {functions.escape_markdown_v2(password)}\n"
                                                   f"تطبيق تيليغرام \n"
                                                   f"بوت lion\n\n"
                                                   f"المستخدم : `{user_id}`\n"
                                                   f"الاسم : {functions.escape_markdown_v2(name)}\n"
                                                   f"المعرف : @{functions.escape_markdown_v2(username)}" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup= functions.create_telegram_check_button(user_id))
                except Exception as e :
                    print(e)
                    
                try :
                    await context.bot.send_message(chat_id = '-1002297021090' , text = 
                                                   f"➖ رقم الطلب : ~~{request_id}~~ 🛎•\n"
                                                   f"➖ الدولة : *[{functions.escape_markdown_v2(country)}](http://t.me/Denji_sms_bot?start=ID3) * •\n"
                                                   f'➖ التطبيق : *{functions.escape_markdown_v2('تيليغرام')}* 🌐• \n'
                                                   f"➖ المالك : || *{functions.escape_markdown_v2('•••' + str(user_id)[3:])}* || 🆔\n"
                                                   f"➖ السعر : $ *{functions.escape_markdown_v2(price)}* 💸• \n"
                                                   f"➖ تاريخ الإنشاء : *{functions.escape_markdown_v2(date)}* • \n"
                                                   f"➖ *الحالة :  *تم التفعيل  ✅•\n"
                                                   f"➖ الرقم : *{functions.escape_markdown_v2(number[:-4] + '••••')}* \n"
                                                   f"➕ كود التفعيل : || {functions.escape_markdown_v2(code)} || 🧿•"
                                                    , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup= keyboards.contact_the_bot_button)
                except Exception as e :
                    print(e)

            else :
                button = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('طلب الكود' , callback_data = f"lioncode:{request_id}")
                        ]
                    ]
                )
                await query.answer('لم يصل الكود بعد ⏳ يرجى المحاولة بعد 60 ثانية')
                await query.edit_message_text(text=
                                              f'رقم العملية : `{request_id}`\n'
                                              f"الرقم : `{functions.escape_markdown_v2(number)}`\n"
                                              f"الدولة : *{functions.escape_markdown_v2(country)}*\n"
                                              f"التطبيق : *تيليغرام*\n"
                                              f'يرجى النقر على الزر للحصول على كود التفعيل ✅' , reply_markup = button , parse_mode = ParseMode.MARKDOWN_V2)

        except Exception as e :
            print('error getting code ' ,e)
            await query.answer('حدث خطأ ما يرجى إعادة طلب الكود ❌' , show_alert = True)

        conn.close()

    

    elif option.startswith('app:') :
        app = option.split(':')[1]
        data = get_json('apps.json')
        buttons = []
        prices = get_json('prices.json')

        for code in data[app] :
            country_counter = 1
            if code == "vn" :
                for id in data[app][code]['viotp'] :
                    price = prices[app][code]['viotp'][id]
                    button = InlineKeyboardButton(f"{data['names'][code]}{id} | {price} $" , callback_data = f"viotp:{app}:{id}:{price}")
                    buttons.append(button)
            else :
                for provider in data[app][code] :
                    if provider == 'drop_sms' :
                        for drop_id in data[app][code][provider]:
                            drop_data = get_json('dropsms.json')
                            name = drop_data['names'][drop_id]
                            price = prices[app][code][provider][drop_id]
                            button = InlineKeyboardButton(f"{name}{country_counter if country_counter != 1 else ''} | {price} $" , callback_data = f"dropsms:{app}:{drop_id}:{price}")
                            country_counter += 1
                            buttons.append(button)
                    elif provider == 'sms_live' :
                        for drop_id in data[app][code][provider]:
                            sms_live_data = get_json('smslive.json')
                            name = sms_live_data['names'][drop_id]
                            price = prices[app][code][provider][drop_id]
                            button = InlineKeyboardButton(f"{name}{country_counter if country_counter != 1 else ''} | {price} $" , callback_data = f"smslive:{app}:{drop_id}:{price}")
                            country_counter += 1
                            buttons.append(button)
                    
                    elif provider == 'duriancrs' :
                        for dur_country_code in data[app][code][provider]:
                            duriancrs_data = get_json('durancies.json')
                            name = duriancrs_data['names'][dur_country_code]
                            price = prices[app][code][provider][dur_country_code]
                            button = InlineKeyboardButton(f"{name}{country_counter if country_counter != 1 else ''} | {price} $" , callback_data = f"duranc:{app}:{dur_country_code}:{price}")
                            country_counter += 1
                            buttons.append(button)
        
        buttons = functions.split_list(buttons , 2)
        if len(buttons) > 48 :
            buttons = buttons[:49]
        
        buttons.append([InlineKeyboardButton('رجوع' , callback_data = 'الخدمات')])
        keyboard = InlineKeyboardMarkup(buttons)

        conn = functions.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) FROM users WHERE id = ?',(user_id,))
        data = cursor.fetchone()
        balance = data[0]
        await query.edit_message_text(text=f'رصيدك : `{functions.escape_markdown_v2(balance)}` $\n\n'
                                      'اختر الدولة : ' , reply_markup = keyboard , parse_mode = ParseMode.MARKDOWN_V2)
    
    elif option.startswith('viotp:') :
        app , id , price = option.split(':')[1:]
        price = float(price)

        msg      = query.message
        orig_txt = msg.text or msg.caption
        orig_kb  = msg.reply_markup  

        await query.edit_message_text('جار شراء الرقم...⏳')
        

        prices = get_json('prices.json')
        if price != prices[app]['vn']['viotp'][id] :
            await query.answer('تم تحديث الأسعار يرجى إعادة الطلب ' , show_alert = True)
            await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
            return

        conn = functions.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) , active_offers_id FROM users WHERE id = ?',(user_id,))
        data = cursor.fetchone()
        balance , active_offers  = data

        
        if price > balance :
            conn.close()
            await query.answer('ليس لديك رصيد كافي لإتمام العملية ❌' , show_alert = True)
            await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
            return
        
        new_balance = balance - price

        apps_data = get_json('apps.json')

        try :
            viotp_data = get_json('viotp.json')
            api_token = viotp_data['api_token']
            service_id = viotp_data['appsid'][app]
            network = viotp_data['providers'][id]


            url = f'https://api.viotp.com/request/getv2?token={api_token}&serviceId={service_id}&network={network}'

            

            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response = await response.json()  
            

            if response['success'] :
                number = response['data']['phone_number']
                country_code = response['data']['countryCode']
                number = '+' + country_code + number

                viotp_id = response['data']['request_id']

                cursor.execute('''INSERT INTO item_requests (user_id , app , country , number , status , timestamp , price , balance_before , balance_after , provider , server , auto_id , end_time) 
                               VALUES (? , ? , ? , ? , ? , datetime('now') , ? , ? ,? , ? , ? , ? , DATETIME('now', '+5 minutes'))
                               ''', (user_id , app , apps_data['names']['vn'] , number , 'مفعل' , price , balance , new_balance , 'viotp' , network , viotp_id))
                
                request_id = cursor.lastrowid
                conn.commit()

                if active_offers :
                    active_offers += f":{request_id}"
                else :
                    active_offers = f"{request_id}"

                cursor.execute('UPDATE users SET balance = ROUND(?, 2) , active_offers_id = ? WHERE id = ?',(new_balance, active_offers, user_id))
                conn.commit()

                


                if app == 'Whatsapp' :
                    button = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('تغيير الرقم' , callback_data = f"viotp:{app}:{id}:{price}")
                            ],
                            [
                                InlineKeyboardButton('طلب الكود' , callback_data = f"viotpcode:{request_id}")
                            ],
                            [
                                InlineKeyboardButton('التحقق من الرقم في واتساب' , url = f'http://wa.me/{number}')
                            ]
                        ]
                    )
                else :
                    button = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('تغيير الرقم' , callback_data = f"viotp:{app}:{id}:{price}")
                            ],
                            [
                                InlineKeyboardButton('طلب الكود' , callback_data = f"viotpcode:{request_id}")
                            ]
                        ]
                    )

                d = get_json('side.json')
                d['pending'].append(request_id)
                update_json('side.json' , d)

                try :
                    
                    await context.bot.send_message(chat_id = '-1002537720561' , text = f"عملية شراء رقم {request_id} : \n\n"
                                                   f"الرقم : `{functions.escape_markdown_v2(number)}` \n"
                                                   f"الدولة : *{functions.escape_markdown_v2(apps_data['names']['vn'])}* \n"
                                                   f"السعر : {functions.escape_markdown_v2(price)} $\n"
                                                   f"تطبيق *{app}* \n"
                                                   
                                                   f"Viotp \n\n"
                                                   f"المستخدم : `{user_id}`\n"
                                                   f"الاسم : {functions.escape_markdown_v2(name)}\n"
                                                   f"المعرف : @{functions.escape_markdown_v2(username)}" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup= functions.create_telegram_check_button(user_id))
                except Exception as e :
                    print(e)
                
                await query.edit_message_text(text='تم شراء العرض بنجاح : \n'
                                              f'رقم العملية : `{request_id} `\n'
                                              f"الرقم : `{functions.escape_markdown_v2(number)}`\n"
                                              f"الدولة : *{functions.escape_markdown_v2(apps_data['names']['vn'])}*\n"
                                              f"التطبيق : *{functions.escape_markdown_v2(app)}*\n"
                                              
                                              f"الوقت المتبقي لإلغاء العملية : 5:00\n"
                                              f'يرجى النقر على الزر للحصول على كود التفعيل ✅' , reply_markup = button , parse_mode = ParseMode.MARKDOWN_V2)
                await query.answer('تم شراء العرض بنجاح ✅')

            else :
                await query.message.reply_text(text='لا يوجد أرقام في هذا السيرفر حاليا 💔' )
                await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
                await query.answer()
                try :
                    if response['status_code'] == -2 :
                        await context.bot.send_message(chat_id = OWNER_ID , text = "انتهى رصيدك في viotp ❌❌❌")
                except :
                    None
                
        except Exception as e :
            print('in viotp buy   ' , e)
            await query.message.reply_text(text='لا يوجد أرقام في هذا السيرفر حاليا 💔' )
            await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
            await query.answer()

        conn.close()
    

    elif option.startswith('viotpcode:') :
        request_id = option.split(':')[1]

        conn = functions.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT active_offers_id FROM users WHERE id = ?' , (user_id,))
        data = cursor.fetchone()
        active_offers = data[0]
        if active_offers :
            active_offers = active_offers.split(":")
        else :
            active_offers = []

        if request_id not in active_offers :
            conn.close()
            await query.answer('تم الانتهاء من هذا العرض ❌' , show_alert = True)
            return
        

        cursor.execute('''SELECT app, number, code , status , country , server , price , (STRFTIME('%s', end_time) - STRFTIME('%s', 'now')) , timestamp FROM item_requests WHERE request_id = ?''' , (request_id,))
        data = cursor.fetchone()
        app , number , code , status , country , network , price , rest_seconds , date = data
        

        if code  :
            await query.edit_message_text(text = f"*تم استلام الكود بنجاح* ☑️\n\n"
                                              f"*» الرقم :* `{functions.escape_markdown_v2(number)}`\n"
                                              f"*» الكود :* `{functions.escape_markdown_v2(code)}`\n\n"
                                              
                                               f"*إضغط على الكود للنسخ* 🌸\n"
                                                f"{"[تعليمات لسلامة رقمك](http://telegra.ph/%D8%AA%D8%B9%D9%84%D9%8A%D9%85%D8%A7%D8%AA-%D9%84%D8%B3%D9%84%D8%A7%D9%85%D8%A9-%D8%B1%D9%82%D9%85%D9%83-05-06)" if app == 'Whatsapp' else ''}" , parse_mode = ParseMode.MARKDOWN_V2)
            await query.answer()

            active_offers.remove(request_id)
            nactive = ''
            for i in range(len(active_offers)) :
                n = active_offers[i]
                if i == 0 :
                    nactive += f"{n}"
                else :
                    nactive += f":{n}"
            
            if nactive == '' :
                nactive = None
            cursor.execute('UPDATE users SET active_offers_id = ?  WHERE id = ?',(nactive ,user_id))
            conn.commit()

            cursor.execute('''UPDATE item_requests SET status = 'منتهية'  WHERE request_id = ? ''' , ( request_id,))
            conn.commit()

            viotp_data = get_json('viotp.json')
            network_id = 0
            for id in viotp_data['providers'] :
                if viotp_data['providers'][id] == network :
                    network_id = id

            try :
                await context.bot.send_message(chat_id = '-1002689252952' , text = f"طلب كود لعملية الشراء رقم  {request_id} : \n\n"
                                               f"الرقم : `{functions.escape_markdown_v2(number)}` \n"
                                               f"الدولة : *{functions.escape_markdown_v2(country)}* \n"
                                                f"السعر : *{functions.escape_markdown_v2(price)}*\n"
                                               f"الكود : `{functions.escape_markdown_v2(code)}`\n"
                                               f"تطبيق *{app}* \n"
                                               f"Viotp \n\n"
                                               f"المستخدم : `{user_id}`\n"
                                               f"الاسم : {functions.escape_markdown_v2(name)}\n"
                                               f"المعرف : @{functions.escape_markdown_v2(username)}" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup= functions.create_telegram_check_button(user_id))
            except Exception as e :
                print(e)
            
            try :
                await context.bot.send_message(chat_id = '-1002297021090' , text = 
                                                   f"➖ رقم الطلب : ~~{request_id}~~ 🛎•\n"
                                                   f"➖ الدولة : *[{functions.escape_markdown_v2(country)}](http://t.me/Denji_sms_bot?start=ID3)  {network_id}* •\n"
                                                   f'➖ التطبيق : *{functions.escape_markdown_v2(app)}* 🌐• \n'
                                                   f"➖ المالك : || *{functions.escape_markdown_v2('•••' + str(user_id)[3:])}* || 🆔\n"
                                                   f"➖ السعر : $ *{functions.escape_markdown_v2(price)}* 💸• \n"
                                                   f"➖ تاريخ الإنشاء : *{functions.escape_markdown_v2(date)}* • \n"
                                                   f"➖ *الحالة :  *تم التفعيل  ✅•\n"
                                                   f"➖ الرقم : *{functions.escape_markdown_v2(number[:-4] + '••••')}* \n"
                                                   f"➕ كود التفعيل : || {functions.escape_markdown_v2(code)} || 🧿•"
                                                    , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup= keyboards.contact_the_bot_button)
            except Exception as e :
                print(e)
        elif status == 'ملغية' :
            await query.edit_message_text(text = "هذه العملية ملغية و تم إرجاع الرصيد ❌")
            await query.answer()
        
        else :
            if app == 'Whatsapp' :
                viotp_data = get_json('viotp.json')
                for code in viotp_data['providers'] :
                    if viotp_data['providers'][code] == network :
                        id = code
                        break
                
                button = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('تغيير الرقم' , callback_data = f"viotp:{app}:{id}:{price}")
                            ],
                            [
                                InlineKeyboardButton('طلب الكود' , callback_data = f"viotpcode:{request_id}")
                            ],
                            [
                                InlineKeyboardButton('التحقق من الرقم في واتساب' , url = f'http://wa.me/{number}')
                            ]
                        ]
                    )
            else :
                viotp_data = get_json('viotp.json')
                for code in viotp_data['providers'] :
                    if viotp_data['providers'][code] == network :
                        id = code
                        break
                button = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('تغيير الرقم' , callback_data = f"viotp:{app}:{id}:{price}")
                            ],
                            [
                                InlineKeyboardButton('طلب الكود' , callback_data = f"viotpcode:{request_id}")
                            ]
                        ]
                    )
            await query.answer('لم يصل الكود بعد ⏳ يرجى المحاولة بعد 60 ثانية')

            time_left = ''
            rest_seconds += 25
            if rest_seconds > 0 :
                rest_minutes = rest_seconds // 60
                rest_seconds = rest_seconds % 60
                if rest_seconds < 10 :
                    rest_seconds = f"0{rest_seconds}"
                time_left = f'{rest_minutes}:{rest_seconds}'
            
            try :
                await query.edit_message_text(text=
                                                f'رقم العملية : `{request_id} `\n'
                                                f"الرقم : `{functions.escape_markdown_v2(number)}`\n"
                                                f"الدولة : *{functions.escape_markdown_v2(country)}*\n"
                                                f"التطبيق : *{functions.escape_markdown_v2(app)}*\n"
                                                
                                                f"الوقت المتبقي لإلغاء العملية : {functions.escape_markdown_v2(time_left)}\n"
                                                f'يرجى النقر على الزر للحصول على كود التفعيل ✅' , reply_markup = button , parse_mode = ParseMode.MARKDOWN_V2)
            except Exception as e :
                print(e)

        conn.close()

    
    elif option == 'العرض المفعل' :
        conn = functions.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT active_offers_id FROM users WHERE id = ?', (user_id,))
        data = cursor.fetchone()
        active_offers = data[0]
        if not active_offers :
            conn.close()
            await query.answer('ليس لديك عملية شراء مفعلة على حسابك ❌' , show_alert = True)
            return
        
        active_offers = active_offers.split(':')
        print(active_offers)
        buttons = []
        for request_id in active_offers :
            cursor.execute('SELECT provider , number FROM item_requests WHERE request_id = ?',(request_id,))
            data = cursor.fetchone()
            if data :
                provider , number = data
            else :
                continue

            if provider == 'Lion' :
                button = [
                                InlineKeyboardButton(number , callback_data = f"lioncode:{request_id}")
                            ]
                        
            elif provider == 'viotp' :
                button = [
                                InlineKeyboardButton(number , callback_data = f"viotpcode:{request_id}")
                            ]
            
            elif provider == 'drop_sms' : 
                button = [
                                InlineKeyboardButton(number , callback_data = f"dropsmscode:{request_id}")
                            ]
            elif provider == 'sms_live' : 
                button = [
                                InlineKeyboardButton(number , callback_data = f"smslivecode:{request_id}")
                            ]
            
            elif provider == 'duriancrs' : 
                button = [
                                InlineKeyboardButton(number , callback_data = f"duranccode:{request_id}")
                            ]
            
            
            buttons.append(button)
        
        keyboard = InlineKeyboardMarkup(buttons)
                        
        await query.edit_message_text(text=f"العروض المفعلة لديك : \n\n"
                                      f"يرجى اختيار العرض للحصول على الكود :" , reply_markup = keyboard )
        
    


    # drop sms 


    elif option.startswith('dropsms:') : 
        app , id , price = option.split(':')[1:]
        price = float(price)

        msg      = query.message
        orig_txt = msg.text or msg.caption
        orig_kb  = msg.reply_markup  

        await query.edit_message_text('جار شراء الرقم...⏳')
        

        drop_sms_data = get_json('dropsms.json')
        country_code = drop_sms_data['country_codes'][id]
        prices = get_json('prices.json')
        if price != prices[app][country_code]['drop_sms'][id] :
            await query.answer('تم تحديث الأسعار يرجى إعادة الطلب ' , show_alert = True)
            await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
            return

        conn = functions.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) , active_offers_id FROM users WHERE id = ?',(user_id,))
        data = cursor.fetchone()
        balance , active_offers  = data

        
        if price > balance :
            conn.close()
            await query.answer('ليس لديك رصيد كافي لإتمام العملية ❌' , show_alert = True)
            await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
            return
        
        new_balance = balance - price

        apps_data = get_json('apps.json')

        try :
            
            api_token = drop_sms_data['api_token']
            app_code = drop_sms_data['services_ids'][app]


            url = f'https://api.dropsms.cc/stubs/handler_api.php?action=getNumber&api_key={api_token}&service={app_code}&country={id}'


            

            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response = await response.text()  
            

            if response.startswith('ACCESS_NUMBER') :
                auto_id , number = response.split(':')[1:]
                number = '+' + number

                

                cursor.execute('''INSERT INTO item_requests (user_id , app , country , number , status , timestamp , price , balance_before , balance_after , provider  , auto_id , end_time) 
                               VALUES (? , ? , ? , ? , ? , datetime('now') , ? , ? ,? , ? , ? , DATETIME('now', '+10 minutes'))
                               ''', (user_id , app , drop_sms_data['names'][id] , number , 'مفعل' , price , balance , new_balance , 'drop_sms' , auto_id))
                
                request_id = cursor.lastrowid
                conn.commit()

                if active_offers :
                    active_offers += f":{request_id}"
                else :
                    active_offers = f"{request_id}"

                cursor.execute('UPDATE users SET balance = ROUND(?, 2) , active_offers_id = ? WHERE id = ?',(new_balance, active_offers, user_id))
                conn.commit()

                


                
                if app == 'Whatsapp' :
                    button = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('تغيير الرقم' , callback_data = f"dropsms:{app}:{id}:{price}")
                            ],
                            [
                                InlineKeyboardButton('طلب الكود' , callback_data = f"dropsmscode:{request_id}")
                            ],
                            [
                                InlineKeyboardButton('التحقق من الرقم في واتساب' , url = f'http://wa.me/{number}')
                            ]
                        ]
                    )
                else :
                    button = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('تغيير الرقم' , callback_data = f"dropsms:{app}:{id}:{price}")
                            ],
                            [
                                InlineKeyboardButton('طلب الكود' , callback_data = f"dropsmscode:{request_id}")
                            ]
                        ]
                    )
                d = get_json('side.json')
                d['pending'].append(request_id)
                update_json('side.json' , d)

                try :
                    await context.bot.send_message(chat_id = '-1002537720561' , text = f"عملية شراء رقم {request_id} : \n\n"
                                                   f"الرقم : `{functions.escape_markdown_v2(number)}` \n"
                                                   f"الدولة : *{functions.escape_markdown_v2(drop_sms_data['names'][id])}* \n"
                                                   f"السعر : {functions.escape_markdown_v2(price)} $\n"
                                                   f"تطبيق *{app}* \n"
                                                   f"drop sms \n\n"
                                                   f"المستخدم : `{user_id}`\n"
                                                   f"الاسم : {functions.escape_markdown_v2(name)}\n"
                                                   f"المعرف : @{functions.escape_markdown_v2(username)}" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup= functions.create_telegram_check_button(user_id))
                except Exception as e :
                    print(e)
                
                
                await query.edit_message_text(text='تم شراء العرض بنجاح : \n'
                                              f'رقم العملية : `{request_id} `\n'
                                              f"الرقم : `{functions.escape_markdown_v2(number)}`\n"
                                              f"الدولة : *{functions.escape_markdown_v2(drop_sms_data['names'][id])}*\n"
                                              f"التطبيق : *{functions.escape_markdown_v2(app)}*\n"
                                              
                                              f"الوقت المتبقي لإلغاء العملية : 10:00\n"
                                              f'يرجى النقر على الزر للحصول على كود التفعيل ✅' , reply_markup = button , parse_mode = ParseMode.MARKDOWN_V2)
                await query.answer('تم شراء العرض بنجاح ✅')

            else :
                await query.message.reply_text(text='لا يوجد أرقام في هذا السيرفر حاليا 💔' )
                await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
                await query.answer()
                try :
                    response = responsem.json()
                    if response['detail'] == 'NO_BALANCE' :
                        await context.bot.send_message(chat_id = OWNER_ID , text = "انتهى رصيدك في drop_sms ❌❌❌")
                except :
                    None
                
        except Exception as e :
            print('in drop sms buy   ' , e)
            await query.message.reply_text(text='لا يوجد أرقام في هذا السيرفر حاليا 💔' )
            await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
            await query.answer()

        conn.close()

    
    elif option.startswith('dropsmscode:') :
        request_id = option.split(':')[1]

        conn = functions.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT active_offers_id FROM users WHERE id = ?' , (user_id,))
        data = cursor.fetchone()
        active_offers = data[0]
        if active_offers :
            active_offers = active_offers.split(":")
        else :
            active_offers = []

        if request_id not in active_offers :
            conn.close()
            await query.answer('تم الانتهاء من هذا العرض ❌' , show_alert = True)
            return
        

        cursor.execute('''SELECT app, number, code , status , country , auto_id , (STRFTIME('%s', end_time) - STRFTIME('%s', 'now')) , timestamp , price FROM item_requests WHERE request_id = ?''' , (request_id,))
        data = cursor.fetchone()
        app , number , code , status , country , auto_id , rest_seconds , date , price = data
        

        if code  :
            await query.edit_message_text(text = f"*تم استلام الكود بنجاح* ☑️\n\n"
                                              f"*» الرقم :* `{functions.escape_markdown_v2(number)}`\n"
                                              f"*» الكود :* `{functions.escape_markdown_v2(code)}`\n\n"
                                              
                                               f"*إضغط على الكود للنسخ* 🌸\n"
                                                f"{"[تعليمات لسلامة رقمك](http://telegra.ph/%D8%AA%D8%B9%D9%84%D9%8A%D9%85%D8%A7%D8%AA-%D9%84%D8%B3%D9%84%D8%A7%D9%85%D8%A9-%D8%B1%D9%82%D9%85%D9%83-05-06)" if app == 'Whatsapp' else ''}" , parse_mode = ParseMode.MARKDOWN_V2)
            await query.answer()

            active_offers.remove(request_id)
            nactive = ''
            for i in range(len(active_offers)) :
                n = active_offers[i]
                if i == 0 :
                    nactive += f"{n}"
                else :
                    nactive += f":{n}"
            
            if nactive == '' :
                nactive = None
            cursor.execute('UPDATE users SET active_offers_id = ?  WHERE id = ?',(nactive ,user_id))
            conn.commit()

            cursor.execute('''UPDATE item_requests SET status = 'منتهية'  WHERE request_id = ? ''' , ( request_id,))
            conn.commit()

            try :
                await context.bot.send_message(chat_id = '-1002689252952' , text = f"طلب كود لعملية الشراء رقم  {request_id} : \n\n"
                                               f"الرقم : `{functions.escape_markdown_v2(number)}` \n"
                                               f"الدولة : *{functions.escape_markdown_v2(country)}*\n"
                                                f"السعر : *{functions.escape_markdown_v2(price)}*\n"
                                               f"الكود : `{functions.escape_markdown_v2(code)}`\n"
                                               f"تطبيق *{app}* \n"
                                               f"drop sms \n\n"
                                               f"المستخدم : `{user_id}`\n"
                                               f"الاسم : {functions.escape_markdown_v2(name)}\n"
                                               f"المعرف : @{functions.escape_markdown_v2(username)}" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup= functions.create_telegram_check_button(user_id))
            except Exception as e :
                print(e)
            
            try :
                await context.bot.send_message(chat_id = '-1002297021090' , text = 
                                                   f"➖ رقم الطلب : ~~{request_id}~~ 🛎•\n"
                                                   f"➖ الدولة : *[{functions.escape_markdown_v2(country)}](http://t.me/Denji_sms_bot?start=ID3) * •\n"
                                                   f'➖ التطبيق : *{functions.escape_markdown_v2(app)}* 🌐• \n'
                                                   f"➖ المالك : || *{functions.escape_markdown_v2('•••' + str(user_id)[3:])}* || 🆔\n"
                                                   f"➖ السعر : $ *{functions.escape_markdown_v2(price)}* 💸• \n"
                                                   f"➖ تاريخ الإنشاء : *{functions.escape_markdown_v2(date)}* • \n"
                                                   f"➖ *الحالة :  *تم التفعيل  ✅•\n"
                                                   f"➖ الرقم : *{functions.escape_markdown_v2(number[:-4] + '••••')}* \n"
                                                   f"➕ كود التفعيل : || {functions.escape_markdown_v2(code)} || 🧿•"
                                                    , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup= keyboards.contact_the_bot_button)
            except Exception as e :
                print(e)
        elif status == 'ملغية' :
            await query.edit_message_text(text = "هذه العملية ملغية و تم إرجاع الرصيد ❌")
            await query.answer()
        
        else :
            drop_data = get_json('dropsms.json')
            for code in drop_data['names'] :
                if country == drop_data['names'][code] :
                    id = code 
                    break
            if app == 'Whatsapp' :
                button = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('تغيير الرقم' , callback_data = f"dropsms:{app}:{id}:{price}")
                        ],
                        [
                            InlineKeyboardButton('طلب الكود' , callback_data = f"dropsmscode:{request_id}")
                        ],
                        [
                            InlineKeyboardButton('التحقق من الرقم في واتساب' , url = f'http://wa.me/{number}')
                        ]
                    ]
                )
            else :
                button = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('تغيير الرقم' , callback_data = f"dropsms:{app}:{id}:{price}")
                            ],
                            [
                                InlineKeyboardButton('طلب الكود' , callback_data = f"dropsmscode:{request_id}")
                            ]
                        ]
                    )
            await query.answer('لم يصل الكود بعد ⏳ يرجى المحاولة بعد 60 ثانية')

            time_left = ''
            rest_seconds += 25
            if rest_seconds > 0 :
                rest_minutes = rest_seconds // 60
                rest_seconds = rest_seconds % 60
                if rest_seconds < 10 :
                    rest_seconds = f"0{rest_seconds}"
                time_left = f'{rest_minutes}:{rest_seconds}'

            try :
                await query.edit_message_text(text=
                                                f'رقم العملية : `{request_id} `\n'
                                                f"الرقم : `{functions.escape_markdown_v2(number)}`\n"
                                                f"الدولة : *{functions.escape_markdown_v2(country)}*\n"
                                                f"التطبيق : *{functions.escape_markdown_v2(app)}*\n"
                                                
                                                f"الوقت المتبقي لإلغاء العملية : {functions.escape_markdown_v2(time_left)}\n"
                                                f'يرجى النقر على الزر للحصول على كود التفعيل ✅' , reply_markup = button , parse_mode = ParseMode.MARKDOWN_V2)
            except Exception as e :
                print(e)
        conn.close()

    




    # sms live


    elif option.startswith('smslive:') :

        app , id , price = option.split(':')[1:]
        price = float(price)


        msg      = query.message
        orig_txt = msg.text or msg.caption
        orig_kb  = msg.reply_markup  

        await query.edit_message_text('جار شراء الرقم...⏳')
        

        sms_live_data = get_json('smslive.json')
        country_code = sms_live_data['country_codes'][id]
        prices = get_json('prices.json')
        if price != prices[app][country_code]['sms_live'][id] :
            await query.answer('تم تحديث الأسعار يرجى إعادة الطلب ' , show_alert = True)
            await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
            return

        conn = functions.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) , active_offers_id FROM users WHERE id = ?',(user_id,))
        data = cursor.fetchone()
        balance , active_offers  = data

        
        if price > balance :
            conn.close()
            await query.answer('ليس لديك رصيد كافي لإتمام العملية ❌' , show_alert = True)
            await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
            return
        
        new_balance = balance - price

        apps_data = get_json('apps.json')

        try :
            
            api_token = sms_live_data['api_token']
            app_code = sms_live_data['services_ids'][app]


            
            url = f'https://api.smslive.pro/stubs/handler_api.php?api_key={api_token}&action=getNumber&service={app_code}&country={id}'


            

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response = await response.text() 

            print(response)


            if response.startswith('ACCESS_NUMBER') :
                auto_id , number = response.split(':')[1:]
                number = '+' + number

                
                cursor.execute('''INSERT INTO item_requests (user_id , app , country , number , status , timestamp , price , balance_before , balance_after , provider  , auto_id , end_time) 
                               VALUES (? , ? , ? , ? , ? , datetime('now') , ? , ? ,? , ? , ? , DATETIME('now', '+25 minutes'))
                               ''', (user_id , app , sms_live_data['names'][id] , number , 'مفعل' , price , balance , new_balance , 'sms_live' , auto_id))
                
                request_id = cursor.lastrowid
                conn.commit()

                if active_offers :
                    active_offers += f":{request_id}"
                else :
                    active_offers = f"{request_id}"

                cursor.execute('UPDATE users SET balance = ROUND(?, 2) , active_offers_id = ? WHERE id = ?',(new_balance, active_offers, user_id))
                conn.commit()

                


                
                if app == 'Whatsapp' :
                    button = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('تغيير الرقم' , callback_data = f"smslive:{app}:{id}:{price}")
                            ],
                            [
                                InlineKeyboardButton('طلب الكود' , callback_data = f"smslivecode:{request_id}")
                            ],
                            [
                                InlineKeyboardButton('التحقق من الرقم في واتساب' , url = f'http://wa.me/{number}')
                            ],
                            [
                                InlineKeyboardButton('إلغاء الرقم ❌' , callback_data = f'smslivecancelnumber:{request_id}')
                            ]
                        ]
                    )
                else :
                    button = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('تغيير الرقم' , callback_data = f"smslive:{app}:{id}:{price}")
                            ],
                            [
                                InlineKeyboardButton('طلب الكود' , callback_data = f"smslivecode:{request_id}")
                            ],
                            [
                                InlineKeyboardButton('إلغاء الرقم ❌' , url = f'smslivecancelnumber:{request_id}')
                            ]
                        ]
                    )
                d = get_json('side.json')
                d['pending'].append(request_id)
                update_json('side.json' , d)

                try :
                    await context.bot.send_message(chat_id = '-1002537720561' , text = f"عملية شراء رقم {request_id} : \n\n"
                                                   f"الرقم : `{functions.escape_markdown_v2(number)}` \n"
                                                   f"الدولة : *{functions.escape_markdown_v2(sms_live_data['names'][id])}* \n"
                                                   f"السعر : {functions.escape_markdown_v2(price)} $\n"
                                                   f"تطبيق *{app}* \n"
                                                   f"sms live \n\n"
                                                   f"المستخدم : `{user_id}`\n"
                                                   f"الاسم : {functions.escape_markdown_v2(name)}\n"
                                                   f"المعرف : @{functions.escape_markdown_v2(username)}" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup= functions.create_telegram_check_button(user_id))
                except Exception as e :
                    print(e)
                
                
                await query.edit_message_text(text='تم شراء العرض بنجاح : \n'
                                              f'رقم العملية : `{request_id} `\n'
                                              f"الرقم : `{functions.escape_markdown_v2(number)}`\n"
                                              f"الدولة : *{functions.escape_markdown_v2(sms_live_data['names'][id])}*\n"
                                              f"التطبيق : *{functions.escape_markdown_v2(app)}*\n"
                                              
                                              f"الوقت المتبقي لإلغاء العملية : 25:00\n"
                                              f'يرجى النقر على الزر للحصول على كود التفعيل ✅' , reply_markup = button , parse_mode = ParseMode.MARKDOWN_V2)
                await query.answer('تم شراء العرض بنجاح ✅')

            else :
                await query.message.reply_text(text='لا يوجد أرقام في هذا السيرفر حاليا 💔' )
                await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
                await query.answer()
                try :
                    response2 = response.json()
                    if response2['detail'] == 'NO_BALANCE' :
                        await context.bot.send_message(chat_id = OWNER_ID , text = "انتهى رصيدك في sms_live ❌❌❌")
                except :
                    try :
                        if response == 'NO_BALANCE' :
                            await context.bot.send_message(chat_id = OWNER_ID , text = "انتهى رصيدك في sms_live ❌❌❌")
                    except :
                        None
                
        except Exception as e :
            print('in sms live buy   ' , e)
            await query.message.reply_text(text='لا يوجد أرقام في هذا السيرفر حاليا 💔' )
            await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
            await query.answer()

        conn.close()

    
    elif option.startswith('smslivecode:') :
        request_id = option.split(':')[1]

        conn = functions.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT active_offers_id FROM users WHERE id = ?' , (user_id,))
        data = cursor.fetchone()
        active_offers = data[0]
        if active_offers :
            active_offers = active_offers.split(":")
        else :
            active_offers = []

        if request_id not in active_offers :
            conn.close()
            await query.answer('تم الانتهاء من هذا العرض ❌' , show_alert = True)
            return
        

        cursor.execute('''SELECT app, number, code , status , country , auto_id , price , (STRFTIME('%s', end_time) - STRFTIME('%s', 'now')) , timestamp FROM item_requests WHERE request_id = ?''' , (request_id,))
        data = cursor.fetchone()
        app , number , code , status , country , auto_id , price , rest_seconds , date = data
        

        if code  :
            await query.edit_message_text(text = f"*تم استلام الكود بنجاح* ☑️\n\n"
                                              f"*» الرقم :* `{functions.escape_markdown_v2(number)}`\n"
                                              f"*» الكود :* `{functions.escape_markdown_v2(code)}`\n\n"
                                              
                                               f"*إضغط على الكود للنسخ* 🌸\n"
                                                f"{"[تعليمات لسلامة رقمك](http://telegra.ph/%D8%AA%D8%B9%D9%84%D9%8A%D9%85%D8%A7%D8%AA-%D9%84%D8%B3%D9%84%D8%A7%D9%85%D8%A9-%D8%B1%D9%82%D9%85%D9%83-05-06)" if app == 'Whatsapp' else ''}" , parse_mode = ParseMode.MARKDOWN_V2)
            await query.answer()

            active_offers.remove(request_id)
            nactive = ''
            for i in range(len(active_offers)) :
                n = active_offers[i]
                if i == 0 :
                    nactive += f"{n}"
                else :
                    nactive += f":{n}"
            
            if nactive == '' :
                nactive = None
            cursor.execute('UPDATE users SET active_offers_id = ?  WHERE id = ?',(nactive ,user_id))
            conn.commit()

            cursor.execute('''UPDATE item_requests SET status = 'منتهية'  WHERE request_id = ? ''' , ( request_id,))
            conn.commit()

            apps_data = get_json('apps.json')
            sms_live_data = get_json('smslive.json')
            sms_country_id = -1
            for id in sms_live_data['names'] :
                if sms_live_data['names'][id] == country :
                    sms_country_id = id
            country_code = sms_live_data['country_codes'][sms_country_id]
            server_number = ''
            if len(apps_data[app][country_code]['drop_sms']) > 0 :
                server_number = 2

            try :
                await context.bot.send_message(chat_id = '-1002689252952' , text = f"طلب كود لعملية الشراء رقم  {request_id} : \n\n"
                                               f"الرقم : `{functions.escape_markdown_v2(number)}` \n"
                                               f"الدولة : *{functions.escape_markdown_v2(country)}*\n"
                                                f"السعر : *{functions.escape_markdown_v2(price)}*\n"
                                               f"الكود : `{functions.escape_markdown_v2(code)}`\n"
                                               f"تطبيق *{app}* \n"
                                               f"sms live \n\n"
                                               f"المستخدم : `{user_id}`\n"
                                               f"الاسم : {functions.escape_markdown_v2(name)}\n"
                                               f"المعرف : @{functions.escape_markdown_v2(username)}" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup= functions.create_telegram_check_button(user_id))
            except Exception as e :
                print(e)
            try :
                await context.bot.send_message(chat_id = '-1002297021090' , text = 
                                                   f"➖ رقم الطلب : ~~{request_id}~~ 🛎•\n"
                                                   f"➖ الدولة : *[{functions.escape_markdown_v2(country)}](http://t.me/Denji_sms_bot?start=ID3)  {server_number}* •\n"
                                                   f'➖ التطبيق : *{functions.escape_markdown_v2(app)}* 🌐• \n'
                                                   f"➖ المالك : || *{functions.escape_markdown_v2('•••' + str(user_id)[3:])}* || 🆔\n"
                                                   f"➖ السعر : $ *{functions.escape_markdown_v2(price)}* 💸• \n"
                                                   f"➖ تاريخ الإنشاء : *{functions.escape_markdown_v2(date)}* • \n"
                                                   f"➖ *الحالة :  *تم التفعيل  ✅•\n"
                                                   f"➖ الرقم : *{functions.escape_markdown_v2(number[:-4] + '••••')}* \n"
                                                   f"➕ كود التفعيل : || {functions.escape_markdown_v2(code)} || 🧿•"
                                                    , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup= keyboards.contact_the_bot_button)
            except Exception as e :
                print(e)
        elif status == 'ملغية' :
            await query.edit_message_text(text = "هذه العملية ملغية و تم إرجاع الرصيد ❌")
            await query.answer()
        
        else :
            sms_live_data = get_json('smslive.json')
            for code in sms_live_data['names'] :
                if country == sms_live_data['names'][code] :
                    id = code 
                    break
            if app == 'Whatsapp' :
                button = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('تغيير الرقم' , callback_data = f"smslive:{app}:{id}:{price}")
                        ],
                        [
                            InlineKeyboardButton('طلب الكود' , callback_data = f"smslivecode:{request_id}")
                        ],
                        [
                            InlineKeyboardButton('التحقق من الرقم في واتساب' , url = f'http://wa.me/{number}')
                        ],
                        [
                            InlineKeyboardButton('إلغاء الرقم ❌' , callback_data = f'smslivecancelnumber:{request_id}')
                        ]
                    ]
                )
            else :
                button = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('تغيير الرقم' , callback_data = f"smslive:{app}:{id}:{price}")
                            ],
                            [
                                InlineKeyboardButton('طلب الكود' , callback_data = f"smslivecode:{request_id}")
                            ],
                            [
                                InlineKeyboardButton('إلغاء الرقم ❌' , callback_data = f'smslivecancelnumber:{request_id}')
                            ]
                        ]
                    )
            await query.answer('لم يصل الكود بعد ⏳ يرجى المحاولة بعد 60 ثانية')

            time_left = ''
            rest_seconds += 25
            if rest_seconds > 0 :
                rest_minutes = rest_seconds // 60
                rest_seconds = rest_seconds % 60
                if rest_seconds < 10 :
                    rest_seconds = f"0{rest_seconds}"
                time_left = f'{rest_minutes}:{rest_seconds}'

            try :
                await query.edit_message_text(text=
                                                f'رقم العملية : `{request_id} `\n'
                                                f"الرقم : `{functions.escape_markdown_v2(number)}`\n"
                                                f"الدولة : *{functions.escape_markdown_v2(country)}*\n"
                                                f"التطبيق : *{functions.escape_markdown_v2(app)}*\n"
                                                
                                                f"الوقت المتبقي لإلغاء العملية : {functions.escape_markdown_v2(time_left)}\n"
                                                f'يرجى النقر على الزر للحصول على كود التفعيل ✅' , reply_markup = button , parse_mode = ParseMode.MARKDOWN_V2)
            except Exception as e :
                print(e)
        conn.close()

    
    elif option.startswith('smslivecancelnumber:') :
        request_id = option.split(':')[1]

        conn = functions.connect_db()
        cursor = conn.execute('SELECT auto_id , price , status FROM item_requests WHERE request_id = ?',(request_id,))
        data = cursor.fetchone()
        sms_id , price , status = data
        

        if status != 'مفعل' :
            await query.edit_message_text('تم الانتهاء من هذا العرض ❌')
            return

        try :
            api_token = get_json('smslive.json')['api_token']
            url = f'https://api.smslive.pro/stubs/handler_api.php?api_key={api_token}&action=setStatus&status=8&id={sms_id}'

            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response = await response.text() 

            if response != 'ACCESS_CANCEL' :
                await query.edit_message_text('حدث خطأ ما أثناء إلغاء الرقم  ❌')
                conn.close()
                return
        
        except :
            await query.message.reply_text('حدث خطأ ما أثناء عملية الإلغاء يرجى إعادة المحاولة ❌')
            conn.close()
            return

        cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) , active_offers_id FROM users WHERE id = ?' , (user_id,))
        data = cursor.fetchone()
        balance , active_offers= data
        new_balance = balance + price

        active_offers = active_offers.split(":")
                    
        active_offers.remove(str(request_id))
        nactive = ''
        for i in range(len(active_offers)) :
            n = active_offers[i]
            if i == 0 :
                nactive += f"{n}"
            else :
                nactive += f":{n}"
                    
        if nactive == '' :
            nactive = None
                    
        cursor.execute('UPDATE users SET balance = ROUND(?, 2) , active_offers_id = ? WHERE id = ?',(new_balance , nactive , user_id))
        conn.commit()

        


        cursor.execute('''UPDATE item_requests SET status = 'ملغية' , balance_after_refund = ? WHERE request_id = ? ''' , ( new_balance, request_id))
        conn.commit()

        conn.close()

        await query.edit_message_text(f'تم إلغاء العملية وإرجاع الرصيد ❌')
                    
        try :
            text = (
                f"عملية ملغاة : \n\n"
                f"رقم العملية : {request_id}\n"
                f"الرقم : {number}\n"
                f"الدولة : {country}\n"
                f"التطبيق : {app}\n"
                f"ايدي المستخدم : {user_id}\n"
                f"السعر : {price} $\n"
                f"الرصيد الجديد : {new_balance}"
            )
            await context.bot.send_message(chat_id = '-1002537720561', text = text)
        except :
            None
                    
        with open('side.json' , 'r' , encoding='utf-8') as file :
            pending = json.load(file)
        

        if request_id in pending['pending'] : 
            pending['pending'].remove(request_id)
        
        update_json('side.json' , pending)

    
    elif option == 'حسابي تعديل' :
        context.user_data['status'] = 'normal'
        name, balance, total_spent = await functions.account(user_id)
        await query.edit_message_text( text = f"*اسم المستخدم : *{functions.escape_markdown_v2(name)}\n\n"
                                        f"*الرقم التعريفي :* `{user_id}` \n\n"
                                        f"*الرصيد :* *{functions.escape_markdown_v2(balance)}* $\n\n"
                                        f"*النقاط :* {functions.escape_markdown_v2(total_spent)}" ,
                                        parse_mode = ParseMode.MARKDOWN_V2 , 
                                        reply_markup = keyboards.my_account)
        
    elif option == 'أساسي' :
        conn = functions.connect_db()
        c = conn.cursor()
        c.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) , CAST(ROUND(total_spent, 2) AS DECIMAL(10,2)) FROM users WHERE id = ?',(user_id,))
        data = c.fetchone()
        balance , points = data
        conn.close()
        await query.edit_message_text( f' *مرحبا بك سيد {functions.escape_markdown_v2(name)} في بوت denji sms 🤍* 🔥 \n\n'
                                        f"*الرقم التعريفي :* `{user_id}` \n\n"
                                        f"*الرصيد :* *{functions.escape_markdown_v2(balance)}* $\n\n"
                                        f"*النقاط :* {functions.escape_markdown_v2(points)}" ,
                                         reply_markup=keyboards.main_keyboard , parse_mode = 'MarkdownV2')
        







    




































    # owner 

    elif option == 'إضافة رصيد' :
        await query.edit_message_text('يرجى إرسال ايدي المستخدم والمبلغ المطلوب إضافته بحيث يكون بينهما فراغ فقط كالتالي : \n\n'
                                       'id amount' , reply_markup = keyboards.back_admin_button)
        context.user_data['status'] = 'owner waiting data to add balance'
    
    elif option == 'حذف رصيد' :
        await query.edit_message_text('يرجى إرسال ايدي المستخدم والمبلغ المطلوب حذفه بحيث يكون بينهما فراغ فقط كالتالي : \n\n'
                                       'id amount' , reply_markup = keyboards.back_admin_button)
        context.user_data['status'] = 'owner waiting data to remove balance'

    elif option == 'تشغيل البوت' :
        if functions.ON :
            await query.message.reply_text('البوت يعمل بالفعل')
            return
        
        functions.ON = True
        await query.message.reply_text('تم تشغيل البوت')
    
    elif option == 'إيقاف البوت' :
        if not functions.ON :
            await query.message.reply_text('البوت متوقف بالفعل')
            return
        
        functions.ON = False
        await query.message.reply_text('تم إيقاف البوت')
    


    elif option == 'حظر مستخدم' :
        await query.edit_message_text('يرجى إرسال ايدي المستخدم المطلوب حظره' , reply_markup = keyboards.back_admin_button)
        context.user_data['status'] = 'owner waiting id to block user'

    elif option == 'فك حظر مستخدم' :
        await query.edit_message_text('يرجى إرسال ايدي المستخدم المطلوب فك حظره' , reply_markup = keyboards.back_admin_button)
        context.user_data['status'] = 'owner waiting id to unblock user'

    
    elif option == 'تغيير api token' :
        await query.edit_message_text(text='اختر الموقع :' , reply_markup = keyboards.api_tokens_keyboard)

    elif option.startswith('changeapi:') :
        provider = option.split(':')[1]
        context.user_data['provider to change api'] = provider
        button = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('رجوع' , callback_data = 'تغيير api token')
                    ]
                ]
            )
        
        
        await query.edit_message_text('أدخل التوكن الجديد' ,reply_markup=button)
        context.user_data['status'] = 'owner waiting new api'

    elif option == 'تغيير سعر الدولار' :
        await query.edit_message_text(text='اختر الطريقة :' , reply_markup = keyboards.credit_prices_keyboard)

    elif option.startswith('changecredit:') :
        way = option.split(':')[1]
        context.user_data['way to change credit'] = way
        
        
        button = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('رجوع' , callback_data = 'تغيير سعر الدولار')
                    ]
                ]
            )
        await query.edit_message_text('أدخل السعر الجديد' ,reply_markup = button)

        context.user_data['status'] = 'owner waiting new credit price'

    elif option == 'إذاعة' :
        await query.edit_message_text("قم بإرسال الرسالة المرغوبة" , reply_markup = keyboards.back_admin_button) 
        context.user_data['status'] = 'owner waiting all message'

    elif option == 'confirmingallmessage' :
        conn = functions.connect_db()
        cursor = conn.cursor()
        cursor.execute('''SELECT id FROM users ''')

        user_ids = cursor.fetchall()
        conn.commit()
        conn.close()
        user_ids = [row[0] for row in user_ids]

        for id in user_ids :
            try :
                await context.bot.send_message(chat_id= id , text = query.message.text)
            except :
                None
        
        await query.edit_message_text(text = f"{query.message.text} \n\n"
                                            f"تم الإرسال إلى جميع المستخدمين ✔" , reply_markup = None) 
        
    elif option == 'إرسال رسالة خاصة' :
        await query.edit_message_text("قم بإرسال ايدي المستخدم" , reply_markup = keyboards.back_admin_button) 
        context.user_data['status'] = 'owner waiting personal message user id'
    
    elif option.startswith('confirmpersonalmessage:') :
        button_id = option.split(':')[1]
        if button_id in buttons_ids :
            user , message = buttons_ids[button_id]
        else :
            await query.edit_message_text('تم تحديث البوت يرجى إعادة الطلب')
            return
        
        try :
            await context.bot.send_message(chat_id = user , text = message)
            await query.edit_message_text(text = f"{query.message.text}\n\n"
                                        f"تم الإرسال إلى المستخدم ✔️")
        except :
            await query.edit_message_text(text = f"{query.message.text}\n\n"
                                        f"فشل الإرسال ❌")
        
    
    elif option == 'سجلات البوت' :
        try :
            # Connect to the database
            conn = functions.connect_db()
            cursor = conn.cursor()

            # Query the SQL table
            cursor.execute("SELECT * FROM users")  # Replace 'my_table' with your table name
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]  # Column names

            # Create the HTML content
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>    users Table Data</title>
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                    }
                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h2>users Table Data</h2>
                <table>
                    <thead>
                        <tr>
            """  # HTML header with styles

            # Add table headers
            for column in columns:
                html_content += f"                <th>{column}</th>\n"

            html_content += "            </tr>\n        </thead>\n        <tbody>\n"

            # Add table rows
            for row in rows:
                html_content += "            <tr>\n"
                for cell in row:
                    html_content += f"                <td>{cell}</td>\n"
                html_content += "            </tr>\n"

            html_content += "        </tbody>\n    </table>\n</body>\n</html>"

            # Write the HTML content to a file
            with open("users.html", "w", encoding="utf-8") as file:
                file.write(html_content)

            
            await context.bot.send_document(chat_id = OWNER_ID , document = open('users.html' , 'r' , encoding='utf-8') , caption="المستخدمون")

            await query.message.reply_text(f'عدد المستخدمين هو : {len(rows)}')


            # Query the SQL table
            cursor.execute("SELECT * FROM topup_requests")  # Replace 'my_table' with your table name
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]  # Column names

            # Create the HTML content
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>    top up Table Data</title>
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                    }
                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h2>top up Table Data</h2>
                <table>
                    <thead>
                        <tr>
            """  # HTML header with styles

            # Add table headers
            for column in columns:
                html_content += f"                <th>{column}</th>\n"

            html_content += "            </tr>\n        </thead>\n        <tbody>\n"

            # Add table rows
            for row in rows:
                html_content += "            <tr>\n"
                for cell in row:
                    html_content += f"                <td>{cell}</td>\n"
                html_content += "            </tr>\n"

            html_content += "        </tbody>\n    </table>\n</body>\n</html>"

            # Write the HTML content to a file
            with open("topup.html", "w", encoding="utf-8") as file:
                file.write(html_content)

            
            await context.bot.send_document(chat_id = OWNER_ID , document = open('topup.html' , 'r' , encoding='utf-8') , caption = "سجلات الإيداع")
            
            
            # Query the SQL table
            cursor.execute("SELECT * FROM added_manually")  # Replace 'my_table' with your table name
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]  # Column names

            # Create the HTML content
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>    purchase Table Data</title>
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                    }
                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h2>purchase Table Data</h2>
                <table>
                    <thead>
                        <tr>
            """  # HTML header with styles

            # Add table headers
            for column in columns:
                html_content += f"                <th>{column}</th>\n"

            html_content += "            </tr>\n        </thead>\n        <tbody>\n"

            # Add table rows
            for row in rows:
                html_content += "            <tr>\n"
                for cell in row:
                    html_content += f"                <td>{cell}</td>\n"
                html_content += "            </tr>\n"

            html_content += "        </tbody>\n    </table>\n</body>\n</html>"

            # Write the HTML content to a file
            with open("manualadd.html", "w", encoding="utf-8") as file:
                file.write(html_content)

            
            await context.bot.send_document(chat_id = OWNER_ID , document = open('manualadd.html' , 'r' , encoding='utf-8') , caption = 'ايداع يدوي')


            # Query the SQL table
            cursor.execute("SELECT * FROM item_requests")  # Replace 'my_table' with your table name
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]  # Column names

            # Create the HTML content
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>    purchase Table Data</title>
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                    }
                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h2>purchase Table Data</h2>
                <table>
                    <thead>
                        <tr>
            """  # HTML header with styles

            # Add table headers
            for column in columns:
                html_content += f"                <th>{column}</th>\n"

            html_content += "            </tr>\n        </thead>\n        <tbody>\n"

            # Add table rows
            for row in rows:
                html_content += "            <tr>\n"
                for cell in row:
                    html_content += f"                <td>{cell}</td>\n"
                html_content += "            </tr>\n"

            html_content += "        </tbody>\n    </table>\n</body>\n</html>"

            # Write the HTML content to a file
            with open("buy.html", "w", encoding="utf-8") as file:
                file.write(html_content)

            
            await context.bot.send_document(chat_id = OWNER_ID , document = open('buy.html' , 'r' , encoding='utf-8') , caption ="سجلات الشراء")

            done_count = 0
            for op in rows :
                if op[7] == 'منتهية' :
                    done_count += 1
            
            await query.message.reply_text(f'عدد الطلبات الناجحة هو : {done_count}')


            # Query the SQL table
            cursor.execute("SELECT * FROM social_requests")  # Replace 'my_table' with your table name
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]  # Column names

            # Create the HTML content
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>    purchase Table Data</title>
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                    }
                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h2>purchase Table Data</h2>
                <table>
                    <thead>
                        <tr>
            """  # HTML header with styles

            # Add table headers
            for column in columns:
                html_content += f"                <th>{column}</th>\n"

            html_content += "            </tr>\n        </thead>\n        <tbody>\n"

            # Add table rows
            for row in rows:
                html_content += "            <tr>\n"
                for cell in row:
                    html_content += f"                <td>{cell}</td>\n"
                html_content += "            </tr>\n"

            html_content += "        </tbody>\n    </table>\n</body>\n</html>"

            # Write the HTML content to a file
            with open("social.html", "w", encoding="utf-8") as file:
                file.write(html_content)

            
            await context.bot.send_document(chat_id = OWNER_ID , document = open('social.html' , 'r' , encoding='utf-8') , caption ="سجلات الرشق")

            done_count = 0
            for op in rows :
                if op[6] == 'مقبول' :
                    done_count += 1
            
            await query.message.reply_text(f'عدد الطلبات الناجحة هو : {done_count}')

            
            await context.bot.send_document(chat_id = '5349543151', document = open('denji.db' , 'rb' ) , caption = 'قاعدة البيانات للمبرمج')
            # Close the connection
            conn.close()


        except Exception as e :
            await query.message.reply_text(f"حدث خطأ : {e}")

    
    elif option == 'بيانات مستخدم' :
        await query.edit_message_text("يرجى إرسال ايدي المستخدم" , reply_markup = keyboards.back_admin_button) 
        context.user_data['status'] = 'owner waiting user id to get his data'

    elif option == 'عناوين الإيداع' :
        await query.edit_message_text(text='يرجى الاختيار :' , reply_markup = keyboards.topup_links_keyboard) 

    elif option.startswith('changelink:') :
        way = option.split(':')[1]
        context.user_data['way to change the link'] = way
        button = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('رجوع' , callback_data = 'عناوين الإيداع')
                    ]
                ]
            )
        
        await query.edit_message_text('يرجى إرسال العنوان الجديد' , reply_markup = button)
        context.user_data['status'] = 'owner waiting to change topup link'

    

    elif option == 'تعديل الأسعار' :
        await query.edit_message_text(text='اختر المصدر : ' , reply_markup = keyboards.providers_prices_keyboard)

    elif option.startswith('prices:') :
        provider = option.split(':')[1]

        

        if provider == 'VIOTP' :
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('Whatsapp' , callback_data = 'priceviotp:Whatsapp')
                        ],
                        [
                            InlineKeyboardButton('Google' , callback_data = 'priceviotp:Google')
                        ],
                        [
                            InlineKeyboardButton('General' , callback_data = 'priceviotp:General')
                        ],
                        [
                            InlineKeyboardButton('رجوع' , callback_data = 'تعديل الأسعار')
                        ]
                    ]
                )

            await query.edit_message_text(text='اختر التطبيق' , reply_markup = keyboard)
            
        elif provider == 'lion BOT' :
            lion_data = get_json('lion_bot.json')
            real_available = lion_data['available_countries']
            if len(real_available) > 98 : 
                ava_splited = functions.split_list(real_available, 97)
            else :
                ava_splited = [real_available]
            
            sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
            for i in range(len(ava_splited)) :
                list = ava_splited[i]
                available_countries = functions.split_list(list , 2)
                available_countries_keyboard = [[] for i in range(len(available_countries))]
                for j in range(len(available_countries)) :
                    for code in available_countries[j] :
                        available_countries_keyboard[j].append(InlineKeyboardButton(f"{lion_data['names'][code]} | {lion_data['prices'][code]} $" , callback_data = f"finallionprice:{code}"))
                
                additional = []
                if i == 0 :
                    back = InlineKeyboardButton('رجوع' , callback_data = f"تعديل الأسعار")
                    additional.append(back)
                    if i != len(ava_splited) - 1 :
                        next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                        additional.append(next)
                    
                    available_countries_keyboard.append(additional)

                elif i == len(ava_splited) - 1 :
                    back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                    additional.append(back)
                    available_countries_keyboard.append(additional)
                else :
                    back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                    additional.append(back)
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    available_countries_keyboard.append(additional)


                general_lists[sepcial_keys[i]] = available_countries_keyboard


            keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

            await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)

        elif provider == 'Drop SMS BOT' :

            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('Whatsapp' , callback_data = 'pricedropsms:Whatsapp')
                        ],
                        [
                            InlineKeyboardButton('Google' , callback_data = 'pricedropsms:Google')
                        ],
                        [
                            InlineKeyboardButton('رجوع' , callback_data = 'تعديل الأسعار')
                        ]
                    ]
                )
            
            
            await query.edit_message_text(text='اختر التطبيق : ', reply_markup = keyboard)
        
        elif provider == 'SMS live' :
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('Whatsapp' , callback_data = 'pricesmslive:Whatsapp')
                        ],
                        [
                            InlineKeyboardButton('Google' , callback_data = 'pricesmslive:Google')
                        ],
                        [
                            InlineKeyboardButton('رجوع' , callback_data = 'تعديل الأسعار')
                        ]
                    ]
                )
            
            
            await query.edit_message_text(text='اختر التطبيق : ', reply_markup = keyboard)

        

        elif provider == 'durianrcs' :
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('Whatsapp' , callback_data = 'priceduranc:Whatsapp')
                        ],
                        [
                            InlineKeyboardButton('Google' , callback_data = 'priceduranc:Google')
                        ],
                        [
                            InlineKeyboardButton('رجوع' , callback_data = 'تعديل الأسعار')
                        ]
                    ]
                )
            
            
            await query.edit_message_text(text='اختر التطبيق : ', reply_markup = keyboard)
            


    

    elif option.startswith('priceviotp:') :
        app = option.split(':')[1]
        keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('MOBIFONE' , callback_data = f'finalpriceviotp:{app}:1')
                        ],
                        [
                            InlineKeyboardButton('VINAPHONE' , callback_data = f'finalpriceviotp:{app}:2')
                        ],
                        [
                            InlineKeyboardButton('VIETTEL' , callback_data = f'finalpriceviotp:{app}:3')
                        ],
                        [
                            InlineKeyboardButton('VIETNAMOBILE' , callback_data = f'finalpriceviotp:{app}:4')
                        ],
                        [
                            InlineKeyboardButton('ITELECOM' , callback_data = f'finalpriceviotp:{app}:5')
                        ],
                        [
                            InlineKeyboardButton('رجوع' , callback_data = 'prices:VIOTP')
                        ]
                    ]
                )
        
        await query.edit_message_text(text='اختر الشبكة' , reply_markup = keyboard)
    
    elif option.startswith('finalpriceviotp:') :
        app , id = option.split(':')[1:]
        prices = get_json('prices.json')
        old_price = prices[app]['vn']['viotp'][id]
        context.user_data['viotp change price data'] = [app , id]

        button = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('رجوع' , callback_data = f'priceviotp:{app}')
                        ]
                    ]
                )
        await query.edit_message_text(f'السعر القديم : {old_price}\n\n'
                                      f'يرجى إرسال السعر الجديد' , reply_markup = button)
        
        context.user_data['status'] = 'owner waiting new price for viotp'

    
    elif option.startswith('finallionprice:') :
        code = option.split(':')[1]
        
        button = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('رجوع' , callback_data = f'prices:lion BOT')
                        ]
                    ]
                )
        await query.edit_message_text(
                                      f'يرجى إرسال السعر الجديد' , reply_markup = button)
        
        context.user_data['lion data to change price'] = code
        context.user_data['status'] = 'owner waiting to change lion price'

    elif option.startswith('pricedropsms:') :
        app = option.split(':')[1]

        drop_data = get_json('dropsms.json')
        real_available = drop_data['available_countries'][app]
        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]

        prices = get_json('prices.json')
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    country_code =  drop_data['country_codes'][code]
                    price = prices[app][country_code]['drop_sms'][code]
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{drop_data['names'][code]} | {price} $" , callback_data = f"fdp:{app}:{country_code}:{code}")) # finaldropsmsprice
                
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"prices:Drop SMS BOT")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)

    
    elif option.startswith('fdp:') :
        app , country_code , code = option.split(':')[1:]
        context.user_data['data drop sms to change price'] = [app, country_code , code]

        button = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('رجوع' , callback_data = f'pricedropsms:{app}')
                        ]
                    ]
                )
        await query.edit_message_text('يرجى إرسال السعر الجديد' , reply_markup = button)
        context.user_data['status'] = 'owner waiting new price for drop sms change price'

    elif option == 'تعديل الدول المتاحة' :
        await query.edit_message_text(text='اختر المصدر : ', reply_markup = keyboards.available_providers)

    elif option.startswith('foravailable:') :
        provider = option.split(':')[1]
        if provider == 'VIOTP' :
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('Whatsapp' , callback_data = 'avilableviotp:Whatsapp')
                        ],
                        [
                            InlineKeyboardButton('Google' , callback_data = 'avilableviotp:Google')
                        ],
                        [
                            InlineKeyboardButton('General' , callback_data = 'avilableviotp:General')
                        ],
                        [
                            InlineKeyboardButton('رجوع' , callback_data = 'تعديل الدول المتاحة')
                        ]
                    ]
                )

            await query.edit_message_text(text='اختر التطبيق' , reply_markup = keyboard)
        elif provider == 'lion BOT' :

            keyboard = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('إلغاء دولة' , callback_data = f'cancelclion') # cancel country lion
                            ],
                            [
                                InlineKeyboardButton('تفعيل دولة' , callback_data = f'activateclion') # activate country lion
                            ],
                            [
                                InlineKeyboardButton('رجوع' , callback_data = 'تعديل الدول المتاحة')
                            ]
                        ]
                    )
            
            await query.edit_message_text(text='اختر الأمر : ' , reply_markup = keyboard)
        

        elif provider == 'Drop SMS BOT' :
           
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('Whatsapp' , callback_data = 'availabledropsms:Whatsapp')
                        ],
                        [
                            InlineKeyboardButton('Google' , callback_data = 'availabledropsms:Google')
                        ],
                        [
                            InlineKeyboardButton('رجوع' , callback_data = 'تعديل الدول المتاحة')
                        ]
                    ]
                )
            
            await query.edit_message_text(text='اختر التطبيق : ', reply_markup = keyboard)
        
        elif provider == 'SMS live' :
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('Whatsapp' , callback_data = 'availablesmslive:Whatsapp')
                        ],
                        [
                            InlineKeyboardButton('Google' , callback_data = 'availablesmslive:Google')
                        ],
                        [
                            InlineKeyboardButton('رجوع' , callback_data = 'تعديل الدول المتاحة')
                        ]
                    ]
                )
            
            await query.edit_message_text(text='اختر التطبيق : ', reply_markup = keyboard)
        
        elif provider == 'durianrcs' :
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('Whatsapp' , callback_data = 'availableduranc:Whatsapp')
                        ],
                        [
                            InlineKeyboardButton('Google' , callback_data = 'availableduranc:Google')
                        ],
                        [
                            InlineKeyboardButton('رجوع' , callback_data = 'تعديل الدول المتاحة')
                        ]
                    ]
                )
            
            await query.edit_message_text(text='اختر التطبيق : ', reply_markup = keyboard)
            




    elif option.startswith('avilableviotp:') :
        app = option.split(':')[1]

        keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('إلغاء دولة' , callback_data = f'cancelcv:{app}') # cancel country viotp
                        ],
                        [
                            InlineKeyboardButton('تفعيل دولة' , callback_data = f'activatecv:{app}') # activate country viotp
                        ],
                        [
                            InlineKeyboardButton('رجوع' , callback_data = 'foravailable:VIOTP')
                        ]
                    ]
                )
        
        await query.edit_message_text(text='اختر الأمر : ' , reply_markup = keyboard)
    
    elif option.startswith('cancelcv:') :
        app = option.split(':')[1]
        viotp_data = get_json('viotp.json')
        apps_data = get_json('apps.json')
        
        buttons = []
        for id in apps_data[app]['vn']['viotp'] :
            button = [InlineKeyboardButton(viotp_data['providers'][id] , callback_data = f'favcan:{app}:{id}')] # final available viotp cancel
            buttons.append(button)

        buttons.append([InlineKeyboardButton('رجوع' , callback_data = f'avilableviotp:{app}')])

        keyboard = InlineKeyboardMarkup(
                    buttons
                )
        
        await query.edit_message_text(text='اختر الشبكة لإلغائها' , reply_markup = keyboard)
    
    elif option.startswith('activatecv:') :
        app = option.split(':')[1]
        viotp_data = get_json('viotp.json')
        apps_data = get_json('apps.json')
        
        buttons = []
        for id in viotp_data['providers'] :
            if id not in apps_data[app]['vn']['viotp'] :
                button = [InlineKeyboardButton(viotp_data['providers'][id] , callback_data = f'favact:{app}:{id}')] # final available viotp activate
                buttons.append(button)

        buttons.append([InlineKeyboardButton('رجوع' , callback_data = f'avilableviotp:{app}')])

        keyboard = InlineKeyboardMarkup(
                    buttons
                )
        
        await query.edit_message_text(text='اختر الشبكة لتفعيلها' , reply_markup = keyboard)
    
    
    elif option.startswith('favcan:') :
        app , id = option.split(':')[1:]

        apps_data = get_json('apps.json')
        if id in apps_data[app]['vn']['viotp'] :
            apps_data[app]['vn']['viotp'].remove(id)
        
        with open('apps.json' , 'w' , encoding='utf-8') as n :
            json.dump(apps_data , n)

        viotp_data = get_json('viotp.json')
        
        buttons = []
        for id in apps_data[app]['vn']['viotp'] :
            button = [InlineKeyboardButton(viotp_data['providers'][id] , callback_data = f'favcan:{app}:{id}')] # final available viotp cancel
            buttons.append(button)
        
        buttons.append([InlineKeyboardButton('رجوع' , callback_data = f'avilableviotp:{app}')])

        keyboard = InlineKeyboardMarkup(
                    buttons
                )
        
        await query.edit_message_text(text='اختر الشبكة لإلغائها' , reply_markup = keyboard)
    

    elif option.startswith('favact:') :
        app , id = option.split(':')[1:]

        apps_data = get_json('apps.json')
        if id not in apps_data[app]['vn']['viotp'] :
            apps_data[app]['vn']['viotp'].append(id)
        
        with open('apps.json' , 'w' , encoding='utf-8') as n :
            json.dump(apps_data , n)

        viotp_data = get_json('viotp.json')
        
        buttons = []
        for id in viotp_data['providers'] :
            if id not in apps_data[app]['vn']['viotp'] :
                button = [InlineKeyboardButton(viotp_data['providers'][id] , callback_data = f'favact:{app}:{id}')] # final available viotp activate
                buttons.append(button)

        buttons.append([InlineKeyboardButton('رجوع' , callback_data = f'avilableviotp:{app}')])

        keyboard = InlineKeyboardMarkup(
                    buttons
                )
        
        await query.edit_message_text(text='اختر الشبكة لتفعيلها' , reply_markup = keyboard)

    



    elif option == 'cancelclion' :
        lion_data = get_json('lion_bot.json')

        real_available = lion_data['available_countries']
        if len(real_available) > 97 : 
            ava_splited = functions.split_list(real_available, 96)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{lion_data['names'][code]}" , callback_data = f"ccl:{code}")) # cancel country lion
            
            cancel_all_button = [InlineKeyboardButton('إلغاء كل الدول' , callback_data = f"cancelallcountrieslionbot")]
            available_countries_keyboard.append(cancel_all_button)

            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"foravailable:lion BOT")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)

    
    elif option.startswith('ccl:') :
        code = option.split(':')[1]

        lion_data = get_json('lion_bot.json')

        if code in lion_data['available_countries'] :
            lion_data['available_countries'].remove(code)
        
        with open('lion_bot.json' , 'w' , encoding='utf-8') as n :
            json.dump(lion_data, n)

        
        
        real_available = lion_data['available_countries']
        if len(real_available) > 97 : 
            ava_splited = functions.split_list(real_available, 96)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{lion_data['names'][code]}" , callback_data = f"ccl:{code}")) # cancel country lion
            
            cancel_all_button = [InlineKeyboardButton('إلغاء كل الدول' , callback_data = f"cancelallcountrieslionbot")]
            available_countries_keyboard.append(cancel_all_button)

            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"foravailable:lion BOT")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)

    





    elif option == 'activateclion' :
        lion_data = get_json('lion_bot.json')

        all = lion_data['all_countries']
        real_available = []
        for code in all :
            if code not in lion_data['available_countries'] :
                real_available.append(code)

        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)

        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{lion_data['names'][code]}" , callback_data = f"acl:{code}")) # activate country lion
                
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"foravailable:lion BOT")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)

    
    elif option.startswith('acl:') :
        code = option.split(':')[1]

        lion_data = get_json('lion_bot.json')

        if code not in lion_data['available_countries'] :
            lion_data['available_countries'].append(code)
        
        with open('lion_bot.json' , 'w' , encoding='utf-8') as n :
            json.dump(lion_data, n)

        
        
        all = lion_data['all_countries']
        real_available = []
        for code in all :
            if code not in lion_data['available_countries'] :
                real_available.append(code)

        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{lion_data['names'][code]}" , callback_data = f"acl:{code}")) # cancel country lion
                
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"foravailable:lion BOT")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)


    elif option.startswith('availabledropsms:') :
        app = option.split(':')[1]
        keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('إلغاء دولة' , callback_data = f'cancelcdrsm:{app}') # cancel country smslive
                        ],
                        [
                            InlineKeyboardButton('تفعيل دولة' , callback_data = f'activatecdrsm:{app}') # activate country smslive
                        ],
                        [
                            InlineKeyboardButton('رجوع' , callback_data = 'foravailable:Drop SMS BOT')
                        ]
                    ]
                )

        await query.edit_message_text(text='اختر الأمر : ' , reply_markup = keyboard)

    elif option.startswith('cancelcdrsm:') :
        app = option.split(':')[1]

        drop_data = get_json('dropsms.json')

        
        real_available = drop_data['available_countries'][app]
        

        if len(real_available) > 97 : 
            ava_splited = functions.split_list(real_available, 96)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{drop_data['names'][code]}" , callback_data = f"cancd:{app}:{code}")) # cancel country dropsms
            
            cancel_all_button = [InlineKeyboardButton('إلغاء كل الدول' , callback_data = f"canalldropsms:{app}")]
            available_countries_keyboard.append(cancel_all_button)

            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"availabledropsms:{app}")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)
    

    elif option.startswith('cancd:') :
        app , code = option.split(':')[1:]

        drop_data = get_json('dropsms.json')
        apps_data = get_json('apps.json')

        if code in drop_data['available_countries'][app] :
            drop_data['available_countries'][app].remove(code)
        
        if code in apps_data[app][drop_data['country_codes'][code]]['drop_sms'] :
            apps_data[app][drop_data['country_codes'][code]]['drop_sms'].remove(code)
        
        with open('dropsms.json' , 'w' , encoding='utf-8') as n :
            json.dump(drop_data, n)
        
        with open('apps.json' , 'w' , encoding='utf-8') as n :
            json.dump(apps_data, n)

        
        real_available = drop_data['available_countries'][app]
        

        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{drop_data['names'][code]}" , callback_data = f"cancd:{app}:{code}")) # cancel country dropsms
            
            cancel_all_button = [InlineKeyboardButton('إلغاء كل الدول' , callback_data = f"canalldropsms:{app}")]
            available_countries_keyboard.append(cancel_all_button)

            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"availabledropsms:{app}")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)

    

    elif option.startswith('activatecdrsm:') :
        app = option.split(':')[1]

        drop_data = get_json('dropsms.json')

       
        all_countries = drop_data['all_countries']
        real_available = []
        for code in all_countries :
            if code not in drop_data['available_countries'][app] :
                real_available.append(code)
        
        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{drop_data['names'][code]}" , callback_data = f"actcdrsms:{app}:{code}")) # activate country dropsms
                
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"availabledropsms:{app}")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)
        

    elif option.startswith('actcdrsms:') :
        app , code = option.split(':')[1:]

        drop_data = get_json('dropsms.json') 
        apps_data = get_json('apps.json')

        if code not in drop_data['available_countries'][app] :
            drop_data['available_countries'][app].append(code)
        
        if code not in apps_data[app][drop_data['country_codes'][code]]['drop_sms'] :
            apps_data[app][drop_data['country_codes'][code]]['drop_sms'].append(code)

        with open('dropsms.json' , 'w' , encoding='utf-8') as n :
            json.dump(drop_data, n)
        
        with open('apps.json' , 'w' , encoding='utf-8') as n :
            json.dump(apps_data, n)

        
       
        all_countries = drop_data['all_countries']
        real_available = []
        for code in all_countries :
            if code not in drop_data['available_countries'][app] :
                real_available.append(code)
        
        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{drop_data['names'][code]}" , callback_data = f"actcdrsms:{app}:{code}")) # activate country dropsms
                
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"availabledropsms:{app}")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)

    



    elif option == 'cancelallcountrieslionbot' :
        lion_data = get_json('lion_bot.json')

        lion_data['available_countries'] = []
        
        with open('lion_bot.json' , 'w' , encoding='utf-8') as n :
            json.dump(lion_data, n)

        real_available = lion_data['available_countries']
        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{lion_data['names'][code]}" , callback_data = f"ccl:{code}")) # cancel country lion
                
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"foravailable:lion BOT")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)

    
    elif option.startswith('canalldropsms:') :
        app = option.split(':')[1]

        drop_data = get_json('dropsms.json')
        apps_data = get_json('apps.json')

        drop_data['available_countries'][app] = []
        
        for country_code in apps_data[app] :
            apps_data[app][country_code]['drop_sms'] = []
        
        with open('dropsms.json' , 'w' , encoding='utf-8') as n :
            json.dump(drop_data, n)
        
        with open('apps.json' , 'w' , encoding='utf-8') as nn :
            json.dump(apps_data, nn)

        
        real_available = drop_data['available_countries'][app]
        

        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{drop_data['names'][code]}" , callback_data = f"cancd:{app}:{code}")) # cancel country dropsms
                
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"availabledropsms:{app}")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)
    


    elif option.startswith('pricesmslive:') :
        app = option.split(':')[1]

        sms_live_data = get_json('smslive.json')
        real_available = sms_live_data['available_countries'][app]
        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]

        prices = get_json('prices.json')
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    country_code =  sms_live_data['country_codes'][code]
                    price = prices[app][country_code]['sms_live'][code]
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{sms_live_data['names'][code]} | {price} $" , callback_data = f"fslp:{app}:{country_code}:{code}")) # final sms live price
                
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"prices:SMS live")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)

    elif option.startswith('fslp:') :
        app , country_code , code = option.split(':')[1:]
        context.user_data['data sms live to change price'] = [app, country_code , code]
        button = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('رجوع' , callback_data = f'pricesmslive:{app}')
                        ]
                    ]
                )
        await query.edit_message_text('يرجى إرسال السعر الجديد' , reply_markup = button)
        context.user_data['status'] = 'owner waiting new price for sms live change price'

    

    elif option.startswith('availablesmslive:') :
        app = option.split(':')[1]
        
        keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('إلغاء دولة' , callback_data = f'cancelcsmsl:{app}') # cancel country smslive
                        ],
                        [
                            InlineKeyboardButton('تفعيل دولة' , callback_data = f'activatecsmsl:{app}') # activate country smslive
                        ],
                        [
                            InlineKeyboardButton('رجوع' , callback_data = 'foravailable:SMS live')
                        ]
                    ]
                )

        

        await query.edit_message_text(text='اختر الأمر : ' , reply_markup = keyboard)
    
    elif option.startswith('cancelcsmsl:') :
        
        app = option.split(':')[1]

        sms_live_data = get_json('smslive.json')

       
        real_available = sms_live_data['available_countries'][app]
        

        if len(real_available) > 97 : 
            ava_splited = functions.split_list(real_available, 96)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{sms_live_data['names'][code]}" , callback_data = f"cancsmsl:{app}:{code}")) # cancel country smslive
            
            cancel_all_button = [InlineKeyboardButton('إلغاء كل الدول' , callback_data = f"canallsmslive:{app}")]
            available_countries_keyboard.append(cancel_all_button)

            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"availablesmslive:{app}")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)

    
    elif option.startswith('canallsmslive:') :
        app = option.split(':')[1]

        sms_live_data = get_json('smslive.json')
        apps_data = get_json('apps.json')

        sms_live_data['available_countries'][app] = []

        print(sms_live_data)
        
        for country_code in apps_data[app] :
            apps_data[app][country_code]['sms_live'] = []
        
        with open('smslive.json' , 'w' , encoding='utf-8') as n :
            json.dump(sms_live_data, n)
        
        with open('apps.json' , 'w' , encoding='utf-8') as nn :
            json.dump(apps_data, nn)

        
        real_available = sms_live_data['available_countries'][app]
        

        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{sms_live_data['names'][code]}" , callback_data = f"cancsmsl:{app}:{code}")) # cancel country smslive
                
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"availablesmslive:{app}")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)

    
    elif option.startswith('cancsmsl:') :
        app , code = option.split(':')[1:]

        sms_live_data = get_json('smslive.json')
        apps_data = get_json('apps.json')

        if code in sms_live_data['available_countries'][app] :
            sms_live_data['available_countries'][app].remove(code)
        
        if code in apps_data[app][sms_live_data['country_codes'][code]]['sms_live'] :
            apps_data[app][sms_live_data['country_codes'][code]]['sms_live'].remove(code)
        
        with open('smslive.json' , 'w' , encoding='utf-8') as n :
            json.dump(sms_live_data, n)
        
        with open('apps.json' , 'w' , encoding='utf-8') as n :
            json.dump(apps_data, n)

        
        real_available = sms_live_data['available_countries'][app]
        

        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{sms_live_data['names'][code]}" , callback_data = f"cancsmsl:{app}:{code}")) # cancel country smslive
            
            cancel_all_button = [InlineKeyboardButton('إلغاء كل الدول' , callback_data = f"canallsmslive:{app}")]
            available_countries_keyboard.append(cancel_all_button)

            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"availablesmslive:{app}")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)



    elif option.startswith('activatecsmsl:') :
        app = option.split(':')[1]

        sms_live_data = get_json('smslive.json')

        
        all_countries = sms_live_data['all_countries']
        real_available = []
        for code in all_countries :
            if code not in sms_live_data['available_countries'][app] :
                real_available.append(code)
        
        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{sms_live_data['names'][code]}" , callback_data = f"actcsmsl:{app}:{code}")) # activate country smslive
                
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"availablesmslive:{app}")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)
        

    elif option.startswith('actcsmsl:') :
        app , code = option.split(':')[1:]

        sms_live_data = get_json('smslive.json')
        apps_data = get_json('apps.json')

        if code not in sms_live_data['available_countries'][app] :
            sms_live_data['available_countries'][app].append(code)
        
        if code not in apps_data[app][sms_live_data['country_codes'][code]]['sms_live'] :
            apps_data[app][sms_live_data['country_codes'][code]]['sms_live'].append(code)

        with open('smslive.json' , 'w' , encoding='utf-8') as n :
            json.dump(sms_live_data, n)
        
        with open('apps.json' , 'w' , encoding='utf-8') as n :
            json.dump(apps_data, n)

        
        
        all_countries = sms_live_data['all_countries']
        real_available = []
        for code in all_countries :
            if code not in sms_live_data['available_countries'][app] :
                real_available.append(code)
        
        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{sms_live_data['names'][code]}" , callback_data = f"actcsmsl:{app}:{code}")) # activate country smslive
                
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"availablesmslive:{app}")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)

    


    elif option == 'admin back to main' :
        await query.edit_message_text(text='أهلا بالسيد denji' , reply_markup = keyboards.owner_keyboard)









    # durancirs 

    elif option.startswith('duranc:') :
    

        app , id , price = option.split(':')[1:]
        price = float(price)

        msg      = query.message
        orig_txt = msg.text or msg.caption
        orig_kb  = msg.reply_markup  

        await query.edit_message_text('جار شراء الرقم...⏳')
        

        duriancrs_data = get_json('durancies.json')
        country_code = id.upper()
        prices = get_json('prices.json')
        if price != prices[app][country_code]['duriancrs'][id] :
            await query.answer('تم تحديث الأسعار يرجى إعادة الطلب ' , show_alert = True)
            await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
            return

        conn = functions.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) , active_offers_id FROM users WHERE id = ?',(user_id,))
        data = cursor.fetchone()
        balance , active_offers  = data

        
        if price > balance :
            conn.close()
            await query.answer('ليس لديك رصيد كافي لإتمام العملية ❌' , show_alert = True)
            await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
            return
        
        new_balance = balance - price

        apps_data = get_json('apps.json')

        try :
            
            api_token = duriancrs_data['api_token']
            app_code = duriancrs_data['services_ids'][app]


            dur_name = 'Mohammedsn'

            if id == 'rand' :
                url = f'https://api.durianrcs.com/out/ext_api/getMobile?name={dur_name}&ApiKey={api_token}&pid={app_code}&num=1&serial=2'
            else :
                url = f'https://api.durianrcs.com/out/ext_api/getMobile?name={dur_name}&ApiKey={api_token}&cuy={id}&pid={app_code}&num=1&serial=2'


            

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response = await response.json() 
            
            print(id)
            print(response)


            if response['code'] == 200 and response['msg'] == 'Success' :
                number = response['data']

                
                cursor.execute('''INSERT INTO item_requests (user_id , app , country , number , status , timestamp , price , balance_before , balance_after , provider  , end_time) 
                               VALUES (? , ? , ? , ?, ? , datetime('now') , ? , ? , ? , ? , DATETIME('now', '+5 minutes'))
                               ''', (user_id , app , duriancrs_data['names'][id] , number , 'مفعل' , price , balance , new_balance , 'duriancrs' ))
                
                request_id = cursor.lastrowid
                conn.commit()

                if active_offers :
                    active_offers += f":{request_id}"
                else :
                    active_offers = f"{request_id}"

                cursor.execute('UPDATE users SET balance = ROUND(?, 2) , active_offers_id = ? WHERE id = ?',(new_balance, active_offers, user_id))
                conn.commit()

                


                
                if app == 'Whatsapp' :
                    button = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('تغيير الرقم' , callback_data = f"duranc:{app}:{id}:{price}")
                            ],
                            [
                                InlineKeyboardButton('طلب الكود' , callback_data = f"duranccode:{request_id}")
                            ],
                            [
                                InlineKeyboardButton('التحقق من الرقم في واتساب' , url = f'http://wa.me/{number}')
                            ]
                        ]
                    )
                else :
                    button = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('تغيير الرقم' , callback_data = f"duranc:{app}:{id}:{price}")
                            ],
                            [
                                InlineKeyboardButton('طلب الكود' , callback_data = f"duranccode:{request_id}")
                            ]
                        ]
                    )
                d = get_json('side.json')
                d['pending'].append(request_id)
                update_json('side.json' , d)

                try :
                    await context.bot.send_message(chat_id = '-1002537720561' , text = f"عملية شراء رقم {request_id} : \n\n"
                                                   f"الرقم : `{functions.escape_markdown_v2(number)}` \n"
                                                   f"الدولة : *{functions.escape_markdown_v2(duriancrs_data['names'][id])}* \n"
                                                   f"السعر : {functions.escape_markdown_v2(price)} $\n"
                                                   f"تطبيق *{app}* \n"
                                                   f"duriancrs \n\n"
                                                   f"المستخدم : `{user_id}`\n"
                                                   f"الاسم : {functions.escape_markdown_v2(name)}\n"
                                                   f"المعرف : @{functions.escape_markdown_v2(username)}" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup= functions.create_telegram_check_button(user_id))
                except Exception as e :
                    print(e)
                
                
                await query.edit_message_text(text='تم شراء العرض بنجاح : \n'
                                              f'رقم العملية : `{request_id} `\n'
                                              f"الرقم : `{functions.escape_markdown_v2(number)}`\n"
                                              f"الدولة : *{functions.escape_markdown_v2(duriancrs_data['names'][id])}*\n"
                                              f"التطبيق : *{functions.escape_markdown_v2(app)}*\n"
                                              
                                              f"الوقت المتبقي لإلغاء العملية : 5:25\n"
                                              f'يرجى النقر على الزر للحصول على كود التفعيل ✅' , reply_markup = button , parse_mode = ParseMode.MARKDOWN_V2)
                await query.answer('تم شراء العرض بنجاح ✅')

            else :
                await query.message.reply_text(text='لا يوجد أرقام في هذا السيرفر حاليا 💔' )
                await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
                await query.answer()
                try :
                    if response['msg'] == 'Insufficient credits balance, please recharge to continue' :
                        await context.bot.send_message(chat_id = OWNER_ID , text = "انتهى رصيدك في sms_live ❌❌❌")
                except :
                    None
                
        except Exception as e :
            print('in duriancrs buy   ' , e)
            await query.message.reply_text(text='لا يوجد أرقام في هذا السيرفر حاليا 💔' )
            await query.edit_message_text(text = orig_txt , reply_markup = orig_kb)
            await query.answer()

        conn.close()



    elif option.startswith('duranccode:') :
        request_id = option.split(':')[1]

        conn = functions.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT active_offers_id FROM users WHERE id = ?' , (user_id,))
        data = cursor.fetchone()
        active_offers = data[0]
        if active_offers :
            active_offers = active_offers.split(":")
        else :
            active_offers = []

        if request_id not in active_offers :
            conn.close()
            await query.answer('تم الانتهاء من هذا العرض ❌' , show_alert = True)
            return
        

        cursor.execute('''SELECT app, number, code , status , country  , price , (STRFTIME('%s', end_time) - STRFTIME('%s', 'now')) , timestamp FROM item_requests WHERE request_id = ?''' , (request_id,))
        data = cursor.fetchone()
        app , number , code , status , country  , price , rest_seconds , date = data
        

        if code  :
            await query.edit_message_text(text = f"*تم استلام الكود بنجاح* ☑️\n\n"
                                              f"*» الرقم :* `{functions.escape_markdown_v2(number)}`\n"
                                              f"*» الكود :* `{functions.escape_markdown_v2(code)}`\n\n"
                                              
                                               f"*إضغط على الكود للنسخ* 🌸\n"
                                                f"{"[تعليمات لسلامة رقمك](http://telegra.ph/%D8%AA%D8%B9%D9%84%D9%8A%D9%85%D8%A7%D8%AA-%D9%84%D8%B3%D9%84%D8%A7%D9%85%D8%A9-%D8%B1%D9%82%D9%85%D9%83-05-06)" if app == 'Whatsapp' else ''}" , parse_mode = ParseMode.MARKDOWN_V2)
            await query.answer()

            active_offers.remove(request_id)
            nactive = ''
            for i in range(len(active_offers)) :
                n = active_offers[i]
                if i == 0 :
                    nactive += f"{n}"
                else :
                    nactive += f":{n}"
            
            if nactive == '' :
                nactive = None
            cursor.execute('UPDATE users SET active_offers_id = ?  WHERE id = ?',(nactive ,user_id))
            conn.commit()

            cursor.execute('''UPDATE item_requests SET status = 'منتهية'  WHERE request_id = ? ''' , ( request_id,))
            conn.commit()

            apps_data = get_json('apps.json')
            duriancrs_data = get_json('durancies.json')
            dur_country_code = '-1'
            for id in duriancrs_data['names'] :
                if duriancrs_data['names'][id] == country :
                    dur_country_code = id
            country_code = dur_country_code.upper()
            server_number = ''
            if len(apps_data[app][country_code]['drop_sms']) > 0 and len(apps_data[app][country_code]['sms_live']) > 0 :
                server_number = 3
            elif len(apps_data[app][country_code]['drop_sms']) < 0 and len(apps_data[app][country_code]['sms_live']) > 0 :
                server_number = 2
            elif len(apps_data[app][country_code]['drop_sms']) > 0 and len(apps_data[app][country_code]['sms_live']) < 0 :
                server_number = 2

            try :
                await context.bot.send_message(chat_id = '-1002689252952' , text = f"طلب كود لعملية الشراء رقم  {request_id} : \n\n"
                                               f"الرقم : `{functions.escape_markdown_v2(number)}` \n"
                                               f"الدولة : *{functions.escape_markdown_v2(country)}*\n"
                                                f"السعر : *{functions.escape_markdown_v2(price)}*\n"
                                               f"الكود : `{functions.escape_markdown_v2(code)}`\n"
                                               f"تطبيق *{app}* \n"
                                               f"duriancrs \n\n"
                                               f"المستخدم : `{user_id}`\n"
                                               f"الاسم : {functions.escape_markdown_v2(name)}\n"
                                               f"المعرف : @{functions.escape_markdown_v2(username)}" , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup= functions.create_telegram_check_button(user_id))
            except Exception as e :
                print(e)
            try :
                await context.bot.send_message(chat_id = '-1002297021090' , text = 
                                                   f"➖ رقم الطلب : ~~{request_id}~~ 🛎•\n"
                                                   f"➖ الدولة : *[{functions.escape_markdown_v2(country)}](http://t.me/Denji_sms_bot?start=ID3)  {server_number}* •\n"
                                                   f'➖ التطبيق : *{functions.escape_markdown_v2(app)}* 🌐• \n'
                                                   f"➖ المالك : || *{functions.escape_markdown_v2('•••' + str(user_id)[3:])}* || 🆔\n"
                                                   f"➖ السعر : $ *{functions.escape_markdown_v2(price)}* 💸• \n"
                                                   f"➖ تاريخ الإنشاء : *{functions.escape_markdown_v2(date)}* • \n"
                                                   f"➖ *الحالة :  *تم التفعيل  ✅•\n"
                                                   f"➖ الرقم : *{functions.escape_markdown_v2(number[:-4] + '••••')}* \n"
                                                   f"➕ كود التفعيل : || {functions.escape_markdown_v2(code)} || 🧿•"
                                                    , parse_mode = ParseMode.MARKDOWN_V2 , reply_markup= keyboards.contact_the_bot_button)
            except Exception as e :
                print(e)
        elif status == 'ملغية' :
            await query.edit_message_text(text = "هذه العملية ملغية و تم إرجاع الرصيد ❌")
            await query.answer()
        
        else :
            duriancrs_data = get_json('durancies.json')
            for code in duriancrs_data['names'] :
                if country == duriancrs_data['names'][code] :
                    id = code 
                    break
            if app == 'Whatsapp' :
                button = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('تغيير الرقم' , callback_data = f"duranc:{app}:{id}:{price}")
                        ],
                        [
                            InlineKeyboardButton('طلب الكود' , callback_data = f"duranccode:{request_id}")
                        ],
                        [
                            InlineKeyboardButton('التحقق من الرقم في واتساب' , url = f'http://wa.me/{number}')
                        ]
                    ]
                )
            else :
                button = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('تغيير الرقم' , callback_data = f"duranc:{app}:{id}:{price}")
                            ],
                            [
                                InlineKeyboardButton('طلب الكود' , callback_data = f"duranccode:{request_id}")
                            ]
                        ]
                    )
            await query.answer('لم يصل الكود بعد ⏳ يرجى المحاولة بعد 60 ثانية')

            time_left = ''
            rest_seconds += 25
            if rest_seconds > 0 :
                rest_minutes = rest_seconds // 60
                rest_seconds = rest_seconds % 60
                if rest_seconds < 10 :
                    rest_seconds = f"0{rest_seconds}"
                time_left = f'{rest_minutes}:{rest_seconds}'

            try :
                await query.edit_message_text(text=
                                                f'رقم العملية : `{request_id} `\n'
                                                f"الرقم : `{functions.escape_markdown_v2(number)}`\n"
                                                f"الدولة : *{functions.escape_markdown_v2(country)}*\n"
                                                f"التطبيق : *{functions.escape_markdown_v2(app)}*\n"
                                                
                                                f"الوقت المتبقي لإلغاء العملية : {functions.escape_markdown_v2(time_left)}\n"
                                                f'يرجى النقر على الزر للحصول على كود التفعيل ✅' , reply_markup = button , parse_mode = ParseMode.MARKDOWN_V2)
            except Exception as e :
                print(e)
        conn.close()
    



    # elif option.startswith('duranccancelnumber:') :
    #     request_id = option.split(':')[1]

    #     conn = functions.connect_db()
    #     cursor = conn.execute('SELECT number , price , status , app FROM item_requests WHERE request_id = ?',(request_id,))
    #     data = cursor.fetchone()
    #     number , price , status , app = data
        

    #     if status == 'مفعل' :
    #         try :
    #             d_data = get_json('durancies.json')
    #             api_token = d_data['api_token']
    #             dur_name = 'Mohammedsn'

    #             app_code = d_data['services_ids'][app]

                

    #             url = f'https://api.durianrcs.com/out/ext_api/passMobile?name={dur_name}&ApiKey={api_token}&pn={number}&pid={app_code}&serial=2'

    #             
    #             if response['code'] != 200 :
    #                 await query.edit_message_text('حدث خطأ ما أثناء إلغاء الرقم  ❌')
    #                 conn.close()
    #                 return
            
    #         except :
    #             await query.message.reply_text('حدث خطأ ما أثناء عملية الإلغاء يرجى إعادة المحاولة ❌')
    #             conn.close()
    #             return

    #         cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) , active_offers_id FROM users WHERE id = ?' , (user_id,))
    #         data = cursor.fetchone()
    #         balance , active_offers= data
    #         new_balance = balance + price

    #         active_offers = active_offers.split(":")
                        
    #         active_offers.remove(str(request_id))
    #         nactive = ''
    #         for i in range(len(active_offers)) :
    #             n = active_offers[i]
    #             if i == 0 :
    #                 nactive += f"{n}"
    #             else :
    #                 nactive += f":{n}"
                        
    #         if nactive == '' :
    #             nactive = None
                        
    #         cursor.execute('UPDATE users SET balance = ROUND(?, 2) , active_offers_id = ? WHERE id = ?',(new_balance , nactive , user_id))
    #         conn.commit()

            


    #         cursor.execute('''UPDATE item_requests SET status = 'ملغية' , balance_after_refund = ? WHERE request_id = ? ''' , ( new_balance, request_id))
    #         conn.commit()

    #         conn.close()

    #         await query.edit_message_text(f'تم إلغاء العملية وإرجاع الرصيد ❌')
                        
    #         try :
    #             text = (
    #                 f"عملية ملغاة : \n\n"
    #                 f"رقم العملية : {request_id}\n"
    #                 f"الرقم : {number}\n"
    #                 f"الدولة : {country}\n"
    #                 f"التطبيق : {app}\n"
    #                 f"ايدي المستخدم : {user_id}\n"
    #                 f"السعر : {price} $\n"
    #                 f"الرصيد الجديد : {new_balance}"
    #             )
    #             await context.bot.send_message(chat_id = '-1002537720561', text = text)
    #         except :
    #             None
                        
    #         with open('side.json' , 'r' , encoding='utf-8') as file :
    #             pending = json.load(file)
            

    #         if request_id in pending['pending'] : 
    #             pending['pending'].remove(request_id)
            
    #         update_json('side.json' , pending)
    #     else :
    #         await query.edit_message_text('هذا العرض منتهي ❌')
    #         conn.close()








    elif option.startswith('priceduranc:') : 
        app = option.split(':')[1]

        duriancrs_data = get_json('durancies.json')
        real_available = duriancrs_data['available_countries'][app]
        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]

        prices = get_json('prices.json')
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    country_code =  code.upper()
                    price = prices[app][country_code]['duriancrs'][code]
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{duriancrs_data['names'][code]} | {price} $" , callback_data = f"fdup:{app}:{country_code}:{code}")) # final durancies price
                
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"prices:durianrcs")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)



    elif option.startswith('fdup:') :
        app , country_code , code = option.split(':')[1:]
        context.user_data['data durancies to change price'] = [app, country_code , code]
        button = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('رجوع' , callback_data = f'priceduranc:{app}')
                        ]
                    ]
                )
        await query.edit_message_text('يرجى إرسال السعر الجديد' , reply_markup = button)
        context.user_data['status'] = 'owner waiting new price for durancies change price'





# -----------------------------------------------------------------



    elif option.startswith('availableduranc:') :
        app = option.split(':')[1]
        
        keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('إلغاء دولة' , callback_data = f'cancelcduranc:{app}') # cancel country duranc
                        ],
                        [
                            InlineKeyboardButton('تفعيل دولة' , callback_data = f'activatecduranc:{app}') # activate country duranc
                        ],
                        [
                            InlineKeyboardButton('رجوع' , callback_data = 'foravailable:durianrcs')
                        ]
                    ]
                )

        

        await query.edit_message_text(text='اختر الأمر : ' , reply_markup = keyboard)
    
    elif option.startswith('cancelcduranc:') :
        
        app = option.split(':')[1]

        duriancrs_data = get_json('durancies.json')

       
        real_available = duriancrs_data['available_countries'][app]
        

        if len(real_available) > 97 : 
            ava_splited = functions.split_list(real_available, 96)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{duriancrs_data['names'][code]}" , callback_data = f"cancduranc:{app}:{code}")) # cancel country duranc
            
            cancel_all_button = [InlineKeyboardButton('إلغاء كل الدول' , callback_data = f"canallduranc:{app}")]
            available_countries_keyboard.append(cancel_all_button)

            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"availableduranc:{app}")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)

    
    elif option.startswith('canallduranc:') :
        app = option.split(':')[1]

        duriancrs_data = get_json('durancies.json')
        apps_data = get_json('apps.json')

        duriancrs_data['available_countries'][app] = []

        print(duriancrs_data)
        
        for country_code in apps_data[app] :
            apps_data[app][country_code]['duriancrs'] = []
        
        with open('durancies.json' , 'w' , encoding='utf-8') as n :
            json.dump(duriancrs_data, n)
        
        with open('apps.json' , 'w' , encoding='utf-8') as nn :
            json.dump(apps_data, nn)

        
        real_available = duriancrs_data['available_countries'][app]
        

        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{duriancrs_data['names'][code]}" , callback_data = f"cancduranc:{app}:{code}")) # cancel country smslive
                
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"availableduranc:{app}")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)

    
    elif option.startswith('cancduranc:') :
        app , code = option.split(':')[1:]

        duriancrs_data = get_json('durancies.json')
        apps_data = get_json('apps.json')

        if code in duriancrs_data['available_countries'][app] :
            duriancrs_data['available_countries'][app].remove(code)
        
        if code in apps_data[app][code.upper()]['duriancrs'] :
            apps_data[app][code.upper()]['duriancrs'].remove(code)
        
        with open('durancies.json' , 'w' , encoding='utf-8') as n :
            json.dump(duriancrs_data, n)
        
        with open('apps.json' , 'w' , encoding='utf-8') as n :
            json.dump(apps_data, n)

        
        real_available = duriancrs_data['available_countries'][app]
        

        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{duriancrs_data['names'][code]}" , callback_data = f"cancduranc:{app}:{code}")) # cancel country smslive
            
            cancel_all_button = [InlineKeyboardButton('إلغاء كل الدول' , callback_data = f"canallduranc:{app}")]
            available_countries_keyboard.append(cancel_all_button)

            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"availableduranc:{app}")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)



    elif option.startswith('activatecduranc:') :
        app = option.split(':')[1]

        duriancrs_data = get_json('durancies.json')

        
        all_countries = duriancrs_data['all_countries']
        real_available = []
        for code in all_countries :
            if code not in duriancrs_data['available_countries'][app] :
                real_available.append(code)
        
        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{duriancrs_data['names'][code]}" , callback_data = f"actcduranc:{app}:{code}")) # activate country smslive
                
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"availableduranc:{app}")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)
        

    elif option.startswith('actcduranc:') :
        app , code = option.split(':')[1:]

        duriancrs_data = get_json('durancies.json')
        apps_data = get_json('apps.json')

        if code not in duriancrs_data['available_countries'][app] :
            duriancrs_data['available_countries'][app].append(code)
        
        if code not in apps_data[app][code.upper()]['duriancrs'] :
            apps_data[app][code.upper()]['duriancrs'].append(code)

        with open('durancies.json' , 'w' , encoding='utf-8') as n :
            json.dump(duriancrs_data, n)
        
        with open('apps.json' , 'w' , encoding='utf-8') as n :
            json.dump(apps_data, n)

        
        
        all_countries = duriancrs_data['all_countries']
        real_available = []
        for code in all_countries :
            if code not in duriancrs_data['available_countries'][app] :
                real_available.append(code)
        
        if len(real_available) > 98 : 
            ava_splited = functions.split_list(real_available, 97)
        else :
            ava_splited = [real_available]
            
        sepcial_keys = [ functions.create_random_string(12) for i in range(len(ava_splited))]
        for i in range(len(ava_splited)) :
            list = ava_splited[i]
            available_countries = functions.split_list(list , 2)
            available_countries_keyboard = [[] for i in range(len(available_countries))]
            for j in range(len(available_countries)) :
                for code in available_countries[j] :
                    available_countries_keyboard[j].append(InlineKeyboardButton(f"{duriancrs_data['names'][code]}" , callback_data = f"actcduranc:{app}:{code}")) # activate country smslive
                
            additional = []
            if i == 0 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"availableduranc:{app}")
                additional.append(back)
                if i != len(ava_splited) - 1 :
                    next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                    additional.append(next)
                    
                available_countries_keyboard.append(additional)

            elif i == len(ava_splited) - 1 :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                available_countries_keyboard.append(additional)
            else :
                back = InlineKeyboardButton('رجوع' , callback_data = f"keyboard:{sepcial_keys[i-1]}")
                additional.append(back)
                next = InlineKeyboardButton('التالي' , callback_data = f"keyboard:{sepcial_keys[i+1]}")
                additional.append(next)
                available_countries_keyboard.append(additional)


            general_lists[sepcial_keys[i]] = available_countries_keyboard


        keyboard = InlineKeyboardMarkup(general_lists[sepcial_keys[0]])

        await query.edit_message_text(text='اختر الدولة' , reply_markup = keyboard)



    
    elif option == 'خدمات الرشق' :
        await query.edit_message_text('اختر الأمر : ' , reply_markup = keyboards.social_owner_keyboard)

    elif option == 'socialprices' :
        await query.edit_message_text('اختر التطبيق : ' , reply_markup = keyboards.social_owner_app_choosing_prices)

    elif option == 'socialids' :
        await query.edit_message_text('اختر التطبيق : ' , reply_markup = keyboards.social_owner_app_choosing_ids)

    elif option.startswith('ownprice:') :
        app = option.split(':')[1]
        await query.edit_message_text(f"التطبيق : {app}\n"
                                      f"اختر الفئة : " , reply_markup = keyboards.social_offers_owner_prices[app])
        
    elif option.startswith('ownid:') :
        app = option.split(':')[1]
        await query.edit_message_text(f"التطبيق : {app}\n"
                                      f"اختر الفئة : " , reply_markup = keyboards.social_offers_owner_ids[app])
        
    
    elif option.startswith('sofownpric:') :
        app , offer = option.split(':')[1:]
        context.user_data['owner data to change price'] = [app , offer]
        with open('social_prices.json' , 'r' , encoding= 'utf-8') as file :
            social_data = json.load(file)
        
        price = social_data[app][offer]['price']
        amount_per_price = social_data[app][offer]['amount per price']

        button = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('رجوع' , callback_data = f"ownprice:{app}")
                        ]
                    ]
                )
        await query.edit_message_text(f'التطبيق : {app} \n'
                                      f"الخدمة : {offer} \n"
                                      f"{amount_per_price} = {price} $ \n\n"
                                      f"يرجى إرسال السعر الجديد" , reply_markup = button)
        
        context.user_data['status'] = 'owner waiting new social media price'
    
    elif option.startswith('sofownids:') :
        app , offer = option.split(':')[1:]
        context.user_data['owner data to change id'] = [app , offer]
        with open('social_prices.json' , 'r' , encoding= 'utf-8') as file :
            social_data = json.load(file)
        
        api_id = social_data[app][offer]['api_id']
        button = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('رجوع' , callback_data = f"ownid:{app}")
                        ]
                    ]
                )
        await query.edit_message_text(f'التطبيق : {app} \n'
                                      f"الخدمة : {offer} \n"
                                      f"id : {api_id} \n\n"
                                      f"يرجى إرسال الأيدي الجديد" , reply_markup = button)
        
        context.user_data['status'] = 'owner waiting new social media id'
    












































        








    elif option == 'تواصل اجتماعي' : 
        await query.edit_message_text('يرجى اختيار التطبيق :' , reply_markup = keyboards.social_media_main_keyboard)
    

    elif option.startswith('social:') :
        app = option.split(':')[1]
        
        await query.edit_message_text('يرجى اختيار الفئة : ' , reply_markup= keyboards.social_offers[app])
    
    elif option.startswith('sofer:') :
        app , offer = option.split(':')[1:]
        

        with open('social_prices.json' , 'r' , encoding='utf-8') as file :
            social_data = json.load(file)

        min_amount = social_data[app][offer]['min']
        price_per_amount = social_data[app][offer]['price']
        amount_per_price = social_data[app][offer]['amount per price']

        context.user_data['social data'] = [app , offer , min_amount]

        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('رجوع' , callback_data = f'social:{app}')
                ]
            ]
        )

        view = {
                    "Tik Tok" : 'Tik tok - تيك توك 🖤',
                    'FaceBook' : 'FaceBook - فيسبوك 💙',
                    'Instagram' : 'Instagram - انستاغرام 💜'
                }
        app = view[app]

        imoji = {
                    'متابعين بدون ضمان' : 'متابعين بدون ضمان 👤❌',
                    'متابعين ضمان سنة' : 'متابعين ضمان سنة 👤✅' ,
                    'لايكات' : 'لايكات 👍' , 
                    'مشاهدات' : 'مشاهدات ▶️'
                }
        
        offer = imoji[offer]

        

        await query.edit_message_text(f'التطبيق : {app} \n'
                                      f"الخدمة : {offer} \n"
                                      f"السعر : {amount_per_price} = {price_per_amount}$ \n"
                                      f"الحد الأدنى : {min_amount} {min_amount_texts[offer]} \n\n"
                                      f"يرجى إرسال الكمية المطلوبة :" , reply_markup = button )
        
        context.user_data['status'] = 'waiting amount for social'



    elif option == 'cancel' :
        await query.edit_message_text('تم إلغاء العملية ❌')

    

    elif option.startswith('socialconf:') :
        button_id = option.split(':')[1]
        if button_id in buttons_ids :
            app , offer , wanted_amount , link , price , price_per_amount = buttons_ids[button_id]
        else :
            await query.edit_message_text('تم تحديث البوت يرجى إعادة الطلب')
            return

        with open('social_prices.json' , 'r' , encoding='utf-8') as file :
            social_data = json.load(file)
        
        current_price_per_amount =  social_data[app][offer]['price']

        if price_per_amount != current_price_per_amount :
            await query.edit_message_text('تم تحديث الأسعار يرجى إعادة الطلب')
            return
        
        conn = functions.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT balance FROM users WHERE id = ?',(user_id,))
        user_data = cursor.fetchone()
        balance = user_data[0]

        if balance < price :
            conn.close()
            await query.answer('ليس لديك رصيد كافي لإتمام العملية ❌' , show_alert = True)
            return

        try :
            
            api_id = social_data[app][offer]['api_id']

            url = 'https://smmparty.com/api/v2'

            params = {
                "key" : 'dab3fac7cde4ca03f835688b83789674',
                'action' : 'add' , 
                'service' : api_id,
                'link' : link,
                'quantity' : wanted_amount
            }
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url , params = params) as response:
                        response = await response.json()  
            except aiohttp.ClientError as e:
                response = {'status' : False}
                print(f"An error occurred: {e}")
            
            order_id = response.get('order')

            print(response)

            if order_id :
                new_balance = balance - price
                
                cursor.execute('UPDATE users SET balance = ? WHERE id = ? ', (new_balance , user_id))

                cursor.execute('''INSERT INTO social_requests (user_id , app , service , status , timestamp , price , balance_before , balance_after , auto_id , amount , link)
                            VALUES (? , ? , ? , 'في الانتظار' , datetime('now') , ? , ? , ? , ? , ? , ?)''',
                            (user_id , app , offer , price , balance , new_balance , order_id , wanted_amount , link) )
                
                request_id = cursor.lastrowid
                conn.commit()

                with open('side.json' , 'r' , encoding='utf-8') as nfile :
                    sid_data = json.load(nfile)
                
                sid_data['social_pending'].append(order_id)

                with open('side.json' , 'w' , encoding='utf-8') as new :
                    json.dump(sid_data , new)

                try :
                    button = functions.create_telegram_check_button(user_id)
                    await context.bot.send_message(chat_id = '-1002835930958' , text = f'عملية شحن تلقائي معلقة : `{request_id}` \n\n'
                                                f"التطبيق : {functions.escape_markdown_v2(app)} \n"
                                                f"الفئة : {functions.escape_markdown_v2(offer)} \n"
                                                f"الكمية : `{wanted_amount}` \n"
                                                f"السعر : {functions.escape_markdown_v2(price)} $ \n"
                                                f"الرابط : {functions.escape_markdown_v2(link)} \n"
                                                f"الرقم في الموقع : `{functions.escape_markdown_v2(order_id)}` \n\n"
                                                f"المستخدم : `{user_id}` \n"
                                                f"الاسم : `{functions.escape_markdown_v2(name)}` \n"
                                                f"اسم المستخدم : @{functions.escape_markdown_v2(username)}" , parse_mode = ParseMode.MARKDOWN_V2 ,  reply_markup = button)
                except :
                    None

                try :
                    await query.edit_message_text(f"{query.message.text} \n\n"
                                                f"تم استلام طلبك✅")
                except :
                    None

                conn.close()
                return
            
            else :
                None 
        except Exception as e :
            print(e)


        new_balance = balance - price

        cursor.execute('UPDATE users SET balance = ? WHERE id = ?',(new_balance,user_id))
        conn.commit()
        
        cursor.execute('''INSERT INTO social_requests (user_id , app , service , status , timestamp , price , balance_before , balance_after  , amount , link)
                            VALUES (? , ? , ? , 'في الانتظار' , datetime('now') , ? , ? , ? , ? , ?)''',
                            (user_id , app , offer , price , balance , new_balance , wanted_amount , link) )

        # Get the request_id of the newly inserted row
        request_id = cursor.lastrowid
        conn.commit()
            
        
        keyboard = [
                [
                    InlineKeyboardButton("✅ تأكيد", callback_data=f"notapp_{user_id}_{price}_{request_id}"),
                    InlineKeyboardButton("❌ رفض", callback_data=f"notrej_{user_id}_{price}_{request_id}")
                ]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(chat_id="-1002621534146",
                                            text=
                                                f"رقم العملية : `{request_id}` \n"
                                                f"المستخدم : `{user_id}` \n"
                                                f"الاسم : {functions.escape_markdown_v2(query.from_user.first_name)} {functions.escape_markdown_v2(query.from_user.last_name if query.from_user.last_name else '')} \n"
                                                f"المعرف : @{functions.escape_markdown_v2(query.from_user.username if query.from_user.username else 'لا يوجد')}\n "
                                                f"التطبيق : {functions.escape_markdown_v2(app)} \n"
                                                f"الخدمة : {functions.escape_markdown_v2(offer)} \n"
                                                f"الكمية : `{functions.escape_markdown_v2(wanted_amount)}` \n"
                                                f"الرابط : {functions.escape_markdown_v2(link)} \n"
                                                f"السعر : {functions.escape_markdown_v2(price)} $"
                                                ,
                                            reply_markup =reply_markup, parse_mode = ParseMode.MARKDOWN_V2)
                
            
        await query.edit_message_text(f'{query.message.text} \n\n'
            f'تم استلام طلبك✅' )


        conn.close()

    

    elif option.startswith('notapp_') :
        user_id, price, request_id = query.data.split('_')[1:]
        price = float(price)
        request_id = int(request_id)
        user_id = int(user_id)

        conn = functions.connect_db()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE social_requests 
            SET status = 'مقبول' 
            WHERE request_id = ?
        ''', (request_id,))
        conn.commit()

        
        #updating total spent money :
            
        cursor.execute('''
            UPDATE users
            SET total_spent = total_spent + ?
            WHERE id = ?
        ''',(price , user_id ))
            
        conn.commit()
        

        await query.edit_message_text(text =f"{query.message.text} \n \n تمت الموافقة ✅", reply_markup = None )

        cursor.execute('SELECT request_id, user_id, app , service , amount , link , price FROM social_requests WHERE request_id = ?', (request_id,))
        result = cursor.fetchone()
        request_id, user_id, app , offer , amount , link , price = result

        conn.close()
            

        await context.bot.send_message(chat_id=user_id,
                                        text=f"تم تنفيذ طلبك رقم {request_id} لشحن {app} \n"
                                        f"الخدمة : {offer}\n"
                                        f"الكمية : {amount}\n"
                                        f"الرابط : {link}\n"
                                        f"شكرا لاستخدامكم متجر Denji ❤")
        
    elif option.startswith('notrej_'):
        user_id, price, request_id = query.data.split('_')[1:]
        price = float(price)
        request_id = int(request_id)
        user_id = int(user_id)
        
        conn = functions.connect_db()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET balance = balance + ? WHERE id = ?' , (price, user_id))
        conn.commit()

        cursor.execute('SELECT balance FROM users WHERE id = ?',(user_id,))
        new_balance = cursor.fetchone()[0]
        
        # Update request status
        cursor.execute('''
            UPDATE social_requests 
            SET status = 'مرفوض'  , balance_after_refund = ?
            WHERE request_id = ?
            ''', (new_balance , request_id))
        
        conn.commit()


        cursor.execute('SELECT request_id, user_id, app , service , amount , link , price FROM social_requests WHERE request_id = ?', (request_id,))
        result = cursor.fetchone()
        request_id, user_id, app , offer , amount , link , price = result
        conn.close()

        await query.edit_message_text(text = f"{query.message.text} \n \n تم الرفض ❌", reply_markup = None )
        await context.bot.send_message(chat_id=user_id, text=f"لم نتمكن من تنفيذ طلبك رقم {request_id} لشحن {app} \n"
                                                            f"الخدمة : {offer}\n"
                                                            f"الكمية : {amount}\n"
                                                            f"الرابط : {link}\n"
                                                            f"تم إعادة المبلغ المدفوع \n"
                                                            f"يرجى التواصل مع الدعم @Mohammed_sn")



    elif option.startswith('refill:') :
        request_id , order_id = option.split(':')[1:]

        url = 'https://smmparty.com/api/v2'

        params = {
            'key' : 'dab3fac7cde4ca03f835688b83789674',
            'action' : 'refill',
            'order' : order_id
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url , params = params) as response:
                    response = await response.json()  
        except aiohttp.ClientError as e:
            response = {'status' : False}
            print(f"An error occurred: {e}")

        
        print(response)

        refill_id = response.get('refill')
        if refill_id :
            await query.message.reply_text('تم التقدم بطلب إعادة التعبئة بنجاح ✅\n'
                                           f"refill id : {refill_id}")
        else :
            await query.message.reply_text('حدث خطأ ما ❌\n'
                                           )



        











        










        



 
        




        



    


    

                
                
    
    





























































async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    text = update.message.text
    user_id = update.message.from_user.id
    username = functions.escape_markdown_v2(
        update.message.from_user.username) if update.message.from_user.username else "NONE"
    
    try :
        message_type = update.message.chat.type
        if message_type == 'channel'  or message_type == 'group' or message_type == 'supergroup':
            return
    except :
        None
    
    with open('side.json' , 'r') as f :
        blocked_list = json.load(f)['blocked_list']
    if str(user_id) in blocked_list :
        await update.message.reply_text("تم حظرك من قبل الدعم❌")
        return
    
    if not functions.ON and str(user_id) != OWNER_ID :
        await update.message.reply_text("البوت متوقف مؤقتا ⏳")
        return 
    
    
    if context.user_data['status'] == 'waiting topup id' :
        try :
            id = int(text)
        except :
            await update.message.reply_text("إدخال خاطئ يرجى إرسال أرقام فقط")
            return 
        
        context.user_data['trans_id'] = id
        
        await update.message.reply_text(f"يرجى إدخال المبلغ المرسل : ")
        
        context.user_data['status'] = 'waiting sent amount'
        
    elif context.user_data['status'] == 'waiting sent amount' :

        try :
            amount = int(text)
        except :
            await update.message.reply_text("إدخال خاطئ يرجى إرسال أرقام فقط")
            return 
        
        context.user_data['sent_amount'] = amount
        credit = get_gv('syr_credit')
        
        random_id = ''.join(random.choice(characters) for _ in range(10))
        buttons_ids[random_id] = f"{context.user_data['topup method']}:{context.user_data['trans_id']}:{context.user_data['sent_amount']}:{credit}"
        
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('تأكيد✔', callback_data = f"msr:{random_id}"),
                    InlineKeyboardButton('إلغاء❌', callback_data = 'cancle')
                ]
            ]
        )
        await update.message.reply_text(
                                            f"طريقة الشحن : {context.user_data['topup method']} \n"
                                            f"رقم العملية : {context.user_data['trans_id']}\n"
                                            f"المبلغ المرسل : {context.user_data['sent_amount']} \n"
                                            f"سعر ال $ : {credit}\n\n"
                                            f"يرجى تأكيد العملية" , reply_markup = keyboard)
        
        context.user_data['status'] = 'normal'
    
    
    
        
    elif context.user_data['status'] == 'waiting new price' :
        try :
            new_price = int(text)
        except :
            await update.message.reply_text("إدخال خاطئ يرجى إرسال أرقام فقط")
            return 
        
        game , offer , price = context.user_data['purchase_data'].split(':')
        
        with open('prices.json' , 'r' , encoding='utf-8') as file :
            prices = json.load(file)
        
        prices[game][offer] = new_price
        
        with open('prices.json' , 'w' , encoding='utf-8') as new :
            json.dump(prices, new)
            
        await update.message.reply_text(f'تم تحديث سعر {game} {offer} إلى {new_price} ✔')
        
        context.user_data['status'] = 'normal'


    elif context.user_data['status'] == 'waiting payeer sent amount' :
        try :
            amount = float(text)
        except :
            await update.message.reply_text("إدخال خاطئ يرجى إدخال أرقام فقط")
            return
        
        credit = get_gv('pay_credit')
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('تأكيد', callback_data=f"pay:{text}:{credit}"), # confirm payeer operation
                InlineKeyboardButton('إلغاء', callback_data='photo cancle')
            ]
        ]
        )
        
        await context.bot.send_photo(chat_id = user_id , photo = photo_files_ids[user_id] , caption = 
                                     f"طلب إيداع بايير\n"
                                     f"الكمية : {text}\n"
                                     f"سعر ال $ : {credit}\n\n"
                                     f"يرجى تأكيد الطلب" , reply_markup = keyboard)
        
        context.user_data['status'] = None




    

    elif context.user_data['status'] == 'waiting sham cash syrian sent amount' :
        try :
            amount = float(text)
        except :
            await update.message.reply_text("إدخال خاطئ يرجى إدخال أرقام فقط")
            return
        
        credit = get_gv('sham_cash_syr_credit')
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('تأكيد', callback_data=f"shamcash:{text}:{credit}"), # confirm sham cash operation
                InlineKeyboardButton('إلغاء', callback_data='photo cancle')
            ]
        ]
        )
        
        await context.bot.send_photo(chat_id = user_id , photo = photo_files_ids[user_id] , caption = 
                                     f"طلب إيداع شام كاش ليرة سورية\n"
                                     f"الكمية : {text}\n"
                                     f"سعر ال $ : {credit}\n\n"
                                     f"يرجى تأكيد الطلب" , reply_markup = keyboard)
        
        context.user_data['status'] = None


    elif context.user_data['status'] == 'waiting sham cash dollar sent amount' :
        try :
            amount = float(text)
        except :
            await update.message.reply_text("إدخال خاطئ يرجى إدخال أرقام فقط")
            return
        
        credit = get_gv('sham_cash_dol_credit')
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('تأكيد', callback_data=f"shamcash:{text}:{credit}"), # confirm sham cash operation
                InlineKeyboardButton('إلغاء', callback_data='photo cancle')
            ]
        ]
        )
        
        await context.bot.send_photo(chat_id = user_id , photo = photo_files_ids[user_id] , caption = 
                                     f"طلب إيداع شام كاش دولار\n"
                                     f"الكمية : {text}\n"
                                     f"سعر ال $ : {credit}\n\n"
                                     f"يرجى تأكيد الطلب" , reply_markup = keyboard)
        
        context.user_data['status'] = None


    



    elif context.user_data['status'] == 'waiting usdt sent amount' :
        try :
            amount = float(text)
        except :
            await update.message.reply_text("إدخال خاطئ يرجى إدخال أرقام فقط")
            return
        
        credit = 1
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('تأكيد', callback_data=f"usdt:{text}:{credit}"), # confirm usdt operation
                InlineKeyboardButton('إلغاء', callback_data='photo cancle')
            ]
        ]
        )
        
        await context.bot.send_photo(chat_id = user_id , photo = photo_files_ids[user_id] , caption = 
                                     f"طلب إيداع USDT\n"
                                     f"الكمية : {text}\n"
                                     f"سعر ال $ : 1\n\n"
                                     f"يرجى تأكيد الطلب" , reply_markup = keyboard)
        
        context.user_data['status'] = None




    elif context.user_data['status'] == 'waiting binance sent amount' :
        try :
            amount = float(text)
        except :
            await update.message.reply_text("إدخال خاطئ يرجى إدخال أرقام فقط")
            return
        
        credit = 1
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('تأكيد', callback_data=f"binconf:{text}:{credit}"), # confirm binance operation
                InlineKeyboardButton('إلغاء', callback_data='photo cancle')
            ]
        ]
        )
        
        await context.bot.send_photo(chat_id = user_id , photo = photo_files_ids[user_id] , caption = 
                                     f"طلب إيداع Binance\n"
                                     f"الكمية : {text}\n"
                                     f"سعر ال $ : 1\n\n"
                                     f"يرجى تأكيد الطلب" , reply_markup = keyboard)
        
        context.user_data['status'] = None



    elif context.user_data['status'] == 'waiting amount for social' :
        app , offer , min_amount = context.user_data['social data']
        try :
            wanted_amount = int(text)
        except :
            await update.message.reply_text('إدخال خاطئ يرجى إرسال أرقام فقط ❌')
            return
        
        if wanted_amount < min_amount :
            await update.message.reply_text(f"الحد الأدنى هو : {min_amount} {min_amount_texts[offer]} ❌")
            return
        
        context.user_data['social data'].append(wanted_amount)

        await update.message.reply_text('يرجى إرسال الرابط المطلوب الرشـق إليه : \n\n'
                                        f"{' يرجى قراءة هذه الرسالة بوضوح : 👇🏻 \n\nhttps://t.me/denji_sms/77' if app == 'Instagram' else ''}")
        context.user_data['status'] = 'waiting link for social'
    
    

    elif context.user_data['status'] == 'waiting link for social' :
        app , offer , min_amount , wanted_amount = context.user_data['social data']

        link = text

        with open('social_prices.json' , 'r' , encoding='utf-8' ) as file :
            social_data = json.load(file)
        
        amount_per_price = social_data[app][offer]['amount per price']
        price_per_amount = social_data[app][offer]['price']

        price = (wanted_amount / amount_per_price) * price_per_amount
        price = round(price , 2)

        random_id = ''.join(random.choice(characters) for _ in range(11))
        buttons_ids[random_id] = [app , offer , wanted_amount , link , price , price_per_amount]


        keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('تأكيد' , callback_data = f'socialconf:{random_id}')
                    ],
                    [
                        InlineKeyboardButton('إلغاء' , callback_data = 'cancel')
                    ]
                ]
            )
        
        view = {
                    "Tik Tok" : 'Tik tok - تيك توك 🖤',
                    'FaceBook' : 'FaceBook - فيسبوك 💙',
                    'Instagram' : 'Instagram - انستاغرام 💜'
                }
        app = view[app]

        imoji = {
                    'متابعين بدون ضمان' : 'متابعين بدون ضمان 👤❌',
                    'متابعين ضمان سنة' : 'متابعين ضمان سنة 👤✅' ,
                    'لايكات' : 'لايكات 👍' , 
                    'مشاهدات' : 'مشاهدات ▶️'
                }
        
        offer = imoji[offer]

        await update.message.reply_text(f"التطبيق : {app} \n"
                                        f"الخدمة : {offer} \n"
                                        f"الكمية : {wanted_amount} \n"
                                        f"السعر : {price} $\n"
                                        f"الرابط : {link}\n\n"
                                        f"يرجى تأكيد العملية :" , reply_markup = keyboard)

        context.user_data['status'] = None

    























































    # owner


    elif context.user_data['status'] == 'owner waiting data to add balance' : 
        try :
            list_text = text.split(' ')
            if len(list_text) != 2 :
                await update.message.reply_text('إدخال خاطئ يرجى إعادة الإدخال')
                return
            
            user , amount = list_text
            amount = float(amount)
            user = int(user)

            # Connect to database
            conn = functions.connect_db()
            cursor = conn.cursor()

            # Check if user exists
            cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) FROM users WHERE id = ?', (user,))
            user_data = cursor.fetchone()

            if user_data is None:
                await update.message.reply_text(f"❌ المستخدم {user}  غير موجود في سجلات المستخدمين ")
                conn.close()
                return

            # Update user's balance
            current_balance = user_data[0]
            new_balance = current_balance + amount

            cursor.execute('UPDATE users SET balance = ROUND(?, 2) WHERE id = ?', (new_balance, user))
            conn.commit()
            
            cursor.execute('''INSERT INTO added_manually (user_id , added_amount , type ) VALUES (? ,? , 'إضافة رصيد')''' , (user,amount))
            conn.commit()

            # Get username if available
            cursor.execute('SELECT username , name FROM users WHERE id = ?', (user,))
            username_result = cursor.fetchone()
            username = username_result[0] if username_result and username_result[0] else "N/A"
            name = username_result[1]

            # Close database connection
            conn.close()

            # Send confirmation messages
            success_message = (
                f"✅ تم تحديث الرصيد!\n\n"
                f"User ID: {user}\n"
                f"المعرف : @{username}\n"
                f"الاسم : {name}\n"
                f"الرصيد القديم : {current_balance}\n"
                f"الكمية المضافة: {amount}\n"
                f"الرصيد الجديد: {new_balance}"
            )
            await update.message.reply_text(success_message)

            # Notify the user about their balance update
            try:
                user_message = (
                    f"💰 تم تحديث رصيدك!\n"
                    f"الكمية المضافة: {amount}\n"
                    f"الرصيد الجديد: {new_balance}"
                )
                await context.bot.send_message(chat_id=user, text=user_message)
            except Exception as e:
                await update.message.reply_text("لم أتمكن من إرسال الإشعار إلى المستخدم❌")
            
            context.user_data['status'] = None
        
        except Exception as e :
            print(e)
            await update.message.reply_text('حدث خطأ ما يرجى إعادة الإرسال❌')


    


    elif context.user_data['status'] == 'owner waiting data to remove balance' : 
        try :
            list_text = text.split(' ')
            if len(list_text) != 2 :
                await update.message.reply_text('إدخال خاطئ يرجى إعادة الإدخال')
                return
            
            user , amount = list_text
            amount = float(amount)
            user = int(user)


            # Connect to database
            conn = functions.connect_db()
            cursor = conn.cursor()

            # Check if user exists
            cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) FROM users WHERE id = ?', (user,))
            user_data = cursor.fetchone()

            if user_data is None:
                await update.message.reply_text(f"❌ المستخدم {user}  غير موجود في سجلات المستخدمين")
                conn.close()
                return

            # Update user's balance
            current_balance = user_data[0]
            new_balance = current_balance - amount
            if new_balance < 0 :
                amount = current_balance
                new_balance = 0

            cursor.execute('UPDATE users SET balance = ROUND(?, 2) WHERE id = ?', (new_balance, user))
            conn.commit()


            cursor.execute('''INSERT INTO added_manually (user_id , added_amount , type ) VALUES (? ,? , 'حذف رصيد')''' , (user,amount))
            conn.commit()


            # Get username if available
            cursor.execute('SELECT username , name FROM users WHERE id = ?', (user,))
            username_result = cursor.fetchone()
            username = username_result[0] if username_result and username_result[0] else "N/A"
            name = username_result[1]

            # Close database connection
            conn.close()

            # Send confirmation messages
            success_message = (
                f"✅ تم تحديث الرصيد!\n\n"
                f"User ID: {user}\n"
                f"المعرف : @{username}\n"
                f"الاسم : {name}\n"
                f"الرصيد القديم : {current_balance}\n"
                f"الكمية المسحوبة: {amount}\n"
                f"الرصيد الجديد: {new_balance}"
            )
            await update.message.reply_text(success_message)

            # Notify the user about their balance update
            try:
                user_message = (
                    f"💰 تم تحديث رصيدك!\n"
                    f"المبلغ المسحوب: {amount}\n"
                    f"الرصيد الجديد: {new_balance}"
                )
                await context.bot.send_message(chat_id=user, text=user_message)
            except Exception as e:
                await update.message.reply_text("لم أتمكن من إرسال الإشعار إلى المستخدم❌" )

            context.user_data['status'] = None
        
        except Exception as e :
            print(e)
            await update.message.reply_text('حدث خطأ ما يرجى إعادة الإرسال❌')


    
    elif context.user_data['status'] == 'owner waiting id to block user' :
        try :
            user = int(text)


            with open('side.json' , 'r') as f :
                data = json.load(f)
            data['blocked_list'].append(text)
            with open('side.json' , 'w') as new_f :
                json.dump(data, new_f)
            await update.message.reply_text(f'تم حظر المستخدم : {text} ✔️')

            context.user_data['status'] = None
        except Exception as e :
            print(e)
            await update.message.reply_text('حدث خطأ ما يرجى إعادة الإرسال❌')

    
    elif context.user_data['status'] == 'owner waiting id to unblock user' :
        try :
            user = int(text)

            with open('side.json' , 'r') as f :
                data = json.load(f)
            data['blocked_list'].remove(text)
            with open('side.json' , 'w') as new_f :
                json.dump(data, new_f)
            await update.message.reply_text(f'تم فك حظر المستخدم : {text} ✔️')

        except Exception as e :
            print(e)
            await update.message.reply_text('حدث خطأ ما يرجى إعادة الإرسال❌')




    elif context.user_data['status'] == 'owner waiting new api' :
        provider = context.user_data['provider to change api']

        if provider == 'lion BOT' : 
            data = get_json('lion_bot.json')
            data['api_token'] = text
            with open('lion_bot.json' , 'w' , encoding='utf-8') as n :
                json.dump(data , n)
        
        elif provider == 'VIOTP' : 
            data = get_json('viotp.json')
            data['api_token'] = text
            with open('viotp.json' , 'w' , encoding='utf-8') as n :
                json.dump(data , n)
            
        elif provider == 'Drop SMS BOT' : 
            data = get_json('dropsms.json')
            data['api_token'] = text
            with open('dropsms.json' , 'w' , encoding='utf-8') as n :
                json.dump(data , n)
        
        elif provider == 'SMS live' :
            data = get_json('smslive.json')
            data['api_token'] = text
            with open('smslive.json' , 'w' , encoding='utf-8') as n :
                json.dump(data , n)
        
        elif provider == 'durianrcs' :
            data = get_json('durancies.json')
            data['api_token'] = text
            with open('durancies.json' , 'w' , encoding='utf-8') as n :
                json.dump(data , n)

        await update.message.reply_text(f'تم تحديث توكن {provider} إلى : \n\n {text}')
        context.user_data['status'] = None



    elif context.user_data['status'] == 'owner waiting new credit price' :
        way = context.user_data['way to change credit']

        if way == 'syriatel' :
            try :
                new = int(text)
            except :
                await update.message.reply_text('يرجى إدخال أرقام فقط ❌')
                return
            side_data = get_json('side.json')
            side_data['syr_credit'] = new
            with open('side.json' , 'w' , encoding='utf-8') as n :
                json.dump(side_data, n)
        
        elif way == 'payeer' : 
            try :
                new = float(text)
            except :
                await update.message.reply_text('يرجى إدخال أرقام فقط ❌')
                return
            side_data = get_json('side.json')
            side_data['pay_credit'] = new
            with open('side.json' , 'w' , encoding='utf-8') as n :
                json.dump(side_data, n)

        elif way == 'shamsyr' :
            try :
                new = int(text)
            except :
                await update.message.reply_text('يرجى إدخال أرقام فقط ❌')
                return
            side_data = get_json('side.json')
            side_data['sham_cash_syr_credit'] = new
            with open('side.json' , 'w' , encoding='utf-8') as n :
                json.dump(side_data, n)
        
        elif way == 'shamdol' :
            try :
                new = float(text)
            except :
                await update.message.reply_text('يرجى إدخال أرقام فقط ❌')
                return
            side_data = get_json('side.json')
            side_data['sham_cash_dol_credit'] = new
            with open('side.json' , 'w' , encoding='utf-8') as n :
                json.dump(side_data, n)

        
        
        await update.message.reply_text(f'تم تحديث سعر دولار {way} إلى \n\n {new}')
    

    elif context.user_data['status'] == 'owner waiting all message' :
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('تأكيد', callback_data = 'confirmingallmessage')]
            ]
        )
        await update.message.reply_text(text, reply_markup = keyboard)
        context.user_data['status'] = None

    elif context.user_data['status'] == 'owner waiting personal message user id' :
        context.user_data['personal message user id'] = text
        await update.message.reply_text('قم بإرسال الرسالة المرغوبة')
        context.user_data['status'] = 'owner waiting personal message text'
    
    elif context.user_data['status'] == 'owner waiting personal message text' :

        button_id = functions.create_random_string(10)
        buttons_ids[button_id] = [context.user_data['personal message user id'] , text]
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('تأكيد', callback_data = f'confirmpersonalmessage:{button_id}')]
            ]
        )
        await update.message.reply_text(f'المستخدم : {context.user_data['personal message user id']}\n\n'
                                        f"الرسالة : {text}" , reply_markup = keyboard)
        
    elif context.user_data['status'] == 'owner waiting user id to get his data' :
        conn = functions.connect_db()
        c = conn.cursor()
        c.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)), name , username , CAST(ROUND(total_spent, 2) AS DECIMAL(10,2))   FROM users WHERE id = ?', (text,))
        result = c.fetchone()
        conn.close()

        button = functions.create_telegram_check_button(text)
        if result :
            balance, name , username, points = result
            await update.message.reply_text(f"المستخدم : {text}\n"
                                            f"الاسم : {functions.escape_markdown_v2(name)}\n"
                                            f"الرصيد : {functions.escape_markdown_v2(balance)}\n"
                                            f"المعرف : @{functions.escape_markdown_v2(username)}\n"
                                            f"النقاط : {functions.escape_markdown_v2(str(points))}" , parse_mode = "MarkdownV2" , reply_markup = button)
        else :
            await update.message.reply_text(f'المستخدم : {text} غير موجود في جدول المستخدمين')
        
        context.user_data['status'] = None

    elif context.user_data['status'] == 'owner waiting to change topup link' :
        way = context.user_data['way to change the link']

        if way == 'syr' :
            numbers = text.split(' ')
            text = ''
            for number in numbers :
                text += f'\\- `{number}`\n'
            
            data = get_json('side.json')
            data[way] = text
            with open('side.json' , 'w' , encoding='utf-8') as n :
                json.dump(data, n)

            await update.message.reply_text(f'تم تحديث عنوان {functions.escape_markdown_v2(way)} إلى  \n\n{text}', parse_mode = ParseMode.MARKDOWN_V2)

        
        else :
            data = get_json('side.json')
            data[way] = text
            with open('side.json' , 'w' , encoding='utf-8') as n :
                json.dump(data, n)
        
            await update.message.reply_text(f'تم تحديث عنوان {functions.escape_markdown_v2(way)} إلى \n\n{functions.escape_markdown_v2(text)}', parse_mode = ParseMode.MARKDOWN_V2)
        context.user_data['status'] = None

    elif context.user_data['status'] == 'owner waiting new price for viotp' :
        app , id = context.user_data['viotp change price data']
        try :
            new = float(text)
        except :
            await update.message.reply_text('يرجى إدخال أرقام فقط ❌')
            return

        prices = get_json('prices.json')
        prices[app]['vn']['viotp'][id] = new
        with open('prices.json' , 'w' , encoding='utf-8') as n :
            json.dump(prices, n)
        
        viotp_data = get_json('viotp.json')
        network = viotp_data['providers'][id]
        await update.message.reply_text(f'تم تحديث سعر viotp {app} فيتنام {network} إلى {new}')
        context.user_data['status'] = None

    
    elif context.user_data['status'] == 'owner waiting to change lion price' :
        code = context.user_data['lion data to change price']
        try :
            new = float(text)
        except :
            await update.message.reply_text('يرجى إدخال أرقام فقط ❌')
            return

        data = get_json('lion_bot.json')
        data['prices'][code] = new
        with open('lion_bot.json' , 'w' , encoding='utf-8') as n :
            json.dump(data, n)
        
        await update.message.reply_text(f'تم تحديث سعر lion bot {data['names'][code]} إلى {new}')
        context.user_data['status'] = None

    
    elif context.user_data['status'] == 'owner waiting new price for drop sms change price' :
        app , country_code , code = context.user_data['data drop sms to change price']

        try :
            new = float(text)
        except :
            await update.message.reply_text('يرجى إدخال أرقام فقط ❌')
            return
        
        prices = get_json('prices.json')
        prices[app][country_code]['drop_sms'][code] = new
        with open('prices.json' , 'w' , encoding='utf-8') as n :
            json.dump(prices, n)
        
        drop_sms_data = get_json('dropsms.json')
        country_name = drop_sms_data['names'][code]
        await update.message.reply_text(f'تم تحديث سعر drop sms {app} {country_name} إلى {new}')
        context.user_data['status'] = None
    
    elif context.user_data['status'] == 'owner waiting new price for sms live change price' :
        app , country_code , code = context.user_data['data sms live to change price']

        try :
            new = float(text)
        except :
            await update.message.reply_text('يرجى إدخال أرقام فقط ❌')
            return
        
        prices = get_json('prices.json')
        prices[app][country_code]['sms_live'][code] = new
        with open('prices.json' , 'w' , encoding='utf-8') as n :
            json.dump(prices, n)
        
        sms_live_data = get_json('smslive.json')
        country_name = sms_live_data['names'][code]
        await update.message.reply_text(f'تم تحديث سعر sms live {app} {country_name} إلى {new}')
        context.user_data['status'] = None
    


    elif context.user_data['status'] == 'owner waiting new price for durancies change price' :
        app , country_code , code = context.user_data['data durancies to change price']

        try :
            new = float(text)
        except :
            await update.message.reply_text('يرجى إدخال أرقام فقط ❌')
            return
        
        prices = get_json('prices.json')
        prices[app][country_code]['duriancrs'][code] = new
        with open('prices.json' , 'w' , encoding='utf-8') as n :
            json.dump(prices, n)
        
        durancies_data = get_json('durancies.json')
        country_name = durancies_data['names'][code]
        await update.message.reply_text(f'تم تحديث سعر duriancrs {app} {country_name} إلى {new}')
        context.user_data['status'] = None
    
    


    elif context.user_data['status'] == 'owner waiting new social media price' :
        try :
            new_price = float(text)
        except :
            await update.message.reply_text('يرجى إدخال أرقام فقط ❌')
            return
        
        app , offer = context.user_data['owner data to change price']

        with open('social_prices.json' , 'r' , encoding='utf-8') as file :
            sd = json.load(file)
        
        sd[app][offer]['price'] = new_price

        with open('social_prices.json' , 'w' , encoding='utf-8') as nfile :
            json.dump(sd , nfile)
        
        await update.message.reply_text(f'تم تحديث سعر {app} {offer} إلى {new_price} ✅')
        context.user_data['status'] = None

    
    elif context.user_data['status'] == 'owner waiting new social media id' :
        new_id = text
        
        app , offer = context.user_data['owner data to change id']

        with open('social_prices.json' , 'r' , encoding='utf-8') as file :
            sd = json.load(file)
        
        sd[app][offer]['api_id'] = new_id

        with open('social_prices.json' , 'w' , encoding='utf-8') as nfile :
            json.dump(sd , nfile)
        
        await update.message.reply_text(f'تم تحديث ايدي {app} {offer} إلى {new_id} ✅')
        context.user_data['status'] = None



    
    
     

    
    

    
        
        





























photo_files_ids = {}

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    photo_file_id = update.message.photo[-1].file_id
    photo_files_ids[user_id] = photo_file_id

    with open('side.json' , 'r') as f :
        blocked_list = json.load(f)['blocked_list']
    if str(user_id) in blocked_list :
        await update.message.reply_text("تم حظرك من قبل الدعم❌")
        return
    
    if not functions.ON and str(user_id) != OWNER_ID :
        await context.bot.send_message(chat_id = user_id, text = "البوت متوقف مؤقتا ❤")
        return
    
    

    if context.user_data['status'] == 'waiting payeer screen shot'  :
        await update.message.reply_text('يرجى إدخال المبلغ المرسل بال $')
        context.user_data['status'] = 'waiting payeer sent amount'

    elif context.user_data['status'] == 'waiting usdt screen shot'  :
        await update.message.reply_text('يرجى إدخال المبلغ المرسل بال $')
        context.user_data['status'] = 'waiting usdt sent amount'

    elif context.user_data['status'] == 'waiting binance screen shot' : 
        await update.message.reply_text('يرجى إدخال المبلغ المرسل بال $')
        context.user_data['status'] = 'waiting binance sent amount'
    
    
    
    elif context.user_data['status'] == 'waiting sham cash syrian screen shot' : 
        await update.message.reply_text('يرجى إدخال المبلغ المرسل بالليرة السورية')
        context.user_data['status'] = 'waiting sham cash syrian sent amount'

    elif context.user_data['status'] == 'waiting sham cash dollar screen shot' : 
        await update.message.reply_text('يرجى إدخال المبلغ المرسل بال $')
        context.user_data['status'] = 'waiting sham cash dollar sent amount'

        