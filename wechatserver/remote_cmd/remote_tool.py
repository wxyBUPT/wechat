# -*- coding: <encoding > -*-
'''
获得access_token 等
'''
__author__ = 'xiyuanbupt'
import json
import datetime,logging
import urllib.request as urllib2

import requests
from requests import Request,Session

from wechatserver.common.comm import Singleton
from wechatserver.models import Token

dlogger = logging.getLogger('debug')
class RemoteTool(Singleton):
    '''
    负责所有向微信服务器发送请求
    '''

    def __init__(self):
        dlogger.debug('init RemoteTool')
        self.token = None
        self.token_get_time = None
        self.token_expires_in = None

    def _need_regain_token(self):
        '''
        判断是否需要重新获得token
        :return:
        '''
        if self.token == None:
            #当Token为None的时候首先尝试从数据库中获得Token
            try:
                token = Token.objects.get(pk=1)
                self.token = token.token
                self.token_get_time = token.get_time
                self.token_expires_in = token.expires_in
                dlogger.debug('get token from db')
            except:
                dlogger.debug('get token from db fail,regain token from wechat server')
                return True
        if datetime.datetime.now() >= (
            self.token_get_time + self.token_expires_in
        ):
            dlogger.debug('db token already outdate,regain token from wechat server')
            return True
        dlogger.debug('use cache token ')
        return False

    def _regain_token(self):
        dlogger.debug('regain token from wechat server')
        from wechatserver.conf import outhUrl
        r = requests.get(outhUrl)
        res = r.json()
        self.token = res['access_token']
        self.token_expires_in = datetime.timedelta(seconds = int(res['expires_in']))
        self.token_get_time = datetime.datetime.now()
        token = Token(
            token = self.token,
            get_time = self.token_get_time,
            expires_in = self.token_expires_in,
            id = 1
        )
        dlogger.debug(token)
        dlogger.debug(
            'save token {t.token} id: {t.id}'.format(
                t = token
            )
        )
        token.save()

    def _post(self,url,data_dict):
        '''
        适用于只在url 后面加access_token 参数的调用
        :param url:
        :param data:
        :return:
        '''
        if url.startswith('http'):
            pass
        else:
            url = 'https://api.weixin.qq.com/cgi-bin/' + url
        par = {
            'access_token':self.get_token()
        }
        data_json = json.dumps(data_dict,ensure_ascii=False)
        r = requests.post(
            url,
            params = par,
            data=data_json.encode('utf-8')
        )
        return r.json()

    def _get(self,url,other_par = {}):
        if url.startswith('http'):
            pass
        else:
            url = 'https://api.weixin.qq.com/cgi-bin/' + url
        par = {
            'access_token':self.get_token()
        }
        par.update(other_par)
        r = requests.get(url,params=par)
        return r.json()

    def get_token(self):
        if self._need_regain_token():
            self._regain_token()
        return self.token

    def get_wechat_server_ip(self):
        from wechatserver.conf import callbackip_url
        ACCESS_TOKEN = self.get_token()
        par = {'access_token':ACCESS_TOKEN}
        r = requests.get(callbackip_url,params=par)
        dlogger.debug(r.url)
        return r.json()['ip_list']

    def create_menu(self,menu_str):
        '''
        创建自定义菜单
        :param menu_str:
        :return:
        '''
        from wechatserver.conf import menu_create_url
        menu_create_url = menu_create_url.format(
            ACCESS_TOKEN = self.get_token()
        )
        #menu_dict = json.dumps(menu_str,ensure_ascii=False).encode('utf-8')
        req = urllib2.Request(url=menu_create_url,data=menu_str.encode('utf-8'))
        req.add_header('Content-Type','application/json')
        req.add_header('encoding','utf-8')
        response = urllib2.urlopen(req)
        r = response.read()
        #r = requests.post(menu_create_url,data=menu_dict)
        r = json.loads(r.decode('utf-8'))
        return r['errcode']

    def create_groups(self,group_name):
        '''
        创建用户分组
        :param group_name:
        :return:
        '''
        from wechatserver.conf import groups_create_url
        groups_create_url = groups_create_url.format(
            ACCESS_TOKEN = self.get_token()
        )
        print(groups_create_url)
        group_dict = {
            "group" : {
                "name":group_name
            }
        }
        group_json = json.dumps(group_dict,ensure_ascii=False)
        req = urllib2.Request(
            url=groups_create_url,
            data=group_json.encode('utf-8')
        )
        response = urllib2.urlopen(req)
        r = response.read()
        r = json.loads(r.decode('utf-8'))
        #print(r)
        return r

    def get_menu(self):
        '''
        获得菜单
        :return:
        '''
        from wechatserver.conf import menu_get_url
        par = {"access_token":self.get_token()}
        r = requests.get(menu_get_url,params=par)
        return r.json()

    def create_groups_bak(self,group_name):
        '''
        创建用户分组
        :return:
        '''
        from wechatserver.conf import groups_create_url_bak
        group_dict = {
            "group" : {
                "name":group_name
            }
        }
        #print(group_dict)
        group_json = json.dumps(group_dict,ensure_ascii=False)
        #print(group_json)
        par = {"access_token":self.get_token()}
        r = requests.post(
            groups_create_url_bak,
            data = group_json.encode('utf-8'),
            params = par,
        )
        return r.json()

    #查询所有的分组
    def query_all_group(self):
        from wechatserver.conf import groups_get_url
        par = {'access_token':self.get_token()}
        r = requests.get(
            groups_get_url,params=par
        )
        r.encoding = 'utf-8'
        #print(r.text)
        return r.json()

    def query_user_group(self,open_id):
        from wechatserver.conf import user_group_get_url
        par = {'access_token':self.get_token()}
        data_dict = {"openid":open_id}
        data_json = json.dumps(data_dict)
        r = requests.post(
            user_group_get_url,data=data_json,
            params = par
        )
        return r.json()

    def rename_group(self,group_id,name):
        '''
        修改分组名称
        :param group_id:
        :param name:
        :return:
        '''
        from wechatserver.conf import groups_update_url
        group_dict = {
            'group':{
                'id':group_id,
                'name':name,
            }
        }
        par = {
            'access_token':self.get_token()
        }
        group_json = json.dumps(group_dict,ensure_ascii=False)
        r = requests.post(
            groups_update_url,
            data=group_json.encode('utf-8'),
            params = par
        )
        return r.json()

    def groups_member_update(self,openid,to_groupid):
        '''
        移动用户分组
        :param openid:
        :param to_groupid:
        :return:
        '''
        from wechatserver.conf import groups_member_update_url
        data_dict = {
            "openid":openid,
            "to_group":to_groupid
        }
        par = {
            'access_token':self.get_token()
        }
        data_json = json.dumps(data_dict,ensure_ascii=False)
        r = requests.post(
            groups_member_update_url,
            data = data_json,
            params = par
        )
        return r.json()

    def groups_members_batchupdate(self,openid_list,to_groupid):
        '''
        批量移动用户分组
        :param openid_list:
        :param to_groupid:
        :return:
        '''
        from wechatserver.conf import groups_member_batchupdate_url
        data_dict = {
            "openid_list":list(openid_list),
            'to_groupid':to_groupid
        }
        par = {
            'access_token':self.get_token()
        }
        data_json = json.dumps(data_dict)
        r = requests.post(
            groups_member_batchupdate_url,
            data=data_json,
            params = par
        )
        return r.json()

    def groups_delete(self,groupid):
        '''
        删除分组
        :return:
        '''
        from wechatserver.conf import groups_delete_url
        data_dict = {
            'group':{
                'id':groupid
            }
        }
        par = {
            'access_token':self.get_token()
        }
        data_json = json.dumps(data_dict,ensure_ascii=False)
        r = requests.post(
            groups_delete_url,
            data=data_json,
            params = par
        )
        #{"errcode": 0, "errmsg": "ok"}
        #{"errcode":40013,"errmsg":"invalid appid"}
        return r.json()

    def updateremark(self,openid,remark):
        from wechatserver.conf import updateremark_url
        data_dict = {
            "openid":openid,
            "remark":remark
        }
        return self._post(updateremark_url,data_dict)

    def get_user_info(self,openid):
        '''
        获得用户基本信息
        :param openid:
        :return:
        '''
        from wechatserver.conf import user_info_url
        par = {
            "openid":openid,
            "lang":"zh_CN"
        }
        return self._get(user_info_url,par)

    def get_user_info_batchget(self,openid_list):
        '''
        批量获取用户基本信息
        :param openid_list:
        :return:
        '''
        from wechatserver.conf import user_info_batchget_url
        tmp = []
        for openid in openid_list:
            tmp.append(
                {
                    "openid":openid,
                    "lang":"zh-CN"
                }
            )
        data_dict = {
            "user_list":tmp
        }
        return self._post(user_info_batchget_url,data_dict)