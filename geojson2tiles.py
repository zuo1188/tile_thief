from supermercado import burntiles, super_utils
import json

def burn(features, zoom):
    """
    Burn a stream of GeoJSONs into a output stream of the tiles they intersect for a given zoom.
    """
    features = [f for f in super_utils.filter_features(features)]

    tiles = burntiles.burn(features, zoom)
    # print(tiles)
    return tiles

def load_geoJSON_from_path(path):
    with open(path) as f:
        data = json.load(f)
    return data

def geojson2tiles(geojson_path, zoom):
    geojson = load_geoJSON_from_path(geojson_path)
    return burn(geojson['features'], zoom)

# geojson2tiles('/Users/jrontend/Downloads/test.geojson', 14)
