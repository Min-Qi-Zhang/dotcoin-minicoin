from flask import Flask, request
import hashlib
import time
from datetime import datetime
import json

genesis_block = None
blockchain = []

class Block:
    def __init__(self, index, hash, prev_hash, timestamp, data):
        self.index = index
        self.hash = hash
        self.prev_hash = prev_hash
        self.timestamp = timestamp
        self.data = data

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def calculate_hash_for_block(self):
        return calculate_hash(self.index, self.prev_hash, self.timestamp, self.data)

def calculate_hash(index, prev_hash, timestamp, data):
    string = str(index) + prev_hash + str(timestamp) + data
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def get_latest_block():
    return blockchain[-1]

def generate_next_block(block_data):
    prev_block = get_latest_block()
    next_index = prev_block.index + 1
    next_timestamp = int(time.mktime(datetime.now().timetuple()))
    next_hash = calculate_hash(next_index, prev_block.hash, next_timestamp, block_data)
    return Block(next_index, next_hash, prev_block.hash, next_timestamp, block_data)

def is_valid_new_block(new_block, prev_block):
    ''' Things to check:
        1. index of new_block must be larger than prev_block than by 1
        2. prev_hash of new_block must match hash of prev_block
        3. hash must be valid
        4. structure must match
    '''
    if (not is_valid_block_structure(new_block)):
        print("Invalid block structure")
        return False
    elif (prev_block.index + 1 != new_block.index):
        print("Invalid index!")
        return False
    elif (new_block.prev_hash != prev_block.hash):
        print("prev_hash doesn't match!")
        return False
    elif (new_block.calculate_hash_for_block() != new_block.hash):
        print("Invalid hash!")
        return False
    return True

def is_valid_block_structure(block):
    return type(block.index) is int \
        and type(block.hash) is str \
        and type(block.prev_hash) is str \
        and type(block.timestamp) is int \
        and type(block.data) is str

def is_valid_chain(blockchain):
    if (blockchain[0] != genesis_block):
        return False
    for i in range(1, len(blockchain)):
        if(not is_valid_new_block(blockchain(i), blockchain(i - 1))):
            return False
    return True

def broadcast_latest():
    # TODO
    return None

def replace_chain(new_blocks):
    if (is_valid_chain(new_blocks) and len(new_blocks) > len(blockchain)):
        print("Valid blockchain received.")
        blockchain = new_blocks
        # broadcast_latest()
    else:
        print("Invalid blockchain received.")

app = Flask(__name__)
app.debug = True

genesis_block = Block(0, '816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7', None, 1664476570, 'This is a genesis block!')
blockchain.append(genesis_block)

@app.route("/")
def index():
    return "Hello World!"

@app.get("/blocks")
def get_blocks():
    return json.dumps([block.toJson() for block in blockchain])

@app.post("/mine_block")
def mine_block():
    new_block = generate_next_block(request.args.get('data'))
    return new_block.toJson()
