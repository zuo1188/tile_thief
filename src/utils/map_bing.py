import requests
import random

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

BING_ACCESS_KEY = "Arzdiw4nlOJzRwOz__qailc8NiR31Tt51dN2D7cm57NrnceZnCpgOkmJhNpGoppU"
BING_METADATA_URL = "https://dev.virtualearth.net/REST/v1/Imagery/Metadata/Aerial?include=ImageryProviders&key="

def xyz2BingQuadKey(coord):
    u = ''
    zoom = coord[2]
    for i in range(zoom, 1, -1):
        b = 0
        mask = 1 << (i - 1)
        if (coord[0] & mask) != 0:
            b = b + 1
        if (coord[1] & mask) != 0:
            b += 2
        u = u + str(b)
    # print(u)
    return u

def bing_get_meta_info():
    r = requests.get(BING_METADATA_URL + BING_ACCESS_KEY, headers=REQUEST_HEADERS)
    bing_meta_info = r.json()
    if bing_meta_info["statusCode"] == 403:
        print("bing accessed error:", bing_meta_info["errorDetails"][0])
    else:
        print(bing_meta_info)
        return bing_meta_info["resourceSets"][0]["resources"][0]

bing_meta = bing_get_meta_info()

def get_bing_url(coord):
    bing_url = bing_meta["imageUrl"].replace("{subdomain}", random.choice(bing_meta["imageUrlSubdomains"]))
    return bing_url.replace("{quadkey}", xyz2BingQuadKey(coord))
    

# print(get_bing_url([47, 103, 7]))