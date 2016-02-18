#coding=utf-8
from django.db import models

# Create your models here.
class Token(models.Model):
    token = models.CharField(max_length=512)
    get_time = models.DateTimeField()
    expires_in = models.DurationField()
    def __str__(self):
        return "%s get time %s expires in %s"%(
            self.token,self.get_time,self.expires_in
        )

#用户分组信息
class Grouping(models.Model):
    grouping_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)

class Country(models.Model):
    '''
    国家信息
    '''
    name = models.CharField(max_length=50)

class Province(models.Model):
    '''
    省份
    '''
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country)

class City(models.Model):
    '''
    城市
    '''
    name = models.CharField(max_length=50)
    province = models.ForeignKey(Province)

class Language(models.Model):
    '''
    语言
    '''
    name = models.CharField(max_length=20)

#关注与未关注公众平台的所有用户
class User(models.Model):
    #经过授权获得的用户基本信息
    #用户是否订阅了该公众号

    openid = models.CharField(
        max_length=100,
        help_text='user unique id for this app',
        primary_key=True
    )
    subscribe = models.BooleanField(default=False)
    def is_subscribe(self):
        return self.subscribe
    #昵称
    nickname = models.CharField(
        max_length=50,
        help_text="user's nickname",
        null=True
    )
    #用户性别
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'
    GENDER = (
        (MALE,'male'),
        (FEMALE,'female'),
        (UNKNOWN,'unknown')
    )
    sex = models.CharField(
        max_length=1,choices = GENDER,
        help_text='user_gender',default=FEMALE,
        null=True
    )
    #备注名
    city = models.ForeignKey(City,null=True)
    country = models.ForeignKey(Country,null=True)
    province = models.ForeignKey(Province,null=True)
    language = models.ForeignKey(Language,null=True)
    headimgurl = models.URLField(null = True)
    subscribe_time = models.DateTimeField(null = True)
    remark = models.CharField(max_length=30,null=True,blank=True)
    unionid = models.CharField(max_length=30,null=True,blank=True)
    groupid = models.ForeignKey(
        Grouping,to_field= "grouping_id",null=True,on_delete=models.SET_NULL
    )

#素材相关的数据库模块
class MediaBase(models.Model):
    '''
    包括素材的
    '''

class ReplyText(models.Model):
    '''
    被动回复的文本消息
    '''
    text = models.TextField()

class ReplyImage(models.Model):
    '''
    被动回复的图片消息
    '''
    media_id = models.CharField(max_length=50)

class ReplyVoice(models.Model):
    '''
    被动回复的语音信息
    '''
    media_id = models.CharField(max_length=50)