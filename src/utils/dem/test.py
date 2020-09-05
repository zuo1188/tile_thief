from gehelper_py import *
ge_helper = CLibGEHelper()
ge_helper.Initialize()
ge_helper.setCachePath("d:/test")
ge_helper.getTmDBRoot()
print("images nums : %d" % ge_helper.getImageNums(106.4753723144531250, 29.5243835449218750, 106.5769958496093750, 29.6150207519531250, 15))
ge_helper.getImage(106.4753723144531250, 29.5243835449218750, 106.5769958496093750, 29.6150207519531250, 15)
ge_helper.getTerrain(106.4753723144531250, 29.5243835449218750, 106.5769958496093750, 29.6150207519531250, 15)
strAllImageDates = ge_helper.getHistoryImageDates(116.13612, 39.710138, 116.657971, 40.096766, 10);
print(strAllImageDates)
ge_helper.getHistoryImageByDates(116.13612, 39.710138, 116.657971, 40.096766, 8, "1984:12:31");