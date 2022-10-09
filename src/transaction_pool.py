from typing import List
from transaction import UTXO, Transaction, find_in_UTXOs, is_valid_transaction

transaction_pool = []

def get_transaction_pool() -> List[Transaction]:
    return transaction_pool

def add_to_transaction_pool(tx: Transaction, a_unspent_tx_outs: List[UTXO]) -> bool:
    if (not is_valid_transaction(tx, a_unspent_tx_outs)):
        return False
    if (not is_valid_tx_for_pool(tx)):
        return False

    transaction_pool.append(tx)
    return True

def is_valid_tx_for_pool(tx: Transaction) -> bool:
    '''
        Indicate whether tx is valid for pool, a valid tx must not already have its tx_ins in exists in transaction pool
    '''
    tx_ins_from_pool = [tx_in for tx in get_transaction_pool() for tx_in in tx.tx_ins]
    for tx_in in tx.tx_ins:
        if (find_in_UTXOs(tx_in, tx_ins_from_pool)):
            return False
    return True

def update_transaction_pool(a_unspent_tx_outs: List[UTXO]) -> None:
    '''
        Remove invalid transactions from transaction_pool. 
        The tx_ins of an invalid transaction is referenced to an unexisted UTXO in unspend_tx_outs.
    '''
    invalid_txs = []
    for tx in get_transaction_pool():
        for tx_in in tx.tx_ins:
            if (not find_in_UTXOs(tx_in, a_unspent_tx_outs)):
                invalid_txs.append(tx)
                break
    
    while(len(invalid_txs) > 0):
        tx_to_remove = invalid_txs.pop(0)
        transaction_pool.remove(tx_to_remove)