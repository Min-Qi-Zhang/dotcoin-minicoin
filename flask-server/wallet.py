# from Crypto.PublicKey import ECC
from nacl.signing import SigningKey
from nacl.encoding import RawEncoder
from os.path import exists
from typing import List, Tuple
import pickle

from p2p import get_my_port
from transaction import UTXO, TxIn, TxOut, Transaction, find_in_UTXOs, get_transaction_id, sign_tx_in

port = get_my_port()
private_key_location = './private_key_' + str(port)

def init_wallet() -> None:
    '''
        Generate a private key if it doesn't exist already
    '''
    if (exists(private_key_location)):
        return
    # private_key = ECC.generate(curve='P-256')
    private_key = SigningKey.generate()
    f = open(private_key_location, 'wb')
    # f.write(private_key.export_key(format='PEM'))
    pickle.dump(private_key, f)
    f.close()

def get_private_from_wallet() -> SigningKey:
    f = open(private_key_location, 'rb')
    # return ECC.import_key(f.read())
    private_key = pickle.load(f)
    f.close()
    return private_key

def get_public_from_wallet() -> str:
    if (not exists(private_key_location)):
        return ''
    private_key = get_private_from_wallet()
    # public_key = ECC.EccKey.public_key(private_key).export_key(format='raw')
    public_key = private_key.verify_key.encode(encoder=RawEncoder)
    return bytes.hex(public_key)

def get_balance(address: str, unspent_tx_outs: List[UTXO]) -> float:
    filtered_utxos = get_utxos_by_address(address, unspent_tx_outs)
    return sum([utxo.amount for utxo in filtered_utxos])

def get_utxos_by_address(address: str, unspent_tx_outs: List[UTXO]) -> List[UTXO]:
    return list(filter(lambda x: (x.address == address), unspent_tx_outs))

##### Start - Helper functions for create_transaction() #####

def find_tx_outs_for_amount(amount: float, my_utxos: List[UTXO]) -> Tuple[List[UTXO], float]:
    '''
        Return (included_utxos, left_over_amount)
        included_utxos: the UTXOs that will be used as tx_in
    '''
    current_amount = 0
    included_utxos = []
    for utxo in my_utxos:
        included_utxos.append(utxo)
        current_amount += utxo.amount
        if (current_amount >= amount):
            left_over_amount = current_amount - amount
            return (included_utxos, left_over_amount)
    return ([], 0)

def to_unsigned_tx_in(utxo: UTXO) -> TxIn:
    '''
        Create an unsigned TxIn from UTXO
    '''
    tx_in = TxIn()
    tx_in.tx_out_id = utxo.tx_out_id
    tx_in.tx_out_index = utxo.tx_out_index
    return tx_in

def create_unsigned_tx_ins(amount: float, my_utxos: List[UTXO]) -> List[TxIn]:
    '''
        Create a list of unsigned TxIn by given amount
    '''
    (included_utxos, left_over_amount) = find_tx_outs_for_amount(amount, my_utxos)
    if (included_utxos == []):
        return []
    return [to_unsigned_tx_in(utxo) for utxo in included_utxos]

def create_tx_outs(receiver_address: str, my_address: str, amount: float, left_over_amount: float) -> List[TxOut]:
    '''
        Create a list of TxOut, return [tx_out_to_receiver (, left_over_tx)]
    '''
    tx_out = TxOut(receiver_address, amount)
    if (left_over_amount == 0):
        return [tx_out]
    else:
        left_over_tx = TxOut(my_address, left_over_amount)
        return [tx_out, left_over_tx]

def filter_tx_pool_txs(a_unspent_tx_outs: List[UTXO], transaction_pool: List[Transaction]) -> List[UTXO]:
    '''
        Filter out the utxos that are already consumed in the transaction pool, return the resulted UTXOs
    '''
    tx_in_from_tx_pool = [tx_in for tx in transaction_pool for tx_in in tx.tx_ins]
    resulted_utxos = filter(lambda utxo: find_in_UTXOs(utxo, tx_in_from_tx_pool) == None, a_unspent_tx_outs)
    return list(resulted_utxos)

##### End - Helper functions for create_transaction() #####

def create_transaction(receiver_address: str, amount: float, a_unspent_tx_outs: List[UTXO], transaction_pool: List[Transaction]) -> Transaction:
    my_address = get_public_from_wallet()
    my_all_utxos = get_utxos_by_address(get_public_from_wallet(), a_unspent_tx_outs)
    my_unconsumed_utxos = filter_tx_pool_txs(my_all_utxos, transaction_pool)
    private_key = get_private_from_wallet()

    (included_utxos, left_over_amount) = find_tx_outs_for_amount(amount, my_unconsumed_utxos)
    if (included_utxos == []):
        print("Not enough UTXOs to spent", flush=True)
        return None

    transaction = Transaction()
    transaction.tx_ins = create_unsigned_tx_ins(amount, my_unconsumed_utxos)
    transaction.tx_outs = create_tx_outs(receiver_address, my_address, amount, left_over_amount)
    transaction.id = get_transaction_id(transaction)

    for i in range(len(transaction.tx_ins)):
        transaction.tx_ins[i].signature = sign_tx_in(transaction, i, private_key, my_address, a_unspent_tx_outs)
    return transaction