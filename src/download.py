import os
import asyncio
import time
import tqdm
import geojson
import json
from collections import namedtuple
from types import SimpleNamespace
from multiprocessing import Pool

from utils.downloader import downloader
from utils.bounds2tiles import bounds2tiles
from utils.geojson2tiles import geojson2tiles,geojson_path2tiles
from utils.download_tile import download_tile
from utils.tiles2mbtiles import tiles2mbtiles
from utils.map_bing import get_bing_url, bing_get_meta_info
from utils.map_tencent import get_tencent_url
from utils.map_baidu import get_baidu_url, baidu_bounds2tiles, baidu_get_number_of_tiles_at_level

SERVER_URL_MAPPING = {
    "google_map_sat": "http://mt0.google.cn/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}",
    "amap_sat": "https://webst04.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}",
    "tianditu_sat": "http://t2.tianditu.gov.cn/DataServer?T=img_w&x={x}&y={y}&l={z}&tk=997487c2aa6dc93d84169f293ae2073d",
    "bing_sat": "",
    "tencent_sat": "",
    "baidu_sat": ""
}

def get_bbox(coord_list):
    box = []
    for i in (0,1):
        res = sorted(coord_list, key=lambda x:x[i])
        box.append((res[0][i],res[-1][i]))
    return [box[0][0], box[1][0], box[0][1], box[1][1]]

def get_download_info(min_zoom, max_zoom, geometry, map_type):
    download_info = {}
    for zoom in range(min_zoom, max_zoom + 1):
        if map_type == 'baidu_sat':
            bbox = get_bbox(list(geojson.utils.coords(geometry)))
            rect_bounds = namedtuple('RectBounds', ['top', 'left', 'bottom', 'right'])
            # get bounds
            rect_bounds.top = bbox[3]
            rect_bounds.bottom = bbox[1]
            rect_bounds.right = bbox[2]
            rect_bounds.left = bbox[0]
            tiles = baidu_bounds2tiles(rect_bounds, zoom)
        else:
            tiles = geojson2tiles(geometry, zoom) 
        download_info['zoom' + str(zoom)] = len(tiles)
    print(download_info)
    return download_info


def download(min_zoom, max_zoom, geometry, map_type, output_dir, process_count):
    bbox = get_bbox(list(geojson.utils.coords(geometry)))
    opts = {}
    opts["min_zoom"]=min_zoom
    opts["max_zoom"]=max_zoom
    opts["geojson_path"]=""
    opts["geojson"]=geometry
    opts["map_type"]=map_type
    opts["output"]=output_dir
    opts["concurrent_num"]=process_count
    opts["top"]=bbox[3]
    opts["bottom"]=bbox[1]
    opts["left"]=bbox[2]
    opts["right"]=bbox[0]
    new_opts=SimpleNamespace(**opts)
    download_tiles(new_opts)
    tiles2mbtiles(new_opts)

def get_vector_info():
    with open("./src/data/vector_list.json",'r') as load_f:
        return json.load(load_f)

def download_vector(name, format, output):
    with open("./src/data/vector_map.json",'r') as load_f:
        vector_mapping = json.load(load_f)
    if name not in vector_mapping:
        print('矢量数据' + name + '不存在')
        return False
    elif format not in vector_mapping[name]:
        print('矢量数据' + name + '不存在' + format + '格式')
        return False
    else:
        print(vector_mapping[name][format])
        filename = output + "/%s.%s" % (name, format)
        downloader(vector_mapping[name][format], filename)
        return True

def download_by_cmd(opts):
    # download
    download_tiles(opts)
    tiles2mbtiles(opts)

