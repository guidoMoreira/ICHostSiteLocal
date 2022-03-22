import random
import re
import sys


from flask import Flask,render_template, url_for, session, request,copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room,close_room, rooms, disconnect
from threading import Lock
import json
import os.path
import websocket
#from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime #Importa tempo e data
app = Flask(__name__)



ws = websocket.WebSocket()
ws.connect("ws://192.168.15.43")
print("Connected to WebSocket server")
#str = input("Say something: ")
#selfhost = "127.0.0.1:5000"
#ws.send(selfhost)

# Wait for server to respond and print it
#result = ws.recv()
#print("Received: " + result)

'''
#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    dateCreated = db.Column(db.DateTime,default=datetime.utcnow())
    def __repr__(self):
        return '<Task %r>' % self.id

'''
@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/overwrite')#methods =['POST','GET']
def Dados():
    ws.send("Request")

    # Wait for server to respond and print it
    result = ws.recv()
    print("Received: " + result)
    '''state = request.args.get('Botao')'''
    s = {
        "Botao" : result
    }
    fname  =os.path.join(app.static_folder,"sample.json")

    with open(fname,"w") as outfile:
        json.dump(s,outfile)
    return 'overwrite com sucesso: Botão ligado?' + result

    #if request.method == 'POST':
    #    return render_template()

@app.route('/read')
def Read():
    fname = os.path.join(app.static_folder,"sample.json")
    with open(fname,'r') as openfile:
        json_obj = json.load(openfile)

    return json_obj['Botao']


@app.route('/<usr>')
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == '__main__':
    app.run()

# Termina conexão
@app.context_processor
def inject_load():
    if sys.platform.startswith('linux'):
        with open('/proc/loadavg', 'rt') as f:
            load = f.read().split()[0:3]
    else:
        load = [int(random.random() * 100) / 100 for _ in range(3)]
    return {'load1': load[0], 'load5': load[1], 'load15': load[2]}
