#!/usr/bin/python
#encoding=utf8

class DecisionNode(object):
    '''
    决策树节点
    '''
    def __init__(self, col=-1, value=None, result=None, tb=None, fb=None):
        self.col = col
        self.value = value
        self.result = result
        self.tb = tb #true branch
        self.fb = fb #false branch

def divideset(rows, column, value):
    '''
    数据集合拆分
    '''
    func = None
    if isinstance(value, str):
        func = lambda row:row[column] == value
    else:
        func = lambda row:row[column] >= value
    true_set = [r for r in rows if func(r)]
    false_set = [r for r in rows if not func(r)]
    return true_set, false_set

def uniquecounts(rows):
    '''
    每行的最后一列是该行数据对应的分类
    '''
    result = {}
    for row in rows:
        r = row[-1]
        result.setdefault(r, 0)
        result[r] += 1
    return result

def geniimpurity(rows):
    '''
    基尼不纯度
    '''
    size = len(rows)
    result = uniquecounts(rows)
    imp = 0
    for k1 in result:
        p1 = result[k1] * 1.0 / size
        for k 2 in result:
            if k1 == k2:
                continue
            p2 = result[k2] * 1.0 / size
            imp += p1 * p2
    return imp

def entropy(rows):
    '''
    熵
    '''
    from math import log
    log2 = lambda x:log(x)/log(2)
    result = uniquecounts(rows)
    ent = 0.0
    size = len(rows)
    for r in result:
        p = result[r] * 1.0 / size
        ent -= p * log2(p)
    return ent

def build_tree(rows, scoref=entropy):
    if not rows:
        return DecisionNode()
    current_score = scoref(rows)

    best_gain = 0.0
    best_criteria = None
    best_sets = None

    column_size = len(rows[0]) - 1 #最后一列代表改行的分类结果
    for col in range(column_size):
        col_values = set()
        for row in rows:
            col_values.add(row[col])
        for value in col_values:
            true_set, false_set = divideset(rows, col, value)
            if not true_set or not false_set:
                continue
            #计算信息增益
            p = len(true_set) * 1.0 / len(rows)
            gain = current_score - p * scoref(true_set) - (1-p) * scoref(false_set)
            if gain > best_gain:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (true_set, false_set)
    if best_gain > 0:
        true_branch = build_tree(true_set, scoref)
        false_branch = build_tree(false_set, scoref)
        return DecisionNode(best_criteria[0], best_criteria[1], true_branch, false_branch)
    else:
        return DecisionNode(result=uniquecounts(rows))
