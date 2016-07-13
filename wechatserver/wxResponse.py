#coding=utf-8
'''
被动回复消息使用
'''
__author__ = 'xiyuanbupt'
from collections import OrderedDict
import time

from lxml.etree import CDATA,Element,ElementTree,tostring
from django.http import HttpResponse

#create a factory function for the cdata element

def dict_to_xml(tag,ori_dict,cdata_except_list=[]):
    '''
    将 key/value 转化为xml，不支持嵌套
    :param tag:
    :param ori_dict:
    :param cdata_key_list: 无需cdata 支持的tag list
    :return:
    '''
    element = Element(tag)
    for key,val in ori_dict.items():
        if type(val) == type({}):
            child = dict_to_xml(key,val,cdata_except_list=cdata_except_list)
            element.append(child)
        elif key not in cdata_except_list:
            child = Element(key)
            child.text = CDATA(val)
            element.append(child)
        else:
            child = Element(key)
            child.text = str(val)
            element.append(child)
    #element = ElementTreeCDATA(element)
    return element


class TextResponse(HttpResponse):
    '''
    Django HttpResponse 的子类，只是固定了 response 实例的content
    内容
    '''

    def __init__(self,toUser,fromUser,text,*args,**kwargs):
        '''

        :param toUser: 接收方账号（收到的OpenId）
        :param fromUser:开发者的微信号
        :param text:回复消息的内容
        :param args:HttpResponse的初始化内容
        :param kwargs:
        :return:
        '''
        super(TextResponse,self).__init__(*args,**kwargs)
        self.content = self._getcontent(toUser,fromUser,text)

    def _getcontent(self,toUser,fromUser,text):
        '''

        :param toUser:
        :param fromUser:
        :param text:
        :return:
        '''
        content_dict = OrderedDict(
            {
                "ToUserName":toUser,
                "FromUserName":fromUser,
                "CreateTime":int(time.time()),
                "MsgType":"text",
                "Content":text
            }
        )
        return tostring(
            dict_to_xml(
                'xml',
                content_dict,
                ["CreateTime",]
            ),
            encoding = "unicode"
        )

class VoiceResponse(HttpResponse):

    def __init__(self,toUser,fromUser,mediaId,*args,**kwargs):
        '''
        Django Response，特定于微信回复语音消息
        :param toUser: 接受方的账号（收到的OpenId）
        :param fromUser: 开发者微信号
        :param mediaId: 通过素材管理接口上传多媒体文件的到的id
        :param args:
        :param kwargs:
        :return:
        '''
        super(VoiceResponse,self).__init__(*args,**kwargs)
        self.content = self._getcontent(toUser,fromUser,mediaId)

    def _getcontent(self,toUser,fromUser,mediaId):
        content_dict = OrderedDict(
            {
                "ToUserName":toUser,
                "FromUserName":fromUser,
                "CreateTime":int(time.time()),
                "MsgType":"voice",
                "Voice":{
                    "MediaId":mediaId
                }
            }
        )
        xml_el = dict_to_xml(
            'xml',content_dict,['CreateTime',]
        )
        return tostring(
            xml_el,
            encoding = "unicode"
        )

class ImageResponse(HttpResponse):

    def __init__(self,toUser,fromUser,mediaId,*args,**kwargs):
        '''
        Django Response，特定于微信回复图片消息
        :param toUser: 接受方的账号（收到的OpenId）
        :param fromUser: 开发者微信号
        :param mediaId: 通过素材管理接口上传多媒体文件的到的id
        :param args:
        :param kwargs:
        :return:
        '''
        super(ImageResponse,self).__init__(*args,**kwargs)
        self.content = self._getcontent(toUser,fromUser,mediaId)

    def _getcontent(self,toUser,fromUser,mediaId):
        content_dict = OrderedDict(
            {
                "ToUserName":toUser,
                "FromUserName":fromUser,
                "CreateTime":int(time.time()),
                "MsgType":"image",
                "Image":{
                    "MediaId":mediaId
                }
            }
        )
        xml_el = dict_to_xml(
            'xml',content_dict,['CreateTime',]
        )
        return tostring(
            xml_el,
            encoding = "unicode"
        )

class VideoResponse(HttpResponse):

    def __init__(
            self,toUser,fromUser,mediaId,
            title,description,
            *args,**kwargs
    ):
        '''
        Django Response，特定于微信回复视频消息
        :param toUser: 接受方的账号（收到的OpenId）
        :param fromUser: 开发者微信号
        :param mediaId: 通过素材管理接口上传多媒体文件的到的id
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        :param args:
        :param kwargs:
        :return:
        '''
        super(ImageResponse,self).__init__(*args,**kwargs)
        self.content = self._getcontent(
            toUser,fromUser,mediaId,
            title,description
        )

    def _getcontent(
            self,toUser,fromUser,mediaId,
            title,description
    ):
        content_dict = OrderedDict(
            {
                "ToUserName":toUser,
                "FromUserName":fromUser,
                "CreateTime":int(time.time()),
                "MsgType":"image",
                "Video":{
                    "MediaId":mediaId,
                    "Title":title,
                    "Description":description,
                }
            }
        )
        xml_el = dict_to_xml(
            'xml',content_dict,['CreateTime',]
        )
        return tostring(
            xml_el,
            encoding = "unicode"
        )

