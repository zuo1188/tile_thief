#!/usr/bin/env python3

import argparse
import math
import requests
import os
import os.path
import sys
import time
import subprocess
from collections import namedtuple

# ukraine top=52.483 bottom=44.056 left=22.500 right=40.430 center=(48.487, 32.915)
# kiev top=51.413 bottom=49.554 left=29.224 right=32.080 center=(50.4448, 30.5489)
# odessa: top=47.458 bottom=45.599 left=29.421 right=32.278 center=(46.4752, 30.7761)
# nikolaev: top=48.162 bottom=46.408 left=30.388 right=33.157 center=(46.9606, 32.0560)
# tileservers:
# argis="https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile"
# opentopomaps: "https://tile.opentopomap.org"
possible_domain_prefixes = ["a", "b", "c"] # Only for OpenTopoMaps

parser = argparse.ArgumentParser(description="Takes a bounds as input, calculates tile numbers from it and downloads them as image files.")
parser.add_argument("--min-zoom", type=int, default=3)
parser.add_argument("--max-zoom", type=int, default=16)
parser.add_argument("--center-lat", type=float, default=30.5489)
parser.add_argument("--center-lon", type=float, default=50.4448)
parser.add_argument("--dot", type=bool, default=False)
parser.add_argument("--top", type=float, default=51.413)
parser.add_argument("--bottom", type=float, default=49.554)
parser.add_argument("--left", type=float, default=29.224)
parser.add_argument("--right", type=float, default=32.080)
parser.add_argument("--url", default="https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile")
parser.add_argument("-o", "--output", default="tiles", help="destination directory")
parser.add_argument("--tile_size", type=int, default=256)

opts = parser.parse_args()
otp = False

if opts.min_zoom > opts.max_zoom:
	print("max-zoom is not > min-zoom")
	sys.exit(1)

if opts.max_zoom > 18:
	print("max-zoom can't be > 18")
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


def download(rect_bounds):
	output_dir = "%s" % os.path.basename(opts.output)
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	total_download_size = 0
	total_optimized_size = 0
	for zoom in range(opts.min_zoom, opts.max_zoom + 1):
		processed_cnt = 0
		download_cnt = 0
		sum_size = 0
		failed_cnt = 0
		(min_x, min_y) = deg2num(rect_bounds.top, rect_bounds.left, zoom)
		(max_x, max_y) = deg2num(rect_bounds.bottom, rect_bounds.right, zoom)

		print("zoom=%d - min_x=%d, min_y=%d, max_x=%d, max_y=%d" % (zoom, min_x, min_y, max_x, max_y))

		for y_index in range(min_y, max_y + 1):
			print(processed_cnt, download_cnt, sum_size)
			for x_index in range(min_x, max_x + 1):
				processed_cnt += 1
				tile_url = opts.url + "/%d/%d/%d.png" % (zoom, y_index, x_index)

				path = "%s/%d/%d" % (output_dir, zoom, x_index)
				filename = path + "/%d.png" % y_index
				if not os.path.exists(path):
					os.makedirs(path)

				data = None
				if not os.path.exists(filename):
					webFile = None

					# low zoom-levels take long to render. Give more time (more retries possible)
					max_retries = 2 ** (15 - zoom)
					if max_retries < 1:
						max_retries = 1

					download_succeeded = False

					for try_nr in range(1, max_retries + 2):
						#for try_nr in range(1, 2):
						try:
							print("trying %s" % tile_url)
							webFile = requests.get(tile_url)
							data = webFile.content
							download_cnt += 1
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
						continue

					try:
						localFile = open(filename, 'wb')
						localFile.write(data)
						webFile.close()
						localFile.close()

						total_download_size += os.path.getsize(filename)

						# if opts.optimize_png:
						# 	tmpfile = "%s/pngcrush_tmp.png" % output_dir
						# 	cmd = "pngcrush -q " + filename + " " + tmpfile
						# 	retcode = subprocess.call(cmd.split(" "))
						# 	if retcode != 0:
						# 		print("ERROR: pngcrush returned %d" % retcode)
						# 	else:
						# 		# replacing the downloaded file with the optimized one
						# 		os.unlink(filename)
						# 		os.rename(tmpfile, filename)
						# 		total_optimized_size += os.path.getsize(filename)

						sum_size += len(data)

					except Exception as e:
						os.unlink(filename)
						failed_cnt += 1
						print(e)
						print("ERROR for %s" % tile_url)
						continue

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

# download
download(rect_bounds)
