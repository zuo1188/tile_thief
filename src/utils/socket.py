import websockets
import json
import asyncio

async def hello():
    uri = 'wss://localhost:6789/user'
    async with websockets.connect(uri) as websocket:
        websocket.send(json.dumps({ "action":"start_task", "params":{ "type": "imagery", "geometry":{ "type":"Feature", "properties":{ }, "geometry":{ "type":"Polygon", "coordinates":[ [ [ 106.4753723144531250, 29.5243835449218750 ], [ 106.4753723144531250, 29.5243835449218750 ], [ 106.5769958496093750, 29.6150207519531250 ], [ 106.5769958496093750, 29.5243835449218750 ], [ 106.4753723144531250, 29.5243835449218750 ] ] ] } }, "min_zoom":3, "max_zoom":12, "map_type":"google_map_sat", "output_dir": "/Users/jrontend/myPrj/tile_thief/beijing_google", "process_count": 3 } }))
        return websocket

# asyncio.get_event_loop().run_until_complete(hello())

