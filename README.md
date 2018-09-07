CMS(Config Manager System: 运维管理平台)
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
pip install -r requirements.txt
```

### 安装并创建数据库cms


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

阿里云接口认证配置settings.py:
```
ACCESS_KEY_ID = 'XXXXXXXXXX'
ACCESS_KEY_SECRET = 'XXXXXXXXXXXXXX'

```


发布文件生成路径配置settings.py:
```
DEPLOY_DIR_PATH = r'D:\release'

```

修改允许访问IPsettings.py:
```
ALLOWED_HOSTS = []

```


### 初始化数据
```
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata default_types
python manage.py loaddata default_user

```


### 创建管理员

```
python manage.py createsuperuser
```

### 交流
![赞赏](https://raw.githubusercontent.com/CJFJack/ConfigManager/master/doc/images/wxzs.png)
![微信](https://raw.githubusercontent.com/CJFJack/ConfigManager/master/doc/images/wx.png)

QQ: 398741302

![cms](https://raw.githubusercontent.com/CJFJack/ConfigManager/master/doc/images/login.png)
![cms](https://raw.githubusercontent.com/CJFJack/ConfigManager/master/doc/images/acs_alarm_report.png)
![cms](https://raw.githubusercontent.com/CJFJack/ConfigManager/master/doc/images/acs_rds_report.png)
![cms](https://raw.githubusercontent.com/CJFJack/ConfigManager/master/doc/images/cms_config_manager.png)
![cms](https://raw.githubusercontent.com/CJFJack/ConfigManager/master/doc/images/cms_ecs_manager.png)
![cms](https://raw.githubusercontent.com/CJFJack/ConfigManager/master/doc/images/cms_deploy_apply.png)