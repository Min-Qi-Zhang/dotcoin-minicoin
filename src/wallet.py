from Crypto.PublicKey import ECC
from os.path import exists
from typing import List, Tuple

from transaction import UTXO, TxIn, TxOut, Transaction, get_transaction_id, sign_tx_in

private_key_location = './private_key.pem'

def init_wallet() -> None:
    '''
        Generate a private key if it doesn't exist already
    '''
    if (exists(private_key_location)):
        return
    private_key = ECC.generate(curve='P-256')
    f = open(private_key_location, 'w')
    f.write(private_key.export_key(format='PEM'))
    f.close()

def get_private_from_wallet() -> ECC.EccKey:
    f = open(private_key_location, 'r')
    return ECC.import_key(f.read())

def get_public_from_wallet() -> str:
    private_key = get_private_from_wallet()
    public_key = ECC.EccKey.public_key(private_key).export_key(format='raw')
    return str(public_key)

def get_balance(address: str, unspent_tx_outs: List[UTXO]) -> float:
    filtered_utxos = filter(lambda x: (x.address == address), unspent_tx_outs)
    return sum([utxo.amount for utxo in filtered_utxos])

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

##### End - Helper functions for create_transaction() #####

def create_transaction(receiver_address: str, amount: float, a_unspent_tx_outs: List[UTXO]) -> Transaction:
    (included_utxos, left_over_amount) = find_tx_outs_for_amount(amount, my_utxos)
    if (included_utxos == []):
        print("Not enough UTXOs to spent")
        return None

    my_address = get_public_from_wallet()
    my_utxos = a_unspent_tx_outs.filter(lambda x: (x.address == my_address), a_unspent_tx_outs)
    private_key = get_private_from_wallet()

    transaction = Transaction()
    transaction.tx_ins = create_unsigned_tx_ins(amount, my_utxos)
    transaction.tx_outs = create_tx_outs(receiver_address, my_address, amount, left_over_amount)
    transaction.id = get_transaction_id(transaction)

    for i in range(len(transaction.tx_ins)):
        transaction.tx_ins[i].signature = sign_tx_in(transaction, i, private_key, my_address, a_unspent_tx_outs)
    return transaction