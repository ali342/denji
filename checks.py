import requests
import json
import sqlite3

import functions 

import time

from telegram import Bot
import asyncio

# TOKEN = '8104378989:AAEywJ79v-ABya3X091P3vAOcVIc2aEuJa0' # denji test
# TOKEN = '7718105050:AAFDSOl-EE4axZ7FO51J4YlFDq9OXvSpANg' # my test

TOKEN = '8004725012:AAGJAkWMb9rEtZxMdGmU2S2PZ93i2M21UCo' # main



bot = Bot(token = TOKEN)

async def send_message(chat_id , text , reply_markup = None) :
    await bot.send_message(chat_id = chat_id, text =text , reply_markup = reply_markup )

def get_json(file_name) : 
    with open(file_name , 'r' , encoding='utf-8')as file :
        data = json.load(file)
    return data

def update_json(file_name , data) : 
    with open(file_name , 'w' , encoding='utf-8')as file :
        json.dump(data,file)






print(' new started')

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

while True :

    try :
    
        with open('side.json' , 'r' , encoding='utf-8') as file :
            pending = json.load(file)
        
        pendings = pending['pending']

        must_remove = []

        for request_id in pendings :
            print(request_id)
            conn = functions.connect_db()
            cursor = conn.cursor()

            cursor.execute('''SELECT auto_id , provider , user_id , price , number , country , app , (STRFTIME('%s', end_time) - STRFTIME('%s', 'now')) , balance_after_refund FROM item_requests WHERE request_id = ?''' , (request_id,))
            data = cursor.fetchone()
            auto_id , provider , user_id , price , number , country , app , left_seconds , balanc_after_rufunded = data

            
            try :
                if provider == 'viotp' :
                    api_token = get_json('viotp.json')['api_token']
                    url = f'https://api.viotp.com/session/getv2?requestId={auto_id}&token={api_token}'

                    response = requests.get(url, timeout=(5,5))
                    response = response.json()

                    status = response['data']['Status']

                    if status == 1 :
                        code = response['data']['Code']
                        cursor.execute('''UPDATE item_requests SET code = ? , status = 'منتهية' WHERE request_id = ? ''' , (code , request_id))
                        cursor.execute('UPDATE users SET total_spent = total_spent + ? WHERE id = ?',(price, user_id))
                        conn.commit()
                        must_remove.append(request_id)
                    elif status == 2 :
                        if balanc_after_rufunded :
                            must_remove.append(request_id)
                            continue
                        cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) , active_offers_id FROM users WHERE id = ?' , (user_id,))
                        data = cursor.fetchone()
                        balance , active_offers= data
                        new_balance = balance + price

                        nactive = ''

                        try :
                            active_offers = active_offers.split(":")
                            if str(request_id) in active_offers :
                                active_offers.remove(str(request_id))
                            nactive = ''
                            for i in range(len(active_offers)) :
                                n = active_offers[i]
                                if i == 0 :
                                    nactive += f"{n}"
                                else :
                                    nactive += f":{n}"
                        except Exception as e :
                            print('active viotp' , e)
                        
                        if nactive == '' :
                            nactive = None
                        
                        try:
                            cursor.execute('UPDATE users SET balance = ? , active_offers_id = ? WHERE id = ?',(new_balance , nactive , user_id))
                            conn.commit()
                            loop.run_until_complete(send_message('5349543151', f"op : {request_id}\n balance now : {new_balance}\n active offers : {nactive}"))
                        except Exception as e :
                            print('updating balance viotp' ,e)
                            try :
                                loop.run_until_complete(send_message('5349543151', f"op : {request_id}\n balance now : {new_balance}\n active offers : {nactive}\n\n{e}"))
                            except Exception as e :
                                print('sending to me' ,e)
                        

                        cursor.execute('''UPDATE item_requests SET status = 'ملغية' , balance_after_refund = ? WHERE request_id = ? ''' , ( new_balance, request_id))
                        conn.commit()

                        must_remove.append(request_id)

                        try :
                            text = (
                                f"تم إلغاء العملية رقم : {request_id} ❌\n\n"
                                f"تم إرجاع الرصيد ✔️"
                            )
                            loop.run_until_complete(send_message(user_id, text))
                        except :
                            None
                        
                        try :
                            button = functions.create_telegram_check_button(user_id)
                            text = (
                                f"عملية ملغاة ❌ : \n\n"
                                f"رقم العملية : {request_id}\n"
                                f"الرقم : {number}\n"
                                f"الدولة : {country}\n"
                                f"التطبيق : {app}\n"
                                f"ايدي المستخدم : {user_id}\n"
                                f"السعر : {price}\n"
                                f"الرصيد الجديد : {new_balance}"
                            )
                            loop.run_until_complete(send_message('-1002537720561', text , button))
                        except  :
                            None
                        
                        
                
                elif provider == 'drop_sms' :
                    api_token = get_json('dropsms.json')['api_token']
                    url = f'https://api.dropsms.cc/stubs/handler_api.php?action=getStatus&api_key={api_token}&id={auto_id}'

                    responsem = requests.get(url , timeout=(5,5))
                    response = responsem.text

                    if response.startswith('STATUS_OK:') :
                        code = response.split(':')[1]
                        cursor.execute('''UPDATE item_requests SET code = ? , status = 'منتهية' WHERE request_id = ? ''' , (code , request_id))
                        cursor.execute('UPDATE users SET total_spent = total_spent + ? WHERE id = ?',(price, user_id))
                        conn.commit()
                        must_remove.append(request_id)
                    elif left_seconds < 0 :
                        if balanc_after_rufunded :
                            must_remove.append(request_id)
                            continue
                        cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) , active_offers_id FROM users WHERE id = ?' , (user_id,))
                        data = cursor.fetchone()
                        balance , active_offers= data
                        new_balance = balance + price

                        nactive = ''

                        try :
                            active_offers = active_offers.split(":")
                            
                            if str(request_id) in active_offers :
                                active_offers.remove(str(request_id))
                            nactive = ''
                            for i in range(len(active_offers)) :
                                n = active_offers[i]
                                if i == 0 :
                                    nactive += f"{n}"
                                else :
                                    nactive += f":{n}"
                        except Exception as e :
                            print('active dropsms' , e)
                        
                        if nactive == '' :
                            nactive = None
                        
                        try:
                            cursor.execute('UPDATE users SET balance = ? , active_offers_id = ? WHERE id = ?',(new_balance , nactive , user_id))
                            conn.commit()
                            loop.run_until_complete(send_message('5349543151', f"op : {request_id}\n balance now : {new_balance}\n active offers : {nactive}"))
                        except Exception as e :
                            print( 'updating balance drop',e)
                            try :
                                loop.run_until_complete(send_message('5349543151', f"op : {request_id}\n balance now : {new_balance}\n active offers : {nactive}\n\n{e}"))
                            except Exception as e :
                                print('sending to me drop',e)

                        

                        cursor.execute('''UPDATE item_requests SET status = 'ملغية' , balance_after_refund = ? WHERE request_id = ? ''' , ( new_balance, request_id))
                        conn.commit()

                        must_remove.append(request_id)
                        try :
                            text = (
                                f"تم إلغاء العملية رقم : {request_id} ❌\n\n"
                                f"تم إرجاع الرصيد ✔️"
                            )
                            loop.run_until_complete(send_message(user_id, text))
                        except :
                            None
                        
                        try :
                            button = functions.create_telegram_check_button(user_id)
                            text = (
                                f"عملية ملغاة ❌ : \n\n"
                                f"رقم العملية : {request_id}\n"
                                f"الرقم : {number}\n"
                                f"الدولة : {country}\n"
                                f"التطبيق : {app}\n"
                                f"ايدي المستخدم : {user_id}\n"
                                f"السعر : {price}\n"
                                f"الرصيد الجديد : {new_balance}"
                            )
                            loop.run_until_complete(send_message('-1002537720561', text , button))
                        except :
                            None
                        
                        



                elif provider == 'sms_live' :
                    api_token = get_json('smslive.json')['api_token']

                    url = f'https://api.smslive.pro/stubs/handler_api.php?api_key={api_token}&action=getStatus&id={auto_id}'


                    responsem = requests.get(url , timeout=(5,5))
                    response = responsem.text

                    if response.startswith('STATUS_OK:') :
                        code = response.split(':')[1]
                        cursor.execute('''UPDATE item_requests SET code = ? , status = 'منتهية' WHERE request_id = ? ''' , (code , request_id))
                        cursor.execute('UPDATE users SET total_spent = total_spent + ? WHERE id = ?',(price, user_id))
                        conn.commit()
                        must_remove.append(request_id)
                    elif left_seconds < 0 or response == 'NO_ACTIVATION' :
                        if balanc_after_rufunded :
                            must_remove.append(request_id)
                            continue
                        cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) , active_offers_id FROM users WHERE id = ?' , (user_id,))
                        data = cursor.fetchone()
                        balance , active_offers= data
                        new_balance = balance + price

                        nactive = ''
                        try :
                            active_offers = active_offers.split(":")
                            
                            if str(request_id) in active_offers :
                                active_offers.remove(str(request_id))
                            nactive = ''
                            for i in range(len(active_offers)) :
                                n = active_offers[i]
                                if i == 0 :
                                    nactive += f"{n}"
                                else :
                                    nactive += f":{n}"
                        except Exception as e :
                            print('active smslive' , e)
                        
                        if nactive == '' :
                            nactive = None
                        
                        try:
                            cursor.execute('UPDATE users SET balance = ? , active_offers_id = ? WHERE id = ?',(new_balance , nactive , user_id))
                            conn.commit()
                            loop.run_until_complete(send_message('5349543151', f"op : {request_id}\n balance now : {new_balance}\n active offers : {nactive}"))
                        except Exception as e :
                            print('update balance smslive',  e)
                            try :
                                loop.run_until_complete(send_message('5349543151', f"op : {request_id}\n balance now : {new_balance}\n active offers : {nactive}\n\n{e}"))
                            except Exception as e :
                                print('sending to me smslive',e)


                        cursor.execute('''UPDATE item_requests SET status = 'ملغية' , balance_after_refund = ? WHERE request_id = ? ''' , ( new_balance, request_id))
                        conn.commit()

                        must_remove.append(request_id)
                        try :
                            text = (
                                f"تم إلغاء العملية رقم : {request_id} ❌\n\n"
                                f"تم إرجاع الرصيد ✔️"
                            )
                            loop.run_until_complete(send_message(user_id, text))
                        except :
                            None
                        
                        try :
                            button = functions.create_telegram_check_button(user_id)
                            text = (
                                f"عملية ملغاة ❌ : \n\n"
                                f"رقم العملية : {request_id}\n"
                                f"الرقم : {number}\n"
                                f"الدولة : {country}\n"
                                f"التطبيق : {app}\n"
                                f"ايدي المستخدم : {user_id}\n"
                                f"السعر : {price}\n"
                                f"الرصيد الجديد : {new_balance}"
                            )
                            loop.run_until_complete(send_message('-1002537720561', text , button))
                        except :
                            None
                





                elif provider == 'duriancrs' :
                    dur_data = get_json('durancies.json')
                    api_token = dur_data['api_token']

                    app_code = dur_data['services_ids'][app]
                    name = 'Mohammedsn'

                    url = f'https://api.durianrcs.com/out/ext_api/getMsg?name={name}&ApiKey={api_token}&pn={number}&pid={app_code}&serial=2'


                    responsem = requests.get(url , timeout=(5,5) )
                    response = responsem.json()

                    if response['code'] == 200 and response['msg'] == 'Success' :
                        code = response['data']
                        cursor.execute('''UPDATE item_requests SET code = ? , status = 'منتهية' WHERE request_id = ? ''' , (code , request_id))
                        cursor.execute('UPDATE users SET total_spent = total_spent + ? WHERE id = ?',(price, user_id))
                        conn.commit()
                        must_remove.append(request_id)
                    elif left_seconds < 0 or response['code'] == 405  :
                        if balanc_after_rufunded :
                            must_remove.append(request_id)
                            continue
                        cursor.execute('SELECT CAST(ROUND(balance, 2) AS DECIMAL(10,2)) , active_offers_id FROM users WHERE id = ?' , (user_id,))
                        data = cursor.fetchone()
                        balance , active_offers= data
                        new_balance = balance + price

                        nactive = ''
                        try :
                            active_offers = active_offers.split(":")
                            
                            if str(request_id) in active_offers :
                                active_offers.remove(str(request_id))
                            nactive = ''
                            for i in range(len(active_offers)) :
                                n = active_offers[i]
                                if i == 0 :
                                    nactive += f"{n}"
                                else :
                                    nactive += f":{n}"
                        except Exception as e :
                            print('active duranc',e)
                        
                        if nactive == '' :
                            nactive = None
                        
                        try:
                            cursor.execute('UPDATE users SET balance = ? , active_offers_id = ? WHERE id = ?',(new_balance , nactive , user_id))
                            conn.commit()
                            loop.run_until_complete(send_message('5349543151', f"op : {request_id}\n balance now : {new_balance}\n active offers : {nactive}"))
                        except Exception as e :
                            print( 'update balance duranc',e)
                            try :
                                loop.run_until_complete(send_message('5349543151', f"op : {request_id}\n balance now : {new_balance}\n active offers : {nactive}\n\n{e}"))
                            except Exception as e :
                                print( 'sending to me duranc',  e)


                        cursor.execute('''UPDATE item_requests SET status = 'ملغية' , balance_after_refund = ? WHERE request_id = ? ''' , ( new_balance, request_id))
                        conn.commit()

                        must_remove.append(request_id)
                        try :
                            text = (
                                f"تم إلغاء العملية رقم : {request_id} ❌\n\n"
                                f"تم إرجاع الرصيد ✔️"
                            )
                            loop.run_until_complete(send_message(user_id, text))
                        except :
                            None
                        
                        try :
                            button = functions.create_telegram_check_button(user_id)
                            text = (
                                f"عملية ملغاة ❌ : \n\n"
                                f"رقم العملية : {request_id}\n"
                                f"الرقم : {number}\n"
                                f"الدولة : {country}\n"
                                f"التطبيق : {app}\n"
                                f"ايدي المستخدم : {user_id}\n"
                                f"السعر : {price}\n"
                                f"الرصيد الجديد : {new_balance}"
                            )
                            loop.run_until_complete(send_message('-1002537720561', text , button))
                        except :
                            None
                        
                        

            except Exception as e:
                print(e)
            
            conn.close()
            time.sleep(1.5)
        
        d = get_json('side.json') 
        
        for num in must_remove :
            try :
                d['pending'].remove(num)
            except :
                None
        
        update_json('side.json' , d)

        
        time.sleep(15)
    except Exception as e :
        print(e)
        try :
            conn.commit()
            conn.close()
        except :
            None



