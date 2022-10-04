from flask import Flask, request
import hashlib
import time
from datetime import datetime
import json

import transaction

genesis_block = None
blockchain = []
BLOCK_GENERATION_INTERVAL = 10
DIFFICULTY_ADJUSTMENT_INTERVAL = 10

class Block:
    def __init__(self, index, hash, prev_hash, timestamp, data, difficulty, nonce):
        self.index = index
        self.hash = hash
        self.prev_hash = prev_hash
        self.timestamp = timestamp
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def calculate_hash_for_block(self):
        return calculate_hash(self.index, self.prev_hash, self.timestamp, self.data)

def calculate_hash(index, prev_hash, timestamp, data):
    string = str(index) + prev_hash + str(timestamp) + data
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def calculate_cumulative_difficulty(blocks):
    cumulative_difficulty = 0
    for block in blocks:
        cumulative_difficulty += pow(2, block.difficulty)
    return cumulative_difficulty

def get_latest_block():
    return blockchain[-1]

def get_current_time():
    return int(time.mktime(datetime.now().timetuple()))

def generate_next_block(block_data):
    prev_block = get_latest_block()
    next_index = prev_block.index + 1
    next_timestamp = get_current_time()
    next_hash = calculate_hash(next_index, prev_block.hash, next_timestamp, block_data)
    next_block = Block(next_index, next_hash, prev_block.hash, next_timestamp, block_data)
    blockchain.append(next_block) # TODO verify the block before adding to the chain
    # TODO broadcast the block. If the block already in blockchain, don't broadcast
    return next_block

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
    elif (not is_valid_timestamp(new_block, prev_block)):
        print("Invalid timestamp!")
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

def is_valid_timestamp(new_block, prev_block):
    ''' Timestamp is valid if:
        cur_time + 60 > new_block.timestamp > prev_block.timestamp - 60
    '''
    return get_current_time() + 60 > new_block.timestamp \
        and new_block.timestamp > prev_block.timestamp - 60

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
    if (is_valid_chain(new_blocks) and \
        calculate_cumulative_difficulty(new_blocks) > calculate_cumulative_difficulty(blockchain)):
        print("Valid blockchain received.")
        blockchain = new_blocks
        # broadcast_latest()
    else:
        print("Invalid blockchain received.")

def hash_match_difficulty(hash, difficulty):
    binary_hash = bin(int(hash, 16)).zfill(8)
    return "0" * difficulty == binary_hash[:difficulty]

def find_block(index, prev_hash, timestamp, data, difficulty):
    nonce = 0
    while(True):
        hash = calculate_hash(index, prev_hash, timestamp, data)
        if (hash_match_difficulty(hash, difficulty)):
            return Block(index, hash, prev_hash, timestamp, data, difficulty, nonce)
        else:
            nonce += 1

def get_difficulty():
    latest_block = blockchain[-1]
    if (latest_block.index != 0 and latest_block.index % DIFFICULTY_ADJUSTMENT_INTERVAL == 0):
        return get_adjusted_difficulty(latest_block)
    else:
        return latest_block.difficulty

def get_adjusted_difficulty(latest_block):
    '''
        Increase the difficulty if the time taken is 2 times greater than expected
        Decrease the difficulty if the time taken is 2 times less than expected
        Otherwise, the difficulty remains the same
    '''
    prev_adjustment_block = blockchain[-DIFFICULTY_ADJUSTMENT_INTERVAL]
    time_expected = BLOCK_GENERATION_INTERVAL * DIFFICULTY_ADJUSTMENT_INTERVAL
    time_taken = latest_block.timestamp - prev_adjustment_block.timestamp
    if (time_taken < time_expected / 2):
        return prev_adjustment_block.difficulty + 1
    elif (time_taken > time_expected * 2):
        return prev_adjustment_block.difficulty - 1
    else:
        return prev_adjustment_block.difficulty

app = Flask(__name__)
app.debug = True

genesis_block = Block(0, '816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7', None, 1664476570, 'This is a genesis block!', 0, 0)
blockchain.append(genesis_block)

@app.route("/")
def index():
    return "Hello World!"

@app.get("/blocks")
def get_blocks():
    return json.dumps([block.toJson() for block in blockchain])

@app.post("/mineBlock")
def mine_block():
    new_block = generate_next_block(request.args.get('data'))
    return new_block.toJson()


# p2p: when a peer wants join, add it to the list, then send it the blockchain
@app.get("/peers")
def get_peers():
    # TODO
    return

@app.post("/add_peer")
def add_peer():
    # TODO
    return

