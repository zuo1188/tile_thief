#!/usr/bin/env python3
import asyncio
import argparse
import math
import requests
import os
import os.path
import sys
import time
import subprocess
from collections import namedtuple
from util import disk_to_mbtiles
from download import download_tile
from bounds2tiles import bounds2tiles
from geojson2tiles import geojson2tiles
import json
import tqdm
import pathlib
# ukraine top=52.483 bottom=44.056 left=22.500 right=40.430 center=(48.487, 32.915)
# kiev top=51.413 bottom=49.554 left=29.224 right=32.080 center=(50.4448, 30.5489)
# odessa: top=47.458 bottom=45.599 left=29.421 right=32.278 center=(46.4752, 30.7761)
# nikolaev: top=48.162 bottom=46.408 left=30.388 right=33.157 center=(46.9606, 32.0560)
# example tileservers:
# argis="https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile"
# opentopomaps: "https://tile.opentopomap.org"
possible_domain_prefixes = ["a", "b", "c"] # Only for OpenTopoMaps

parser = argparse.ArgumentParser(description="Takes a bounds as input, calculates tile numbers from it and downloads them as image files.")
parser.add_argument("--min-zoom", type=int, default=5)
parser.add_argument("--max-zoom", type=int, default=16)
parser.add_argument("--center-lat", type=float, default=30.5489)
parser.add_argument("--center-lon", type=float, default=50.4448)
parser.add_argument("--dot", type=bool, default=False)
parser.add_argument("--top", type=float, default=51.413)
parser.add_argument("--bottom", type=float, default=49.554)
parser.add_argument("--left", type=float, default=29.224)
parser.add_argument("--right", type=float, default=32.080)
parser.add_argument("--url", default="http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}")
parser.add_argument("-o", "--output", default="tiles", help="destination directory")
parser.add_argument("--tile_size", type=int, default=256)
parser.add_argument("--geojson_path", default="")

opts = parser.parse_args()
otp = False

if opts.min_zoom > opts.max_zoom:
	print("max-zoom is not > min-zoom")
	sys.exit(1)

if opts.max_zoom > 22:
	print("max-zoom can't be > 22")
	sys.exit(1)

if opts.min_zoom < 1:
	print("min-zoom < 1")
	sys.exit(1)

if opts.left > opts.right:
	print(" left > right, exchanging")
	tmp = opts.left
	opts.left = opts.right
	opts.right = tmp

if opts.top < opts.bottom:
	print(" top < bottom, exchanging")
	tmp = opts.top
	opts.top = opts.bottom
	opts.bottom = tmp

if opts.dot:
	otp = True


def deg2num(lat_deg, lon_deg, zoom):
	lat_rad = math.radians(lat_deg)
	n = 2.0 ** zoom
	xtile = int((lon_deg + 180.0) / 360.0 * n)
	ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
	return xtile, ytile

def download(rect_bounds, geojson_path):
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

		if geojson_path == '':
			tiles = bounds2tiles(rect_bounds, zoom)
		else:
			tiles = geojson2tiles(geojson_path, zoom)

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

		async def taskDispatcher(download_infos):
			tasks = map(download_tile, download_infos)
			done, pending = await asyncio.wait(tasks) # 子生成器
			pbar = tqdm.tqdm(total=len(tiles))
			for r in done: # done和pending都是一个任务，所以返回结果需要逐个调用result()
				pbar.update()
				result = r.result()
				# print(result['tile_info'])
				if result['download_status'] == 'success':
					# download_cnt += 1
					filename = result['tile_info']['filename']
					data = result['data']
					saveFile(filename, data)

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

def get_tile_bounds(zoom, x_index, y_index):
	n = 2.0 ** zoom
	lon_min = x_index / n * 360.0 - 180.0
	lat_min_rad = math.atan(math.sinh(math.pi * (1 - 2 * y_index / n)))
	lat_min = math.degrees(lat_min_rad)

	lon_max = (x_index + 1) / n * 360.0 - 180.0
	lat_max_rad = math.atan(math.sinh(math.pi * (1 - 2 * (y_index + 1) / n)))
	lat_max = math.degrees(lat_max_rad)

	print("lat_min %f, lat_max %f, lon_min %f, lon_max %f" % (lat_min, lat_max, lon_min, lon_max))
	return lat_min, lat_max, lon_min, lon_max

# TODO: Revert to list (namedtuple wtf??)`
rect_bounds = namedtuple('RectBounds', ['top', 'left', 'bottom', 'right'])

# returns tuple (top, left, bottom, right)
def get_bounds():
	return rect_bounds[1]


# get bounds
rect_bounds.top = opts.top
rect_bounds.bottom = opts.bottom
rect_bounds.right = opts.right
rect_bounds.left = opts.left
geojson_path = opts.geojson_path

# download
download(rect_bounds, geojson_path)

#write metadata.json to directory
with open('%s/metadata.json' % pathlib.Path(__file__).parent.absolute()) as meta_file:
	meta_json = json.load(meta_file)
	meta_json['bounds']=",".join([str(rect_bounds.left),str(rect_bounds.bottom),str(rect_bounds.right),str(rect_bounds.top)])
	center_x = (rect_bounds.left+rect_bounds.right)/2.0
	center_y = (rect_bounds.top+rect_bounds.bottom)/2.0
	meta_json['center']=",".join([str(center_x),str(center_y),'14'])
	meta_json['minzoom']=str(opts.min_zoom)
	meta_json['maxzoom']=str(opts.max_zoom)
	output_meta_file_name = "%s/metadata.json" % opts.output
	if os.path.exists(output_meta_file_name):
		os.remove(output_meta_file_name)
	with open(output_meta_file_name,'w') as output_meta_file:
		json.dump(meta_json,output_meta_file)


mbtile_name = "%s.mbtiles" % opts.output
if os.path.exists(mbtile_name):
	os.remove(mbtile_name)

print("merge directory to mbtiles: %s" % mbtile_name)
kwargs = {"silent":True,
		"commpression":False,		
		'scheme':'xyz',
		'format':'png',
		'callback':'grid'}
disk_to_mbtiles(opts.output,mbtile_name,**kwargs)
print("end")