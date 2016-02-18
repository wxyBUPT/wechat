#coding=utf-8
import json
from django.test import TestCase

# Create your tests here.
class TestConf(TestCase):
    def test_conf(self):
        from wechatserver.conf import appid,secret
        self.assertEqual(appid,'wx78d33529680d969d')
        #print(appid,secret)
        from wechatserver.conf import outhUrl
        #print(outhUrl)
from wechatserver.remote_cmd.remote_tool import RemoteTool
remote_tool = RemoteTool()
class TestRemoteTool(TestCase):
    def test_get_token(self):
        token = remote_tool.get_token()
        #print('token是',token)
        #print('有效时间是',remote_tool.token_expires_in)
        self.assertIsNotNone(token)
        print(token)

    def test_get_ip(self):
        #print(remote_tool.get_wechat_server_ip())
        self.assertIsNotNone(remote_tool.get_wechat_server_ip())

    def test_create_menue(self):

        from wechatserver.remote_cmd.all_menu import my_menu_dict
        my_menu_str = json.dumps(my_menu_dict,ensure_ascii=False)
        res = remote_tool.create_menu(my_menu_str)
        self.assertEqual(res,0)

    def test_create_groups(self):
        json_resp = remote_tool.create_groups("新分组")
        self.assertIsNotNone(json_resp)
        #print(json_resp)
    def test_create_groups_bak(self):
        json_resp = remote_tool.create_groups_bak("最新")
        self.assertIsNotNone(json_resp)
        print(json_resp)

    def test_get_groups(self):
        response = remote_tool.query_all_group()
        self.assertIsNotNone(response)

    def test_query_delete_groups(self):
        res_dict = remote_tool.query_all_group()
        for item in res_dict['groups']:
            id = item['id']
            if id >= 1001:
                res = remote_tool.groups_delete(id)
                #print('删除的返回值为')
                #print(res)
                #self.assertEqual(res['errcode'],0)
        res_dict = remote_tool.query_all_group()
        print(res_dict)
        pass

import wechatserver.models as md
from django.db.models import F,Q
from wechatserver.models import Token
import datetime
class TestWechatserverModels(TestCase):
    def test_token(self):
        token = Token(
            token = 'lZg-E-uc55m8tycgRFLTbtk647tGempZLrFuHQXVpSmiamwNRx2irFhKr23gGLjLXEZOpkxnLMB6N2uHdK6OPAalLGc46TzM25oKub9KGtDsgEv1eGmHVPxsy8Uyg7MWDQIdADAREW',
            get_time = datetime.datetime.now(),
            expires_in = datetime.timedelta(seconds = 3200),
            id = 1
        )
        #print(token.id)
        #print('保存token')
        self.assertEqual(1,token.id)


