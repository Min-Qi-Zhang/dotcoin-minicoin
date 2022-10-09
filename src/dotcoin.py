from flask import Flask, request, Response
import json

from blockchain import generate_next_block, get_UTXOs, get_account_balance, get_blockchain, get_my_UTXOs, send_tx
from wallet import get_public_from_wallet

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return "Hello World!"

@app.get("/blocks")
def get_blocks():
    return json.dumps([block.toJson() for block in get_blockchain()])

@app.get("/unspentTransactionOutputs")
def unspent_transaction_outputs():
    return json.dumps([utxo.toJson() for utxo in get_UTXOs()])

@app.get("/myUnspentTransactionOutputs")
def my_unspent_transaction_outputs():
    return json.dumps([utxo.toJson() for utxo in get_my_UTXOs()])

@app.get("/address")
def get_address():
    return Response(str({'address': get_public_from_wallet()}))

@app.post("/mineBlock")
def mine_block():
    new_block = generate_next_block()
    if (new_block):
        return new_block.toJson()
    return Response("{'message': 'Failed to mine a block'}", status=400)

@app.get("/balance")
def balance():
    return Response(str({'balance': get_account_balance()}))

# @app.post("/mineTransaction")
# def mine_transaction():
#     receiver_address = request.get_json().get('address')
#     amount = request.get_json().get('amount')
#     new_block = generate_block_with_transaction(receiver_address, amount)
#     if (new_block):
#         return new_block.toJson()
#     return Response("{'message': 'Failed to mine transaction'}", status=400)

@app.post("/sendTransaction")
def send_transaction():
    receiver_address = request.get_json().get('address')
    amount = request.get_json().get('amount')
    tx = send_tx(receiver_address, amount)
    if (tx):
        return tx.toJson()
    return Response("{'message': 'Failed to send transaction'}", status=400)

# p2p: when a peer wants join, add it to the list, then send it the blockchain
@app.get("/peers")
def get_peers():
    # TODO
    return

@app.post("/add_peer")
def add_peer():
    # TODO
    return

