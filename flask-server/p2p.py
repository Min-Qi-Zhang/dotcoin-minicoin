from flask import request
from typing import List
import os
import requests
import json

peer_urls = []

def get_my_port() -> int:
    return os.environ.get("PORT")

def get_my_url() -> str:
    (ip, port) = request.environ['werkzeug.socket'].getsockname()
    return "http://" + ip + ":" + str(port)

def broadcast_latest() -> None:
    # TODO broadcast the block. If the block already in blockchain, don't broadcast
    pass

def broadcast_transaction_pool() -> None:
    pass

def add_peer_to_list(url: str) -> str:
    if (url not in peer_urls):
        peer_urls.append(url)
    return get_my_url()
    
def join_network(url: str) -> bool:
    data = json.dumps({'url': get_my_url()})
    request_url = url + '/addPeer'
    
    try:
        result = requests.post(request_url, data=data, headers={"Content-Type": "application/json"})
        status = result.status_code
        if (status == 200):
            add_peer_to_list(url)
            return True
        else:
            return False
    except Exception:
        return False

def get_peers_list() -> List[str]:
    return peer_urls