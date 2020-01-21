from enum import Enum
from django.db import models


# 视频类型
class VideoType(Enum):
    movie = 'movie'
    cartoon = 'cartoon'  # 卡通
    episode = 'episode'  # 电视剧
    variety = 'variety'  # 综艺
    other = 'other'


VideoType.movie.label = '电影'
VideoType.cartoon.label = '卡通'
VideoType.episode.label = '电视剧'
VideoType.variety.label = '综艺'
VideoType.other.label = '其它'


# 电影来源
class FromType(Enum):
    youku = 'youku'
    custom = 'custom'
    bilibili = 'bilibili'


FromType.youku.label = '优酷'
FromType.custom.label = '自制'
FromType.bilibili.label = 'B站'


# 国家类型
class Nationality(Enum):
    china = 'china'
    japan = 'japan'
    korea = 'korea'
    america = 'america'
    other = 'other'


Nationality.china.label = '中国'
Nationality.japan.label = '日本'
Nationality.korea.label = '韩国'
Nationality.america.label = '美国'
Nationality.other.label = '其它'


# 身份类型
class IdentityType(Enum):
    to_star = 'to_star' # 主演
    supporting_rule = 'supporting_rule' # 配角
    director = 'director'

IdentityType.to_star.label = '主演'
IdentityType.supporting_rule.label = '配角'
IdentityType.director.label = '导演'


# 视频
class Video(models.Model):
    name = models.CharField(max_length=100, null=False)
    image = models.CharField(max_length=500, default='')
    video_type = models.CharField(max_length=50, default=VideoType.other.value)
    from_to = models.CharField(max_length=20, null=False, default=FromType.custom.value)
    nationality = models.CharField(max_length=20, default=Nationality.other.value)  # 国家
    info = models.TextField()
    status = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'video_type', 'from_to', 'nationality')  # 联合索引,只有其中之一不重复即可

    def __str__(self):
        return self.name


# 演员表
class VideoStar(models.Model):
    video = models.ForeignKey(Video, related_name='video_star', on_delete=models.SET_NULL, null=True)  # 关联字段
    name = models.CharField(max_length=100, null=False)
    identity = models.CharField(max_length=50, default='')  # 身份

    class Meta:
        unique_together = ('video', 'name', 'identity')


# 播放地址
class VideoSub(models.Model):
    video = models.ForeignKey(Video, related_name='video_sub', on_delete=models.SET_NULL, null=True)  # 关联字段
    url = models.CharField(max_length=500, null=False)
    number = models.IntegerField(default=1)  # 集数

    class Meta:
        unique_together = ('video', 'number')

    def __str__(self):
        return 'video:{}, num:{}'.format(self.video, self.number)




