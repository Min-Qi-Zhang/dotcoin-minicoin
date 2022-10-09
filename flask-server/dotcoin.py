from flask import Flask, request, Response, render_template
import json

from blockchain import generate_next_block, get_UTXOs, get_account_balance, get_block_info, get_blockchain, get_info_by_address, get_my_UTXOs, get_transaction_by_id, send_tx
from wallet import get_public_from_wallet

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/blocks")
def get_blocks():
    return json.dumps([block.toJson() for block in get_blockchain()])

@app.get("/block/<string:hash>")
def get_block(hash):
    block = get_block_info(hash)
    return block.toJson() if block else Response("{'message': 'Block does not exist'}", status=400)

@app.get("/transaction/<string:id>")
def get_transaction(id):
    tx = get_transaction_by_id(id)
    return tx.toJson() if tx else Response("{'message': 'Transaction does not exist'}", status=400)

@app.get("/unspentTransactionOutputs")
def unspent_transaction_outputs():
    return json.dumps([utxo.toJson() for utxo in get_UTXOs()])

@app.get("/myUnspentTransactionOutputs")
def my_unspent_transaction_outputs():
    return json.dumps([utxo.toJson() for utxo in get_my_UTXOs()])

@app.get("/address")
def get_address():
    return Response(str({'address': get_public_from_wallet()}))

@app.get("/address/<string:address>")
def get_address_info(address):
    return json.dumps([utxo.toJson() for utxo in get_info_by_address(address)])

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

