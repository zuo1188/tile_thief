import pathlib
import os
import json
from utils import util

def tiles2mbtiles(opts):
	#write metadata.json to directory
	with open('%s/metadata.json' % pathlib.Path(__file__).parent.absolute()) as meta_file:
		meta_json = json.load(meta_file)
		meta_json['bounds']=",".join([str(opts.left),str(opts.bottom),str(opts.right),str(opts.top)])
		center_x = (opts.left + opts.right)/2.0
		center_y = (opts.top + opts.bottom)/2.0
		meta_json['center']=",".join([str(center_x), str(center_y), '14'])
		meta_json['minzoom']=str(opts.min_zoom)
		meta_json['maxzoom']=str(opts.max_zoom)
		output_meta_file_name = "%s/metadata.json" % opts.output
		if os.path.exists(output_meta_file_name):
			os.remove(output_meta_file_name)
		with open(output_meta_file_name,'w') as output_meta_file:
			json.dump(meta_json,output_meta_file)

	mbtile_name = "%s.mbtiles" % opts.output
	if os.path.exists(mbtile_name):
		os.remove(mbtile_name)

	print("merge directory to mbtiles: %s" % mbtile_name)
	kwargs = {"silent":True,
			"commpression":False,		
			'scheme':'xyz',
			'format':'png',
			'callback':'grid'}
	util.disk_to_mbtiles(opts.output, mbtile_name, **kwargs)
	print("end")