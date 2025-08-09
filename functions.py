import re
import sqlite3
import json
import requests
import random
import string

from telegram import Update, InlineKeyboardMarkup, ChatMember, InlineKeyboardButton


from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes
    

from telegram.constants import ParseMode

import keyboards
# OWNER_ID = '5349543151'
OWNER_ID = '5363898935'

import aiohttp


ON = True


def escape_markdown_v2(text):
    try : 
        text = str(text)
        escape_chars = r'_*[]()~`>#+-=|{}.!'
        return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text)
    except :
        return 'None'


def connect_db():
    return sqlite3.connect('denji.db')


def create_random_string(length=32) :
    characters = string.ascii_letters + string.digits
    random_str = ''.join(random.choices(characters , k=length))
    return random_str




async def check_membership(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    # channel_id = '-1002298536366'
    # channel_id2  = '-1002297021090'
    channel_id2  = '@abbas_IT_bots'
    channel_id = '@abbas_IT_bots'


    member = await context.bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    member2 = await context.bot.get_chat_member(chat_id=channel_id2, user_id=user_id)

    if member.status in [ChatMember.ADMINISTRATOR, ChatMember.MEMBER, 'creator'] and member2.status in [ChatMember.ADMINISTRATOR, ChatMember.MEMBER, 'creator']:
        return True
    else:
        return False








async def get_topup_record(user_id) :
    user_id = int(user_id)
    with sqlite3.connect('denji.db') as conn :
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM topup_requests WHERE user_id = ?',(user_id,))
        result = cursor.fetchall()
    
    return result








async def get_account(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    if str(update.message.from_user.id) != OWNER_ID:
        await update.message.reply_text("⚠️ ليس لديك الصلاحية لتنفيذ هذا الأمر")
        return
    
    # Check if correct number of arguments are provided
    if len(context.args) != 1:
        await update.message.reply_text("❌ صيغة خاطئة , استخدم: /account id")
        return

    try:
        id = str(context.args[0])

        conn = connect_db()
        c = conn.cursor()
        c.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)), name , username , CAST(ROUND(total_spent, 2) AS DECIMAL(10,2))   FROM users WHERE id = ?', (id,))
        result = c.fetchone()

        conn.close()
        balance, name , username, points = result
        await update.message.reply_text(f"المستخدم : {id}\n"
                                        f"الاسم : {escape_markdown_v2(name)}\n"
                                        f"الرصيد : {escape_markdown_v2(balance)}\n"
                                        f"المعرف : @{escape_markdown_v2(username)}\n"
                                        f"النقاط : {escape_markdown_v2(str(points))}" , parse_mode = "MarkdownV2")
        

        
        


    except ValueError:
        await update.message.reply_text("❌ كمية خاطئة أو رقم تعريفي خاطئ يرجى استخدام أرقام فقط")
    except Exception as e:
        await update.message.reply_text(f"❌ An error occurred: {str(e)}")
       # logging.error(f"Error in add_balance: {str(e)}")




async def account(user_id) :
    with sqlite3.connect('denji.db') as conn :
        cursor = conn.cursor()
        cursor.execute('SELECT name, CAST(ROUND(balance, 2) AS DECIMAL(10,2)), CAST(ROUND(total_spent, 2) AS DECIMAL(10,2))  FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
    
    name, balance, total_spent = result
    return (name, balance, total_spent)






async def change_syr(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    if str(update.message.from_user.id) != OWNER_ID:
        await update.message.reply_text("⚠️ ليس لديك الصلاحية لتنفيذ هذا الأمر")
        return
    
    # Check if correct number of arguments are provided
    if len(context.args) == 0 :
        await update.message.reply_text("❌ صيغة خاطئة , استخدم: /syr numbers")
        return
    
    numbers = ''
    for number in context.args :
        numbers += f" `{number}` \n"
    
    keyboards.syr = numbers
    
    await update.message.reply_text(f"تم تحديث أرقام سيريتل إلى {numbers}")
    
    
    







async def change_usd(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    if str(update.message.from_user.id) != OWNER_ID:
        await update.message.reply_text("⚠️ ليس لديك الصلاحية لتنفيذ هذا الأمر")
        return
    
    # Check if correct number of arguments are provided
    if len(context.args) == 0 :
        await update.message.reply_text("❌ صيغة خاطئة , استخدم: /usd price")
        return
    
    try :
        new = int(context.args[0])
        keyboards.usd = new
    
    except :
        await update.message.reply_text(f"إدخال خاطئ")
        return
    
    await update.message.reply_text(f"تم تحديث سعر الدولار إلى {new}")





def split_list(lst, size):
    return [lst[i:i + size] for i in range(0, len(lst), size)]



async def logout_lion(number , api_key , owner_id) : 
    url = f'https://TG-Lion.net?action=logout_number&number={number}&apiKey={api_key}&YourID={owner_id}'

    try :
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response = await response.json() 

        if response['message'].startswith('Successfully logged out and deleted number') :
            return True
        else :
            return False
    except :
        return False




def create_telegram_check_button(user_id) :
    button = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('تحقق من المستخدم' , url = f'tg://openmessage?user_id={user_id}')
        ]
    ]
)
    
    return button


