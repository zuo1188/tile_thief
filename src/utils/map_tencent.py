from .tile_util import reverse_y_tag 

NUMBER_OF_LEVEL_ZERO_TILES_Y = 1
TENCENT_TEMPLATE_URL = "https://p0.map.gtimg.com/sateTiles/{z}/{sx}/{sy}/{x}_{y}.jpg"

def get_sx(x):
    return x>>4

def get_sy(y, level):
    return reverse_y_tag(y, level)>>4

def get_tencent_url(coord):
    x = coord[0]
    y = coord[1]
    z = coord[2]
    sx = get_sx(x)
    sy = get_sy(y, z)
    tencent_url = TENCENT_TEMPLATE_URL.replace("{x}", str(x))
    tencent_url = tencent_url.replace("{y}", str(reverse_y_tag(y, z)))
    tencent_url = tencent_url.replace("{z}", str(z))
    tencent_url = tencent_url.replace("{sx}", str(sx))
    tencent_url = tencent_url.replace("{sy}", str(sy))
    print(tencent_url)
    return tencent_url

# get_tencent_url([56, 23, 6])
# https://p0.map.gtimg.com/sateTiles/6/3/2/56_40.jpg