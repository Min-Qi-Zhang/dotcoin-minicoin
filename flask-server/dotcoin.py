from flask import Flask, request, Response, render_template
import json
import os

from blockchain import generate_next_block, get_UTXOs, get_account_balance, get_block_info, get_blockchain, get_info_by_address, get_my_UTXOs, get_transaction_by_id, send_tx, generate_key_pair, get_blocks_from_first_peer, receive_tx, receive_block
from wallet import get_public_from_wallet
from transaction_pool import get_transaction_pool
from p2p import add_peer_to_list, join_network, get_peers_list

app = Flask(__name__)
app.debug = True

port = 5000

@app.route("/")
def index():
    return render_template("index.html", flask_token="Hello   world")

@app.get("/blocks")
def get_blocks():
    return json.dumps([block.toJson() for block in get_blockchain()])

@app.post("/blocks")
def get_blocks_from_peer():
    result = get_blocks_from_first_peer()
    return {'success': result}

@app.get("/block/<string:hash>")
def get_block(hash):
    block = get_block_info(hash)
    return block.toJson() if block else Response("{'message': 'Block does not exist'}", status=400)

@app.get("/transaction/<string:id>")
def get_transaction(id):
    tx = get_transaction_by_id(id)
    return tx.toJson() if tx else Response("{'message': 'Transaction does not exist'}", status=400)

@app.get("/transactionPool")
def get_tx_pool():
    return json.dumps([tx.toJson() for tx in get_transaction_pool()])

@app.get("/unspentTransactionOutputs")
def unspent_transaction_outputs():
    return json.dumps([utxo.toJson() for utxo in get_UTXOs()])

@app.get("/myUnspentTransactionOutputs")
def my_unspent_transaction_outputs():
    return json.dumps([utxo.toJson() for utxo in get_my_UTXOs()])

@app.get("/address")
def get_address():
    return {'address': get_public_from_wallet()}

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
    return {'balance': get_account_balance()}

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
    try:
      amount = float(request.get_json().get('amount'))
    except ValueError:
      return Response("{'message': 'Invalid amount'}", status=400)
    tx = send_tx(receiver_address, amount)
    if (tx):
        return tx.toJson()
    return Response("{'message': 'Failed to send transaction'}", status=400)

@app.get("/getKeyPair")
def get_key_pair():
    return {'address': generate_key_pair()}

# p2p: when a peer wants join, add it to the list, then send it the blockchain
@app.get("/peers")
def get_peers():
    return json.dumps(get_peers_list())

@app.post("/addPeer")
def add_peer():
    '''Receive request from new node to join the network'''
    my_url = request.get_json().get('url')
    return {'url': add_peer_to_list(my_url)}

@app.post("/joinNetwork")
def join():
    '''Send request to a node in the network'''
    url = request.get_json().get('url')
    result = join_network(url)
    if (result):
        return {'success': True}
    return Response("{'success': False}", status=400)

@app.post("/message")
def receive_message_from_peer():
    type = request.get_json().get('type')
    data = request.get_json().get('data')
    if (type == 'Transaction'):
        receive_tx(data)
    elif (type == 'Block'):
        receive_block(data)
    return {'success': True}

if __name__ == "dotcoin":
    port = os.environ.get("PORT", default=5000)
    print("This node is running on port: " + str(port), flush=True)