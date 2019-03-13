#!/usr/bin/env python3

import base64
from argparse import ArgumentParser
from os import urandom

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from flask import Flask, request, send_from_directory

app = Flask(__name__)

key = b""


def main():
    global key
    key = urandom(16)


def decrypt(data):
    cipher = Cipher(algorithms.AES(key), modes.CBC(key), backend=default_backend()).decryptor()
    data = cipher.update(data) + cipher.finalize()
    padder = padding.PKCS7(128).unpadder()
    return padder.update(data) + padder.finalize()


@app.route('/')
def get_index():
    return send_from_directory('website', 'index.html')


@app.route('/api/decrypt', methods=["POST"])
def post_decrypt():
    return base64.b64encode(decrypt(base64.b64decode(request.get_json().get('data').encode('utf-8'))))


@app.route('/api/verify', methods=["POST"])
def verify_key():
    if base64.b64decode(request.get_json().get('key')) == key:
        return "You won!"
    else:
        return "Invalid!"


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
