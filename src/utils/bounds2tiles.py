import math
# from collections import namedtuple

def deg2num(lat_deg, lon_deg, zoom):
	lat_rad = math.radians(lat_deg)
	n = 2.0 ** zoom
	xtile = int((lon_deg + 180.0) / 360.0 * n)
	ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
	return xtile, ytile

def bounds2tiles(rect_bounds, zoom):
    # print(rect_bounds)
    (min_x, min_y) = deg2num(rect_bounds.top, rect_bounds.left, zoom)
    (max_x, max_y) = deg2num(rect_bounds.bottom, rect_bounds.right, zoom)

    print("zoom=%d - min_x=%d, min_y=%d, max_x=%d, max_y=%d" % (zoom, min_x, min_y, max_x, max_y))

    tiles = []
    for y_index in range(min_y, max_y + 1):
        #print(processed_cnt, download_cnt, sum_size)
        for x_index in range(min_x, max_x + 1):
            tiles.append([x_index, y_index, zoom])
    # print(tiles)
    return tiles

# rect_bounds = namedtuple('RectBounds', ['top', 'left', 'bottom', 'right'])
# rect_bounds.top = 40
# rect_bounds.bottom = 39
# rect_bounds.left = 116
# rect_bounds.right = 117
# bounds2tiles(rect_bounds, 15)