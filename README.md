# 开发环境
* Python (3.6.1)
* Django (2.1.7)

# 实现功能当
1. 基于ajax和用户组件的登陆验证
2. 基于ajax和form组件的注册功能
3. 滑动验证功能
4. 系统首页、个人站点、后台管理功能
5. 添加、编辑、删除文章
6. 点赞与踩
7. 评论功能
8. 富文本编辑器
9. 防止xss攻击


# 配置开发环境
## 使用虚拟环境(virturalenv)
```
pip install virtualenv
mkvirtualenv cnblog -p 'python3.6'
workon cnblog
```

# 生成表结构
```
./manage.py makemigrations
./manage.py migrate
```

# 程序的启动方式
./manage.py runserver

# 登陆用户信息
配置mysql后在register页面注册

# 程序运行效果
![cnblog.png](https://github.com/Edward66/cnblog/blob/07-optimization/cnblog.png)
![cnblog2.png](https://github.com/Edward66/cnblog/blob/07-optimization/cnblog2.png)
