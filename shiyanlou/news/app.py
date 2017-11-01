from flask import Flask,render_template
import json
import os


app = Flask(__name__)

#================CLASS ERROR=================

class ValueError(Exception):
	status_code = 400

	def __init__(self,message,status_code=400):
		Exception.__init__(self)
		self.message = message
		self.status_code = status_code

#================INDEX=================

@app.route('/')
def index():
	with open('/home/keeper/shiyanlou/files/helloshiyanlou.json','r') as helloshiyanlou_files:
		shiyanlou_dict = json.loads(helloshiyanlou_files.read())

	with open('/home/keeper/shiyanlou/files/helloworld.json','r') as helloworld_files:
		world_dict = json.loads(helloworld_files.read())

	return render_template('index.html',helloworld_title = world_dict['title'],helloshiyanlou_title = shiyanlou_dict['title'])

#================FILES=================

@app.route('/files/<filename>') 
def file(filename):
	file_abspath = '/home/keeper/shiyanlou/files/' + filename + '.json'
	if os.path.exists(file_abspath):
		with open(file_abspath) as helloshiyanlou_files:
			shiyanlou_filedict = json.loads(helloshiyanlou_files.read())
			return render_template('file.html',hello_file = shiyanlou_filedict['content'])
	else:
		return render_template('404.html')

#================NOT FOUND=================
# @app.errorhandler(ValueError)
# def page_not_found(error):
# 	return render_template('404.html'),ValueError

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html')	


#================MAIN=================

if __name__ == '__main__':
	# readjson()
	app.run

