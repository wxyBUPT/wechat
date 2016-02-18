#coding=utf-8
__author__ = 'xiyuanbupt'
import time
print(time.time())

xml_str = '''
<?xml version="1.0"?>
<doc>
    <branch name="testing" hash="1cdf045c">
        text,source
    </branch>
    <branch name="release01" hash="f200013e">
        <sub-branch name="subrelease01">
            xml,sgml
        </sub-branch>
    </branch>
    <branch name="invalid">
    </branch>
</doc>
'''
xml_str1 = '''
<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
'''
def CDATA(text=None):
    element = ET.Element(CDATA)
    element.text = text
    return element

xml_str2 = b'<xml><ToUserName><![CDATA[gh_01c6fefd895a]]></ToUserName>\n<FromUserName><![CDATA[oDSH6siiDZPcSWoBWmQP4LVwaCzk]]></FromUserName>\n<CreateTime>1455184638</CreateTime>\n<MsgType><![CDATA[text]]></MsgType>\n<Content><![CDATA[\xe4\xbd\xa0\xe5\xa5\xbd]]></Content>\n<MsgId>6249970430253128569</MsgId>\n</xml>'
import xml.etree.ElementTree as ET
root = ET.fromstring(xml_str2)
print(root.tag)
from pprint import pprint
print('在这里')

for child in root:
    print(child.tag,child.attrib)
    print(child.text)

from functools import wraps
class Async:
    def __init__(self,func,args):
        self.func = func
        self.args = args

class Foo:
    def foo(self):
        print('do foo')

    def bar(self):
        print('do bar')

    DICT = {
        'foo':'self.foo()',
        'bar':'self.bar()',
    }

    def nothing(self):
        print('nothing happend')

    def action_map(self,action):
        DICT = {
            'foo':self.foo,
            'bar':self.bar,
        }
        return DICT.get(action,self.nothing)


if __name__ =="__main__":
    k = Foo()
    action = k.action_map('foo')
    action()
    action = k.action_map('b')
    action()



