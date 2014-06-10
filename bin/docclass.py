#!/usr/bin/python
#encoding=utf8
import os
import sys
import pdb
import math
sys.path.append('../common')
from tcseg import *


def getwords(doc):
    items = tcsegment(doc)
    words = [item[0].lower() for item in items if len(item[0]) > 2 and len(item[0]) < 50]
    return dict([(w, 1) for w in words])

class Classifier(object):
    '''
    '''
    def __init__(self, getfeatures):
        tcinit()
        #feature -> category -> cnt
        self.fc = {}
        #category -> cnt
        self.cc = {}
        #
        self.getfeatures = getfeatures


    def __del__(self):
        tcuninit()

    def incf(self, f, c):
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(c, 0)
        self.fc[f][c] += 1

    def incc(self, c):
        self.cc.setdefault(c, 0)
        self.cc[c] += 1

    def fcount(self, f, c):
        if f in self.fc and c in self.fc[f]:
            return self.fc[f][c]
        return 0

    def ccount(self, c):
        if c in self.cc:
            return self.cc[c]
        return 0

    def totalcount(self):
        return sum(self.cc.values())

    def categories(self):
        return self.cc.keys()

    def fprob(self, f, c):
        if self.ccount(c) == 0: return 0
        return self.fcount(f, c) * 1.0 / self.ccount(c)

    def weightedprob(self, f, c, prf, weight=1.0, ap=0.5):
        '''
        用初始概率0.5进行平滑
        '''
        basicprob = prf(f, c)
        totals = sum([self.fcount(f, c) for c in self.categories()])
        #计算加权平均
        bp = ((weight * ap) + (totals * basicprob)) / (totals + weight)
        return bp

    def train(self, doc, c):
        features = self.getfeatures(doc)
        for f in features:
            self.incf(f, c)
        self.incc(c)

class Naivebayes(Classifier):
    '''
    #P(A|B) = P(B|A) * P(A)/P(B)
    #P(Category|Doc) = P(Doc|Category) * P(Category) / P(Doc)
    '''
    def __init__(self, getfeatures):
        Classifier.__init__(self, getfeatures)
        self.thresholds = {}

    def docprob(self, doc, c):
        '''
        计算P(Doc|Category)
        '''
        features = self.getfeatures(doc)
        p = 1.0
        for f in features:
            pc = self.weightedprob(f, c, self.fprob)
            #print f, c, pc
            p *= pc
        return p

    def prob(self, doc, c):
        '''
        计算P(Category|Doc)
        '''
        pc = self.ccount(c) *1.0 / self.totalcount()
        pd = self.docprob(doc, c)
        return pc * pd

    def classify(self, doc, default=None):
        probs = {}
        max = -1
        best = default
        for c in self.categories():
            probs[c] = self.prob(doc, c)
            if probs[c] > max:
                max = probs[c]
                best = c
        #for c in probs:
        #    if c == best: continue
        #    if probs[c] * self.thresholds.get(best, 1.0) > probs[best]: return default, probs[c]
        return best, probs[best]

class FisherClassifier(Classifier):
    '''
    #P(A|B) = P(B|A) * P(A)/P(B)
    #P(Category|Doc) = P(Doc|Category) * P(Category) / P(Doc)
    '''
    def __init__(self, getfeatures):
        Classifier.__init__(self, getfeatures)
        self.thresholds = {}

    def fprob(self, f, c):
        '''
        fisher方法的关键
        属于某分类的概率 clf = P(feature|category)
        属于所有分了的概率 freqsum = P(feature|category) 之和
        cprob = clf / (clf + nclf)
        '''
        totals = sum([self.fcount(f, c_) for c_ in self.categories()])
        if self.ccount(c) == 0: return 0
        return self.fcount(f, c) * 1.0 / totals

    def invchi2(self, chi, df):
        '''
        倒置对数卡方分布
        '''
        m = chi / 2.0
        sum = term = math.exp(-m)
        for i in range(1, df // 2):
            term *= m / i
            sum += term
        return min(sum, 1.0)

    def docprob(self, doc, c):
        features = self.getfeatures(doc)
        p = 1.0
        for f in features:
            pf = self.weightedprob(f, c, self.fprob)
            if pf * p > 0:
                p *= pf
        fscore = -2 * math.log(p)
        return self.invchi2(fscore, len(features) * 2)

    def classify(self, doc, default=None):
        best = default
        max = 0.0
        for c in self.categories():
            p = self.docprob(doc, c)
            threshold = self.thresholds.get(c, 0.0)
            if p > threshold and p > max:
                best = c
                max = p
        return best, max

def test():
    #classifier = Classifier(getwords)
    #classifier = Naivebayes(getwords)
    classifier = FisherClassifier(getwords)
    path = '../Sample'
    for root, dirs, files in os.walk(path):
        if root == path:
            continue
        dir_name = os.path.split(root)[-1]
        for f in files:
            fname = os.path.join(root, f)
            doc = open(fname).read().decode('gbk', 'ignore')
            classifier.train(doc, dir_name)

    for root, dirs, files in os.walk(path):
        if root == path:
            continue
        dir_name = os.path.split(root)[-1]
        for f in files:
            fname = os.path.join(root, f)
            doc = open(fname).read().decode('gbk', 'ignore')
            cls, prob = classifier.classify(doc)
            if cls != dir_name:
                print 'fname[%s] prob[%s] orig_cls[%s]->auto_cls[%s] not match!' % (fname, prob, dir_name, cls)

if __name__ == '__main__':
    test()

