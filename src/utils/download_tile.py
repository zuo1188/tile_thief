import time
import requests
import os
from utils.dem import gehelper_py

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}


def download_tile(download_tasks):
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
        # for try_nr in range(1, 2):
        try:
            # print("trying %s" % tile_url)
            webFile = requests.get(tile_url, headers=REQUEST_HEADERS)
            data = webFile.content
            download_succeeded = True
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


def download_ge_tile(download_tasks):
    # print(download_tasks)
    download_succeeded = False
    bbox = download_tasks['bbox']
    min_x = bbox[0]
    min_y = bbox[1]
    max_x = bbox[2]
    max_y = bbox[3]

    min_zoom = download_tasks['min_zoom']
    max_zoom = download_tasks['max_zoom']
    date = download_tasks['date']
    map_type = download_tasks['map_type']
    output = download_tasks['output']
    # ge_helper = download_tasks['ge_helper']

    ge_helper = gehelper_py.CLibGEHelper()
    ge_helper.Initialize()
    ge_helper.getTmDBRoot()
    output_gbk = output.encode("gbk")
    ge_helper.setCachePath(output_gbk)

    for zoom in range(min_zoom, max_zoom + 1):
        if date != "":
            # dowload history data
            if map_type == "google_earth_sat":
                print("start ge_helper.getHistoryImageByDates %f,%f,%f,%f zoom:%d date:%s" % (min_x, min_y, max_x, max_y, zoom, date) )
                ge_helper.getHistoryImageByDates(min_x, min_y, max_x, max_y, zoom, date)
            else:
                print("google earth dem only support latest dem")
        else:
            # dowload latest data
            if map_type == "google_earth_sat":
                print("start ge_helper.getImage %f,%f,%f,%f zoom:%d" % (min_x, min_y, max_x, max_y, zoom) )
                ge_helper.getImage(min_x, min_y, max_x, max_y, zoom)
            else:
                print("start ge_helper.getTerrain %f,%f,%f,%f zoom:%d" % (min_x, min_y, max_x, max_y, zoom) )
                ge_helper.getTerrain(min_x, min_y, max_x, max_y, zoom)

    return {'download_status': 'success', 'tile_info': download_tasks}


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
