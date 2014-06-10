#encoding=gbk
import sys
import time
import pdb
sys.path.append('../src')
from uniq import get_simhash
from db import DBQuery

class IRecord(object):
    '''
    '''
    PRIMARY_KEY = 'id'
    DB_TABLE = ''
    KEYS = []
    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

    def __cmp__(self, other):
        return cmp(self.id, other.id)

    def get_sort_key(self):
        '''
        qiyi, youku, qq, sohu, tudou, fusion, pps, letv

        '''
        default = 100
        dic = {u'baidu':5, u'douban':6, u'mtime':7,\
               u'youku':11, u'qiyi':12, u'tudou':13, u'sohu':14, u'letv':15, u'56':16, u'sina':17, \
               u'funshion':18, u'pps':19, u'kankan':20}
        return dic.get(self.site, default)
    
    @staticmethod
    def get_site_rank(site):
        default = 1.0
        dic = {u'douban':default, u'mtime':default, u'baidu':1.2, \
               u'youku':default, u'qiyi':default, u'tudou':default, u'sohu':default, u'letv':default, \
               u'56':default, u'sina':default, \
               u'funshion':default, u'pps':default, u'kankan':default}
        return dic.get(site, default)
    
    @staticmethod
    def get_key_title_site_rank(site):
        default = 1.0
        dic = {u'douban':default, u'mtime':default, u'baidu':10, \
               u'youku':default, u'qiyi':default, u'tudou':default, u'sohu':default, u'letv':default, \
               u'56':default, u'sina':default, \
               u'funshion':default, u'pps':default, u'kankan':default}
        return dic.get(site, default)
    
    @staticmethod
    def get_episode_site_rank(site):
        default = 0.5
        dic = {u'baidu':0.9945, u'qq':0.8893, u'tvmao':0.7560, u'tudou':0.8571,\
                u'douban':0.0023, u'qiyi':0.9306, u'56':0.8514, u'wasu':0.8407,\
                u'pptv':0.9216, u'sohu':0.8848, u'youku':0.9117, u'cntv':0.7645,\
                u'funshion':0.8590, u'letv':0.9141, u'pps':0.9009, u'sina':0.8758}
        return dic.get(site, default)

class AlbumCompareRecord(IRecord):
    '''
    聚合用的record
    '''
    DB_TABLE = ''
    PRIMARY_KEY = 'id'
    KEYS = []
    def __init__(self):
        self.raw_record = None
        self.id = 0
        self.title = ''
        self.alias = ''
        self.site = ''
        #预处理分析出来的
        ############
        self.segments = []
        self.trunk = ''
        self.trunk_season = ''
        self.key_title = ''
        self.sub_title = ''
        self.season_num = 0
        self.sub_season = ''
        self.total_season_num = 0
        self.season_type = ''
        self.version = ''
        self.vversion = ''
        self.version_type = 1
        self.title_language = ''
        self.region_language = ''
        self.video_type = 0
        #verbose video type
        self.vvt = ''
        ############
        self.poster_md = ''
        self.poster_url = ''
        self.image_size = 0
        self.album_language = ''
        self.video_language = ''
        self.category = ''
        self.album_type = ''
        self.directors = ''
        self.actors = ''
        self.intro = ''
        self.site = ''
        self.total_episode_num = 0
        self.newest_episode_num = 0
        self.region = ''
        self.pub_year = 0
        self.pub_time = 0
        self.siteid_pair_list = ''
        self.dead = False
        self.ended = 0
        self.simhash_set = set()

    def to_repository_record(self):
        rawrecord = self.raw_record
        record = AlbumRepositoryRecord()
        record.id = self.id
        record.title = self.title
        record.key_title = self.key_title
        record.sub_title = self.sub_title
        record.trunk = self.trunk
        record.sub_season = self.sub_season
        record.show_title = self.title
        record.alias = self.alias
        record.category = self.category
        record.album_type = self.album_type
        record.directors = self.directors
        record.actors = self.actors
        record.intro = self.intro
        record.region = self.region
        record.pub_year = '%04d' % self.pub_year
        record.pub_time = self.pub_time
        record.total_episode_num = self.total_episode_num
        record.newest_episode_num = self.newest_episode_num
        record.siteid_pair_list = self.siteid_pair_list
        record.season_num = self.season_num or 0
        record.total_season_num = self.total_season_num or 0
        record.album_language = self.region_language
        record.ended = self.ended
        record.video_type = self.video_type
        record.poster_md = self.poster_md
        strtime = time.strftime('%F %T' , time.localtime(time.time()))
        record.insert_time = strtime
        record.update_time = strtime
        record.status = 0
        record.score = 0
        record.manual_checked = 0
        record.manual_deleted = 0
        return record

