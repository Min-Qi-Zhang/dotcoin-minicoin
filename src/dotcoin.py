from flask import Flask, request, Response
import json

from blockchain import generate_block_with_transaction, generate_next_block, generate_next_raw_block, get_account_balance, get_blockchain
from wallet import init_wallet

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return "Hello World!"

@app.get("/blocks")
def get_blocks():
    return json.dumps([block.toJson() for block in get_blockchain()])

@app.post("/mineRawBlock")
def mine_raw_block():
    '''
        Mine a block with given data
    '''
    data = request.get_json().get('data')
    if (not data):
        return Response("{'message': 'data is missing'}", status=400)

    new_block = generate_next_raw_block(data)
    if (new_block != None):
        return new_block.toJson()
    return Response("{'message': 'Failed to mine a block'}", status=400)

@app.post("/mineBlock")
def mine_block():
    '''
        Mine a block without data, the generated block only contains a coinbase transaction
    '''
    new_block = generate_next_block()
    if (new_block):
        return new_block.toJson()
    return Response("{'message': 'Failed to mine a block'}", status=400)

@app.get("/balance")
def balance():
    return Response(str({'balance': get_account_balance()}))

@app.post("/mineTransaction")
def mine_transaction():
    receiver_address = request.get_json().get('address')
    amount = request.get_json().get('amount')
    new_block = generate_block_with_transaction(receiver_address, amount)
    if (new_block):
        return new_block.toJson()
    return Response("{'message': 'Failed to mine transaction'}", status=400)

# p2p: when a peer wants join, add it to the list, then send it the blockchain
@app.get("/peers")
def get_peers():
    # TODO
    return

@app.post("/add_peer")
def add_peer():
    # TODO
    return

