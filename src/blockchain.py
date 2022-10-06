import json
import hashlib
import time
from datetime import datetime
from typing import List

genesis_block = None
blockchain = []

# in seconds
BLOCK_GENERATION_INTERVAL = 10

# in blocks
DIFFICULTY_ADJUSTMENT_INTERVAL = 10

class Block:
    def __init__(self, index: int, hash: str, prev_hash: str, timestamp: int, data: str, difficulty: int, nonce: int):
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
        return calculate_hash(self.index, self.prev_hash, self.timestamp, self.data, self.difficulty, self.nonce)

genesis_block = Block(0, '816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7', None, 1664476570, 'This is a genesis block!', 0, 0)
blockchain.append(genesis_block)

def get_latest_block() -> Block:
    return blockchain[-1]

def get_blockchain() -> List[Block]:
    return blockchain

def get_genesis_block() -> Block:
    return genesis_block

def get_current_time() -> int:
    return int(time.mktime(datetime.now().timetuple()))

def calculate_hash(index: int, prev_hash: str, timestamp: int, data: str, difficulty: int, nonce: int) -> str:
    '''
        Compute hash over all data of block
    '''
    string = str(index) + prev_hash + str(timestamp) + data + str(difficulty) + str(nonce)
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def calculate_cumulative_difficulty(blocks: List[Block]) -> int:
    '''
        Sum of 2^difficulty of each block
    '''
    cumulative_difficulty = 0
    for block in blocks:
        cumulative_difficulty += pow(2, block.difficulty)
    return cumulative_difficulty

def get_difficulty() -> int:
    latest_block = get_latest_block()
    if (latest_block.index != 0 and latest_block.index % DIFFICULTY_ADJUSTMENT_INTERVAL == 0):
        return get_adjusted_difficulty(latest_block)
    else:
        return latest_block.difficulty

def get_adjusted_difficulty(latest_block: Block) -> int:
    '''
        Increase the difficulty if the time taken is 2 times greater than expected
        Decrease the difficulty if the time taken is 2 times less than expected
        Otherwise, the difficulty remains the same
    '''
    prev_adjustment_block = get_blockchain()[-DIFFICULTY_ADJUSTMENT_INTERVAL]
    time_expected = BLOCK_GENERATION_INTERVAL * DIFFICULTY_ADJUSTMENT_INTERVAL
    time_taken = latest_block.timestamp - prev_adjustment_block.timestamp
    if (time_taken < time_expected / 2):
        return prev_adjustment_block.difficulty + 1
    elif (time_taken > time_expected * 2):
        return prev_adjustment_block.difficulty - 1
    else:
        return prev_adjustment_block.difficulty

def generate_next_block(block_data: str) -> Block:
    prev_block = get_latest_block()
    next_index = prev_block.index + 1
    next_timestamp = get_current_time()
    next_difficulty = get_difficulty()
    next_block = find_block(next_index, prev_block.hash, next_timestamp, block_data, next_difficulty)
    if (add_block_to_chain(next_block)):
        broadcast_latest();
        return next_block
    return None

def is_valid_timestamp(new_block: Block, prev_block: Block) -> bool:
    ''' Timestamp is valid if:
        cur_time + 60 > new_block.timestamp > prev_block.timestamp - 60
    '''
    return get_current_time() + 60 > new_block.timestamp \
        and new_block.timestamp > prev_block.timestamp - 60

def is_valid_new_block(new_block: Block, prev_block: Block) -> bool:
    ''' Things to check:
        1. index of new_block must be larger than prev_block than by 1
        2. prev_hash of new_block must match hash of prev_block
        3. hash must be valid
        4. structure must match
        5. timestamp is valid
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

def is_valid_block_structure(block: Block) -> bool:
    '''
        Check type of each field in block
    '''
    return type(block.index) is int \
        and type(block.hash) is str \
        and type(block.prev_hash) is str \
        and type(block.timestamp) is int \
        and type(block.data) is str \
        and type(block.difficulty) is int \
        and type(block.nonce) is int

def is_valid_chain(blockchain_to_check: List[Block]) -> bool:
    '''
        First, check first block is genesis block, 
        then validation the rest of blocks.
    '''
    if (blockchain_to_check[0] != get_genesis_block()):
        return False
    for i in range(1, len(blockchain_to_check)):
        if(not is_valid_new_block(blockchain_to_check(i), blockchain_to_check(i - 1))):
            return False
    return True

def hash_match_difficulty(hash: str, difficulty: int) -> bool:
    '''
        Check whether hash starts with difficulty number of zeros
    '''
    binary_hash = bin(int(hash, 16)).zfill(8)
    return "0" * difficulty == binary_hash[:difficulty]

def replace_chain(new_blocks: List[Block]) -> None:
    '''
        Replace the chain with highest cummulative difficulty
    '''
    if (is_valid_chain(new_blocks) and \
        calculate_cumulative_difficulty(new_blocks) > calculate_cumulative_difficulty(blockchain)):
        print("Valid blockchain received.")
        blockchain = new_blocks
        broadcast_latest()
    else:
        print("Invalid blockchain received.")

def find_block(index: int, prev_hash: str, timestamp: int, data: str, difficulty: int) -> Block:
    '''
        Keep increasing nonce until we get a hash that matches difficulty,
        return a Block once a valid hash is found
    '''
    nonce = 0
    while(True):
        hash = calculate_hash(index, prev_hash, timestamp, data, difficulty, nonce)
        if (hash_match_difficulty(hash, difficulty)):
            return Block(index, hash, prev_hash, timestamp, data, difficulty, nonce)
        else:
            nonce += 1

def add_block_to_chain(block: Block) -> bool:
    '''
        Add block to blockchain, return True if success, return False otherwise
    '''
    if (is_valid_new_block(block, get_latest_block())):
        blockchain.append(block)
        return True
    return False

def broadcast_latest() -> None:
    # TODO broadcast the block. If the block already in blockchain, don't broadcast
    pass