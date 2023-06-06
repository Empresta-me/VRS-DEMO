import requests

class reset():
    def __init__(self):
        self.url = 'http://localhost:5000/api/reset'

    def go(self):
        print(requests.post(self.url))

    def __str__(self):
        return "Reset network"

class add_node():
    def __init__(self, name : str):
        self.url = 'http://localhost:5000/api/add-node'
        self.headers = {'name': name}

    def go(self):
        print(requests.post(self.url, headers=self.headers))

    def __str__(self):
        return f"Create {self.headers['name']}"

class vouch_for:
    def __init__(self, sender: str, receiver : str):
        self.url = 'http://localhost:5000/api/vouch-for'
        self.headers = {'sender': sender, 'receiver' : receiver}

    def go(self):
        print(requests.post(self.url, headers=self.headers))

    def __str__(self):
        return f"{self.headers['sender']} vouches for {self.headers['receiver']}"

class vouch_against:
    def __init__(self, sender: str, receiver : str):
        self.url = 'http://localhost:5000/api/vouch-against'
        self.headers = {'sender': sender, 'receiver' : receiver}

    def go(self):
        print(requests.post(self.url, headers=self.headers))

    def __str__(self):
        return f"{self.headers['sender']} vouches against {self.headers['receiver']}"

print("type 'help' for help")

while True:
    command = input("\nCommand: ")

    if command == "help":
        print("c <name> - Create node")
        print("+ <vouching> <vouched> - Vouch for")
        print("- <vouching> <vouched> - Vouch against")
        print("reset - Reset network")
        continue

    if command == "reset":
        reset().go()
        continue

    args = command.split(" ")

    if args[0] == "c": 
        name = args[1]
        add_node(name).go()
        continue

    if args[0] == "+":
        node_vouching = args[1]
        node_vouched = args[2]

        vouch_for(node_vouching,node_vouched).go()
        vouch_for(node_vouched,node_vouching).go()
        continue

    if args[0] == "-":
        node_vouching = args[1]
        node_vouched = args[2]

        vouch_against(node_vouching,node_vouched).go()
        continue
