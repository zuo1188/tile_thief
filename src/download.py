import os
import asyncio
import time
import tqdm
from collections import namedtuple

from utils.bounds2tiles import bounds2tiles
from utils.geojson2tiles import geojson2tiles
from utils.download_tile import download_tile
from utils.tiles2mbtiles import tiles2mbtiles

def start_download(opts):
    rect_bounds = namedtuple('RectBounds', ['top', 'left', 'bottom', 'right'])

    # get bounds
    rect_bounds.top = opts.top
    rect_bounds.bottom = opts.bottom
    rect_bounds.right = opts.right
    rect_bounds.left = opts.left

    # download
    download(opts, rect_bounds)
    tiles2mbtiles(opts)

def download(opts, rect_bounds):
    output_dir = "%s" % opts.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    total_download_size = 0
    total_optimized_size = 0
    for zoom in range(opts.min_zoom, opts.max_zoom + 1):
        processed_cnt = 0
        download_cnt = 0
        sum_size = 0
        failed_cnt = 0

        if opts.geojson_path == '':
            tiles = bounds2tiles(rect_bounds, zoom)
        else:
            tiles = geojson2tiles(opts.geojson_path, zoom)

        download_tasks = []
        for tile in tiles:
            # processed_cnt += 1
            # pbar.update()
            #tile_url = opts.url + "/%d/%d/%d.png" % (zoom, y_index, x_index)
            tile_url = opts.url
            x_index = tile[0]
            y_index = tile[1]
            tile_url=tile_url.replace('{z}',str(zoom))
            tile_url=tile_url.replace('{x}',str(x_index))
            tile_url=tile_url.replace('{y}',str(y_index))

            path = "%s/%d/%d" % (output_dir, zoom, x_index)
            filename = path + "/%d.png" % y_index
            if not os.path.exists(path):
                os.makedirs(path)

            if not os.path.exists(filename):
                download_tasks.append({
                    'tile_index': [x_index, y_index, zoom],
                    'tile_url': tile_url,
                    'filename': filename
                })


        def saveFile(filename, data):
            try:
                print(filename, data)
                localFile = open(filename, 'wb')
                localFile.write(data)
                localFile.close()

                # total_download_size += os.path.getsize(filename)
                # sum_size += len(data)
            except Exception as e:
                os.unlink(filename)
                # failed_cnt += 1
                print(e)
                print("ERROR for %s" % tile_url)

        async def taskDispatcher(download_infos):
            no_concurrent = 1
            dltasks = set()
            i = 3
            pbar = tqdm.tqdm(total=len(tiles))
            for download_info_item in download_infos:
                pbar.update()
                if len(dltasks) >= no_concurrent:
                    # Wait for some download to finish before adding a new one
                    _done, dltasks = await asyncio.wait(dltasks)
                    for r in _done:  # done和pending都是一个任务，所以返回结果需要逐个调用result()
                        result = r.result()
                        # print(result)
                        # print(result['tile_info'])
                        if result['download_status'] == 'success':
                            # download_cnt += 1
                            filename = result['tile_info']['filename']
                            data = result['data']
                            saveFile(filename, data)
                dltasks.add(download_tile(download_info_item))
			# tasks = map(download_tile, download_infos)
			# done, pending = await asyncio.wait(tasks) # 子生成器
			# pbar = tqdm.tqdm(total=len(tiles))
			# for r in done: # done和pending都是一个任务，所以返回结果需要逐个调用result()
			# 	pbar.update()
			# 	result = r.result()
			# 	# print(result['tile_info'])
			# 	if result['download_status'] == 'success':
			# 		# download_cnt += 1
			# 		filename = result['tile_info']['filename']
			# 		data = result['data']
			# 		saveFile(filename, data)

        if len(download_tasks) > 0:
            start = time.time()
            loop = asyncio.get_event_loop()
            # try:
            # print(download_tasks)
            loop.run_until_complete(taskDispatcher(download_tasks)) # 完成事件循环，直到最后一个任务结束
            # finally:
                # loop.close() # 结束事件循环
            print('所有IO任务总耗时%.5f秒' % float(time.time()-start))
            
        success_cnt = processed_cnt - failed_cnt
        avg_size = 0
        # avoid possible division by zero
        if success_cnt != 0:
            avg_size = sum_size / success_cnt

        print("processed %d tiles - downloaded: %d, failed: %d, avg size: %d" % (processed_cnt, download_cnt, failed_cnt, avg_size))
    print("total download size: %d, total optimized size: %d" % (total_download_size, total_optimized_size))