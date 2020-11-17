// libgeDemo.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "libge.h"

int _tmain(int argc, _TCHAR* argv[])
{
	LibGE::CLibGEHelper::Initialize();
	LibGE::CLibGEHelper helper("e:/test6");
	helper.getTmDBRoot();
	helper.cachePath("e:/test6");
	//std::string strAllImageDates = helper.getHistoryImageDates(116.13612, 39.710138, 116.657971, 40.096766, 10, 256, 256, false);
	//helper.getHistoryImageByDates(116.13612, 39.710138, 116.657971, 40.096766, 8, "1984:12:31", 256, 256, false);
	//helper.getQuadtree(0, 0, 0, 0, true);
	//helper.getQuadtree("0300", false);
	/*helper.getImage("0", 0);
	helper.getImage("00", 0);
	helper.getImage("01", 0);
	helper.getImage("02", 0);
	helper.getImage("03", 0);

	helper.getImage("021031220", 0);
	helper.getTerrain("021031220", 0);
	helper.getImage("021031221", 0);
	helper.getTerrain("021031221", 0);
	helper.getImage("021031222", 0);
	helper.getTerrain("021031222", 0);
	helper.getImage("021031223", 0);
	helper.getTerrain("021031223", 0);

	helper.getImage("0210230303103", 0);
	helper.getTerrain("0210230303103", 0);

	helper.getImage("0210230303100", 0);
	helper.getTerrain("0210230303100", 0);
	helper.getImage("0210230303101", 0);
	helper.getTerrain("0210230303101", 0);
	helper.getImage("0210230303102", 0);
	helper.getTerrain("0210230303102", 0);
	helper.getImage("0210230303103", 0);
	helper.getTerrain("0210230303103", 0);*/

	//helper.getTerrain("021032", 0);
	//helper.getTerrain(206138, 111358, 18, 0);
	//helper.getTerrain(206138, 111359, 18, 0);

	//helper.getImage("021023310120320", 0);
	//helper.getImage(26978, 12414, 15, 0);

	//long image_nums = helper.getImageNums(106.4753723144531250, 29.5243835449218750, 106.5769958496093750, 29.6150207519531250, 15, 256, 256, false);

	//helper.getImage(65.71648222118225, 31.62623091778558, 65.74604425124875, 31.6430146895391, 17, 17, 256, false);

	//helper.getTerrain(28.520508, 40.963308, 28.542480, 40.9798980, 18, 256, 256, false);

	//helper.getTerrain(106.4753723144531250, 29.5243835449218750, 106.5769958496093750, 29.6150207519531250, 3, 256, 256, false);

	helper.getImage(139.39856879708, 35.2806334954318, 139.408261153539, 35.3223243282888, 10, 256, 256, false);
	//helper.getTerrain(106.4753723144531250, 29.5243835449218750, 106.5769958496093750, 29.6150207519531250, 15, 256, 256, false);
	

	/*helper.getImage("0", 0, true);

	helper.getTerrain("0210313121011", 0, true);
	helper.getImage("0210313121011", 0, true);

	helper.getTerrain("02103131210110", 0, true);
	helper.getImage("02103131210110", 0, true);
	helper.getTerrain("02103131210111", 0, true);
	helper.getImage("02103131210111", 0, true);
	helper.getTerrain("02103131210112", 0, true);
	helper.getImage("02103131210112", 0, true);
	helper.getTerrain("02103131210113", 0, true);
	helper.getImage("02103131210113", 0, true);*/

// 	helper.getDBRoot("http://kh.google.com/dbRoot.v5");
// 	helper.geauth("http://kh.google.com/geauth");
// 	helper.getFlatfile("http://kh.google.com/flatfile?q2-02103122-q.729");
// 	helper.getFlatfile("http://kh.google.com/flatfile?q2-021031222010-q.729");
// 	helper.getFlatfile("http://kh.google.com/flatfile?f1-021033021-i.708");
// 	helper.getFlatfile("http://kh.google.com/flatfile?f1c-02103133220-t.524");
// 	helper.getFlatfile("http://kh.google.com/flatfile?f1c-021031223-t.674");
// 
// 	helper.getFlatfile("http://kh.google.com/flatfile?f1c-0210230303103-t.367");
// 	helper.getFlatfile("http://kh.google.com/flatfile?f1c-0210230303102-t.367");
// 	helper.getFlatfile("http://kh.google.com/flatfile?f1c-021023002-t.726");
// 	helper.getFlatfile("http://kh.google.com/flatfile?f1c-021031020-t.674");
// 	helper.getFlatfile("http://kh.google.com/flatfile?f1c-0210310-t.727");
	LibGE::CLibGEHelper::UnInitialize();
	return 0;
}

