# -*- coding: utf-8 -*-
'''
@createBy  :   xiaowu 
@date    :   2019/10/28 10:58:08
'''

import aiohttp
import asyncio

# async def main():
#     print('Hello ...')
#     await asyncio.sleep(1)
#     print('... World!')

# # Python 3.7+
# asyncio.run(main())

async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(response)
            print(time.time())

import time
async def request():
    url = "http://www.baidu.com"
    result = await get(url)

tasks = [asyncio.ensure_future(request()) for _ in range(10)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))