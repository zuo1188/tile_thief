#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
from types import SimpleNamespace
from download import download, download_vector, get_Imagery_count, get_ge_history, download_ge_data, get_vector_count
from multiprocessing import Process,Manager
import psutil
import signal
import os
logging.basicConfig()

STATE = {"progress": 0, "param": ""}

ws_user = None
ws_worker = None

USERS = dict()


def state_event():
    return json.dumps({"type": "state", **STATE})



workers = {}

# 异步起动进程
async def start_task(params):

    worker_dict=Manager().dict()
    worker_dict["progress_value"]=0
    worker_dict["error_message"]=[]
    if params["type"] == "imagery":
        # todo: 这里应该加参数校验
        if "date" in params:
            dt = params["date"]
        else:
            dt = ""
        p_worker = Process(target=download,args=[params["min_zoom"], params["max_zoom"], params["geometry"], params["map_type"],params["output_dir"], params["process_count"],worker_dict,dt])
        p_worker.start()
        workers[p_worker.pid] = {}
        workers[p_worker.pid]["worker"] = p_worker
        workers[p_worker.pid]["data"] = worker_dict
        
    elif params["type"] == "vector":
        p_worker = Process(target=download_vector,args=[params["name"], params["format"], params["output_dir"],worker_dict])
        p_worker.start()
        workers[p_worker.pid] = {}
        workers[p_worker.pid]["worker"] = p_worker
        workers[p_worker.pid]["data"] = worker_dict
    return json.dumps({"status": 0,"pid":p_worker.pid})


def cancle_task(pid):
    if pid in workers:
        p = psutil.Process(pid)
        p.kill()
    output = {"status": 0}
    return json.dumps(output)


def get_google_history(geometry, zoom):
    output = get_ge_history(geometry, zoom)
    return output


def get_data_count(params):
    #图像以瓦片为单位
    if params["type"] == "imagery":
        output = get_Imagery_count(params["min_zoom"], params["max_zoom"], params["geometry"], params["map_type"])
    #矢量数据以字节为单位
    elif params["type"] == "vector":
        vec_size = get_vector_count(params["name"], params["format"])
        output = {"vector_size":vec_size}
    return json.dumps(output)



def get_progress(pids):
    output = {}
    for pid in pids:
        if pid in workers:
            output[pid]=workers[pid]["data"]["progress_value"]
    
    return json.dumps(output)

def get_error_logs(pids, count):
    output = {}
    for pid in pids:
        if pid in workers:
            if not count:
                output[pid]=workers[pid]["data"]["error_message"][::-1]
            else:
                output[pid]=workers[pid]["data"]["error_message"][int(count) * -1:][::-1]

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
                    await websocket.send(cancle_task(data["pid"]))
                if data["action"] == "get_google_history":
                    await websocket.send(get_google_history(data["params"]["geometry"], data["params"]["zoom"]))
                if data["action"] == "get_data_count":
                    await websocket.send(get_data_count(data["params"]))
                if data["action"] == "get_progress":
                    await websocket.send(get_progress(data["pid"]))
                if data["action"] == "get_error_logs":
                    if 'count' in data:
                        await websocket.send(get_error_logs(data["pid"], data["count"])) 
                    else:
                        await websocket.send(get_error_logs(data["pid"], None))
        finally:
            del USERS['user']


if __name__ == '__main__':
    start_server = websockets.serve(serve, "localhost", 6789)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
