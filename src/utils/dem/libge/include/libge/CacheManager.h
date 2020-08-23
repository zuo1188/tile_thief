#pragma once
#include "export.h"
#include "sqlite3.h"
#include <string>
#include <set>

LIBGE_NAMESPACE_BEGINE
class LIBGE_API CacheManager
{
public:
	typedef enum 
	{
		TYPE_IMAGE = 0,
		TYPE_TERRAIN,
		TYPE_QUADTREE,
		TYPE_VECTOR,
		TYPE_HISTORY_IMAGE,
		TYPE_HISTORY_IMAGE_DATE,
		TYPE_HISTORY_IMAGE_INFO,
		TYPE_UNKNOWN
	}ETableType;

public:
	typedef int(*sqlite3_callback)(void*, int, char**, char**);

public:
	CacheManager();
	~CacheManager();

public:
	static CacheManager& GetInstance() { return _instance; }

public:
	sqlite3* GetSqlite() { return m_pSqlite; }
	bool Open(const char* lpszFile);
	void Close();

	// ������
	// ��ʼ������
	bool BeginTransaction();

	// �ύ����
	bool Commit();

	// �ع�����
	bool Rollback();

	// ִ��SQL���
	bool SQLExec(const char* lpszSQL, sqlite3_callback xCallback, void *pArg, char **pzErrMsg);
	sqlite3_stmt* SQLExec(const char* lpszSQL, char **pzErrMsg);

	// �ǲ�ѯִ�����
	bool ExecNoQuery(const char* lpszSQL, char **pzErrMsg);

	bool AddProvider(unsigned int provider, const std::string& name, unsigned int type);
	bool AddVersion(const std::string& name, unsigned int x, unsigned int y, unsigned int level, unsigned int version, unsigned int channel, unsigned int provider, const std::string& tileDate, ETableType type);
	unsigned int GetVersion(const std::string& name, ETableType type);
	unsigned int GetVersion(unsigned int x, unsigned int y, unsigned int level, ETableType type);

	bool AddFaltfile(const std::string& url, const std::string data, ETableType type);
	std::string GetFaltfile(const std::string& url, ETableType type);

	bool AddImageDates(const std::string& name, const std::string data, ETableType type);
	std::string GetImageDates(const std::string& name, ETableType type);

	bool AddHistoryImageVersionInfo(const std::string& name, const std::string data, ETableType type);
	std::string GetHistoryImageVersionInfo(const std::string& name, ETableType type);

protected:
	sqlite3* _open(const char* lpszFile);
	std::string versionTableName(ETableType type);
	std::string faltFileTableName(ETableType type);

protected:
	sqlite3* m_pSqlite;

private:
	sqlite3_stmt* m_pQuadtreeInsertStmt;

	// runtime
	sqlite3_stmt* m_pRuntimeInsertStmt;
	void* m_hRuntimeMutex;

	// ��ѯTile
	sqlite3_stmt* m_pTileSelectStmt;
	void* m_hSelectMutex;

private:
	static CacheManager _instance;
};
LIBGE_NAMESPACE_END
