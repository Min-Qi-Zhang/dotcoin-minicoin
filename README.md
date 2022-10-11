Dotcoin
-----

In this assignment, you will build a small ledger-based blockchain similar to Bitcoin. The original Bitcoin [whitepaper](https://Bitcoin.org/Bitcoin.pdf) is an excellent resource however the tutorial [Naivecoin: a tutorial for building a cryptocurrency](https://lhartikk.github.io/) provides a simpler but yet comprehensive overview of the most important Bitcoin concepts.

You are tasked to implement a Python version of Naivecoin called *Dotcoin*. The goal is not solely to translate this code into python but rather understand in details the Bitcoin mechanics. You code must work but your grade will also depend on your understanding of the concepts. You will likely be asked to explain your code during during a live meeting with the instructor. 

The blockchain will run within a [Docker container](https://thierrysans.me/CSCD27/doc/docker/) and use [Python Flask](https://palletsprojects.com/p/flask/) for the HTTP server (instead of Node Express in the tutorial) and the [Python Libsodium Library (PyNaCl)](https://pynacl.readthedocs.io/en/latest/) for the cryptography primitives.

Build the docker image (first time only)

```
docker build -t dotcoin .
```

To run your code in debug mode (the server will automatically reload when the source files change)

```
docker run --rm -p 5000:5000 -v $(pwd)/flask-server:/shared dotcoin flask --app dotcoin.py --debug run --host=0.0.0.0
```

Type `ctrl-c` to stop the server. 

How to Run
-----
Step 1 - Build React app
```
cd react-app && npm run build
```

Step 2 - Create docker network
```
docker network create -d bridge my-bridge-network
```

Step 3 - Run multiple nodes
```
docker run --rm --network=my-bridge-network -p {{ PORT_NUM }}:5000 -e PORT={{ PORT_NUM }} -v $(pwd)/flask-server:/shared dotcoin flask --app dotcoin.py --debug run --host=0.0.0.0
```
Replace `{{ PORT_NUM }}` with port number that you want to run the node on. For example, to run on port `5001`: 
```
docker run --rm --network=my-bridge-network -p 5001:5000 -e PORT=5001 -v $(pwd)/flask-server:/shared dotcoin flask --app dotcoin.py --debug run --host=0.0.0.0
```
Step 4 - Open `http://localhost:5000` in the browser to see the UI.


API
---

### Get blockchain
- description: retrieve all blocks in blockchain
- request: `GET /blocks`
```
$ curl http://localhost:5000/blocks
```

### Update blockchain
- description: update blockchain by getting it first peer in peer list, this is used after connected to the network
- request: `PATCH /blocks`
```
$ curl -X PATCH http://localhost:5000/blocks
```

### Find block by hash
- request: `GET /block/:hash`
```
$ curl http://localhost:5000/block/816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7
```

### Find transaction by id
- request: `GET /transaction/:id`
```
$ curl http://localhost:5000/transaction/b4cd43dcf8ae6f51316d388ded308ff99ead8c2e1fc1e2e1247475e058b6b1d7
```

### Get transaction pool
- request: `GET /transactionPool`
```
$ curl http://localhost:5000/transactionPool
```

### Get all UTXOs
- request: `GET /unspentTransactionOutputs`
```
$ curl http://localhost:5000/unspentTransactionOutputs
```

### Get my UTXOs
- request: `GET /myUnspentTransactionOutputs`
```
$ curl http://localhost:5000/myUnspentTransactionOutputs
```

### Get address (public key)
- request: `GET /address`
```
$ curl http://localhost:5000/address
```

### Get UTXOs by address
- description: return a list of UTXOs of a given address
- request: `GET /address/:address`
```
$ curl http://localhost:5000/address/4e64c77bac3408cd916d0ce4fea383df2c56954e22e88d2859dca5e2e4187d49
```

### Mine block
- description: this API is for testing purpose only, it's not used by frontend. The actual mine block task is running continuously in the background.
- request: `POST /mineBlock`
```
$ curl -X POST http://localhost:5000/mineBlock
```

### Get balance
- request: `GET /balance`
```
$ curl http://localhost:5000/address
```

### Send transaction
- description: create a transaction and broadcast it to its connected peers
- request: `POST /sendTransaction`
- body: object
  - address: (string) public key of receiver
  - amount: (number) amount to send
```
$ curl -X POST -H "Content-Type: application/json" -d '{"address": "c3797bc67dff6f53efa0c4d166f5c29eb33ebf09f8b9c21af1a84ef7d537a9cd", "amount": 10}' http://localhost:5000/sendTransaction
```

### Generate key pair
- description: generate a key pair and return public key
- request: `GET /getKeyPair`
```
$ curl http://localhost:5000/getKeyPair
```

### Get peers
- description: return a list of urls of connected peers
- request: `GET /peers`
```
$ curl http://localhost:5000/peers
```

### Join network
- description: join the network by sending the request to the url you want to connect to
- request: `POST /joinNetwork`
  - body: object
    - url: (string) url of node you want to connect
```
$ curl -X POST -H "Content-Type: application/json" -d '{"url": "http://172.18.0.3:5000"}' http://localhost:5000/joinNetwork
```


- The url can be found by running the following command (get ip of containers): 
```
docker network inspect my-bridge-network
```