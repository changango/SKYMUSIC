from django.db import models

# Create your models here.
from datetime import datetime


# 歌曲分类表
class songsort(models.Model):
    songsort_id = models.AutoField('序号', primary_key=True)
    songsortname = models.CharField('歌曲类别', max_length=10)

    def toDict(self):
        return {'songsort_id': self.songsort_id,
                'songsortname': self.songsortname}

    class Meta:
        # 设置Admin界面的显示内容
        managed = False
        db_table = "songsort"


# 歌手分类表
class singersort(models.Model):
    singersort_id = models.AutoField('序号', primary_key=True)
    singersortname = models.CharField('歌手类别', max_length=10)

    def toDict(self):
        return {'singersort_id': self.singersort_id,
                'singersortname': self.singersortname}

    class Meta:
        # 设置Admin界面的显示内容
        managed = False
        db_table = "singersort"


# 歌手模块
class singers(models.Model):
    singers_id = models.AutoField('序号', primary_key=True)
    singername = models.CharField('歌手', max_length=50)
    sex = models.CharField('性别', max_length=10)
    singerpicture = models.CharField('歌手图', max_length=255)
    englishname = models.CharField('英文名', max_length=50)
    nationality = models.CharField('国籍', max_length=20)
    birthplace = models.CharField('出生地', max_length=20)
    birthdate = models.DateTimeField('出生日期', default=datetime.now)
    personalintroduction = models.CharField('个人简介', max_length=255)
    singertype = models.ForeignKey(singersort, on_delete=models.CASCADE, verbose_name='歌手分类')

    def toDick(self):
        return {'singers_id': self.singers_id,
                'singername': self.singername,
                'sex': self.sex,
                'singerpicture': self.singerpicture,
                'englishname': self.englishname,
                'nationality': self.nationality,
                'birthplace': self.birthplace,
                'birthdate': self.birthdate.strftime('%Y年%m月%d日'),
                'personalintroduction': self.personalintroduction}

    class Meta:
        managed = False
        db_table = "singers"
        # managed = False


# 用户模块
class users(models.Model):
    users_id = models.AutoField('序号', primary_key=True)
    username = models.CharField('用户名', max_length=50)
    nickname = models.CharField('昵称', max_length=50)
    headprotrait = models.CharField('头像', max_length=255)
    sex = models.CharField('性别', max_length=10)
    password_hash = models.CharField('密码', max_length=100)
    password_salt = models.CharField('密码干扰值', max_length=50)
    status = models.IntegerField('用户级别', default=1)
    create_time = models.DateTimeField('创建时间', default=datetime.now)
    update_time = models.DateTimeField('修改时间', default=datetime.now)
    musicsinger = models.ForeignKey(singers, on_delete=models.CASCADE, verbose_name='音乐人', null=True)
    is_status = models.CharField('用户状态', max_length=20, default="offline")

    def toDict(self):
        return {'users_id': self.users_id,
                'username': self.username,
                'nickname': self.nickname,
                'headprotrait': self.headprotrait,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'musicsinger': self.musicsinger_id,
                'is_status': self.is_status, }

    class Meta:
        managed = False
        db_table = "users"


# 歌曲模块/*-+
class songs(models.Model):
    songs_id = models.AutoField('序号', primary_key=True)
    songname = models.CharField('歌名', max_length=50)
    singername = models.CharField('歌手', max_length=50)
    songlanguages = models.CharField('语言', max_length=20)
    songsource = models.CharField('歌曲来源分类', max_length=10)
    songpicture = models.CharField('歌曲图', max_length=255)
    songimgtype = models.CharField('歌曲图类型', max_length=50)
    filename = models.CharField('歌曲文件名', max_length=255)
    songfile = models.CharField('歌曲文件', max_length=255)
    songfiletype = models.CharField('歌曲文件类型', max_length=50)
    songlyrics = models.CharField('歌词文件', max_length=50)
    releasetime = models.DateTimeField('发行时间', default=datetime.now)
    updatetime = models.DateTimeField('修改时间', default=datetime.now)
    songtype = models.ForeignKey(songsort, on_delete=models.CASCADE, verbose_name='歌曲分类')
    singerinfo = models.ForeignKey(singers, on_delete=models.CASCADE, verbose_name='歌手信息')

    def toDick(self):
        return {'songs_id': self.songs_id,
                'songname': self.songname,
                'singername': self.singername,
                'songsource': self.songsource,
                'songpicture': self.songpicture,
                'songimgtype': self.songimgtype,
                'filename': self.filename,
                'songfile': self.songfile,
                'songfiletype': self.songfiletype,
                'releasetime': self.releasetime.strftime('%Y-%m-%d %H:%M:%S'),
                'updatetime': self.updatetime.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        managed = False
        db_table = "songs"
        # 后台管理系统显示app数据
        # verbase_name = '音乐'
        # verbase_name_plural = verbase_name


# dynamic模块
class dynamic(models.Model):
    dynamic_id = models.AutoField('序号', primary_key=True)
    songname = models.CharField('歌名', max_length=50)
    plays = models.IntegerField('播放次数')
    search = models.IntegerField('搜索次数')
    down = models.IntegerField('下载次数')
    song = models.ForeignKey('songs', on_delete=models.CASCADE, verbose_name='歌名')

    class Meta:
        db_table = "dynamic"
        managed = False


# comment评论模块
class comment(models.Model):
    comment_id = models.AutoField('序号', primary_key=True)
    commenttext = models.CharField('内容', max_length=500)
    commentuser = models.ForeignKey('users', on_delete=models.CASCADE, verbose_name='用户名')
    commentsong = models.ForeignKey('songs', on_delete=models.CASCADE, verbose_name='歌名')
    commentdate = models.DateTimeField('发布时间', default=datetime.now)

    class Meta:
        # 设置Admin界面的显示内容
        db_table = "comment"
        managed = False


# 音乐收藏
class cltmusic(models.Model):
    cltmusic_id = models.AutoField('序号', primary_key=True)
    cltmusic_user = models.ForeignKey('users', on_delete=models.CASCADE, verbose_name='收藏用户')
    cltmusic_song = models.ForeignKey('songs', on_delete=models.CASCADE, verbose_name='收藏歌名')
    cltmusicdate = models.DateTimeField('收藏时间', default=datetime.now)

    class Meta:
        # 设置Admin界面的显示内容
        db_table = "cltmusic"
        managed = False


# 歌手收藏
class cltsinger(models.Model):
    cltsinger_id = models.AutoField('序号', primary_key=True)
    cltsinger_user = models.ForeignKey('users', on_delete=models.CASCADE, verbose_name='收藏用户')
    cltsinger_singer = models.ForeignKey('singers', on_delete=models.CASCADE, verbose_name='收藏歌手名')
    cltsingerdate = models.DateTimeField('收藏时间', default=datetime.now)

    class Meta:
        # 设置Admin界面的显示内容
        db_table = "cltsinger"
        managed = False


# 好友列表
class friends(models.Model):
    friend_id = models.AutoField('序号', primary_key=True)
    friend_user1 = models.ForeignKey('users', on_delete=models.CASCADE, verbose_name='用户关系1', related_name='user1')
    friend_user1_status = models.IntegerField('状态1', default=0)
    friend_user2 = models.ForeignKey('users', on_delete=models.CASCADE, verbose_name='用户关系2', related_name='user2')
    friend_user2_status = models.IntegerField('状态2', default=0)
    friend_date = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        db_table = "friends"
        managed = False
