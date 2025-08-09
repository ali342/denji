import asyncpg
import asyncio

POOL: asyncpg.Pool | None = None

_init_lock = asyncio.Lock()


async def get_db_pool() -> asyncpg.Pool:
    global POOL
    if POOL is not None:
        return POOL

    async with _init_lock:
        if POOL is None:
            POOL = await asyncpg.create_pool(
                            user='myuser',
                            password='abbasbots',
                            database='denji_main',
                            host='103.110.65.69',
                            max_size=40
                        )
    return POOL


async def close_db_pools() -> None:
    global POOL
    if POOL is not None:
        await POOL.close()
        POOL = None




async def connect_to_db():
    conn = await asyncpg.connect(
        user='myuser',
        password='abbasbots',
        database='denji_main',
        host='103.110.65.69',
        port="5432" 
    )
    return conn




async def initialize_db() :

    conn = await connect_to_db()
   

    await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                name TEXT,
                balance FLOAT DEFAULT 0,
                total_spent FLOAT DEFAULT 0,
                active_offers_id TEXT
            )
        ''')









    await conn.execute('''
                CREATE TABLE IF NOT EXISTS topup_requests (
                    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount_sent TEXT,
                    credit_price INTEGER,
                    amount_added FLOAT DEFAULT 0,
                    trans_id INTEGER,
                    balance_before FLOAT,
                    balance_after FLOAT,
                    status TEXT,
                    timestamp TIMESTAMP,
                    topup_type TEXT, 
                    photo_file_id TEXT,
                    message_id TEXT,   
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')





    await conn.execute('''
                CREATE TABLE IF NOT EXISTS item_requests(
                    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    app TEXT,
                    country TEXT,
                    number TEXT,
                    server TEXT,
                    provider TEXT,
                    status TEXT,
                    timestamp TIMESTAMP,
                    price FLOAT,
                    balance_before FLOAT,
                    balance_after FLOAT,
                    balance_after_refund FLOAT, 
                    code TEXT,
                    auto_id TEXT,
                    end_time TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
                ''')







    await conn.execute('''
                CREATE TABLE IF NOT EXISTS social_requests(
                    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    app TEXT,
                    service TEXT,
                    amount INT,
                    link TEXT,
                    status TEXT,
                    timestamp TIMESTAMP,
                    price FLOAT,
                    balance_before FLOAT,
                    balance_after FLOAT,
                    balance_after_refund FLOAT,
                    refunded FLOAT,
                    remained INT,
                    auto_id TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
                ''')





    await conn.execute(
        '''
                CREATE TABLE IF NOT EXISTS added_manually(
                    user_id TEXT,
                    added_amount FLOAT,
                    type TEXT,
                    date TIMESTAMP DEFAULT NOW()
                    )
    ''')


    await conn.close()

