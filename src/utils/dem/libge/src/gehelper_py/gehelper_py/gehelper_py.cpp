// gehelper_py.cpp : 定义 DLL 应用程序的导出函数。
//

#include "stdafx.h"
#include <string>
#include "gehelper_py.h"
#include "libge.h"
#include "boost/python.hpp"

using namespace boost::python;
using namespace LibGE;

BOOST_PYTHON_MODULE(gehelper_py)
{
	std::string(CLibGEHelper::*getImage1)(double, double, double, double, unsigned int) = &CLibGEHelper::getImage;
	std::string(CLibGEHelper::*getTerrain1)(double, double, double, double, unsigned int) = &CLibGEHelper::getTerrain;

	std::string(CLibGEHelper::*getHistoryImageDates1)(double, double, double, double, unsigned int) = &CLibGEHelper::getHistoryImageDates;

	std::string(CLibGEHelper::*getHistoryImageByDates1)(double, double, double, double, unsigned int, const std::string&) = &CLibGEHelper::getHistoryImageByDates;

	std::string(CLibGEHelper::*cachePath)() = &CLibGEHelper::cachePath;
	void (CLibGEHelper::*setCachePath)(const std::string& path) = &CLibGEHelper::cachePath;


	class_<CLibGEHelper>("CLibGEHelper", init<>()) //导入一个默认构造函数的，类
		.def("Initialize", &CLibGEHelper::Initialize)
		.staticmethod("Initialize")
		.def("getImage", getImage1)
		.def("getTerrain", getTerrain1)
		.def("setCachePath", setCachePath)
		.def("getHistoryImageDates", getHistoryImageDates1)
		.def("getTmDBRoot", &CLibGEHelper::getTmDBRoot)
		.def("getHistoryImageByDates", getHistoryImageByDates1)
		;

};