#coding=utf-8
import xml.etree.ElementTree as ET
import hashlib

from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,Http404
from django.template.loader import get_template
from django.template import Template
from django.views.generic import View
# Create your views here.


class RootViewBase(View):

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
        print('文本消息，消息内容是')
        print(self.xmlContent)
        pass

    def on_link(self,request):
        '''
        响应连接消息
        '''
        pass

    def on_image(self,request):
        '''
        响应图片消息
        '''
        pass

    def on_voice(self,request):
        '''
        响应语音消息
        '''
        pass

    def on_video(self,request):
        '''
        响应视频消息
        '''
        pass

    def on_shortvideo(self,request):
        '''
        响应小视频消息
        '''
        pass

    def on_location(self,request):
        '''
        响应地理位置消息
        '''
        pass

    def on_subscribe(self,request):
        pass

    def on_unsubscribe(self,request):
        pass

    def on_click(self,request):
        pass

    def on_scan(self,request):
        pass

    def on_location_update(self,request):
        pass

    def on_view(self):
        pass

    def on_scancode_push(self,request):
        pass

    def on_scancode_waitmsg(self,request):
        pass

    def on_pic_sysphoto(self,request):
        pass

    def on_pic_photo_or_album(self,request):
        pass

    def on_pic_weixin(self,request):
        pass

    def on_location_select(self,request):
        pass

    def not_defined(self,request):
        pass

    def action_map(self,action):

        ACTION_MAP = {
            'text':self.on_text,
            'image':self.on_image,
            'voice':self.on_voice,
            'video':self.on_video,
            'shortvideo':self.on_shortvideo,
            'location':self.on_location,
            'link':self.on_link,
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
