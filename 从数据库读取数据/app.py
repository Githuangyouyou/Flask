from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime
import time
import json

#================连接数据库/创建表/写入数据=================
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:2621262@localhost/shiyanlou'
db = SQLAlchemy(app)
engine = create_engine('mysql://root:2621262@localhost/shiyanlou')
Session = sessionmaker(bind=engine)
session = Session()

class File(db.Model):
	__tablename__ = 'file'
	id = db.Column(Integer, primary_key=True)
	title = db.Column(String(80))
	create_time =  db.Column(String(200)) 
	category_id = db.Column(Integer, ForeignKey('category.id'))
	content = db.Column(String(100))
	category = relationship('Category')

class Category(db.Model):
	__tablename__ = 'category'
	id = db.Column(Integer,primary_key=True)
	name = db.Column(String(80))

db.create_all()

java = Category(name='java') 
python = Category(name='Python')
db.session.add(java)	
db.session.add(python)
db.session.commit() #注意category表内容提交必须放在file表内容提交之前,不然会报错,因为找不到名叫"java","python"的category,报错AttributeError: 'NoneType' object has no attribute 'id'

category = session.query(Category).filter(Category.name=='java').first()
file1 = File(title='Hello java', create_time=str(datetime.utcnow()),category_id=category.id, content='File-content - Java is cool')
category = session.query(Category).filter(Category.name=='python').first()
file2 = File(title='Hello python', create_time=str(datetime.utcnow()), category_id=category.id, content='File-content - python is cool')	
db.session.add(file1)
db.session.add(file2)
db.session.commit()

#================将数据库中的title返回给INDEX页面=================	
def from_mysql_to_index():
	mysql_title_list = engine.execute('select title from file').fetchall()
	return mysql_title_list

#================将数据库中的1.文章ID,2.文章内容/创建时间/类别名称显示=================	
def from_mysql_to_files(filename):
	file = session.query(File).filter(File.title == filename).first()
	category = session.query(Category).filter(Category.id == file.category_id).first()
	return file,category

#================INDEX=================	
@app.route('/')
def index():
	title_list = []
	mysql_title_list= from_mysql_to_index() 

	for i in range(0,len(mysql_title_list)):
		title_list.append(str(mysql_title_list[i]).strip("('").strip("'),"))
	return render_template('index.html',title_list=title_list)

# ================FILES========	=========
@app.route('/file/<filename>')
def file(filename):
	file,category = from_mysql_to_files(filename)
	return render_template('file.html',file=file,category=category)

#================NOT FOUND=================
@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html')	

#================MAIN=================
if __name__ == '__main__':
	app.run