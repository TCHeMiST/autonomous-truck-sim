#!/usr/bin/env python

from flask import Flask, request, abort
from flask_cors import CORS
import socket, pickle
import json

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

@app.route('/sendlocation', methods=['POST']) 
def send_data():
    if not request.get_json():
        abort(400)
        
    location = request.get_json()
    print(location)
    return json.dumps(location)


@app.route('/startstop', methods=['POST']) 
def send_startstop():
    if not request.get_json():
        abort(400)
        
    startstop = request.get_json()

    if (startstop['Action'] == 1):
        print("START!")
    else:
        print("STOP!")
    return json.dumps(startstop)