class AlbumRepositoryRecord(IRecord):
    '''
    知识库
    '''
    PRIMARY_KEY = 'id'
    DB_TABLE = 'album_repository'
    KEYS = ['id', 'title', 'key_title', 'trunk', 'sub_title', 'show_title','sub_season', \
            'alias', 'category', 'play_times', 'album_type', 'status',\
           'album_language', 'directors', 'is_hd', 'actors', 'intro', 'region', 'pub_year', 'pub_time', 'video_type',\
           'tag', 'poster_md', 'score', 'total_episode_num', 'newest_episode_num', \
           'manual_deleted', 'major_version_rating',\
           'siteid_pair_list', 'ended', 'manual_weights', 'manual_checked', 'manual_edited_fields', 'simhash',\
            'season_num', 'total_season_num', 'sim_siteid_pair_list',\
            'version', 'insert_time', 'update_time']
    STATUS_NORMAL = 0
    STATUS_UPDATE = 1
    STATUS_NEW = 2
    def __init__(self):
        super(self.__class__, self).__init__()
        for key in  self.KEYS:
            self.__setattr__(key, '')
        self.compare_record = None
        self.simhash_set = set()
        self.site = 'repository'
    
    #建立simhash , 方便站内排重
    def build_simhash_set(self, album_records_id_dict):
        for siteid_pair in self.siteid_pair_list.split('|'):
            items = siteid_pair.split(':')
            if len(items) < 2:
                continue
            site, id = items[:2]
            if not id.isdigit():
                continue
            id = int(id)
            if id not in album_records_id_dict:
                continue
            record = album_records_id_dict[id]
            simhash = get_simhash(record)
            self.simhash_set.add(simhash)
    
    def get_album_compare_record(self, nmlz_func=None, debug=False):
        if not self.compare_record:
            self.compare_record = self.to_album_compare_record(nmlz_func, debug)
        return self.compare_record

    def to_album_compare_record(self, nmlz_func=None, debug=False):
        record = AlbumCompareRecord()
        record.raw_record = self
        record.id = self.id
        record.title = self.title
        record.alias = self.alias
        #预处理分析出来的
        ############
        record.season_num = self.season_num or 0
        record.total_season_num = self.total_season_num or 0
        record.album_language = self.album_language
        record.version = self.version
        record.trunk = self.trunk
        record.sub_season = self.sub_season
        ############
        record.poster_md = self.poster_md
        record.category = self.category
        record.album_type = self.album_type
        record.directors = self.directors
        record.actors = self.actors
        record.intro = self.intro
        record.site = 'repository'
        record.total_episode_num = self.total_episode_num
        record.newest_episode_num = self.newest_episode_num
        record.region = self.region
        record.video_type = self.video_type
        try:
            record.pub_year = int(self.pub_year)
        except:
            record.pub_year = 0
        record.pub_time = self.pub_time
        siteid_pair_list = ''
        for spl in self.siteid_pair_list.split('|'):
            if not spl or ':' not in spl or spl in siteid_pair_list:
                continue
            if not siteid_pair_list:
                siteid_pair_list = spl
            else:
                siteid_pair_list += '|' + spl
        record.siteid_pair_list = siteid_pair_list
        record.simhash_set = self.simhash_set
        if nmlz_func:
            nmlz_func(record, debug)
        return record

    def merge_compare_record(self, compare_record):
        if not self.siteid_pair_list:
            self.siteid_pair_list = compare_record.siteid_pair_list
        else:
            for spl in compare_record.siteid_pair_list.split('|'):
                spl = spl.strip()
                if not spl or spl in self.siteid_pair_list:
                    continue
                if len(self.siteid_pair_list) + len(spl) >= 2000:
                    print >> sys.stderr, 'repository_id:%d siteid_pair_list too long' % self.id
                    continue
                self.siteid_pair_list += '|' + spl
        self.simhash_set |= compare_record.simhash_set
        #知识库数据不更新
        #for k in ['alias', 'directors', 'actors', 'album_type']:
        #    if k in self.manual_edited_fields:
        #        continue
        #    origin = self.__dict__[k]
        #    new = compare_record.__dict__[k]
        #    new_str = ';'.join([t for t in new.split(';') if t not in origin.split(';')])
        #    if new_str:
        #        self.__dict__[k] = ';'.join([origin, new_str])
        #
        #for k in ['season_num', 'album_language', 'version']:
        #    if k not in self.manual_edited_fields and not self.__dict__[k]:
        #        self.__dict__[k] = compare_record.__dict__[k]
        #        #用信息量最大的title作为show_title
        #        self.show_title = compare_record.title

        for k in ['region', 'intro', 'total_episode_num', 'newest_episode_num']:
            if k not in self.manual_edited_fields and not self.__dict__[k]:
                self.__dict__[k] = compare_record.__dict__[k]

        if not self.pub_year and compare_record.pub_year:
            self.pub_year = '%04d' % compare_record.pub_year

        if not self.season_num:
            self.season_num = 0
        if self.total_season_num < compare_record.total_season_num:
            self.total_season_num = compare_record.total_season_num
        
        if not self.ended:
            self.ended = compare_record.ended
        #merge过后的repository_record需要重新生成compare_record?
        if self.compare_record:
            if not self.compare_record.ended:
                self.compare_record.ended = compare_record.ended
            if not self.compare_record.sub_title:
                self.compare_record.sub_title = compare_record.sub_title
            if not self.compare_record.season_num:
                self.compare_record.season_num = compare_record.season_num
            if not self.compare_record.pub_year:
                self.compare_record.pub_year = compare_record.pub_year
            if not self.compare_record.version:
                self.compare_record.version = compare_record.version
            if not self.compare_record.album_language:
                self.compare_record.album_language = compare_record.album_language
            if self.compare_record.total_season_num < compare_record.total_season_num:
                self.compare_record.total_season_num = compare_record.total_season_num
            self.compare_record.simhash_set |= compare_record.simhash_set

