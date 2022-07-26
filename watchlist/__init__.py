import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
# 注意更新这里的路径，把 app.root_path 添加到 os.path.dirname() 中
# 以便把文件定位到项目根目录
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
# 创建用户加载回调函数，接受用户ID作为参数
def load_user(user_id):
	from watchlist.models import User
	user = User.query.get(int(user_id))  # 用ID作为User模型的主键查询对应的用户
	return user  # 返回用户对象


login_manager.login_view = 'login'
login_manager.login_message = '请登录后再试。'


# 模板上下文处理函数
@app.context_processor
def inject_user():  # 函数名可以随意修改
	from watchlist.models import User
	user = User.query.first()
	return dict(user=user)  # 需要返回字典，等同于 return {'user': user}



from watchlist import views, errors, commands
