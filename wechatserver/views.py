#coding=utf-8
import xml.etree.ElementTree as ET
import hashlib

from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,Http404
from django.template.loader import get_template
from django.template import Template
from django.views.generic import View

from wechatserver.wxResponse import TextResponse,ImageResponse,VoiceResponse
from wechatserver.wxResponse import VideoResponse
# Create your views here.


class RootViewBase(View):
    '''
    具体的业务逻辑需要重写响应方法，
    当前业务逻辑为回复用户发送过来的消息
    '''

    def debug_response(self,func):
        toUser = self.xmlContent.findtext('ToUserName')
        fromUser = self.xmlContent.findtext('FromUserName')
        msgType = self.xmlContent.findtext('MsgType')
        content = 'in %s : mygType:%s'%(func,msgType)
        return TextResponse(fromUser,toUser,content)

    def _getTFUser(self):
        '''
        一个下面各个方法用的比较多的部分
        '''
        return self.xmlContent.findtext('ToUserName'),self.xmlContent.findtext('FromUserName')

    def get(self,request):
        signature = request.GET['signature']
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        TOKEN = 'TOKEN'
        def check_signature(signature,timestamp,nonce):
            L = [timestamp,nonce,TOKEN]
            L.sort()
            s = L[0] + L[1] + L[2]
            return hashlib.sha1(s.encode('utf-8')).hexdigest() == signature
        if check_signature(signature,timestamp,nonce):
            echostr = request.GET['echostr']
            return HttpResponse(echostr)
        else:
            return Http404('not found')

    def on_text(self,request):
        '''
        响应文本消息
        '''
        toUser = self.xmlContent.findtext('ToUserName')
        fromUser = self.xmlContent.findtext('FromUserName')
        content = self.xmlContent.findtext('Content')
        msgId = self.xmlContent.findtext('MsgId')
        response = TextResponse(fromUser,toUser,'已经收到')
        return response

    def on_link(self,request):
        '''
        响应连接消息
        '''
        return self.debug_response('on_link')

    def on_image(self,request):
        '''
        响应图片消息
        '''
        toUser,fromUser = self._getTFUser()
        mediaId = self.xmlContent.findtext('MediaId')
        imageResponse = ImageResponse(
            fromUser,toUser,mediaId
        )
        return imageResponse

    def on_voice(self,request):
        '''
        响应语音消息
        '''
        toUser , fromUser = self._getTFUser()
        createTime = self.xmlContent.findtext('CreateTime')
        mediaId = self.xmlContent.findtext('MediaId')
        format = self.xmlContent.findtext('Format')
        msgId = self.xmlContent.findtext('MsgId')
        response = VoiceResponse(
            fromUser,toUser,mediaId
        )
        return response

    def on_video(self,request):
        '''
        响应视频消息
        '''
        toUser , fromUser = self._getTFUser()
        mediaId = self.xmlContent.findtext('MediaId')
        thumbMediaId = self.xmlContent.findtext('ThumbMediaId')
        response = VideoResponse(
            fromUser,toUser,mediaId,'你发过来的视频','简单的回复了你的视频'
        )

        return response

    def on_shortvideo(self,request):
        '''
        响应小视频消息
        '''
        return self.debug_response('on_shortvideo')

    def on_location(self,request):
        '''
        响应地理位置消息
        '''
        return self.debug_response('on_location')

    def on_subscribe(self,request):
        if 'subscribed':
            return self.debug_response('on_subscribe')
        elif 'unsubscribed':
            return self.debug_response('on_subscribe')
        pass

    def on_unsubscribe(self,request):
        return self.debug_response('on_unsubscribe')

    def on_click(self,request):
        return self.debug_response('on_click')

    def on_scan(self,request):
        return self.debug_response('on_scan')

    def on_location_update(self,request):
        return self.debug_response('on_location_update')

    def on_view(self):
        return self.debug_response('on_view')

    def on_scancode_push(self,request):
        '''
        扫码推时间的时间推送
        '''
        return self.debug_response('on_scancode_push')

    def on_scancode_waitmsg(self,request):
        return self.debug_response('on_scancode_waitmsg')

    def on_pic_sysphoto(self,request):
        return self.debug_response('on_pic_sysphoto')

    def on_pic_photo_or_album(self,request):
        return self.debug_response('on_pic_photo_or_album')

    def on_pic_weixin(self,request):
        return self.debug_response('on_pic_weixin')

    def on_location_select(self,request):
        return self.debug_response('on_location_select')

    def not_defined(self,request):
        return self.debug_response('not_defined')

    def route_event(self):
        '''
        为event 事件添加路由
        '''
        ACCTION_MAP = {
            #notice subscribe have two condition
            'subscribe':self.on_subscribe,
            'unsubscribe':self.on_unsubscribe,
            'SCAN':self.on_scan,
            'LOCATION':self.on_location,
            'CLICK':self.on_click,
            'VIEW':self.on_view,
            'scancode_push':self.on_scancode_push,
            'scancode_waitmsg':self.on_scancode_waitmsg,
            'pic_sysphoto':self.on_pic_sysphoto,
            'pic_photo_or_album':self.on_pic_photo_or_album,
            'pic_weixin':self.on_pic_weixin,
            'location_select':self.on_location_select,
        }
        event = self.xmlContent.findtext('Event')
        return ACCTION_MAP.get(event,self.not_defined)

    def action_map(self,action):

        ACTION_MAP = {
            'text':self.on_text,
            'image':self.on_image,
            'voice':self.on_voice,
            'video':self.on_video,
            'shortvideo':self.on_shortvideo,
            'location':self.on_location,
            'link':self.on_link,
            'event':self.route_event(),
        }
        return ACTION_MAP.get(action,self.not_defined)

    def post(self,request):
        self.xmlContent = ET.parse(request)
        msgType = self.xmlContent.findtext('MsgType')
        return self.action_map(msgType)(request)

def get_message(request):
    '''
    获得消息类型
    :param request:
    :return:
    '''
    print('get_message called')
    #print(request.body)
    print(request.user)
    print(request.session)
    print(request.method)
    xmlContent = ET.parse(request)
    msgType = xmlContent.findtext('MsgType')
    print(msgType)

    test_ret_mes = '''
    <xml><ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[fromUser]]></FromUserName>
    <CreateTime>12345678</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[你好]]></Content>
    </xml>
    '''
    t = Template(
        '<xml><ToUserName><![CDATA[gh_01c6fefd895a]]></ToUserName>\n<FromUserName><![CDATA[oDSH6siiDZPcSWoBWmQP4LVwaCzk]]></FromUserName>\n<CreateTime>1455184638</CreateTime>\n<MsgType><![CDATA[text]]></MsgType>\n<Content><![CDATA[\xe4\xbd\xa0\xe5\xa5\xbd]]></Content>\n<MsgId>6249970430253128569</MsgId>\n</xml>'
    )
    return HttpResponse(test_ret_mes)

from django.views.generic import View
class MyView(View):
    http_method_names = ['get',]

from wechatserver.forms import ContactForm
from django.views.generic.edit import FormView

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        form.send_email()
        return super(ContactView,self).form_valid(form)

class BaseReceiveView(View):
    http_method_names = ['post']
    def post(self):
        pass
