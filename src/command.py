#!/usr/bin/env python3
import argparse
import sys

from download import download

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
parser.add_argument("--geojson")
parser.add_argument("--concurrent_num", type=int, default=3)
parser.add_argument("--map_type", default="google")

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


download(opts)
