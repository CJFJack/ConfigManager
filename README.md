CMS(Config Manager Platform: 运维管理平台)
==============================================

[![Build Status](https://img.shields.io/travis/rust-lang/rust.svg)](https://img.shields.io/travis/rust-lang/rust.svg)
[![Python Version](https://img.shields.io/badge/Python--2.7-paasing-green.svg)](https://img.shields.io/badge/Python--2.7-paasing-green.svg)
[![Django Version](https://img.shields.io/badge/Django--1.11.15-paasing-green.svg)](https://img.shields.io/badge/Django--1.11.15-paasing-green.svg)

> CMS现有功能:

- 统计Dashboard
- 系统管理
- 发布管理
- 报警管理

## 部署

### 安装依赖

```
pip install -i https://pypi.douban.com/simple/  -r requirements.txt
```

### 修改配置


MySQL配置修改settings.py:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cms',
        'USER': 'root',
        'PASSWORD': 'xxxx',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


```

配置同步Zabbix 故障数据settings.py:
```
ZABBIX_AUTO_RECORD = True
ZABBIX_DB_HOST = '192.168.104.152'
ZABBIX_DB_PORT = '3306'
ZABBIX_DB_USER = 'test'
ZABBIX_DB_PASSWORD = 'geekwolf'
ZABBIX_DB_NAME = 'zabbix'
ZABBIX_SYNC_INTERVAL = 600  # 10分钟
```

### 初始化数据
```
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata default_types
python manage.py loaddata default_user

```

### 启动同步进程
```
screen python manage.py zbxsync
注释：若ZABBIX_AUTO_RECORD = False 可以忽略此步骤
```

### 登录

```
python manage.py runserver
http://127.0.0.1:8000
admin admin
```

### 交流
![赞赏](https://raw.githubusercontent.com/geekwolf/fms/master/doc/images/wxzf.png)
![微信](https://raw.githubusercontent.com/geekwolf/fms/master/doc/images/wx.jpg)

QQ群1: 541071512

![fms](https://raw.githubusercontent.com/geekwolf/fms/master/doc/images/dashboard.jpg)
![fms](https://raw.githubusercontent.com/geekwolf/fms/master/doc/images/fms.jpg)
![fms](https://raw.githubusercontent.com/geekwolf/fms/master/doc/images/add_fms.jpg)
![fms](https://raw.githubusercontent.com/geekwolf/fms/master/doc/images/add_user.jpg)
![fms](https://raw.githubusercontent.com/geekwolf/fms/master/doc/images/group_perm.jpg)