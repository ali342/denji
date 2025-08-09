
import aiohttp
import asyncio

async def main() :


    url = 'https://smmparty.com/api/v2'

    params = {
        'key' : 'dab3fac7cde4ca03f835688b83789674',
        'action' : 'refill',
        'order' : 843332
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
    print(refill_id)

asyncio.run(main())