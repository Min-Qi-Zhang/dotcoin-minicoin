from Crypto.PublicKey import ECC
from os.path import exists

from transaction import TxIn, TxOut, Transaction, get_transaction_id, sign_tx_in

private_key_location = 'node/wallet/private_key.pem'

def init_wallet():
    if (exists(private_key_location)):
        return
    private_key = ECC.generate(curve='P-256')
    f = open(private_key_location, 'w')
    f.write(private_key.export_key(format='PEM'))
    f.close()

def get_private_from_wallet():
    f = open(private_key_location, 'r')
    return ECC.import_key(f.read())

def get_public_from_wallet():
    private_key = get_private_from_wallet()
    return ECC.EccKey.public_key(private_key)

def get_balance(address, unspent_tx_outs):
    filtered_utxos = filter(lambda x: (x.address == address), unspent_tx_outs)
    return sum([utxo.amount for utxo in filtered_utxos])

def find_tx_outs_for_amount(amount, my_utxos):
    current_amount = 0
    included_utxos = []
    for utxo in my_utxos:
        included_utxos.append(utxo)
        current_amount += utxo.amount
        if (current_amount >= amount):
            left_over_amount = current_amount - amount
            return (included_utxos, left_over_amount)
    return ([], -1)

def to_unsigned_tx_in(utxo):
    tx_in = TxIn()
    tx_in.tx_out_id = utxo.tx_out_id
    tx_in.tx_out_index = utxo.tx_out_index
    return tx_in

def create_unsigned_tx_ins(amount, my_utxos):
    (included_utxos, left_over_amount) = find_tx_outs_for_amount(amount, my_utxos)
    return [to_unsigned_tx_in(utxo) for utxo in included_utxos]

def create_tx_outs(receiver_address, my_address, amount, left_over_amount):
    tx_out = TxOut(receiver_address, amount)
    if (left_over_amount == 0):
        return [tx_out]
    else:
        left_over_tx = TxOut(my_address, left_over_amount)
        return [tx_out, left_over_tx]

def create_transaction(receiver_address, amount, a_unspent_tx_outs):
    my_address = get_private_from_wallet()
    my_utxos = a_unspent_tx_outs.filter(lambda x: (x.address == my_address), a_unspent_tx_outs)
    private_key = get_private_from_wallet()
    public_key = get_public_from_wallet()

    transaction = Transaction()
    transaction.tx_ins = create_unsigned_tx_ins(amount, my_utxos)
    transaction.tx_outs = create_tx_outs(receiver_address, my_address, amount, find_tx_outs_for_amount(amount, my_utxos)[1])
    transaction.id = get_transaction_id(transaction)

    for i in range(len(transaction.tx_ins)):
        transaction.tx_ins[i].signature = sign_tx_in(transaction, i, private_key, public_key, a_unspent_tx_outs)
    return transaction