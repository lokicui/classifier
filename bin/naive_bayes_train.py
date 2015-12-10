#encoding=utf8
import os
import sys
import pdb
import cPickle
import itertools
import numpy as np
from scipy.sparse import coo_matrix
from datetime import datetime
from collections import defaultdict
from segment import Segmentor
from sklearn.datasets.base import Bunch
from feature_extraction import bow
from sklearn.externals.joblib import Parallel, delayed
from sklearn.externals import joblib

def load_train_file(fname, selected_categorys=None, description=None):
    import json
    data = []
    target = []
    segmentor = Segmentor()
    with open(fname) as ifd:
        for line in ifd:
            obj = json.loads(line)
            if 'topic' not in obj or 'title' not in obj:
                continue
            title = obj['title']
            L = bow(title, skip_unigram=False, segmentor=segmentor)
            title_words = [i.word for i in L]
            #title_words_str = ' '.join(title_words)
            for tname, tidstr in obj['topic'].iteritems():
                if selected_categorys and tname not in selected_categorys:
                    continue
                #data.append(title_words_str)
                data.append(title_words)
                target.append(tname)
    print '%s file name[%s] load %d records' % (datetime.now(), fname, len(data))
    return Bunch(fname=fname,
                         data=data,
                         target=target,
                             DESCR=description)

def train_bunch(bunch, unique_x, unique_y):
    '''
    多项式模型
    _______________________
    文档->category
    转化为
    category ->(feature count)
    '''
    #计算P(W|C), 用稀疏矩阵, sparse matrix
    PWC = {}
    #计算P(C)
    CC = np.zeros(len(unique_y)) #dense vector
    #DF 计算IDF用, 每个词的DF
    DF = np.zeros(len(unique_x))
    for i, (y, X) in enumerate(itertools.izip(bunch.target, bunch.data)):
        y_i = unique_y.searchsorted(y)
        CC[y_i] += 1
        PWC.setdefault(y_i, defaultdict(int))
        for x in X:
            x_i = unique_x.searchsorted(x)
            PWC[y_i][x_i] += 1
            DF[x_i] += 1

    data = []
    row = []
    col = []
    for c,vv in PWC.iteritems():
        for w,v in vv.iteritems():
            row.append(c)
            col.append(w)
            data.append(v)
    return coo_matrix((data, (row,col)), shape=(len(unique_y), len(unique_x))), CC, DF

def train_files(train_glob, selected_categorys=None, description=None):
    import json
    import glob
    fnames = []
    n_jobs = 32
    for i,fname in enumerate(glob.glob(train_glob)):
        fnames.append(fname)

    #map 并行加载数据, 数据解析, 生成 feature
    data_trees = Parallel(n_jobs=n_jobs, verbose=False,
                backend="multiprocessing")(
                delayed(load_train_file)(i, selected_categorys, i)  for i in fnames)

    ################################################################
    #reduce  数据合并
    data = []
    target = []
    feature_set = set()
    for bunch in data_trees:
        for df in bunch.data:
            for f in df:
                feature_set.add(f)
        data.extend(bunch.data)
        target.extend(bunch.target)

    ##map 并行训练
    unique_feature = np.unique(list(feature_set))
    unique_target = np.unique(target)
    print '%s load %d unique features, %d records, %d unique target' % (datetime.now(), len(unique_feature), len(data), len(unique_target))

    train_trees = Parallel(n_jobs=n_jobs, verbose=False,
                backend="multiprocessing")(
                delayed(train_bunch)(i, unique_feature, unique_target)  for i in data_trees)

    #reduce FC进行合并
    PWC, CC, DF = train_trees[0]

    for pwc, cc, df in train_trees[1:]:
        PWC += pwc
        CC += cc
        DF += df
    return PWC, CC, DF, len(target), unique_feature, unique_target

