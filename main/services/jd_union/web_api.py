#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
'''
    :Author: yuangezhizao
    :Time: 2019/2/13 0013 21:55
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
'''
import json
import math

import pymongo
import requests
from bson import ObjectId
from flask import current_app


class WebApi:
    BASE_URL = 'https://union.jd.com/api/'
    GET_CODE_METHOD = 'receivecode/getCode'

    SAVE_GUIDE_SOCIAL_METHOD = 'socialMedia/saveGuideSocial'
    REMOVE_GUIDE_SOCIAL_METHOD = 'socialMedia/removeGuideSocial'
    GET_GUIDE_SOCIAL_LIST_METHOD = 'socialMedia/getGuideSocialList'

    SAVE_PROMOTION_SITE_METHOD = 'promotion/savePromotionSite'
    DEL_PROMOTION_SITE = 'promotion/delPromotionSite'
    QUERY_PROMOTION_SITE_LISTS = 'promotion/queryPromotionSiteLists'

    def __init__(self):
        self.conn = pymongo.MongoClient(current_app.config['MONGODB_SETTINGS']['host'])['jd']
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'content-type': 'application/json',
            'cookie': self.conn['admin_cookie'].find_one({'_id': ObjectId('5c5d7e772c56c16ebefbeff7')})['cookie']
        }

    def create_url(self, social_media_id, sub_pid, channel_url):
        data = {
            'data': {'materialType': 7, 'promotionId': sub_pid, 'promotionType': 3, 'promotionTypeId': social_media_id,
                     'receiveType': 'cps', 'wareUrl': channel_url, 'isSmartGraphics': 0}}
        r = requests.post(self.BASE_URL + self.GET_CODE_METHOD, data=json.dumps(data), headers=self.headers).json()
        if r['code'] == 200:
            return r['data']
        else:
            print(str(r))
            return r

    def create_social_media(self, channel_url, account, social_media_name):
        # 推广管理 > 社交媒体管理 > 添加社交媒体
        # 用户主页地址
        # 登录帐号
        # 媒体名称
        data = {'data': {'homeUrl': channel_url, 'loginAccount': account, 'mediaName': social_media_name}}
        r = requests.post(self.BASE_URL + self.SAVE_GUIDE_SOCIAL_METHOD, data=json.dumps(data),
                          headers=self.headers).json()
        result = self.get_social_media_list()
        if isinstance(result, bool):
            result = 'Update success'
        else:
            result = 'Update failed'
        return r

    def remove_social_media(self, social_media_id):
        # 推广管理 > 社交媒体管理 > 删除社交媒体
        social_media_id = int(social_media_id)
        data = {'data': {'id': social_media_id}}
        r = requests.post(self.BASE_URL + self.REMOVE_GUIDE_SOCIAL_METHOD, data=json.dumps(data),
                          headers=self.headers).json()
        if r['code'] == 200:
            self.conn['jdunion_socialmedia'].remove({'_id': social_media_id})
        else:
            print(str(r))
        result = self.get_social_media_list()
        if isinstance(result, bool):
            result = 'Update success'
        else:
            result = 'Update failed'
        return r

    def get_social_media_list(self, page=1):  # page 参数无需手动传入
        # 推广管理 > 社交媒体管理
        page = int(page)
        data = {'data': {}, 'pageNo': page, 'pageSize': 50, 'totalCount': 0}
        r = requests.post(self.BASE_URL + self.GET_GUIDE_SOCIAL_LIST_METHOD, data=json.dumps(data),
                          headers=self.headers).json()
        if r['code'] == 200:
            self.conn['jdunion_socialmedia'].drop()
            result = r['data']
            for each in result['unionGuideSocialResList']:
                each['_id'] = each['id']
                each.pop('id')
                each.pop('appKeyKpl')
                each.pop('appSecretKpl')
                try:
                    self.conn['jdunion_socialmedia'].insert(each)
                except Exception as e:
                    print(e)
            totalcount = result['page']['totalCount']
            totalpage = int(math.ceil(float(totalcount) / 50.0))
            if page < totalpage:
                self.get_social_media_list(page + 1)
            return True
        else:
            print(str(r))
            return r
        # result = []
        # for each in self.conn['jdunion_socialmedia'].find():
        #     result.append(each)
        # return result
        # 鉴于要加上分页操作，不再此处返回结果

    def create_social_media_loc(self, social_media_id, sub_name):
        # 推广管理 > 推广位管理 > 社交媒体推广位 > 创建推广位
        # 推广位名称
        data = {'data': {'siteId': social_media_id, 'spaceName': sub_name, 'type': '3'}}
        r = requests.post(self.BASE_URL + self.SAVE_PROMOTION_SITE_METHOD, data=json.dumps(data),
                          headers=self.headers).json()
        return r

    def remove_social_media_loc(self, sub_pid):
        # 推广管理 > 推广位管理 > 社交媒体推广位 > 删除社交媒体推广位
        sub_pid = int(sub_pid)
        data = {'data': {'id': sub_pid}}
        r = requests.post(self.BASE_URL + self.DEL_PROMOTION_SITE, data=json.dumps(data), headers=self.headers).json()
        code = r['code']
        if code == 200:
            self.conn['jdunion_socialmedia_loc'].remove({'_id': sub_pid})
        else:
            print(str(r))
        return r

    def get_social_media_loc_list(self, social_media_id, page=1):
        # 推广管理 > 推广位管理 > 社交媒体推广位
        social_media_id = int(social_media_id)
        page = int(page)
        data = {'data': {'id': social_media_id, 'opType': 2, 'promotionType': '3'}, 'pageNo': page, 'pageSize': 50,
                'totalCount': 100}
        r = requests.post(self.BASE_URL + self.QUERY_PROMOTION_SITE_LISTS, data=json.dumps(data),
                          headers=self.headers).json()
        if r['code'] == 200:
            self.conn['jdunion_socialmedia_loc'].drop()
            result = r['data']
            for each in result['promotionLists']:
                each['_id'] = each['id']
                each['social_media'] = social_media_id
                try:
                    self.conn['jdunion_socialmedia_loc'].insert(each)
                except Exception as e:
                    print(e)
            totalcount = result['page']['totalCount']
            totalpage = int(math.ceil(float(totalcount) / 50.0))
            if page < totalpage:
                self.get_social_media_loc_list(social_media_id, page + 1)
            return True
        else:
            print(str(r))
            return r
        # result = []
        # for each in self.conn['jdunion_socialmedia_loc'].find():
        #     result.append(each)
        # return result
        # 鉴于要加上分页操作，不再此处返回结果

    def get_social_media_by_args(self, social_media_id='', social_media_name='', channel_url='', account=''):
        args = {}
        result = []
        if social_media_id:
            args['id'] = int(social_media_id)
        if social_media_name:
            args['mediaName'] = social_media_name
        if channel_url:
            args['homeUrl'] = channel_url
        if account:
            args['loginAccount'] = account
        for each in self.conn['jdunion_socialmedia'].find(args):
            result.append(each)
        return result

    def get_social_media_loc_by_args(self, social_media_id, sub_name=''):
        args = {}
        result = []
        if sub_name:
            args['promotionName'] = sub_name
        args['social_media'] = int(social_media_id)
        for each in self.conn['jdunion_socialmedia_loc'].find(args):
            result.append(each)
        return result
