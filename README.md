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
docker run --rm -p 5000:5000 -v $(pwd)/src:/shared dotcoin flask --app dotcoin.py --debug run
```

Type `ctrl-c` to stop the server. 