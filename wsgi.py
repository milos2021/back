from run import create_app
from flask_socketio import SocketIO,emit,send
import eventlet
import time
import os
import json
import threading
from flask import Flask
import datetime
import linecache
#from gevent import monkey
#monkey.patch_all()
eventlet.monkey_patch()
app = create_app()
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")


@socketio.on('connect')
def test_connect(auth):
	emit('my response', {'data': 'Connected'})
@socketio.on('difference')
def handleDifference(t):
	data = t
	dir_path = os.path.dirname(os.path.realpath(__file__))
	for i in list(range(1,11)):
		try:
			with open(os.path.join(dir_path, 'monitoring/versions.txt')) as txtfile:
				text = txtfile.readlines()
				versions = [text[0].strip(),text[-1][:-5]]
			txtfile.close()
			zahtevane = t['versions']
			poslati=[]
			for dostupne in versions:
				if dostupne not in zahtevane:
					poslati.append(dostupne)
			if len(poslati)==0:
				emit("difference",None)
			elif len(poslati)==1:
				try:
					with open(os.path.join(dir_path, 'monitoring/razlika_'+str(poslati[0])+'.json')) as jsonfile:
						d = json.load(jsonfile)
						d['version'] = poslati[0]
						emit("difference", d)
						break
				except:
					with open(os.path.join(dir_path, 'monitoring/error_log.txt'),'a') as err:
						err.write("File not found - "+str(datetime.datetime.now())+", "+poslati[0]+"\n")

			else:
				try:
					with open(os.path.join(dir_path, 'monitoring/razlika_'+str(poslati[0])+'.json')) as jsonfile:
						d = json.load(jsonfile)
						d['version'] = poslati[0]
						emit("difference", d)
						time.sleep(3)
				except:
					with open(os.path.join(dir_path, 'monitoring/error_log.txt'),'a') as err:
						err.write("File not found - "+str(datetime.datetime.now())+", "+poslati[0]+"\n")

				try:
					with open(os.path.join(dir_path, 'monitoring/razlika_'+str(poslati[1])+'.json')) as jsonfile:
						d = json.load(jsonfile)
						d['version'] = poslati[1]
						emit("difference", d)
						break
				except:
					with open(os.path.join(dir_path, 'monitoring/error_log.txt'),'a') as err:
						err.write("File not found - "+str(datetime.datetime.now())+", "+poslati[1]+"\n")
		except:
			time.sleep(3)

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

@socketio.on("razrada")
def getMatch(id):
	if id is not None:
		dir_path = os.path.dirname(os.path.realpath(__file__))
		msg = {"FD":{}}
		for i in list(range(1,11)):
			try:
				with open(os.path.join(dir_path, 'monitoring/razrada_mini.json')) as jsonfile:
					msg = json.load(jsonfile)
					break
			except:
				time.sleep(1)
		else:
			with open(os.path.join(dir_path, 'monitoring/error_log.txt'),'a') as err:
				err.write("Razrada read error - "+str(datetime.datetime.now())+"\n")
		for match in msg:
			if str(match['matchId']) == str(id):
				emit("razrada",match)
				break
		else:
			emit("razrada",None)
	else:
		emit("razrada",None)

@socketio.on("cp")
def check(msg):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	if msg == 'fix_basic':
		with open(os.path.join(dir_path, 'monitoring/process_running.json'), 'w') as outfile:
			json.dump({"is_process_running":0}, outfile)
			emit("cp","fixed")
	elif msg == 'fix_advanced':
		emit("cp","fixed_a")
	else:
		files = []
		for i in os.listdir(dir_path+"/monitoring"):
			if os.path.isfile(os.path.join(dir_path+"/monitoring",i)) and 'razlika_' in i and not '%' in i and not 'betradar' in i and not 'prod' in i:
				files.append(i.split("_")[1].split(".")[0])
		now = str(datetime.datetime.now()).split(" ")[1].split(".")[0]
		times = 0
		for x in files:
			t1 = datetime.datetime.strptime(now,'%H:%M:%S')
			t2 = datetime.datetime.strptime(x,'%H:%M:%S')
			if (t1 - t2).total_seconds() / 60.0 >= 4.00:
				times+=1
		if times == 0:
			emit("cp",{"code":0, "t1":files[0], "t2":files[1]})
		elif times == 1:
			emit("cp",{"code":1, "t1":files[0], "t2":files[1]})
		else:
			emit("cp",{"code":2, "t1":files[0], "t2":files[1]})

def setInterval(func,time):
	e = threading.Event()
	while not e.wait(time):
		func()

if __name__ == "__main__":
	socketio.run(app, host="0.0.0.0", port="8000", debug=True)
	# app.run(host='0.0.0.0',port=5000, debug=True)

