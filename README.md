# Lab RR Application

## 简介

一个基于Django的，应该不能真用的，实验室招新报名系统。

前端参考[madlogos blog](https://madlogos.github.io/post/flask-socketio-site-demo/)

## 版本

### v0.1施工中...


## 小问题记录 

### 数据库无法创建时

```shell
python manage.py makemigrations --empty <应用名>
python manage.py makemigrations
python manage.py migrate
```