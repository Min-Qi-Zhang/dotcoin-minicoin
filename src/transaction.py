import hashlib
import json
# from Crypto.Signature import DSS
# from Crypto.PublicKey import ECC
# from Crypto.Hash import SHA256
from nacl.signing import SigningKey
from nacl.signing import VerifyKey
from nacl.encoding import RawEncoder
from nacl.exceptions import BadSignatureError
from typing import List, Union

COINBASE_AMOUNT = 50

class TxOut:
    def __init__(self, address: str, amount: float):
        self.address = address  # an ECDSA public-key
        self.amount = amount

class TxIn:
    '''
        tx_out_id: str
        tx_out_index: int
        signature: str
    '''
    def __init__(self):
        self.tx_out_id = ''
        self.tx_out_index = 0
        self.signature = ''

class Transaction:
    '''
        id: str
        tx_ins: List[TxIn]
        tx_outs: List[TxOut]
    '''
    def __init__(self): 
        self.id = ''
        self.tx_ins = []
        self.tx_outs = []

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

class UTXO:
    def __init__(self, tx_out_id: str, tx_out_index: int, address: str, amount: float):
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

    def toJson(self):
        return json.dumps(self, default=lambda o: {'tx_out_id': self.tx_out_id, 'tx_out_index': self.tx_out_index, 'address': self.address, 'amount': self.amount})

def get_transaction_id(transaction: Transaction) -> str:
    '''
        Compute transaction id over the contents of transaction (except signature of TxIn)
    '''
    tx_in_content = ''
    for tx_in in transaction.tx_ins:
        tx_in_content += (tx_in.tx_out_id + str(tx_in.tx_out_index))

    tx_out_content = ''
    for tx_out in transaction.tx_outs:
        tx_out_content += (tx_out.address + str(tx_out.amount))

    string = tx_in_content + tx_out_content
    return hashlib.sha256(string.encode('utf-8')).hexdigest()
    
def sign_tx_in(transaction: Transaction, tx_in_index: int, private_key: SigningKey, public_key: str, a_unspent_tx_outs: List[UTXO]) -> str:
    '''
        First, check if tx_in is referenced to an existing UTXO (raise Exception if DNE),
        then, check address of UTXO matches public_key (raise Exception if doesn't match),
        lastly, sign transaction id and return signature
    '''
    tx_in = transaction.tx_ins[tx_in_index]

    referenced_utxo = find_in_UTXOs(tx_in, a_unspent_tx_outs)
    if (referenced_utxo == None):
        raise Exception("Could not find reference tx_out")

    referenced_address = referenced_utxo.address
    if (public_key != referenced_address):
        raise Exception("Key does not match the address that is referenced in tx_in")

    data_to_sign = transaction.id
    # https://pycryptodome.readthedocs.io/en/latest/src/signature/dsa.html
    # h = SHA256.new(data_to_sign.encode('utf-8'))
    # signer = DSS.new(private_key, 'fips-186-3')
    # signature = signer.sign(h).hex()
    signed_raw = private_key.sign(data_to_sign.encode('utf-8'), encoder=RawEncoder)
    signature_bytes = RawEncoder.decode(signed_raw.signature)
    return bytes.hex(signature_bytes)

def new_unspent_tx_outs(new_transactions: List[Transaction]) -> List[UTXO]:
    '''
        Retrieve all new unspent transaction outputs from the new block
    '''
    new_UTXOs = []
    for t in new_transactions:
        for index in range(len(t.tx_outs)):
            tx_out = t.tx_outs[index]
            new_UTXOs.append(UTXO(t.id, index, tx_out.address, tx_out.amount))
    return new_UTXOs

def consumed_tx_outs(new_transactions: List[Transaction]) -> List[UTXO]:
    '''
        Retrieve all UTXOs that are consumed by new transactions
    '''
    tx_ins = []
    for t in new_transactions:
        tx_ins += t.tx_ins
    return [UTXO(tx_in.tx_out_id, tx_in.tx_out_index, '', 0) for tx_in in tx_ins]

def find_in_UTXOs(target: Union[TxIn, UTXO], lst: Union[List[TxIn], List[UTXO]]) -> UTXO:
    '''
        Find target in lst, return it if exists, otherwise return None
        :param TxIn/UTXO target: tx_in or an unspent tx_out
        :param List[TxIn]/List[UTXO] lst: a list of tx_in or a list of UTXO
    '''
    for u in lst:
        if u.tx_out_id == target.tx_out_id \
            and u.tx_out_index == target.tx_out_index:
            return u
    return None

def resulting_unspent_tx_outs(new_transactions: List[Transaction], a_unspent_tx_outs: List[UTXO]) -> List[UTXO]:
    '''
        Return the resulting UTXOs by removing consumed UTXOs and adding new UTXOs
    '''
    new_UTXOs = new_unspent_tx_outs(new_transactions)
    consumed_UTXOs = consumed_tx_outs(new_transactions)
    filtered_UTXOs = filter(lambda utxo: find_in_UTXOs(utxo, consumed_UTXOs) == None, a_unspent_tx_outs)
    return list(filtered_UTXOs) + new_UTXOs

##### Start - Helper functions for is_valid_transaction() #####

