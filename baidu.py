# 此文件无效
import math
from pyproj import Proj

def deg2num(lat_deg, lon_deg, zoom):
    zoom = zoom - 1
    # if lat_deg > 0:
    #     lat_rad = math.radians(90-lat_deg)
    #     is_negative = False
    # else:
    #     lat_rad = math.radians(90+lat_deg)
    #     is_negative = True
    lat_rad = math.radians(lat_deg)
    is_negative = False
    
    n = 2.0 ** zoom
    xtile = int((lon_deg) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    if is_negative == True:
        ytile = ytile * -1 - 1

    print(xtile, ytile)

    return xtile, ytile

# deg2num(40.0005, 116.345, 4)