class MusicResponse(HttpResponse):

    def __init__(
            self,toUser,fromUser,
            title,description,musicUrl,
            hQmusicUrl,thumbMediaId,
            *args,**kwargs
    ):
        '''
        Django Response 特定于回复音乐消息
        :param toUser:
        :param fromUser:
        :param title: 音乐标题
        :param description:音乐描述
        :param musicUrl:音乐链接
        :param hQMusciUrl:高质量音乐链接，WIFI环境有限使用该链接播放音乐
        :param thumbMediaId:缩略图的媒体id，通过素材管理接口上传多媒体文件
        :param args:
        :param kwargs:
        :return:
        '''
        super(MusicResponse,self).__init__(*args,**kwargs)
        self.content = self._getcontent(
            toUser,fromUser,
            title,description,
            musicUrl,hQmusicUrl,thumbMediaId
        )

    def _getcontent(
            self,toUser,fromUser,
            title,description,
            musicUrl,hQmusicUrl,
            thumbMediaId
    ):
        content_dict = OrderedDict(
            {
                "ToUserName":toUser,
                "FromUserName":fromUser,
                "CreateTime":int(time.time()),
                "MsgType":"image",
                "Music":{
                    "Title":title,
                    "Description":description,
                    "MusicUrl":musicUrl,
                    "HQMusicUrl":hQmusicUrl,
                    "ThumbMediaId":thumbMediaId
                }
            }
        )
        xml_el = dict_to_xml(
            'xml',content_dict,['CreateTime',]
        )
        return tostring(
            xml_el,
            encoding = "unicode"
        )

class NewsResponse(HttpResponse):
    '''
    Django response ，特定于回复图文消息
    并因为微信的发送消息条数的限制，超过10 条的信息将被忽略
    '''
    def __init__(
            self,toUserName,fromUserName,
            iterItem,*args,**kwargs
    ):
        '''
        :param toUserName:
        :param fromUserName:
        :param iterItem: 一个iterAble
        iterItem 需要支持如下操作
        for item in iterItem :
            title = item.title
            description = item.description
            picur = item.picurl
            url = item.url
        :return:
        '''
        super(NewsResponse,self).__init__(*args,**kwargs)
        self.content = self._getcontent(toUserName,fromUserName,iterItem)

    def _getcontent(self,toUserName,fromUserName,iterItem):
        articleElement = Element('Articles')
        item_count = 0
        for item in iterItem:
            item_count += 1
            if item_count >= 10:
                break
            ori_dict = {
                "Title":item.title,
                "Description":item.description,
                "PicUrl":item.picurl,
                "Url":item.url,
            }
            element = dict_to_xml('item',ori_dict=ori_dict)
            articleElement.append(element)
        ori_dict = {
            "ToUserName":toUserName,
            "FromUserName":fromUserName,
            "CreateTime":int(time.time()),
            "MsgType":"news",
            "ArticleCount":item_count,
        }
        element = dict_to_xml(
            'xml',ori_dict,["CreateTime","ArticleCount"]
        )
        element.append(articleElement)
        return tostring(
            element,
            encoding = "unicode"
        )


if __name__ == "__main__":
    class Structure:
        _fields = []
        def __init__(self,*args):
            if len(args) != len(self._fields):
                raise TypeError('Expected {} arguments'.format(
                    len(self._fields)
                ))
            for name,value in zip(self._fields,args):
                setattr(self,name,value)

    class Item(Structure):
        _fields = ["title","description",'picurl',"url"]

    iterItem = [
        Item("here is title","here is decription",'here is picurl','www.baidu.cmo'),
        Item("here is title2","here is description2","here is picurl2",'www.souhu.com')
    ]
    def _getcontent(toUserName,fromUserName,iterItem):
        articleElement = Element('Articles')
        item_count = 0
        for item in iterItem:
            item_count += 1
            if item_count >= 10:
                break
            ori_dict = {
                "Title":item.title,
                "Description":item.description,
                "PicUrl":item.picurl,
                "Url":item.url,
            }
            element = dict_to_xml('item',ori_dict=ori_dict)
            articleElement.append(element)
        ori_dict = {
            "ToUserName":toUserName,
            "FromUserName":fromUserName,
            "CreateTime":int(time.time()),
            "MsgType":"news",
            "ArticleCount":item_count,
        }
        element = dict_to_xml(
            'xml',ori_dict,["CreateTime","ArticleCount"]
        )
        element.append(articleElement)
        return tostring(
            element,
            encoding = "unicode"
        )
    print(_getcontent("wang","xi",iterItem))