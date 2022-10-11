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

def add_to_peer_list(url: str) -> None:
    if (url not in peer_urls):
        peer_urls.append(url)

def get_peers_list() -> List[str]:
    return peer_urls

