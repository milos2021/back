from run import create_app
from flask_socketio import SocketIO,emit,send
import eventlet
import time
import os
import json
import threading
from flask import Flask
import datetime
#from gevent import monkey
#monkey.patch_all()
eventlet.monkey_patch()
app = create_app()
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins=['http://10.0.90.23','http://localhost:8080'])


@socketio.on('connect')
def test_connect(auth):
    emit('my response', {'data': 'Connected'})
@socketio.on('difference')
def handleDifference(t):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	max = 10
	for i in list(range(1,11)):
		try:
			size = os.path.getsize(os.path.join(dir_path, 'monitoring/razlika.json'))/(1024*1024)
			size_data = os.path.getsize(os.path.join(dir_path, 'monitoring/data.json'))/(1024*1024)
			if size_data - size > 3:
				with open(os.path.join(dir_path, 'monitoring/razlika.json')) as jsonfile:
					d = json.load(jsonfile)
					emit("difference", d)
					break
			else:
				with open(os.path.join(dir_path, 'monitoring/data.json')) as jsonfile:
					d = json.load(jsonfile)
					emit("difference", d)
					with open(os.path.join(dir_path, 'monitoring/error_log.txt'),'a') as err:
						err.write("Big file, whole set returned - "+str(datetime.datetime.now())+"\n")
					break
				# raise Exception('File too big')
		except:
			time.sleep(3)
	else:
		with open(os.path.join(dir_path, 'monitoring/error_log.txt'),'a') as err:
			err.write("Razlika read error - "+str(datetime.datetime.now())+"\n")
@socketio.on('actual')
def handleActual(t):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	max = 10
	for i in list(range(1,11)):
		try:
			with open(os.path.join(dir_path, 'monitoring/aktuelni.json')) as jsonfile:
				d = json.load(jsonfile)
				emit("actual", d)
				break
		except:
			time.sleep(3)
	else:
		with open(os.path.join(dir_path, 'monitoring/error_log.txt'),'a') as err:
			err.write("Actual matches read error - "+str(datetime.datetime.now())+"\n")
@socketio.on('blocked')
def handleNepovezani(t):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	max = 10
	for i in list(range(1,11)):
		try:
			with open(os.path.join(dir_path, 'monitoring/data_nepovezani.json')) as jsonfile:
				d = json.load(jsonfile)
				emit("blocked", d)
				break
		except:
			time.sleep(3)
	else:
		with open(os.path.join(dir_path, 'monitoring/error_log.txt'),'a') as err:
			err.write("Blocked/Not Connected matches read error - "+str(datetime.datetime.now())+"\n")
@socketio.on('message')
def handleMessage(msg):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	max = 10
	for i in list(range(1,11)):
		try:
			with open(os.path.join(dir_path, 'monitoring/data.json')) as jsonfile:
				d = json.load(jsonfile)
				emit("message", d)
				break
		except:
			time.sleep(3)
	else:
		with open(os.path.join(dir_path, 'monitoring/error_log.txt'),'a') as err:
			err.write("Main data read error - "+str(datetime.datetime.now())+"\n")

def setInterval(func,time):
	e = threading.Event()
	while not e.wait(time):
		func()

if __name__ == "__main__":
	socketio.run(app, host="0.0.0.0", port="8000", debug=True)
	# app.run(host='0.0.0.0',port=5000, debug=True)

