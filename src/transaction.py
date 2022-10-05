import hashlib
from Crypto.Signature import DSS
from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256

unspent_tx_outs = []
COINBASE_AMOUNT = 50

class TxOut:
    def __init__(self, address, amount):
        self.address = address  # an ECDSA public-key
        self.amount = amount

class TxIn:
    tx_out_id = ''
    tx_out_index = -1
    signature = ''

class Transaction:
    id = ''
    tx_ins = []
    tx_outs = []

class UTXO:
    def __init__(self, tx_out_id, tx_out_index, address, amount):
        self._tx_out_id = tx_out_id
        self._tx_out_index = tx_out_index
        self._address = address
        self._amount = amount

    @property
    def tx_out_id(self):
        return self._tx_out_id

    @property
    def tx_out_index(self):
        return self._tx_out_index

    @property
    def address(self):
        return self._address
    
    @property
    def amount(self):
        return self._amount

def get_UTXOs():
    return unspent_tx_outs

def get_transaction_id(transaction):
    tx_in_content = ''
    for tx_in in transaction.tx_ins:
        tx_in_content += (tx_in.tx_out_id + str(tx_in.tx_out_index))

    tx_out_content = ''
    for tx_out in transaction.tx_outs:
        tx_out_content += (tx_out.address + str(tx_out.amount))

    string = tx_in_content + tx_out_content
    return hashlib.sha256(string.encode('utf-8')).hexdigest()
    
def sign_tx_in(transaction, tx_in_index, private_key, public_key, a_unspent_tx_outs):
    tx_in = transaction.tx_ins[tx_in_index]

    referenced_utxo = find_in_UTXOs(tx_in, a_unspent_tx_outs)
    if (referenced_utxo == None):
        raise Exception("Could not find reference tx_out")

    referenced_address = referenced_utxo.address
    if (public_key != referenced_address):
        raise Exception("Key does not match the address that is referenced in tx_in")

    data_to_sign = transaction.id
    # https://pycryptodome.readthedocs.io/en/latest/src/signature/dsa.html
    h = SHA256.new(data_to_sign.encode('utf-8'))
    signer = DSS.new(private_key, 'fips-186-3')
    signature = signer.sign(h).hex()
    return signature

def new_unspent_tx_outs(new_transactions):
    new_UTXOs = []
    for t in new_transactions:
        for index in range(len(t.tx_outs)):
            tx_out = t.tx_outs[index]
            new_UTXOs.append(UTXO(t.id, index, tx_out.address, tx_out.amount))
    return new_UTXOs

def consumed_tx_outs(new_transactions):
    tx_ins = []
    for t in new_transactions:
        tx_ins += t.tx_ins
    return [UTXO(tx_in.tx_out_id, tx_in.tx_out_index, '', 0) for tx_in in tx_ins]

def find_in_UTXOs(target, utxos):
    '''
        Find target in utxos, return it if exists, otherwise return None
    '''
    for u in utxos:
        if u.tx_out_id == target.tx_out_id \
            and u.tx_out.index == target.tx_out.index:
            return u
    return None

def resulting_unspent_tx_outs(new_transactions):
    new_UTXOs = new_unspent_tx_outs(new_transactions)
    consumed = consumed_tx_outs(new_transactions)
    filtered_UTXOs = filter(lambda utxo: find_in_UTXOs(utxo, consumed) == None, get_UTXOs())
    return filtered_UTXOs + new_UTXOs

def is_valid_transaction_structure(transaction):
    if (not type(transaction.id) is str):
        print("Invalid type of transaction id")
        return False

    for tx_in in transaction.tx_ins:
        if (not type(tx_in.tx_out_id) is str):
            print("Invalid type of tx_in.tx_out_id")
            return False
        elif (not type(tx_in.tx_out_index) is int):
            print("Invalid type of tx_in.tx_out_index")
            return False
        elif (not type(tx_in.signature) is str):
            print("Invalid type of signature")
            return False
    
    for tx_out in transaction.tx_outs:
        if (not type(tx_out.address) is str):
            print("Invalid type of tx_out.address")
            return False
        elif (not type(tx_out.amount) is int):
            print("Invalid type of tx_out.amount")
            return False

    return True

def is_valid_tx_id(transaction):
    return get_transaction_id(transaction) == transaction.id

def is_valid_tx_ins(tx_in, transaction):
    referenced_utxo = find_in_UTXOs(tx_in, get_UTXOs())
    if (referenced_utxo == None):
        print("Referenced utxo not found")
        return ''
    public_key = referenced_utxo.address

    # https://pycryptodome.readthedocs.io/en/latest/src/signature/dsa.html
    h = SHA256.new(transaction.id.encode('utf-8'))
    verifier = DSS.new(public_key, 'fips-186-3')
    try:
        verifier.verify(h, bytes.fromhex(tx_in.signature))
        print ("The message is authentic.")
        return True
    except ValueError:
        print ("The message is not authentic.")
        return False

def is_valid_tx_out_values(transaction):
    total_in = 0
    total_out = 0

    for tx_in in transaction.tx_ins:
        total_in += find_in_UTXOs(tx_in, get_UTXOs()).amount

    for tx_out in transaction.tx_outs:
        total_out += tx_out.amount

    return total_in == total_out

def validate_coinbase_tx(transaction, block_index):
    ''' Conditions:
        1. transaction id must be valid
        2. only one tx_in
        3. tx_ins[0].tx_out_index == block_index
        4. only one tx_out
        5. amount must equal to COINBASE_AMOUNT
    '''
    if (get_transaction_id(transaction) != transaction.id):
        print("Invalid coinbase tx id")
        return False
    elif (len(transaction.tx_ins) != 1):
        print("One tx_in must be specified in coinbase transaction")
        return False
    elif (transaction.tx_ins[0].tx_out_index != block_index):
        print("Index must be same as block index")
        return False
    elif (len(transaction.tx_outs) != 1):
        print("Invalid number of tx_outs in coinbase transaction")
        return False
    elif (transaction.tx_outs[0].amount != COINBASE_AMOUNT):
        print("Invalid coinbase amount")
        return False
    return True