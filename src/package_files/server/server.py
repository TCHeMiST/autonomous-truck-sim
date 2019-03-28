#!/usr/bin/env python

from flask import Flask
from flask_cors import CORS
import socket, pickle

app = Flask(__name__)
CORS(app)

@app.route('/')
def share_location():
    s = socket.socket()          
    port = 12345                
    s.connect(('127.0.0.1', port)) 
    
    data = s.recv(1024) 
    # data_variable = pickle.loads(data)
    s.close()      

    return data
