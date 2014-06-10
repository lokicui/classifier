/**
 * @file TCPub.h
 *
 * @author jianzhu 
 *
 * @date   2007-09-25
 * 
 * 功能说明.
 *
 * 定义了分词器中所有的开关
 *
 */

#ifndef TX_PECKER_TCPUB_H
#define TX_PECKER_TCPUB_H

#include <cstddef>

/////////////////////////////////////////////////////////////////////////////////////////////
//                        新的分词结果获取接口                                             //
/////////////////////////////////////////////////////////////////////////////////////////////
typedef struct _token_t
{
    const char      *word; // 词条
    unsigned char   pos;   // 词性
    size_t          wlen;  // 词长
    unsigned char   wtype; // 词类(0-普通词 1-multiseg第一种切分形式 2-multiseg第二种切分形式)
}token_t;

typedef struct _comb_token_t
{
    const char      *word; // 词条
    unsigned char   pos;   // 词性
    size_t          wlen;  // 词长
    int             cls;   // 分类号 （该信息只对用户自定义词、短语词有效）
    size_t          sidx;  // 在细切分中开始词索引
    size_t          eidx;  // 在细切分中结束词索引
}comb_token_t;

typedef struct _seg_tokens_t
{
    // 细粒度切分词条
    token_t        *fine_grain_seg_tokens;
    size_t          fine_grain_tokens_num;
    
    // 粗粒度切分词条
    comb_token_t   *thick_seg_tokens;
    size_t          thick_seg_tokens_num;

    // 用户自定义词切分词条
    comb_token_t   *custom_defined_tokens;
    size_t          custom_tokens_num;

    // 用户自定义短语切分词条
    comb_token_t   *custom_defined_phrases;
    size_t          custom_phrases_num;

    // 同义词词条
    comb_token_t   *synonym_tokens;
    size_t          synonym_tokens_num;
}seg_tokens_t;

//////////////////////////////////////////////////////////////////////////////////////////////
//                        旧的分词结果获取接口                                              //
//////////////////////////////////////////////////////////////////////////////////////////////
// 用于保存分词返回结果的结构体
typedef struct wordpos
{
    const char* word;
    int         pos;
    bool        bcw;  // 用户自定义词 ? true : false
    int         cls;  // (用户自定义词 && TC_CLS) ? 用户自定义词分类号 : NULL
}WP, *pWP;

// 用于保存multi-seg分词返回结果的结构体
typedef struct
{
   char *word;
   int	idx;
}ms_word_t, *p_ms_word_t;

// 用于保存mult-seg分词词性标注返回结果的结构体
typedef struct
{
    const char* word;
    int         pos;
    bool        bcw;  // 用户自定义词 ? true : false
    int         cls;  // (用户自定义词 && TC_CLS) ? 用户自定义词分类号 : NULL
    int         idx;
}ms_wp_t, *p_ms_wp_t;


///////////////////////////////////////////////////////////////////////////////////
//                使用用户自定义词后的取词输出模式(default:OUT_WORD)             //
///////////////////////////////////////////////////////////////////////////////////
enum OutMode {
    OUT_WORD = 1,
    OUT_PHRASE,
    OUT_SUBPHRASE
};

////////////////////////////////////////////////////////////////////////////////////
//                             分词切分开关                                       //
////////////////////////////////////////////////////////////////////////////////////
// 数字英文串连续时使用小粒度模式（优先级高于TC_GU)
#define TC_ENGU             0x00000001

// 整个分词系统使用小粒度模式
#define TC_GU               0x00000002

// 进行词性标注
#define TC_POS              0x00000004

// 使用用户自定义词
#define TC_USR              0x00000008

// 进行全角半角转换
#define TC_S2D              0x00000010

// 进行英文大小写转换
#define TC_U2L              0x00000020

// 标注用户自定义词分类号
#define TC_CLS              0x00000040

// 使用规则
#define TC_RUL              0x00000080

// 使用人名识别
#define TC_CN               0x00000100

// 使用繁体转简体
#define TC_T2S              0x00000200

// 人名小粒度开关
#define TC_PGU              0x00000400

// 地名小粒读开关
#define TC_LGU              0x00000800

// 带后缀字的词小粒度开关
#define TC_SGU              0x00001000

// 短语模式切分开关
#define TC_CUT              0x00002000

// 篇章信息分词开关
#define TC_TEXT             0x00004000

// 字符！，： ；？全半角转换关闭开关
#define TC_CONV             0x00008000

// 共享单字片段采用Multi-Seg
#define TC_WMUL             0x00010000

// 真组合歧义片段采用Multi-Seg
#define TC_PMUL             0x00020000

// ASCII字符串作为整体切分
#define TC_ASC              0x00040000

// 使用二级词性
#define TC_SECPOS           0x00080000

// 字符串编码格式
// GBK编码
#define TC_GBK              0x00100000

// UTF-8编码
#define TC_UTF8             0x00200000

// 用于生成新的接口形式即可同时返回
// 细切分、粗切分、用户自定义词、短语词、同义词
#define TC_NEW_RES          0x00400000

// 用于生成同义词
#define TC_SYN              0x00800000

// 地名识别开关
#define TC_LN               0x01000000

// 共享单字片段采用细切分
#define TC_WGU              0x02000000

///////////////////////////////////////////////////////////////////////////////////////////////////
//                            分词词性                                                           //
///////////////////////////////////////////////////////////////////////////////////////////////////
#define TC_A    1   // 形容词
#define TC_AD   2   // 副形词
#define TC_AN   3   // 名形词
#define TC_B    4   // 区别词
#define TC_C    5   // 连词
#define TC_D    6   // 副词
#define TC_E    7   // 叹词
#define TC_F    8   // 方位词
#define TC_G    9   // 语素词
#define TC_H    10  // 前接成分
#define TC_I    11  // 成语
#define TC_J    12  // 简称略语
#define TC_K    13  // 后接成分
#define TC_L    14  // 习用语
#define TC_M    15  // 数词
#define TC_N    16  // 名词
#define TC_NR   17  // 人名
#define TC_NRF  18  // 姓
#define TC_NRG  19  // 名
#define TC_NS   20  // 地名
#define TC_NT   21  // 机构团体
#define TC_NZ   22  // 其他专名
#define TC_NX   23  // 非汉字串
#define TC_O    24  // 拟声词
#define TC_P    25  // 介词
#define TC_Q    26  // 量词
#define TC_R    27  // 代词
#define TC_S    28  // 处所词
#define TC_T    29  // 时间词
#define TC_U    30  // 助词
#define TC_V    31  // 动词
#define TC_VD   32  // 副动词
#define TC_VN   33  // 名动词
#define TC_W    34  // 标点符号
#define TC_X    35  // 非语素字
#define TC_Y    36  // 语气词
#define TC_Z    37  // 状态词
#define TC_AG   38  // 形语素
#define TC_BG   39  // 区别语素
#define TC_DG   40  // 副语素
#define TC_MG   41  // 数词性语素
#define TC_NG   42  // 名语素
#define TC_QG   43  // 量语素
#define TC_RG   44  // 代语素
#define TC_TG   45  // 时语素
#define TC_VG   46  // 动语素
#define TC_YG   47  // 语气词语素
#define TC_ZG   48  // 状态词语素
#define TC_SOS  49  // 开始词
#define TC_EOS  55  // 结束词
#define TC_UNK  0   // 未知词性

#define TC_WWW      50  // URL
#define TC_TELE     51  // 电话号码
#define TC_EMAIL    52  // email

#endif /* TX_PECKER_TCPUB_H */
