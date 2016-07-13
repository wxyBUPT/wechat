#coding=utf-8
__author__ = 'xiyuanbupt'
from configparser import ConfigParser
configParser = ConfigParser()
configParser.read('./wechatserver/conf.conf')
appid = configParser.get('outh','APPID')
secret = configParser.get('outh','SECRET')
outhUrl = configParser.get('outh','url').format(
    APPID = appid,SECRET = secret
)
callbackip_url = configParser.get('url','callback_ip_url')
menu_create_url = configParser.get('url','menu_create')
menu_get_url = configParser.get('url','menu_get')
groups_create_url = configParser.get('url','groups_create')
groups_create_url_bak = configParser.get('url','groups_create_bak')
groups_get_url = configParser.get('url','groups_get')
user_group_get_url = configParser.get('url','user_group_get')
groups_update_url = configParser.get('url','groups_update')
groups_member_update_url = configParser.get('url','groups_member_update')
groups_member_batchupdate_url = configParser.get('url','groups_member_batchupdate')
groups_delete_url = configParser.get('url','groups_delete')
updateremark_url = configParser.get('url','updateremark')
user_info_url = configParser.get('url','user_info')
user_info_batchget_url = configParser.get('url','user_info_batchget')
