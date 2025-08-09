import sqlite3
from telegram import Bot



import time
import json
import asyncio

import requests
import functions

from telegram.constants import ParseMode

TOKEN = '8004725012:AAGJAkWMb9rEtZxMdGmU2S2PZ93i2M21UCo'
# TOKEN = '7718105050:AAFDSOl-EE4axZ7FO51J4YlFDq9OXvSpANg' # my test


# request = Request(connect_timeout = 20, read_timeout = 20)
bot = Bot(token = TOKEN)


async def send(user_id, text) :
    await bot.send_message(chat_id = user_id, text =text )


async def accepted(text , reply_markup = None) :
    await bot.send_message(chat_id = '-1002879904667', text =text , reply_markup = reply_markup , parse_mode= ParseMode.MARKDOWN_V2 )

async def rejected(text) :
    await bot.send_message(chat_id = '-1002849483030', text =text , parse_mode= ParseMode.MARKDOWN_V2 )

async def partial(text , reply_markup = None) :
    await bot.send_message(chat_id = '-1002822978724', text =text , reply_markup = reply_markup , parse_mode= ParseMode.MARKDOWN_V2)






loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)



print('started')
while True :
    try :
        with open('side.json' , 'r' , encoding='utf-8') as f :
            data = json.load(f)
        
        requests_list = data['social_pending']
        
        to_remove = []

        

        for order_id in requests_list :
            time.sleep(4)

            try :

                url = "https://smmparty.com/api/v2"
                
                params = {
                    'key' : 'dab3fac7cde4ca03f835688b83789674',
                    'action' : 'status',
                    'order' : order_id

                }
                try :
                    response = requests.get(url , params=params , timeout=(10, 10))
                    response = response.json()
                except :
                    continue   
                
                

                print(response)


                status = response['status']

                if status == 'Completed' :  # to fix 
                    time.sleep(1)
                    try :
                        with sqlite3.connect('denji.db') as conn :
                            cursor = conn.cursor()
                            cursor.execute('SELECT request_id, user_id, app , service , amount , link , price  FROM social_requests WHERE auto_id = ?', (order_id,))
                            result = cursor.fetchone()
                            request_id, user_id, app , offer , amount , link , price  = result

                            cursor.execute('''UPDATE social_requests SET status = 'مقبول' WHERE auto_id = ? ''', (order_id,))
                            conn.commit()
                            
                            cursor.execute('SELECT name, username FROM users WHERE id = ?' , (user_id,))
                            name ,username = cursor.fetchone()
                    except Exception as e:
                        print('the accepting', e)
                    
                    time.sleep(1)

                    
                    
                    added_points = price

                    
                    #updating total spent money :
                    try :
                        with sqlite3.connect('denji.db') as conn :
                            cursor = conn.cursor()
                            cursor.execute('''
                                UPDATE users
                                SET total_spent = total_spent + ?
                                WHERE id = ?
                            ''',(added_points , user_id ,))
                                
                            conn.commit()
                    except Exception as e :
                        print( 'updating total spent', e)

                    view = {
                                "Tik Tok" : 'Tik tok - تيك توك 🖤',
                                'FaceBook' : 'FaceBook - فيسبوك 💙',
                                'Instagram' : 'Instagram - انستاغرام 💜'
                            }
                    app_view = view[app]

                    imoji = {
                                'متابعين بدون ضمان' : 'متابعين بدون ضمان 👤❌',
                                'متابعين ضمان سنة' : 'متابعين ضمان سنة 👤✅' ,
                                'لايكات' : 'لايكات 👍' , 
                                'مشاهدات' : 'مشاهدات ▶️'
                            }
                    
                    offer_view = imoji[offer]

                    text = (f"تم تنفيذ طلبك رقم {request_id} لشحن {app_view} \n"
                    f"الخدمة : {offer_view}\n"
                    f"الكمية : {amount}\n"
                    f"الرابط : {link}\n"
                    f"شكرا لاستخدامكم متجر Denji ❤")

                    time.sleep(1)
                    try :
                        loop.run_until_complete(send(user_id, text))
                    except Exception as e :
                        print( 'telling the user' , e)

                    if offer == 'متابعين ضمان سنة':
                        button = functions.create_refill_button(request_id , order_id)
                    else :
                        button = None

                    done_text = (f"عملية ناجحة : \n\n"
                    f"رقم العملية : `{request_id}` \n"
                    f"رقم الطلب في الموقع : `{order_id}` \n"
                    f"التطبيق : {functions.escape_markdown_v2(app)}\n"
                    f"الخدمة : {functions.escape_markdown_v2(offer)}\n"
                    f"الكمية : {functions.escape_markdown_v2(amount)}\n"
                    f"الرابط : {functions.escape_markdown_v2(link)}\n"
                    f"السعر : {functions.escape_markdown_v2(price)}\n"
                    f"المستخدم : `{user_id}`\n"
                    f"الاسم : {functions.escape_markdown_v2(name)} \n"
                    f"المعرف : @{functions.escape_markdown_v2(username)}"
                    )

                    time.sleep(1)
                    try :
                        loop.run_until_complete(accepted(done_text , button))
                
                        to_remove.append(order_id)
                    except Exception as e :
                        print( 'sending to success group', e)

                elif status == 'Canceled' :    
                    time.sleep(1)
                    try :
                        with sqlite3.connect('denji.db') as conn :
                            cursor = conn.cursor()
                            cursor.execute('SELECT request_id, user_id, app , service , amount , link , price , refunded FROM social_requests WHERE auto_id = ?', (order_id,))
                            result = cursor.fetchone()
                            request_id, user_id, app , offer , amount , link , price , refunded = result

                            cursor.execute('''UPDATE social_requests SET status = 'مرفوض' WHERE auto_id = ? ''', (order_id,))
                            conn.commit()
                            
                            cursor.execute('SELECT name , username FROM users WHERE id = ?' , (user_id,))
                            name , username = cursor.fetchone()
                    except Exception as e :
                        print('the rejecting' ,e)

                    if refunded :
                        to_remove.append(order_id)
                        continue

                    time.sleep(1)
                    try :

                        with sqlite3.connect('denji.db') as conn :
                            cursor = conn.cursor()
                            cursor.execute('''
                                UPDATE users
                                SET balance = balance + ?
                                WHERE id = ?
                            ''',(price , user_id ,))
                            conn.commit()

                            cursor.execute('SELECT balance FROM users WHERE id = ?',(user_id,))
                            user_data = cursor.fetchone()
                            new_b = user_data[0]


                            cursor.execute('UPDATE social_requests SET balance_after_refund = ? , refunded = ?  WHERE request_id = ?',(new_b , price , request_id))
                                
                            conn.commit()
                    except Exception as e :
                        print( 'refunding' , e)

                    view = {
                                "Tik Tok" : 'Tik tok - تيك توك 🖤',
                                'FaceBook' : 'FaceBook - فيسبوك 💙',
                                'Instagram' : 'Instagram - انستاغرام 💜'
                            }
                    app_view = view[app]

                    imoji = {
                                'متابعين بدون ضمان' : 'متابعين بدون ضمان 👤❌',
                                'متابعين ضمان سنة' : 'متابعين ضمان سنة 👤✅' ,
                                'لايكات' : 'لايكات 👍' , 
                                'مشاهدات' : 'مشاهدات ▶️'
                            }
                    
                    offer_view = imoji[offer]

                    text = (f"لم نتمكن من تنفيذ طلبك رقم {request_id} لشحن {app_view} \n"
                    f"الخدمة : {offer_view}\n"
                    f"الكمية : {amount}\n"
                    f"الرابط : {link}\n"
                    f"تم إعادة المبلغ المدفوع \n"
                    f"يرجى التواصل مع الدعم @Mohammed_sn")

                    time.sleep(1)
                    try :
                        loop.run_until_complete(send(user_id, text))
                    except Exception as e :
                        print( 'while telling the user reject' , e)

                    done_text = (f"عملية فاشلة : \n\n"
                    f"رقم العملية : `{request_id}`\n"
                    f"رقم الطلب في الموقع : `{order_id}`\n"
                    f"التطبيق : {functions.escape_markdown_v2(app)}\n"
                    f"الخدمة : {functions.escape_markdown_v2(offer)}\n"
                    f"الكمية : {functions.escape_markdown_v2(amount)}\n"
                    f"الرابط : {functions.escape_markdown_v2(link)}\n"
                    f"السعر : {functions.escape_markdown_v2(price)}\n"
                    f"المستخدم : `{user_id}`\n"
                    f"الاسم : {functions.escape_markdown_v2(name)} \n"
                    f"المعرف : @{functions.escape_markdown_v2(username)}"
                    )

                    time.sleep(1)
                    try :
                        loop.run_until_complete(rejected(done_text))
                        to_remove.append(order_id)
                    except Exception as e :
                        print( 'sending to fail group' , e)

                elif status == 'Partial' :    
                    time.sleep(1)
                    try :
                        with sqlite3.connect('denji.db') as conn :
                            cursor = conn.cursor()
                            cursor.execute('SELECT request_id, user_id, app , service , amount , link , price , refunded FROM social_requests WHERE auto_id = ?', (order_id,))
                            result = cursor.fetchone()
                            request_id, user_id, app , offer , amount , link , price , refunded = result

                            cursor.execute('''UPDATE social_requests SET status = 'مقبول جزئيا' WHERE auto_id = ? ''', (order_id,))
                            conn.commit()
                            
                            cursor.execute('SELECT name , username FROM users WHERE id = ?' , (user_id,))
                            name , username = cursor.fetchone()
                    except Exception as e :
                        print('the rejecting' ,e)

                    
                    if refunded :
                        to_remove.append(order_id)
                        continue
                    
                    remained = int(response['remains'])

                    remain_percent = remained / amount

                    must_refund = float(price * remain_percent)
                    must_refund = round(must_refund , 2)


                    time.sleep(1)
                    try :

                        with sqlite3.connect('denji.db') as conn :
                            cursor = conn.cursor()
                            
                            cursor.execute('''
                                UPDATE users
                                SET balance = balance + ?
                                WHERE id = ?
                            ''',(must_refund , user_id ,))
                                
                            conn.commit()

                            cursor.execute('SELECT balance FROM users WHERE id = ?',(user_id,))
                            ud = cursor.fetchone()
                            new_b = ud[0]

                            cursor.execute('UPDATE social_requests SET balance_after_refund = ? , refunded = ? , remained = ? WHERE request_id = ?',(new_b , must_refund , int(remained) , request_id))
                    except Exception as e :
                        print( 'refunding' , e)


                    view = {
                                "Tik Tok" : 'Tik tok - تيك توك 🖤',
                                'FaceBook' : 'FaceBook - فيسبوك 💙',
                                'Instagram' : 'Instagram - انستاغرام 💜'
                            }
                    app_view = view[app]

                    imoji = {
                                'متابعين بدون ضمان' : 'متابعين بدون ضمان 👤❌',
                                'متابعين ضمان سنة' : 'متابعين ضمان سنة 👤✅' ,
                                'لايكات' : 'لايكات 👍' , 
                                'مشاهدات' : 'مشاهدات ▶️'
                            }
                    
                    offer_view = imoji[offer]

                    text = (f"لم نتمكن من تنفيذ طلبك رقم {request_id} لشحن {app_view} بشكل كامل \n"
                    f"الخدمة : {offer_view}\n"
                    f"الكمية : {amount}\n"
                    f"الرابط : {link}\n"
                    f"متبقي : {remained} \n"
                    f"تم إعادة {must_refund} $ \n"
                    f"يرجى التواصل مع الدعم @Mohammed_sn")

                    time.sleep(1)
                    try :
                        loop.run_until_complete(send(user_id, text))
                    except Exception as e :
                        print( 'while telling the user reject' , e)

                    
                    if offer == 'متابعين ضمان سنة':
                        button = functions.create_refill_button(request_id , order_id)
                    else :
                        button = None

                    done_text = (f"عملية مكتملة جزئيا : \n\n"
                    f"رقم العملية : `{request_id}`\n"
                    f"رقم الطلب في الموقع : `{order_id}`\n"
                    f"التطبيق : {functions.escape_markdown_v2(app)}\n"
                    f"الخدمة : {functions.escape_markdown_v2(offer)}\n"
                    f"الكمية : {functions.escape_markdown_v2(amount)}\n"
                    f"الرابط : {functions.escape_markdown_v2(link)}\n"
                    f"السعر : {functions.escape_markdown_v2(price)}\n"
                    f"متبقي : {functions.escape_markdown_v2(remained)}\n"
                    f"المبلغ المعاد : {functions.escape_markdown_v2(must_refund)}\n"
                    f"المستخدم : `{user_id}`\n"
                    f"الاسم : {functions.escape_markdown_v2(name)} \n"
                    f"المعرف : @{functions.escape_markdown_v2(username)}"
                    )

                    time.sleep(1)
                    try :
                        loop.run_until_complete(partial(done_text , button))
                        to_remove.append(order_id)
                    except Exception as e :
                        print( 'sending to partial group' , e)
            except :
                continue




        
        

                

        time.sleep(1)

        with open('side.json' , 'r' , encoding='utf-8') as f :
            data = json.load(f)

        

        for order in to_remove :
            try :
                data['social_pending'].remove(order)
            except :
                None
                
        
        try :
            with open('side.json' , 'w' , encoding='utf-8') as new_f :
                json.dump(data, new_f)
        except Exception as e :
            print( 'what the fuck?' , e)
    
    except Exception as e :
        print(e)
            
    
    time.sleep(10)
    