from flask import Flask, jsonify, request, render_template
from network import Network
import json

ascii_art = '''
`7MMF'   `7MF'`7MM"""Mq.   .M"""bgd 
  `MA     ,V    MM   `MM. ,MI    "Y 
   VM:   ,V     MM   ,M9  `MMb.     
    MM.  M'     MMmmdM9     `YMMNq. 
    `MM A'      MM  YM.   .     `MM 
     :MM;       MM   `Mb. Mb     dM 
      VF      .JMML. .JMM.P"Ybmmd"  
      
        Vouch Reputation System
           Bruno Rocha Moura
'''
print(ascii_art)

app = Flask("Demo Webserver", template_folder='web/templates', static_folder='web/static')
network = Network()

# always start with adam
network.add_node('Adam')

@app.route("/", methods=['GET'])
def visualizer():
    return render_template('visualizer.html', topology=network.get_diagram('Adam'))

@app.route("/api/add-node", methods=['POST'])
def add_node():
    name = request.headers.get("name", None)
    if name:
	
        network.nodes[name] = network.add_node(name)
        return f"Node '{name}' added", 200
    else:
        return "Missed the name", 401

@app.route("/api/vouch-for", methods=['POST'])
def vouch_for():
    sender = request.headers.get("sender", None)
    receiver = request.headers.get("receiver", None)

    if not sender or not receiver:
        return "Missed sender and/or receiver", 401

    if not any([ i.id == name for i in network.nodes ]):
	return "Node not found", 401

    try:
        network.nodes[sender].vouch(receiver, True)
        return "Vouch successful"
    except Exception as e:
        return "Something went wrong\n"+str(e), 500

@app.route("/api/vouch-against", methods=['POST'])
def vouch_against():
    sender = request.headers.get("sender", None)
    receiver = request.headers.get("receiver", None)

    if not sender or not receiver:
        return "Missed sender and/or receiver", 401

    if not any([ i.id == name for i in network.nodes ]):
	return "Node not found", 401

    try:
        network.nodes[sender].vouch(receiver, False)
        return "Vouch successful"
    except Exception as e:
        return "Something went wrong\n"+str(e), 500

@app.route("/api/calculate-reputation", methods=['GET'])
def calculate_reputation():
    observer = request.headers.get("observer", None)

    try:
        return network.calculate_reputation(observer)
    except Exception as e:
        return "Something went wrong\n"+str(e), 500

@app.route("/api/diagram", methods=['GET'])
def diagram():

    observer = request.headers.get("observer", "Adam")

    if not observer:
        return "Observer missing", 401

    return network.get_diagram(observer)

@app.route("/api/reset", methods=['POST'])
def reset():
    network.nodes = {}
    network.add_node('Adam')
    return "Reset"

app.run(host='0.0.0.0')
