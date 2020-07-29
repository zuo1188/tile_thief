python main.py --left 116.2 --bottom 39.1 --right 116.3 --top 39.2 --max-zoom 16 --output /Users/zuojingwei/Dev/tile_spider/beijing
python main.py --top 35.63 --left 139.77 --bottom 35.62 --right 139.78 --max-zoom 19 --output /Users/zuojingwei/Dev/tile_stealer/tiles/tokyo

python main.py --left 103.8506 --bottom 1.3108 --top 1.314298 --right 103.854034  --min-zoom 15 --max-zoom 21 --output /Users/zuojingwei/Dev/tile_stealer/tile/singapore

# amap
python main.py --url https://webst04.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z} \
--left 116.2 --bottom 39.1 --right 116.3 --top 39.2 --max-zoom 15 --output /Users/jrontend/myPrj/tile_thief/beijing_amap

python main.py --url https://webst04.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z} \
--geojson_path /Users/jrontend/Downloads/test.geojson --max-zoom 15 --output /Users/jrontend/myPrj/tile_thief/beijing_amap

# tencent
# https://p0.map.gtimg.com/sateTiles/6/3/2/56_40.jpg
# python main.py --url https://webst01.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z} \
# --left 116.2 --bottom 39.1 --right 116.3 --top 39.2 --max-zoom 16 --output /Users/jrontend/myPrj/tile_thief/beijing
# baidu
# python main.py --url http://shangetu6.map.bdimg.com/it/u=x={x};y={y};z={z};v=009;type=sate&fm=46 \
# --left 116.2 --bottom 39.1 --right 116.3 --top 39.2 --max-zoom 16 --output /Users/jrontend/myPrj/tile_thief/beijing_baidu
# tianditu
# python main.py --url https://t1.tianditu.gov.cn/DataServer?T=img_c&x={x}&y={y}&l={z}&tk=979370626f38396281484293eb175e2e \
# --left 116.2 --bottom 39.1 --right 116.3 --top 39.2 --max-zoom 16 --output /Users/jrontend/myPrj/tile_thief/beijing_tianditu