def download_tiles(opts):
    print(opts)
    output_dir = "%s" % opts.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if opts.map_type == 'bing_sat':
        bing_meta_info = bing_get_meta_info()

    total_download_size = 0
    total_optimized_size = 0
    for zoom in range(opts.min_zoom, opts.max_zoom + 1):
        processed_cnt = 0
        download_cnt = 0
        sum_size = 0
        failed_cnt = 0

        if opts.geojson_path == '' and opts.geojson == '':
            rect_bounds = namedtuple('RectBounds', ['top', 'left', 'bottom', 'right'])

            # get bounds
            rect_bounds.top = opts.top
            rect_bounds.bottom = opts.bottom
            rect_bounds.right = opts.right
            rect_bounds.left = opts.left
            tiles = bounds2tiles(rect_bounds, zoom)
        elif opts.map_type == 'baidu_sat':
            rect_bounds = namedtuple('RectBounds', ['top', 'left', 'bottom', 'right'])

            # get bounds
            rect_bounds.top = opts.top
            rect_bounds.bottom = opts.bottom
            rect_bounds.right = opts.right
            rect_bounds.left = opts.left
            tiles = baidu_bounds2tiles(rect_bounds, zoom)
        elif opts.geojson_path != '':
            tiles = geojson_path2tiles(opts.geojson_path, zoom)
        else:
            tiles = geojson2tiles(opts.geojson, zoom) 

        download_tasks = []
        for tile in tiles:
            # processed_cnt += 1
            # pbar.update()
            #tile_url = opts.url + "/%d/%d/%d.png" % (zoom, y_index, x_index)
            print(opts.map_type)
            tile_url=''
            x_index = tile[0]
            y_index = tile[1]
            if opts.map_type == 'bing_sat':
                tile_url=get_bing_url([x_index,y_index,zoom], bing_meta_info)
            elif opts.map_type == 'tencent_sat':
                tile_url=get_tencent_url([x_index,y_index,zoom])
            elif opts.map_type == 'baidu_sat':
                tile_url=get_baidu_url([x_index,y_index,zoom]) 
            else:
                tile_url = SERVER_URL_MAPPING[opts.map_type]
                tile_url=tile_url.replace('{z}',str(zoom))
                tile_url=tile_url.replace('{x}',str(x_index))
                tile_url=tile_url.replace('{y}',str(y_index))

            path = "%s/%d/%d" % (output_dir, zoom, x_index)
            filename = path + "/%d.png" % y_index
            if opts.map_type == 'baidu_sat':
                filename = path + "/%d.png" % (baidu_get_number_of_tiles_at_level(zoom) - int(y_index))
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
                # print(filename, data)
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

        def taskDispatcher(download_infos):
            no_concurrent = opts.concurrent_num
            print(no_concurrent)
            pool = Pool(int(no_concurrent))
            pbar = tqdm.tqdm(total=len(tiles))
            def callback(result):
                # print(result)
                # print(result['tile_info'])
                pbar.update()
                if result['download_status'] == 'success':
                    # download_cnt += 1
                    filename = result['tile_info']['filename']
                    data = result['data']
                    saveFile(filename, data)

            for download_info_item in download_infos:
                pool.apply_async(download_tile, args=(download_info_item,), callback=callback)
            pool.close()
            pool.join()
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
            # loop = asyncio.get_event_loop()
            # try:
            # print(download_tasks)
            # loop.run_until_complete(taskDispatcher(download_tasks)) # 完成事件循环，直到最后一个任务结束
            # finally:
                # loop.close() # 结束事件循环
            # pool = Pool(5)
            taskDispatcher(download_tasks)
            print('所有IO任务总耗时%.5f秒' % float(time.time()-start))
            
        success_cnt = processed_cnt - failed_cnt
        avg_size = 0
        # avoid possible division by zero
        if success_cnt != 0:
            avg_size = sum_size / success_cnt

        print("processed %d tiles - downloaded: %d, failed: %d, avg size: %d" % (processed_cnt, download_cnt, failed_cnt, avg_size))
    print("total download size: %d, total optimized size: %d" % (total_download_size, total_optimized_size))


# if __name__ == '__main__':
#     download(6, 12, {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Polygon",
#         "coordinates": [
#           [
#             [
#               116.39739990234375,
#               40.01499435375046
#             ],
#             [
#               116.39190673828124,
#               39.91289633555756
#             ],
#             [
#               116.22161865234376,
#               39.8992015115692
#             ],
#             [
#               116.25045776367186,
#               39.74204232950662
#             ],
#             [
#               116.49902343749999,
#               39.716694496739876
#             ],
#             [
#               116.51275634765624,
#               39.99395569397331
#             ],
#             [
#               116.39739990234375,
#               40.01499435375046
#             ]
#           ]
#         ]
#       }
#     }, 'tianditu_sat', '/Users/jrontend/myPrj/tile_thief/beijing_google', 1)
# get_vector_info()

# download_vector('Azores', 'pbf', '/Users/jrontend/myPrj/tile_thief/')
# get_download_info(6, 12, {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Polygon",
#         "coordinates": [
#           [
#             [
#               116.39739990234375,
#               40.01499435375046
#             ],
#             [
#               116.39190673828124,
#               39.91289633555756
#             ],
#             [
#               116.22161865234376,
#               39.8992015115692
#             ],
#             [
#               116.25045776367186,
#               39.74204232950662
#             ],
#             [
#               116.49902343749999,
#               39.716694496739876
#             ],
#             [
#               116.51275634765624,
#               39.99395569397331
#             ],
#             [
#               116.39739990234375,
#               40.01499435375046
#             ]
#           ]
#         ]
#       }
#     }, 'tianditu_sat')