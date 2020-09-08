#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
from types import SimpleNamespace
from download import download, download_vector, get_download_info, get_ge_history, download_ge_data

logging.basicConfig()

STATE = {"progress": 0, "param": ""}

ws_user = None
ws_worker = None

USERS = dict()


def state_event():
    return json.dumps({"type": "state", **STATE})


# 异步起动进程
async def start_task(params):
    if params["type"] == "imagery":
        # todo: 这里应该加参数校验
        download_imagery = download(params["min_zoom"], params["max_zoom"], params["geometry"], params["map_type"],
                                    params["output_dir"], params["process_count"])
        asyncio.ensure_future(download_imagery)
    elif params["type"] == "vector":
        flag = await download_vector(params["name"], params["format"], params["output_dir"])
        if flag == False:
            return json.dumps({"status": -1})
    return json.dumps({"status": 0})


def cancle_task():
    return 1


def get_google_history(geometry, zoom):
    output = get_ge_history(geometry, zoom)
    return output


def get_tile_count(params):
    output = get_download_info(params["min_zoom"], params["max_zoom"], params["geometry"], params["map_type"])
    return json.dumps(output)


def get_google_earth_tile(params):
    new_opts = SimpleNamespace(**params)
    output = download_ge_data(new_opts)
    return json.dumps(output)


async def serve(websocket, path):
    if path == "/user":
        USERS['user'] = websocket
        try:
            await websocket.send(state_event())
            async for message in websocket:
                data = json.loads(message)
                if data["action"] == "start_task":
                    response = await start_task(data["params"])
                    await websocket.send(response)
                if data["action"] == "cancle_task":
                    await websocket.send(cancle_task())
                if data["action"] == "get_google_history":
                    await websocket.send(get_google_history(data["params"]["geometry"], data["params"]["zoom"]))
                if data["action"] == "get_tile_count":
                    await websocket.send(get_tile_count(data["params"]))
                if data["action"] == "get_google_earth_tile":
                    await websocket.send(get_google_earth_tile(data["params"]))
        finally:
            del USERS['user']
    if path == "/worker":
        USERS['worker'] = websocket
        try:
            async for message in websocket:
                data = json.loads(message)
                if data["action"] == "progress":
                    STATE["progress"] = data["progress_value"]
                    print(data["progress_value"])
                    #如果progress为负值说明运行出错
                    if 'user' in USERS:
                        await USERS['user'].send(message)
        finally:
            del USERS['worker']


if __name__ == '__main__':
    start_server = websockets.serve(serve, "localhost", 6789)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
