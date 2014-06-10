#!/usr/local/bin/python
#encoding=gbk

import os
import sys
sys.path.append('../common')
import TCWordSeg

OUT_WORD = TCWordSeg.OUT_WORD
OUT_PHRASE = TCWordSeg.OUT_PHRASE
OUT_SUBPHRASE = TCWordSeg.OUT_SUBPHRASE
TC_ENGU = TCWordSeg.TC_ENGU
TC_GU = TCWordSeg.TC_GU
TC_POS = TCWordSeg.TC_POS
TC_USR = TCWordSeg.TC_USR
TC_S2D = TCWordSeg.TC_S2D
TC_U2L = TCWordSeg.TC_U2L
TC_CLS = TCWordSeg.TC_CLS
TC_RUL = TCWordSeg.TC_RUL
TC_CN = TCWordSeg.TC_CN
TC_T2S = TCWordSeg.TC_T2S
TC_PGU = TCWordSeg.TC_PGU
TC_LGU = TCWordSeg.TC_LGU
TC_SGU = TCWordSeg.TC_SGU
TC_CUT = TCWordSeg.TC_CUT
TC_TEXT = TCWordSeg.TC_TEXT
TC_CONV = TCWordSeg.TC_CONV
TC_WMUL = TCWordSeg.TC_WMUL
TC_PMUL = TCWordSeg.TC_PMUL
TC_ASC = TCWordSeg.TC_ASC
TC_SECPOS = TCWordSeg.TC_SECPOS
TC_GBK = TCWordSeg.TC_GBK
TC_UTF8 = TCWordSeg.TC_UTF8
TC_NEW_RES = TCWordSeg.TC_NEW_RES
TC_SYN = TCWordSeg.TC_SYN
TC_LN = TCWordSeg.TC_LN
TC_WGU = TCWordSeg.TC_WGU
TC_A = TCWordSeg.TC_A
TC_AD = TCWordSeg.TC_AD
TC_AN = TCWordSeg.TC_AN
TC_B = TCWordSeg.TC_B
TC_C = TCWordSeg.TC_C
TC_D = TCWordSeg.TC_D
TC_E = TCWordSeg.TC_E
TC_F = TCWordSeg.TC_F
TC_G = TCWordSeg.TC_G
TC_H = TCWordSeg.TC_H
TC_I = TCWordSeg.TC_I
TC_J = TCWordSeg.TC_J
TC_K = TCWordSeg.TC_K
TC_L = TCWordSeg.TC_L
TC_M = TCWordSeg.TC_M
TC_N = TCWordSeg.TC_N
TC_NR = TCWordSeg.TC_NR
TC_NRF = TCWordSeg.TC_NRF
TC_NRG = TCWordSeg.TC_NRG
TC_NS = TCWordSeg.TC_NS
TC_NT = TCWordSeg.TC_NT
TC_NZ = TCWordSeg.TC_NZ
TC_NX = TCWordSeg.TC_NX
TC_O = TCWordSeg.TC_O
TC_P = TCWordSeg.TC_P
TC_Q = TCWordSeg.TC_Q
TC_R = TCWordSeg.TC_R
TC_S = TCWordSeg.TC_S
TC_T = TCWordSeg.TC_T
TC_U = TCWordSeg.TC_U
TC_V = TCWordSeg.TC_V
TC_VD = TCWordSeg.TC_VD
TC_VN = TCWordSeg.TC_VN
TC_W = TCWordSeg.TC_W
TC_X = TCWordSeg.TC_X
TC_Y = TCWordSeg.TC_Y
TC_Z = TCWordSeg.TC_Z
TC_AG = TCWordSeg.TC_AG
TC_BG = TCWordSeg.TC_BG
TC_DG = TCWordSeg.TC_DG
TC_MG = TCWordSeg.TC_MG
TC_NG = TCWordSeg.TC_NG
TC_QG = TCWordSeg.TC_QG
TC_RG = TCWordSeg.TC_RG
TC_TG = TCWordSeg.TC_TG
TC_VG = TCWordSeg.TC_VG
TC_YG = TCWordSeg.TC_YG
TC_ZG = TCWordSeg.TC_ZG
TC_SOS = TCWordSeg.TC_SOS
TC_EOS = TCWordSeg.TC_EOS
TC_UNK = TCWordSeg.TC_UNK
TC_WWW = TCWordSeg.TC_WWW
TC_TELE = TCWordSeg.TC_TELE
TC_EMAIL = TCWordSeg.TC_EMAIL

g_seghandle = None
def tcinit(SEG_MODE=TC_ENGU|TC_U2L|TC_POS|TC_S2D|TC_T2S|TC_CN|TC_TEXT|TC_CUT|TC_USR|TC_T2S):
    global g_seghandle
    if g_seghandle:
        return False
    TCWordSeg.TCInitSeg('../data/tc_seg')
    g_seghandle = TCWordSeg.TCCreateSegHandle(SEG_MODE)
    return g_seghandle

def tcuninit():
    global g_seghandle
    if not g_seghandle:
        return False
    TCWordSeg.TCCloseSegHandle(g_seghandle)
    TCWordSeg.TCUnInitSeg()
    return True

def tcsegment(string):
    ret = []
    global g_seghandle
    TCWordSeg.TCSegment(g_seghandle, string.encode('gbk'))
    rescount = TCWordSeg.TCGetResultCnt(g_seghandle)
    last_pos = 0
    for i in range(rescount):
        wordpos = TCWordSeg.TCGetAt(g_seghandle, i);
        word = wordpos.word.decode('gbk')
        pos  = wordpos.pos
        bcw = wordpos.bcw
        cls = wordpos.cls
        idx = last_pos
        last_pos = idx + len(word)
        ret.append((word, pos, bcw, cls, idx))
    return ret




if __name__ == '__main__':
    tcinit()
    for item in  tcsegment(sys.argv[1].decode('utf8')):
        print item[0].encode('utf8'), item[1], item[4]
    tcuninit()


