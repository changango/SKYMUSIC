# Generated by Django 3.2.12 on 2022-04-24 23:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='singers',
            fields=[
                ('singers_id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('singername', models.CharField(max_length=50, verbose_name='歌手')),
                ('sex', models.CharField(max_length=10, verbose_name='性别')),
                ('singerpicture', models.CharField(max_length=255, verbose_name='歌手图')),
                ('englishname', models.CharField(max_length=50, verbose_name='英文名')),
                ('nationality', models.CharField(max_length=20, verbose_name='国籍')),
                ('birthplace', models.CharField(max_length=20, verbose_name='出生地')),
                ('birthdate', models.DateTimeField(default=datetime.datetime.now, verbose_name='出生日期')),
                ('personalintroduction', models.CharField(max_length=255, verbose_name='个人简介')),
            ],
            options={
                'db_table': 'singers',
            },
        ),
        migrations.CreateModel(
            name='singersort',
            fields=[
                ('singersort_id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('singersortname', models.CharField(max_length=10, verbose_name='歌手类别')),
            ],
            options={
                'db_table': 'singersort',
            },
        ),
        migrations.CreateModel(
            name='songsort',
            fields=[
                ('songsort_id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('songsortname', models.CharField(max_length=10, verbose_name='歌曲类别')),
            ],
            options={
                'db_table': 'songsort',
            },
        ),
        migrations.CreateModel(
            name='users',
            fields=[
                ('users_id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('username', models.CharField(max_length=50, verbose_name='用户名')),
                ('nickname', models.CharField(max_length=50, verbose_name='昵称')),
                ('headprotrait', models.CharField(max_length=255, verbose_name='头像')),
                ('sex', models.CharField(max_length=10, verbose_name='性别')),
                ('password_hash', models.CharField(max_length=100, verbose_name='密码')),
                ('password_salt', models.CharField(max_length=50, verbose_name='密码干扰值')),
                ('status', models.IntegerField(default=1, verbose_name='用户级别')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='修改时间')),
                ('is_status', models.CharField(default='offline', max_length=20, verbose_name='用户状态')),
                ('musicsinger', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myadmin.singers', verbose_name='音乐人')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='songs',
            fields=[
                ('songs_id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('songname', models.CharField(max_length=50, verbose_name='歌名')),
                ('singername', models.CharField(max_length=50, verbose_name='歌手')),
                ('songlanguages', models.CharField(max_length=20, verbose_name='语言')),
                ('songsource', models.CharField(max_length=10, verbose_name='歌曲来源分类')),
                ('songpicture', models.CharField(max_length=255, verbose_name='歌曲图')),
                ('songimgtype', models.CharField(max_length=50, verbose_name='歌曲图类型')),
                ('filename', models.CharField(max_length=255, verbose_name='歌曲文件名')),
                ('songfile', models.CharField(max_length=255, verbose_name='歌曲文件')),
                ('songfiletype', models.CharField(max_length=50, verbose_name='歌曲文件类型')),
                ('songlyrics', models.CharField(max_length=50, verbose_name='歌词文件')),
                ('releasetime', models.DateTimeField(default=datetime.datetime.now, verbose_name='发行时间')),
                ('updatetime', models.DateTimeField(default=datetime.datetime.now, verbose_name='修改时间')),
                ('singerinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.singers', verbose_name='歌手信息')),
                ('songtype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.songsort', verbose_name='歌曲分类')),
            ],
            options={
                'db_table': 'songs',
            },
        ),
        migrations.AddField(
            model_name='singers',
            name='singertype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.singersort', verbose_name='歌手分类'),
        ),
        migrations.CreateModel(
            name='friends',
            fields=[
                ('friend_id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('friend_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('friend_user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1', to='myadmin.users', verbose_name='用户关系1')),
                ('friend_user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2', to='myadmin.users', verbose_name='用户关系2')),
            ],
            options={
                'db_table': 'friends',
            },
        ),
        migrations.CreateModel(
            name='dynamic',
            fields=[
                ('dynamic_id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('songname', models.CharField(max_length=50, verbose_name='歌名')),
                ('plays', models.IntegerField(verbose_name='播放次数')),
                ('search', models.IntegerField(verbose_name='搜索次数')),
                ('down', models.IntegerField(verbose_name='下载次数')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.songs', verbose_name='歌名')),
            ],
            options={
                'db_table': 'dynamic',
            },
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('commenttext', models.CharField(max_length=500, verbose_name='内容')),
                ('commentdate', models.DateTimeField(default=datetime.datetime.now, verbose_name='发布时间')),
                ('commentsong', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.songs', verbose_name='歌名')),
                ('commentuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.users', verbose_name='用户名')),
            ],
            options={
                'db_table': 'comment',
            },
        ),
        migrations.CreateModel(
            name='cltsinger',
            fields=[
                ('cltsinger_id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('cltsingerdate', models.DateTimeField(default=datetime.datetime.now, verbose_name='收藏时间')),
                ('cltsinger_singer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.singers', verbose_name='收藏歌手名')),
                ('cltsinger_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.users', verbose_name='收藏用户')),
            ],
            options={
                'db_table': 'cltsinger',
            },
        ),
        migrations.CreateModel(
            name='cltmusic',
            fields=[
                ('cltmusic_id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('cltmusicdate', models.DateTimeField(default=datetime.datetime.now, verbose_name='收藏时间')),
                ('cltmusic_song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.songs', verbose_name='收藏歌名')),
                ('cltmusic_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.users', verbose_name='收藏用户')),
            ],
            options={
                'db_table': 'cltmusic',
            },
        ),
    ]
