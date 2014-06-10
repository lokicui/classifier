import os
import sys

g_idf_dict = {}
for line in open('../data/idf/idf_bin.dat'):
    item = line.strip().split('\t')
    g_idf_dict[int(item[0])] = float(item[1])


def idf(wordid):
    if wordid not in g_idf_dict:
        return 0
    return g_idf_dict[wordid]
