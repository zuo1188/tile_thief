// ���� ifdef ���Ǵ���ʹ�� DLL �������򵥵�
// ��ı�׼�������� DLL �е������ļ��������������϶���� GEHELPER_PY_EXPORTS
// ���ű���ġ���ʹ�ô� DLL ��
// �κ�������Ŀ�ϲ�Ӧ����˷��š�������Դ�ļ��а������ļ����κ�������Ŀ���Ὣ
// GEHELPER_PY_API ������Ϊ�Ǵ� DLL ����ģ����� DLL ���ô˺궨���
// ������Ϊ�Ǳ������ġ�
#ifdef GEHELPER_PY_EXPORTS
#define GEHELPER_PY_API __declspec(dllexport)
#else
#define GEHELPER_PY_API __declspec(dllimport)
#endif

// �����Ǵ� gehelper_py.dll ������
class GEHELPER_PY_API Cgehelper_py {
public:
	Cgehelper_py(void);
	// TODO:  �ڴ�������ķ�����
};

extern GEHELPER_PY_API int ngehelper_py;

GEHELPER_PY_API int fngehelper_py(void);
