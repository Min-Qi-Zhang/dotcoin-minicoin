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

def broadcast_latest_block(message) -> None:
    for url in peer_urls:
        print("Send block to " + url + "...", flush=True)
        request_url = url + '/message'
        body = {"data": message.toJson(), "type": "Block"}
        requests.post(request_url, data=json.dumps(body), headers={"Content-Type": "application/json"})

def broadcast_transaction(message) -> None:
    for url in peer_urls:
        print("Send transaction to " + url + "...", flush=True)
        request_url = url + '/message'
        body = {"data": message.toJson(), "type": "Transaction"}
        requests.post(request_url, data=json.dumps(body), headers={"Content-Type": "application/json"})

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

