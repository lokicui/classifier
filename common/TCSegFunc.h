/**
 * @file TCSegFunc.h
 *
 * @author jianzhu 
 *
 * @date   2007-09-25
 * 
 * 功能说明.
 *
 * 定义了分词器调用接口
 *
 */

#ifndef TX_PECKER_TCSEGFUNC_H
#define TX_PECKER_TCSEGFUNC_H

#include "TCPub.h"

typedef void* HANDLE;  

/** 
 * @brief 初始化腾讯分词系统，加载分词用数据.
 *
 * @param lpszDataDirPath 分词词典资源目录
 * @return 是否初始化成功
 */
bool TCInitSeg(const char* lpszDataDirPath);


/** 
 * @brief 创建自动中文分词结果句柄
 *
 * @param  iResultMode 分词开关
 * @return 分词句柄
 */
HANDLE TCCreateSegHandle(int iResultMode);


/** 
 * @brief 字符串自动中文分词函数
 * 
 * @param hHandle   分词句柄
 * @param lpText    待切分文本
 * @param nTextLen  待切分文本长度
 * @param nCharSet  字符编码
 * 
 * @return 是否切分成功
 */
bool TCSegment(HANDLE hHandle, const char* lpText, size_t nTextLen = 0, size_t nCharSet = TC_GBK);


/** 
 * @brief 得到分词结果中的词的个数
 * @param hHandle 分词句柄
 */
int  TCGetResultCnt(HANDLE hHandle);


/** 
 * @brief 获得分词结果中指定位置的词
 * 
 * @param hHandle 分词句柄
 * @param index   词的位置
 * 
 * @return 分词结果中 index 位置的词
 */
char* TCGetWordAt(HANDLE hHandle, int index);


/** 
 * @brief 获得分词结果中指定位置的词和词性
 * 
 * @param hHandle 分词句柄
 * @param index   词的位置
 * 
 * @return 分词结果中 index 位置的词和词性
 */
pWP TCGetAt(HANDLE hHandle, int index);

/** 
 * @brief 获得分词结果中指定位置的词(Multi-Seg)
 * 
 * @param hHandle 分词句柄
 * @param index   词的位置
 * 
 * @return 分词结果中 index 位置的词
 */
p_ms_word_t TCMSGetWordAt(HANDLE hHandle, int index);


/** 
 * @brief 获得分词结果中指定位置的词和词性(Multi-Seg)
 * 
 * @param hHandle 分词句柄
 * @param index   词的位置
 * 
 * @return 分词结果中 index 位置的词和词性
 */
p_ms_wp_t TCMSGetAt(HANDLE hHandle, int index);

/**
 * @brief 获取所有分词结果
 *
 * @param hHandle    分词句柄
 * @param seg_tokens 所有分词结果
 *
 * @return 所有分词结果保存在seg_tokens中
 */
void TCGetAllSegInfo(HANDLE hHandle, seg_tokens_t &seg_tokens);

/**
 * @brief 将词条的编码从GBK转换为utf8
 *
 * @param hHandle 分词句柄
 * @param word 词条
 * @param wlen 词长
 */
void TCConvertWordCharsetToUTF8(HANDLE hHandle, const char *&word, size_t &wlen);

/** 
 * @brief  关闭分词句柄
 * 
 * @param hHandle 分词句柄
 */
void TCCloseSegHandle(HANDLE hHandle);


/** 
 * @brief 卸载腾讯中文分词系统，释放分词系统所占资源
 */
void TCUnInitSeg(void);

/**
 * @brief 获取用户自定义词类别数
 *
 * @param hHandle 分词句柄
 * @param cls     用户自定义词类别索引
 *
 * @return 返回该分类号对应的分类数
 */
int TCGetClsNum(HANDLE hHandle, int cls);


/**
 * @brief 获取用户自定义词的类别
 *
 * @param hHandle 分词句柄
 * @param cls     用户自定义词类别索引
 * @param idx     要获取的类别索引
 *
 * @return 返回索引指定的类别
 */
const char* TCGetClsAt(HANDLE hHandle, int cls, int idx);



/**
 * @brief 设定用户自定义词匹配后,分词输出模式
 *
 * 使用用户自定义后，分词输出有如下三种模式
 * OUT_WORD          普通分词输出
 * OUT_PHRASE        包含自定义短语最大匹配的输出
 * OUT_SUBPHRASE     所有匹配的短语列表输出
 *
 * @param hHandle     分词句柄
 * @param outMode     输出取词模式
 */
void TCSetOutMode(HANDLE hHandle, OutMode outMode);


/** 
 * @brief 切换用户用户自定义词典
 * 
 * @param sUserDict 用户自定义词典路径
 */
void TCChangeUserDict(const char* sUserDict);


/** 
 * @brief 将整数表示的词性转为字符串表示
 * 
 * @param idPos  [in]  输入的词性索引
 * @param strPos [out] 输出对应的词性串
 */
void TCPosId2Str(int idPos, char* strPos);


/** 
 * @brief 使用 pku 模式词识别， 用于内部测试
 * @param hHandle 分词句柄
 */
void TCSetPKUMode(HANDLE hHandle);


#endif /* TX_PECKER_TCSEGFUNC_H */
