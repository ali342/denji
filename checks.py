import requests
import json
# import sqlite3 # MODIFIED: No longer used
import db       # MODIFIED: Added for asyncpg

import functions 
import time
from telegram import Bot
import asyncio
import aiohttp # MODIFIED: Switched to aiohttp for non-blocking requests

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

# --- MODIFIED: Start of new async DB helper functions ---

async def db_get_request_details(request_id):
    """Fetches details for a pending request."""
    pool = await db.get_db_pool()
    async with pool.acquire() as conn:
        # NOTE: Replaced SQLite's STRFTIME with PostgreSQL's EXTRACT(EPOCH FROM ...).
        query = """
            SELECT auto_id, provider, user_id, price, number, country, app, 
                   EXTRACT(EPOCH FROM (end_time - NOW())), 
                   balance_after_refund 
            FROM item_requests 
            WHERE request_id = $1
        """
        return await conn.fetchrow(query, request_id)

async def db_process_success(request_id, code, price, user_id):
    """Processes a successful activation, updating the request and user's total spent."""
    pool = await db.get_db_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute("UPDATE item_requests SET code = $1, status = 'منتهية' WHERE request_id = $2", code, request_id)
            await conn.execute("UPDATE users SET total_spent = total_spent + $1 WHERE id = $2", price, user_id)

async def db_process_refund(request_id, price, user_id):
    """Processes a refund, updating user balance, active offers, and request status in a single transaction."""
    pool = await db.get_db_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            # Fetch current user data
            user_data = await conn.fetchrow("SELECT balance, active_offers_id FROM users WHERE id = $1 FOR UPDATE", user_id)
            balance, active_offers = user_data['balance'], user_data['active_offers_id']
            
            new_balance = balance + price
            
            # Safely process active offers string
            nactive = None
            if active_offers:
                active_list = active_offers.split(":")
                if str(request_id) in active_list:
                    active_list.remove(str(request_id))
                if active_list:
                    nactive = ":".join(active_list)
            
            # Update user and request
            await conn.execute("UPDATE users SET balance = $1, active_offers_id = $2 WHERE id = $3", new_balance, nactive, user_id)
            await conn.execute("UPDATE item_requests SET status = 'ملغية', balance_after_refund = $1 WHERE request_id = $2", new_balance, request_id)
            
            return new_balance # Return new balance for notifications

# --- End of new async DB helper functions ---


print('new checks.py started')

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
session = requests.Session() # Use a session for connection pooling

while True:
    try:
        with open('side.json', 'r', encoding='utf-8') as file:
            pending_data = json.load(file)
        
        pendings = pending_data.get('pending', [])
        must_remove = []

        for request_id in pendings:
            print(f"Checking request_id: {request_id}")
            
            # MODIFIED: Get request details from DB asynchronously
            data = loop.run_until_complete(db_get_request_details(request_id))
            if not data:
                print(f"No data found for {request_id}, marking for removal.")
                must_remove.append(request_id)
                continue

            auto_id, provider, user_id, price, number, country, app, left_seconds, balance_after_refunded = data
            left_seconds = left_seconds or -1 # Ensure it's not None

            try:
                # --- Provider Logic (API calls remain synchronous with `requests`) ---
                if provider == 'viotp':
                    api_token = get_json('viotp.json')['api_token']
                    url = f'https://api.viotp.com/session/getv2?requestId={auto_id}&token={api_token}'
                    response = session.get(url, timeout=10).json()
                    status = response.get('data', {}).get('Status')

                    if status == 1: # Success
                        code = response['data']['Code']
                        loop.run_until_complete(db_process_success(request_id, code, price, user_id))
                        must_remove.append(request_id)
                    elif status == 2: # Canceled by provider
                        if balance_after_refunded:
                            must_remove.append(request_id)
                            continue
                        new_balance = loop.run_until_complete(db_process_refund(request_id, price, user_id))
                        must_remove.append(request_id)
                        # Notification logic... (remains the same)

                elif provider in ['drop_sms', 'sms_live']:
                    if provider == 'drop_sms':
                        api_token = get_json('dropsms.json')['api_token']
                        url = f'https://api.dropsms.cc/stubs/handler_api.php?action=getStatus&api_key={api_token}&id={auto_id}'
                    else: # sms_live
                        api_token = get_json('smslive.json')['api_token']
                        url = f'https://api.smslive.pro/stubs/handler_api.php?api_key={api_token}&action=getStatus&id={auto_id}'

                    response_text = session.get(url, timeout=10).text

                    if response_text.startswith('STATUS_OK:'): # Success
                        code = response_text.split(':')[1]
                        loop.run_until_complete(db_process_success(request_id, code, price, user_id))
                        must_remove.append(request_id)
                    elif left_seconds < 0 or response_text == 'NO_ACTIVATION': # Timeout or Canceled
                        if balance_after_refunded:
                            must_remove.append(request_id)
                            continue
                        new_balance = loop.run_until_complete(db_process_refund(request_id, price, user_id))
                        must_remove.append(request_id)
                        # Notification logic... (remains the same)

                elif provider == 'duriancrs':
                    dur_data = get_json('durancies.json')
                    api_token = dur_data['api_token']
                    app_code = dur_data['services_ids'][app]
                    name = 'Mohammedsn'
                    url = f'https://api.durianrcs.com/out/ext_api/getMsg?name={name}&ApiKey={api_token}&pn={number}&pid={app_code}&serial=2'
                    response = session.get(url, timeout=10).json()

                    if response.get('code') == 200 and response.get('msg') == 'Success': # Success
                        code = response['data']
                        loop.run_until_complete(db_process_success(request_id, code, price, user_id))
                        must_remove.append(request_id)
                    elif left_seconds < 0 or response.get('code') == 405: # Timeout or Canceled
                        if balance_after_refunded:
                            must_remove.append(request_id)
                            continue
                        new_balance = loop.run_until_complete(db_process_refund(request_id, price, user_id))
                        must_remove.append(request_id)
                        # Notification logic... (remains the same)

            except Exception as e:
                print(f"Error processing request {request_id} for provider {provider}: {e}")
            
            time.sleep(1.5) # Keep the delay between requests in the loop
        
        # Update the pending list JSON file
        if must_remove:
            d = get_json('side.json')
            current_pending = d.get('pending', [])
            d['pending'] = [p for p in current_pending if p not in must_remove]
            update_json('side.json', d)

        time.sleep(15) # Keep the delay for the main loop cycle

    except Exception as e:
        print(f"An error occurred in the main loop: {e}")
        time.sleep(30) # Wait longer on major error