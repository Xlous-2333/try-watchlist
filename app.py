#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time: 2022/7/21 11:47
# @File: app
# @Author: cong

from flask import Flask, url_for, render_template
from markupsafe import escape

app = Flask(__name__)

name = 'Xlous2333'
movies = [
	{'title': 'My Neighbor Totoro', 'year': '1988'},
	{'title': 'Dead Poets Society', 'year': '1989'},
	{'title': 'A Perfect World', 'year': '1993'},
	{'title': 'Leon', 'year': '1994'},
	{'title': 'Mahjong', 'year': '1996'},
	{'title': 'Swallowtail Butterfly', 'year': '1996'},
	{'title': 'King of Comedy', 'year': '1999'},
	{'title': 'Devils on the Doorstep', 'year': '1999'},
	{'title': 'WALL-E', 'year': '2008'},
	{'title': 'The Pork of Music', 'year': '2012'},
]


@app.route('/')  # 注册(装饰器：绑定对应的url(相对地址))
# render_template()函数可将模板渲染出来，同时可接受参数传入)
def index():
	return render_template('index.html', name=name, movies=movies)


@app.route('/index')
@app.route('/home')
def hello():  # 视图函数(请求处理函数)
	return '<h1 style="color: gold;width: 600px;text-align: center;position: relative;">Welcome to My ' \
	       'Watchlist!</h1><br /><img src="https://helloflask.com/totoro.gif" style="position: absolute;bottom: ' \
	       '0;left: 250px">'


@app.route('/user/<name>')
def user_page(name):  # 用户的输入不安全，需要通过escape对变量进行转义处理，从而避免浏览器将其当作代码执行
	return f'<h1>User:<span style="color: red">{escape(name)}</span>,Hello.<h1>'


# 测试
@app.route('/test')
def test_url_for():
	# 下面是一些调用示例（请访问 http://localhost:5000/test 后在命令行窗口查看输出的 URL）：
	print(url_for('hello'))  # 生成 hello 视图函数对应的 URL，将会输出：/
	# 注意下面两个调用是如何生成包含 URL 变量的 URL 的
	print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
	print(url_for('user_page', name='peter'))  # 输出：/user/peter
	print(url_for('test_url_for'))  # 输出：/test
	# 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
	print(url_for('test_url_for', num=2))  # 输出：/test?num=2
	return 'Test page'
