# Tile Thief 网络地图下载

## 1.安装

1.1安装 python 3.8.x 版本, 并配置python环境变量
https://www.runoob.com/python/python-install.html

1.2 运行库安装

先 安装rasterio开发库，https://www.lfd.uci.edu/~gohlke/pythonlibs/#rasterio
碰到缺什么，直接pip install 就可以了
``` bash
pip install ****

```

### 2  使用说明
使用websocket client 打开地址 ``` ws://localhost:6789/user ``` 连接成功后可以send请求到服务端

action说明如下
#### 2.1 get_google_history 

查询某一层级google earth可供下载的历史影像列表

参数：

**geometry** : geojson格式多边形，代表下载区域范围

**zoom** : 0~22 数值,代表不同比例尺等级

example:
```
{"action":"get_google_history","params":{"geometry":{
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              106.4753723144531250, 29.5243835449218750
            ],
            [
              106.4753723144531250,
              29.5243835449218750
            ],
            [
              106.5769958496093750, 29.6150207519531250
            ],
            [
              106.5769958496093750, 29.5243835449218750
            ],
            [
              106.4753723144531250, 29.5243835449218750
            ]
          ]
        ]
      }
    },"zoom":9}}
``` 

#### 2.1.2 get_tile_count 
给定下载范围和下载层级获取每个层级包含的瓦片数量，目前百度地图只支持矩形查询；根据瓦片数量可以大致估算出需要下载的字节大小，每个缩放等级对应的比例尺信息请参考水经注软件

**min_zoom** : 最小缩放层级

**max_zoom** : 最大缩放层级

**geometry** ：geojson格式范围

**map_type** ："google_map_sat","amap_sat","tianditu_sat","bing_sat","tencent_sat"","baidu_sat","google_earth_sat","google_earth_dem" （google earth暂未实现）

example:
```
{"action":"get_tile_count","params":{"geometry":{
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              106.4753723144531250, 29.5243835449218750
            ],
            [
              106.4753723144531250,
              29.5243835449218750
            ],
            [
              106.5769958496093750, 29.6150207519531250
            ],
            [
              106.5769958496093750, 29.5243835449218750
            ],
            [
              106.4753723144531250, 29.5243835449218750
            ]
          ]
        ]
      }
    },"min_zoom":3,"max_zoom":16,"map_type":"google_map_sat"}}
```

#### 2.1.3 start_task(暂未实现)



#### 2.1.4 cancle_task (暂未实现)

#### 2.2 进度条更新
任务创建成功后，服务端会推送任务进度信息到client端，请使用recv函数接收

### 2.2 待完成功能

...