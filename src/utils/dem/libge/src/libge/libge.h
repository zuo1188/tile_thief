// libge.cpp : 定义 DLL 应用程序的导出函数。
//
#ifndef _LIBGE_H
#define _LIBGE_H

#include "export.h"
#include <assert.h>
#include <string>
#include <set>
#include <vector>
#include "QuadTreePacket.h"
#include "Terrain.h"
#include "CacheManager.h"

LIBGE_NAMESPACE_BEGINE
class LIBGE_API CLibGEHelper
{
public:
	typedef enum
	{
		FALTFILE_IMAGE = 0,
		FALTFILE_HISTORY_IMAGE,
		FALTFILE_TERRAIN,
		FALTFILE_Q2TREE,
		FALTFILE_QPTREE,
		FALTFILE_LAYER,
		FALTFILE_LAYER_3D,
		FALTFILE_TEXTURE,
		FALTFILE_UNKNOWN = 0xFF
	}EFaltfileType;
public:
	CLibGEHelper();
	virtual ~CLibGEHelper();

public:
	std::string cachePath() { return _cachePath; }
	void cachePath(const std::string& path) { _cachePath = path; }

public:
	int  getDBRoot();
	int  getTmDBRoot();
	std::string getImage(double minX, double minY, double maxX, double maxY, unsigned int level, unsigned int rasterXSize, unsigned int rasterYSize, bool is_mercator = false);
	std::string getImage(double minX, double minY, double maxX, double maxY, unsigned int level);
	std::string getImage(unsigned int x, unsigned int y, unsigned level, int version, bool is_mercator = false);
	std::string getImage(const char* name, int version, bool is_mercator = false);
	std::string getTerrain(unsigned int x, unsigned int y, unsigned level, int version, int* pCols = nullptr, int* pRows = nullptr, bool is_mercator = false);
	std::string getTerrain(const char* name, int version, int* pCols = nullptr, int* pRows = nullptr, bool is_mercator = false);
	std::string getTerrain(double minX, double minY, double maxX, double maxY, unsigned int level, unsigned int rasterXSize, unsigned int rasterYSize, bool is_mercator = false);
	std::string getTerrain(double minX, double minY, double maxX, double maxY, unsigned int level);

	std::string getHistoryImageDates(double minX, double minY, double maxX, double maxY, unsigned int level, unsigned int rasterXSize, unsigned int rasterYSize, bool is_mercator = false);
	std::string getHistoryImageDates(double minX, double minY, double maxX, double maxY, unsigned int level);
	std::set<std::string> getImageDates(const char* name, CacheManager::ETableType type);

	std::string getHistoryImageInfo(const char* name, CacheManager::ETableType type);

	std::string getHistoryImageByDates(double minX, double minY, double maxX, double maxY, unsigned int level, const std::string &date, unsigned int rasterXSize, unsigned int rasterYSize, bool is_mercator = false);
	std::string getHistoryImageByDates(double minX, double minY, double maxX, double maxY, unsigned int level, const std::string &date);

	std::set<std::string> strToSet(const std::string &input);
	std::string setToStr(const std::set<std::string> &input);

	std::string getHistoryImage(const char* name, const std::string &version, const std::string &date_hex, bool is_mercator);

protected:	
	bool geauth();
	QuadTreePacket16* getQuadtree(unsigned int x, unsigned int y, unsigned level, int version);
	QuadTreePacket16* getQuadtree(const char* name, int version);
	QuadTreePacket16* getTmQuadtree(const char* baseGEName, int version);
	std::string randomServerURL();
	std::string randomGEAuth();
	int getVersion(const char* name, CacheManager::ETableType type);
	
	std::string getGEName(const std::string& strUrl);
	EFaltfileType faltFileType(const std::string& strUrl);	
	int Get(const std::string & strUrl, std::string & strResponse, bool useSession);
	int Post(const std::string & strUrl, const char* szPost, int postSize, std::string & strResponse, bool useSession);
	std::string getFlatfile(const std::string& url, const std::string& key, CacheManager::ETableType type);

	std::string UnPackGEZlib(char* srcData, unsigned long srcSize);
	bool  DecodeImage(const char* srcData, unsigned long srcSize, const char* filePath);
	Terrain* DecodeTerrain(const char* name, const char* srcData, unsigned long srcSize);
	QuadTreePacket16* DecodeQuadtree(const char* srcData, unsigned long srcSize);
	QuadTreePacket16* DecodeTmQuadtree(const char* srcData, unsigned long srcSize);

public:
	static void Initialize();
	static void UnInitialize();

private:
	std::string _cachePath;
	std::string _baseURL;
	std::string _hl;
	std::string _gl;
	char _crypt_key[1024];
	std::vector<std::string> _SessionIds;
	std::vector<std::string> _serverURLs;
	std::vector<std::string> _geAuths;
	unsigned short _version;
	unsigned short _tm_version;

	CacheManager _cacheManager;
};

LIBGE_NAMESPACE_END
#endif //_LIBGE_H

