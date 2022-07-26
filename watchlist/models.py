from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from watchlist import db


# 使用SQLAlchemy需要：
# 配置连接
# 创建数据库模型(类)：类要声明继承 db.Model 。每个类属性(字段)要实例化 db.Column ，传入的参数为字段类型
# 字段类型有 db.Integer db.String(size) db.Text db.DateTime db.Float db.Boolean
# 可额外传入参数进行设置： primary_key(布尔值，是否设为主键) nullable(布尔值，是否允许空值) index(布尔值，是否设索引) unique(布尔值，是否允许重复) default(设默认值)

# 表名为 user（自动生成，小写处理），若要指定表名，定义 __tablename__ 属性
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)  # 主键
	name = db.Column(db.String(20))  # 名字
	username = db.Column(db.String(20))  # 用户名
	password_hash = db.Column(db.String(128))  # 密码的散列值

	def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
		self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

	def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
		return check_password_hash(self.password_hash, password)  # 返回布尔值


# 表名为 movie
class Movie(db.Model):
	id = db.Column(db.Integer, primary_key=True)  # 主键
	title = db.Column(db.String(60))  # 电影标题
	year = db.Column(db.String(4))  # 电影年份
