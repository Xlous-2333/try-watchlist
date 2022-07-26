from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from watchlist import app, db
from watchlist.models import User, Movie


@app.route('/', methods=['GET', 'POST'])  # 注册(装饰器：绑定对应的url(相对地址))
# render_template()函数可将模板渲染出来，同时可接受参数传入)
def index():
	if request.method == 'POST':  # 判断是否是 POST 请求
		if not current_user.is_authenticated:  # 如果当前用户未认证
			flash('请登陆后再试。')
			return redirect(url_for('index'))
		# 获取表单数据
		title = request.form.get('title')  # 传入表单对应输入字段的 name 值
		year = request.form.get('year')
		# 验证数据
		if not title or not year or len(year) > 4 or len(title) > 60:
			flash('无效输入。')  # 显示错误提示，Flash存储在session对象里，数据签名后存储到浏览器的Cookie中
			return redirect(url_for('index'))  # 重定向回主页
		# 保存表单数据到数据库
		movie = Movie(title=title, year=year)  # 创建记录
		db.session.add(movie)  # 添加到数据库会话
		db.session.commit()  # 提交数据库会话
		flash('添加成功。')  # 显示成功添加的提示
		return redirect(url_for('index'))  # 重定向回主页
	movies = Movie.query.all()  # 读取所有电影记录
	return render_template('index.html', movies=movies)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if not username or not password:
			flash('无效输入。')
			return redirect(url_for('login'))
		user = User.query.first()
		if username == user.username and user.validate_password(password):
			login_user(user)  # 登入用户
			flash('登录成功。')
			return redirect(url_for('index'))  # 重定向至主页
		flash('用户名或密码错误，请重试。')  # 验证失败
		return redirect(url_for('login'))
	return render_template('login.html')


@app.route('/logout')
@login_required  # 用于视图保护，对于不允许未登录用户访问的视图，为视图函数附加 login_required 装饰器可将未登录用户拒之门外。
def logout():
	logout_user()  # 登出用户
	flash('再见。')
	return redirect(url_for('index'))


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
	movie = Movie.query.get_or_404(movie_id)
	if request.method == 'POST':  # 处理编辑表单的提交请求
		title = request.form['title']
		year = request.form['year']
		if not title or not year or len(year) != 4 or len(title) > 60:
			flash('无效输入。')
			return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面
		movie.title = title  # 更新标题
		movie.year = year  # 更新年份
		db.session.commit()  # 提交数据库会话
		flash('修改成功')
		return redirect(url_for('index'))  # 重定向回主页
	return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
	movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
	db.session.delete(movie)  # 删除对应记录
	db.session.commit()  # 提交数据库会话
	flash('删除成功。')
	return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
	if request.method == 'POST':
		name = request.form['name']
		if not name or len(name) > 20:
			flash('无效输入。')
			return redirect(url_for(settings))
		current_user.name = name  # current_user会返回当前登录用户的数据库记录对象
		db.session.commit()
		flash('设置已更新。')
		return redirect(url_for('index'))
	flash('请重试。')
	return render_template('settings.html')
