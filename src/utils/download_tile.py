import time
import requests
import asyncio
import os
import aiohttp

async def download_tile(download_tasks):
    # print(download_tasks) 
    webFile = None
    data = None
    download_succeeded = False
    tile_url = download_tasks['tile_url']

    zoom = 4
    max_retries = 2 ** (15 - zoom)
    if max_retries < 1:
        max_retries = 1

    for try_nr in range(1, max_retries + 2):
        #for try_nr in range(1, 2):
        try:
            print("trying %s" % tile_url)
            async with aiohttp.ClientSession() as session:
                async with session.get(tile_url) as resp:
                    data = await resp.read()
                    download_succeeded = True
                    resp.close()
                    break
        except Exception as e:
            print(e)
            print("%s failed on try nr %d" % (tile_url, try_nr))
            # give the server some time, maybe that helps
            time.sleep(2)

    if not download_succeeded:
        # TODO: Try to find true server
        print(tile_url)
        return {'download_status': 'error', 'tile_info': download_tasks}
    else:
        return {'download_status': 'success', 'tile_info': download_tasks, 'data': data}

# async def taskDispatcher(download_tasks): # 调用方
#     tasks = map(download, download_tasks)
#     done,pending = await asyncio.wait(tasks) # 子生成器
#     for r in done: # done和pending都是一个任务，所以返回结果需要逐个调用result()
#         result = r.result()
#         if result['download_status'] == 'error':

#         elif result['download_status'] == 'success':
#         # print('协程无序返回值：'+r.result())

# if __name__ == '__main__':
#     urls = [
#         "https://maponline1.bdimg.com/starpic/?qt=satepc&u=x=M5;y=1;z=4;v=009;type=sate&fm=46&app=webearth2&v=009&udt=20200716",
#         "https://maponline1.bdimg.com/starpic/?qt=satepc&u=x=3;y=1;z=4;v=009;type=sate&fm=46&app=webearth2&v=009&udt=20200716",
#         "https://maponline1.bdimg.com/starpic/?qt=satepc&u=x=2;y=1;z=4;v=009;type=sate&fm=46&app=webearth2&v=009&udt=20200716",
#         "https://maponline1.bdimg.com/starpic/?qt=satepc&u=x=1;y=1;z=4;v=009;type=sate&fm=46&app=webearth2&v=009&udt=20200716"
#     ]

#     start = time.time()
#     loop = asyncio.get_event_loop()
#     try:
#         loop.run_until_complete(taskDispatcher(urls)) # 完成事件循环，直到最后一个任务结束
#     finally:
#         loop.close() # 结束事件循环
#     print('所有IO任务总耗时%.5f秒' % float(time.time()-start))