def is_valid_tx_structure(transaction: Transaction) -> bool:
    if (not type(transaction.id) is str):
        print("Invalid type of transaction id", flush=True)
        return False

    for tx_in in transaction.tx_ins:
        if (not type(tx_in.tx_out_id) is str):
            print("Invalid type of tx_in.tx_out_id", flush=True)
            return False
        elif (not type(tx_in.tx_out_index) is int):
            print("Invalid type of tx_in.tx_out_index", flush=True)
            return False
        elif (not type(tx_in.signature) is str):
            print("Invalid type of signature", flush=True)
            return False
    
    for tx_out in transaction.tx_outs:
        if (not type(tx_out.address) is str):
            print("Invalid type of tx_out.address", flush=True)
            return False
        elif (not (type(tx_out.amount) is float or type(tx_out.amount) is int)):
            print("Invalid type of tx_out.amount", flush=True)
            return False

    return True

def is_valid_tx_id(transaction: Transaction) -> bool:
    return get_transaction_id(transaction) == transaction.id

def is_valid_tx_ins(tx_in: TxIn, transaction: Transaction, a_unspent_tx_outs: List[UTXO]) -> bool:
    '''
        Validate the signature in TxIns
    '''
    referenced_utxo = find_in_UTXOs(tx_in, a_unspent_tx_outs)
    if (referenced_utxo == None):
        print("Referenced utxo not found", flush=True)
        return False
    public_key = referenced_utxo.address

    # https://pycryptodome.readthedocs.io/en/latest/src/signature/dsa.html
    # key = ECC.import_key(bytes.fromhex(public_key), curve_name='P-256') # convert from str to ECC.EccKey object
    # h = SHA256.new(transaction.id.encode('utf-8'))
    # verifier = DSS.new(key, 'fips-186-3')
    verify_key = VerifyKey(bytes.fromhex(public_key), encoder=RawEncoder)
    try:
    #     verifier.verify(h, bytes.fromhex(tx_in.signature))
        verify_key.verify(transaction.id.encode('utf-8'), bytes.fromhex(tx_in.signature), encoder=RawEncoder)
        print ("The message is authentic.")
        return True
    except BadSignatureError:
        print ("The message is not authentic.")
        return False

def is_valid_tx_out_values(transaction: Transaction, a_unspent_tx_outs: List[UTXO]) -> bool:
    '''
        Check whether total of TxIns matches the total of TxOuts in transaction
    '''
    total_in = 0
    total_out = 0

    for tx_in in transaction.tx_ins:
        total_in += find_in_UTXOs(tx_in, a_unspent_tx_outs).amount

    for tx_out in transaction.tx_outs:
        total_out += tx_out.amount

    return total_in == total_out

##### End - Helper functions for is_valid_transaction() #####

def is_valid_transaction(transaction: Transaction, a_unspent_tx_outs: List[UTXO]) -> bool:
    for tx_in in transaction.tx_ins:
        if (not is_valid_tx_ins(tx_in, transaction, a_unspent_tx_outs)):
            return False

    return is_valid_tx_structure(transaction) \
        and is_valid_tx_id(transaction) \
            and is_valid_tx_out_values(transaction, a_unspent_tx_outs)

def is_valid_coinbase_tx(transaction: Transaction, block_index: int) -> bool:
    ''' Conditions:
        1. transaction id must be valid
        2. only one tx_in
        3. tx_ins[0].tx_out_index == block_index
        4. only one tx_out
        5. amount must equal to COINBASE_AMOUNT
        6. transaction structure must be valid
    '''
    if (not is_valid_tx_structure(transaction)):
        print("Invalid coinbase tx structure", flush=True)
        return False
    elif (get_transaction_id(transaction) != transaction.id):
        print("Invalid coinbase tx id", flush=True)
        return False
    elif (len(transaction.tx_ins) != 1):
        print("One tx_in must be specified in coinbase transaction", flush=True)
        return False
    elif (transaction.tx_ins[0].tx_out_index != block_index):
        print("Index must be same as block index", flush=True)
        return False
    elif (len(transaction.tx_outs) != 1):
        print("Invalid number of tx_outs in coinbase transaction", flush=True)
        return False
    elif (transaction.tx_outs[0].amount != COINBASE_AMOUNT):
        print("Invalid coinbase amount", flush=True)
        return False
    return True

def is_valid_block_transactions(transactions: List[Transaction], block_index: int, a_unspent_tx_outs: List[UTXO]) -> bool:
    # Check coinbase transaction
    if (not is_valid_coinbase_tx(transactions[0], block_index)):
        print("The first transaction is not coinbase transaction", flush=True)
        return False

    # Check for duplicate TxIns
    all_tx_ins = []
    for tx in transactions:
        for tx_in in tx.tx_ins:
            if tx_in not in all_tx_ins:
                all_tx_ins.append(tx_in)
            else:
                print("Duplicate found", flush=True)
                return False

    # Check the rest of transactions
    for i in range(1, len(transactions)):
        tx = transactions[i]
        if (not is_valid_transaction(tx, a_unspent_tx_outs)):
            print("Invalid transaction", flush=True)
            return False
    return True

def process_transactions(transactions: List[Transaction], index: int, a_unspent_tx_outs: List[UTXO]) -> Union[List[UTXO], None]:
    '''
        Validate each transaction and return UTXOs if the check is passed.
        Return None if transaction validation failed, otherwise return resulted UTXOs
    '''
    if (not is_valid_block_transactions(transactions, index, a_unspent_tx_outs)):
        return None
    return resulting_unspent_tx_outs(transactions, a_unspent_tx_outs)

def create_coinbase_tx(address: str, block_index: int) -> Transaction:
    tx = Transaction()

    tx_in = TxIn()
    tx_in.tx_out_index = block_index
    tx_in.tx_out_id = ''
    tx_in.signature = ''
    tx.tx_ins = [tx_in]

    tx.tx_outs = [TxOut(address, COINBASE_AMOUNT)]
    tx.id = get_transaction_id(tx)
    return tx