def create_refill_button(request_id , order_id) : 
    button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('إعادة التعبئة' , callback_data = f'refill:{request_id}:{order_id}')
                ]
            ]
        )
    
    return button








def cal(user , cursor) :
    accepted_topup = 0
    successful_number_buy = 0
    successful_social_buy = 0
    added_removed_manual = 0
    
    cursor.execute('SELECT name , username , balance FROM users WHERE id = ?',(user,))
    data = cursor.fetchone()
    name, username ,balance = data

    cursor.execute('''SELECT amount_added FROM topup_requests WHERE user_id = ? AND (status = 'مقبول' OR status = 'approved' )''' , (user,))
    top = cursor.fetchall()
    for op in top :
        amount = op[0]
        
        
        
        accepted_topup += amount
        

    cursor.execute('''SELECT request_id, price FROM item_requests WHERE (status = 'منتهية' OR status = 'مفعل' OR code IS NOT NULL) AND user_id = ? ''',(user,))
    numbers = cursor.fetchall()

    for op in numbers :
        req , price = op
        successful_number_buy += price
        
    

    cursor.execute('''SELECT price , refunded FROM social_requests WHERE (status = 'مقبول' OR status = 'في الانتظار' OR status = 'مقبول جزئيا' )  AND user_id = ? ''',(user,))
    socials = cursor.fetchall()

    for op in socials :
        price , refunded = op
        if refunded :
            successful_social_buy += price - refunded
        else :
            successful_social_buy += price
        
    

    cursor.execute('SELECT added_amount , type FROM added_manually WHERE user_id = ? ',(user,))
    manual = cursor.fetchall()

    for op in manual :
        amount , type = op
        if type == 'إضافة رصيد' :
            added_removed_manual += amount
        elif type == 'حذف رصيد' :
            added_removed_manual -= amount
    
    total_revenue = accepted_topup + added_removed_manual - balance - successful_number_buy - successful_social_buy  # if positive , we he needs , if negative, we need

    return name , username , balance , accepted_topup , added_removed_manual , successful_number_buy , successful_social_buy , total_revenue




async def record(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    if str(update.message.from_user.id) != '5349543151' and str(update.message.from_user.id) != OWNER_ID :
        await update.message.reply_text("⚠️ ليس لديك الصلاحية لتنفيذ هذا الأمر")
        return
    
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE id <> 5349543151 AND id <> 5363898935 AND id <> 6313379271 AND id <> 1693441250 AND id <> 6306691535')
    users = cursor.fetchall()

    text = ''
    total = 0
    data = {}
    for user in users :
        user = user[0]
        name , username , balance , accepted_topup , added_removed_manual , successful_number_buy , successful_social_buy , total_revenue = cal(user , cursor )
        total_revenue = round(total_revenue, 2)
        total += total_revenue
        data[str(user)] = {}
        data[str(user)]['name']  = name
        data[str(user)]['username']  = username
        data[str(user)]['balance']  = balance
        data[str(user)]['accepted_topup']  = accepted_topup
        data[str(user)]['added_removed_manual']  = added_removed_manual
        data[str(user)]['successful_number_buy']  = successful_number_buy
        data[str(user)]['successful_social_buy']  = successful_social_buy
        data[str(user)]['total_revenue']  = total_revenue

        if total_revenue != 0 :
            text += f"{user} : {total_revenue} \n"
        
    
    text += f" ------------------------ \n {total}"


    conn.close()

    with open('record.json' , 'w' , encoding= 'utf-8') as file :
        json.dump(data , file)

    await update.message.reply_text(text)
    
    
        
    

