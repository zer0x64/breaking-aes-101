#!/usr/bin/env python3

import random
import base64
from argparse import ArgumentParser
from os import urandom

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

flag = ""
key = b""
nonce = b""

leaks = []


def main():
    global flag, leaks, key, nonce

    key = urandom(32)
    nonce = urandom(16)

    flag = gen_flag()
    leaks.append(base64.b64encode(encrypt(flag.encode('utf-8'))).decode('utf-8'))

    for _ in range(0, 64):
        leaks.append(base64.b64encode(encrypt(gen_flag().encode('utf-8'))).decode('utf-8'))


def encrypt(data):
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend()).encryptor()
    return cipher.update(data) + cipher.finalize()


def gen_flag():
    a = "0123456789abcdef"
    b = "FLAG-{"
    for _ in range(0, 32):
            b = b + random.choice(a)
    b = b + "}"
    return b


@app.route('/')
def get_index():
    return send_from_directory('website', 'index.html')


@app.route('/api/verify', methods=["POST"])
def verify_secret():
    if request.get_json().get('data') == flag:
        return "You won!"
    else:
        return "Invalid!"


@app.route('/api/leaks')
def api_get_leak():
    return jsonify(leaks)


@app.route('/<path:path>')
def get_website(path):
    return send_from_directory('website', path)


main()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-H',
                        '--host',
                        action='store',
                        dest='host',
                        default='127.0.0.1',
                        help='Host address')
    parser.add_argument('-p',
                        '--port',
                        action='store',
                        dest='port',
                        default=5000,
                        help='Host port')

    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
