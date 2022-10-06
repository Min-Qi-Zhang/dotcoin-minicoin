from flask import Flask, request, Response
import json

from blockchain import generate_next_block, get_blockchain
from wallet import init_wallet

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return "Hello World!"

@app.get("/blocks")
def get_blocks():
    return json.dumps([block.toJson() for block in get_blockchain()])

@app.post("/mineBlock")
def mine_block():
    data = request.get_json().get('data')
    if (not data):
        return Response("{'message': 'data is missing'}", status=400)

    new_block = generate_next_block(data)
    if (new_block != None):
        return new_block.toJson()
    return Response("{'message': 'Failed to mine a block'}", status=400)

# p2p: when a peer wants join, add it to the list, then send it the blockchain
@app.get("/peers")
def get_peers():
    # TODO
    return

@app.post("/add_peer")
def add_peer():
    # TODO
    return