class MultinomialNB(object):
    '''
    numpy scipy 实现的多项式naive bayes
    '''
    def __init__(self):
        self._feature_df = None
        self._pwc = None
        self._cc = None
        self._idf = None
        self._feature_log_prob = None
        self._class_log_prior = None
        self._unique_feature = None
        self._unique_target = None

    def fit(self, train_glob='../zhihu_title_kwds_20151119/JS*', fit_prior=True, selected_categorys=None, description=None):
        #selected_categorys = set([i.strip().decode('utf8') for i in open('list')])
        self._pwc, self._cc, self._feature_df, N, self._unique_feature, self._unique_target = train_files(train_glob, selected_categorys, description)
        smooth_pwc = self._pwc + np.ones((len(self._unique_target), len(self._unique_feature)))
        self._feature_log_prob = np.log(smooth_pwc) - np.log(smooth_pwc.sum(axis=1).reshape(-1, 1))
        self._idf = np.log(N + self._feature_df) - np.log(self._feature_df)  # log(1 + N/ni)
        if fit_prior:
            self._class_log_prior = np.log(self._cc)  - np.log(self._cc.sum()) #先验
        else:
            self._class_log_prior = np.zeros(len(self._unique_target)) - np.log(len(self._unique_target)) # 1/n
        return self

    def predict(self, X):
        F = self.transformer(X)
        probas = F * self._feature_log_prob.T
        return probas

    def transformer(self, X):
        row = []
        col = []
        data = []
        for i,vec in enumerate(X):
            unique_vec, C = np.unique(vec, return_counts=True)
            for f,c in itertools.izip(unique_vec, C):
                x_i = self._unique_feature.searchsorted(f)
                row.append(i)
                col.append(x_i)
                data.append(c)
        return coo_matrix((data, (row,col)), shape=(len(X), len(self._unique_feature)))


#def train_model(model_fname = '../model/classifier.model.%s'):
#    model_fname = model_fname % datetime.now().strftime('%Y%m%d_%H%M%S')
#    clf = MultinomialNB()
#    clf.fit()
#    clf.predict([u'网络游戏'])
#    return
#    print '%s using load %d target' % (datetime.now(), len(train_bunch.target))
#    if True or not os.path.isfile(model_fname):
#        #train_data, test_data, train_data_target, test_data_target = train_test_split(all_train_data, all_target, test_size=0.0)
#
#        #count_vect = CountVectorizer(max_df=0.7, min_df=10, ngram_range=(1, 3))
#        #X_train_counts = count_vect.fit_transform(train_bunch.data)
#        #transformer = TfidfTransformer(ngram_range=(1,3), max_df=0.5, min_df=10)
#        #X_train_tfidf = transformer.fit_transform(train_bunch.data)
#        #上面四句和下面两句的效果一样
#        ###########################################################################
#        #vectorizer = TfidfVectorizer(ngram_range=(1,2), max_df=0.25, min_df=10, norm='l1', max_features=20000)
#        vectorizer = TfidfVectorizer(ngram_range=(1,3), min_df=1, max_df=0.75, norm='l2', max_features=180000)
#        X_train_tfidf = vectorizer.fit_transform(train_bunch.data)
#        print X_train_tfidf.shape
#        ##########################################################################
#        #clf = BernoulliNB()     #伯努利模型
#        clf = MultinomialNB(fit_prior=False)  #多项式模型
#        N = 50000
#        size = X_train_tfidf.shape[0]
#        classes = np.unique(train_bunch.target)
#        for i in range(0, size, N):
#            j = min(i + N, size)
#            print '%s [%s:%s]' % (datetime.now(), i,j)
#            sys.stdout.flush()
#            pdb.set_trace()
#            clf.partial_fit(X_train_tfidf[i:j], train_bunch.target[i:j], classes)# 训练。喝杯咖啡吧
#        joblib.dump((vectorizer, clf), model_fname)
#
#        #for testing
#        for i, tname in enumerate(clf.predict(X_train_tfidf[:100])):
#            #pdb.set_trace()
#            info = '%s=>%s' % (''.join(train_bunch.data[i][:80]), tname)
#            print info.encode('utf8')
#    return joblib.load(model_fname)
#
#if __name__ == '__main__':
#    #tfidf_transformer, clf = train_model()
#    train_model()
#    print 'fit finished!'
#    sys.stdout.flush()
#
