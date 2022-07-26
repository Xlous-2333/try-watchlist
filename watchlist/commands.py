import click

from watchlist import app, db
from watchlist.models import User, Movie


@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
	"""Initialize the database."""
	if drop:  # 判断是否输入了选项
		db.drop_all()
	db.create_all()
	click.echo('已初始化数据库。')  # 输出提示信息


@app.cli.command()
@click.option('--username', prompt=True, help='该用户名用于登录')
# hide_input=True会让密码输入隐藏 confirmation_prompt=True会要求二次确认输入
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='该密码用于登录')
def admin(username, password):
	"""创建用户"""
	db.create_all()

	user = User.query.first()
	if user is not None:
		click.echo('更新用户信息...')
		user.username = username
		user.set_password(password)  # 设置密码
	else:
		click.echo('创建新用户...')
		user = User(username=username, name='Admin')
		user.set_password(password)  # 设置密码
		db.session.add(user)

	db.session.commit()  # 提交数据库会话
	click.echo('完成。')


@app.cli.command()  # 注册为命令，使用flask forge调用
def forge():
	"""生成测试数据"""
	db.create_all()

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

	user = User(name=name)
	db.session.add(user)
	for m in movies:
		movie = Movie(title=m['title'], year=m['year'])
		db.session.add(movie)
	db.session.commit()
	click.echo('数据生成完成。')
