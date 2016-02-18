#coding=utf-8
__author__ = 'xiyuanbupt'
test_menu_str = '''
 {
     "button":[
     {
          "type":"click",
          "name":"today_son",
          "key":"V1001_TODAY_MUSIC"
      },
      {
           "name":"menu",
           "sub_button":[
           {
               "type":"view",
               "name":"search",
               "url":"http://www.soso.com/"
            },
            {
               "type":"view",
               "name":"video",
               "url":"http://v.qq.com/"
            },
            {
               "type":"click",
               "name":"nice",
               "key":"V1001_GOOD"
            }]
       }
       ]
 }
'''

my_menu_dict = {
    "button": [
        {
            "name": "扫码",
            "sub_button": [
                {
                    "type": "scancode_waitmsg",
                    "name": "扫码带提示",
                    "key": "rselfmenu_0_0",
                    "sub_button": [ ]
                },
                {
                    "type": "scancode_push",
                    "name": "扫码推事件",
                    "key": "rselfmenu_0_1",
                    "sub_button": [ ]
                }
            ]
        },
        {
            "name": "发图",
            "sub_button": [
                {
                    "type": "pic_sysphoto",
                    "name": "系统拍照发图",
                    "key": "rselfmenu_1_0",
                   "sub_button": [ ]
                 },
                {
                    "type": "pic_photo_or_album",
                    "name": "拍照或者相册发图",
                    "key": "rselfmenu_1_1",
                    "sub_button": [ ]
                },
                {
                    "type": "pic_weixin",
                    "name": "微信相册发图",
                    "key": "rselfmenu_1_2",
                    "sub_button": [ ]
                }
            ]
        },
        {
          "name" : "其他" ,
          "sub_button": [
              {
                  "name":"发送位置",
                  "type":"location_select",
                  "key":"rselfmenu_2_0"
              },
              {
                  "name":"点击推事件",
                  "type":"click",
                  "key":"rselfmenu_2_1"
              },
              {
                  "type":"view",
                  "name":"跳转url",
                  "url":"http://www.baidu.com"
              },
          ]
        },
    ]
}