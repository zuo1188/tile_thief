import math
from collections import namedtuple

R=6378137
BAIDU_TEMPLATE_URL = "http://shangetu6.map.bdimg.com/it/u=x={x};y={y};z={z};v=009;type=sate&fm=46"
# BAIDU_TEMPLATE_URL = "http://online1.map.bdimg.com/onlinelabel/?qt=tile&x={x}&y={y}&z={z}&styles=pl&scaler=1&p=1"

def baidu_get_number_of_tiles_at_level(zoom):
    return math.ceil(2 * math.pi * R / math.pow(2, 26 - zoom))

def baidu_bounds2tiles(rect_bounds, zoom):
    # print(rect_bounds)
    (max_x, max_y) = baidu_coord_to_xy(rect_bounds.top, rect_bounds.left, zoom)
    (min_x, min_y) = baidu_coord_to_xy(rect_bounds.bottom, rect_bounds.right, zoom)

    print("zoom=%d - min_x=%d, min_y=%d, max_x=%d, max_y=%d" % (zoom, min_x, min_y, max_x, max_y))

    tiles = []
    for y_index in range(min_y, max_y + 1):
        #print(processed_cnt, download_cnt, sum_size)
        for x_index in range(min_x, max_x + 1):
            tiles.append([x_index, y_index, zoom])
    # print(tiles)
    return tiles

def baidu_coord_to_xy(lat_deg, lon_deg, zoom):
    lon_rad = math.pi * lon_deg / 180
    lat_rad = math.pi * lat_deg / 180
    x = math.floor(math.pow(2, (zoom - 26)) * R * lon_rad)
    y = math.floor(math.pow(2, (zoom - 26)) * R * math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))))
    return x,y

def get_baidu_url(coord):
    print(coord)
    x = coord[0]
    y = coord[1]
    z = coord[2]
    baidu_url = BAIDU_TEMPLATE_URL.replace("{x}", str(x))
    baidu_url = baidu_url.replace("{y}", str(y))
    baidu_url = baidu_url.replace("{z}", str(z))
    print(baidu_url)
    return baidu_url

# get_baidu_url([52, 24, 6])