class AlbumRecord(IRecord):
    '''
    raw album
    '''
    PRIMARY_KEY = 'id'
    DB_TABLE = 'raw_album'
    KEYS = ['id', 'A1', 'A10', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'actors', \
        'album_final_id', 'album_language', 'language', 'album_type', 'album_url', 'area', 'category', \
        'change_signal', 'collection_count', 'comment_count', 'cover_image_download_status', \
        'cover_image_md5', 'cover_image_url', 'cover_image_url1', 'cover_image_url1_download_status', \
        'cover_image_url1_md5', 'description', 'directors', 'from_channel', 'hd', 'image_size', \
        'insert_time', 'is_end', 'key_md5', 'key_md5_1', 'key_md5_2', 'last_chage_time', \
        'last_update_time', 'manual_deleted', 'now_episode', 'other_title', 'play_count', 'pub_time', \
        'pub_year', 'real_now_episode', 'scores', 'season', 'version', 'site', 'site_album_id', \
        'status', 'tag', 'title', 'total_episode', 'update_level', 'update_time', 'dead_link', \
        'protocol_deleted', 'video_type', 'manual_edited_fields', 'video_language', 'src_rank']
    STATUS_NORMAL = 0
    STATUS_UPDATE = 1
    def __init__(self):
        super(self.__class__, self).__init__()
        for key in  self.KEYS:
            self.__setattr__(key, '')
        self.compare_record = None
    
    def dead(self):
        return self.protocol_deleted or self.manual_deleted or self.dead_link or self.src_rank == -1

    def get_album_compare_record(self, nmlz_func=None, debug=False):
        if not self.compare_record:
            self.compare_record = self.to_album_compare_record(nmlz_func, debug)
        return self.compare_record
    
    def to_album_compare_record(self, nmlz_func=None, debug=False):
        record = AlbumCompareRecord()
        record.dead = self.dead()
        record.raw_record = self
        record.id = self.id
        record.title = self.title
        record.alias = self.other_title
        record.album_language = self.album_language
        record.video_language = self.video_language
        #预处理分析出来的
        ############
        record.key_title = ''
        record.sub_title = ''
        record.season_num = 0
        record.version = ''
        record.title_language = ''
        #############
        record.category = self.from_channel
        record.album_type = self.album_type
        record.directors = self.directors
        record.actors = self.actors
        record.intro = self.description
        record.site = self.site
        record.poster_md = self.cover_image_md5
        record.poster_url = self.cover_image_url
        record.image_size = self.image_size
        record.ended = self.is_end
        record.video_type = self.video_type
        try:
            record.total_episode_num = int(self.total_episode)
        except:
            record.total_episode_num = 0
        record.newest_episode_num = int(self.real_now_episode)
        if self.now_episode.isdigit() and record.newest_episode_num < int(self.now_episode):
            record.newest_episode_num = int(self.now_episode)
        #try:
        #    record.newest_episode_num = int(record.newest_episode_num)
        #except:
        #    record.newest_episode_num = 0

        #if record.total_episode_num and record.total_episode_num < record.newest_episode_num:
        #    record.total_episode_num = record.newest_episode_num

        record.region = self.area
        try:
            record.pub_year = int(self.pub_year[:4])
        except:
            record.pub_year = 0
        record.pub_time = self.pub_time
        record.simhash_set.add(get_simhash(self))
        record.siteid_pair_list = '%s:%s' % (self.site, self.id)
        if nmlz_func:
            nmlz_func(record, debug)
        return record
    
class VideoRecord(IRecord):
    '''
    单视频
    '''
    DB_TABLE = 'video_records'
    PRIMARY_KEY = 'id'
    KEYS = ['id', 'B1', 'B2', 'B3', 'B4', 'actors', 'album_final_id', 'change_signal', \
        'collection_number', 'comment_number', 'complete_title', 'description', 'directors',\
         'duration', 'episode_number', 'hd', 'image_download_status', 'image_md5', \
        'image_size', 'image_url', 'insert_time', 'key_md5', 'key_md5_1', 'manual_deleted', \
        'pub_time', 'raw_album_id', 'site', 'status', 'tag', 'title', 'update_time', 'url']
    def __init__(self):
        super(self.__class__, self).__init__()
        for key in  self.KEYS:
            self.__setattr__(key, '')

class ClusterRelationRecord(IRecord):
    '''
    '''
    DB_TABLE = 'checked_final_relation'
    PRIMARY_KEY = 'key_id'
    KEYS = ['relation', 'kid', 'pid', 'user', 'comment']
    def __init__(self):
        super(self.__class__, self).__init__()
        for key in  self.KEYS:
            self.__setattr__(key, '')

