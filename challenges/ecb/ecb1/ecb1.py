#!/usr/bin/env python3

import base64
import urllib
from argparse import ArgumentParser
from os import urandom

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from flask import Flask, request, send_from_directory

app = Flask(__name__)

secret = ""
key = b""


def main():
    global key
    key = urandom(32)


def encrypt(data):
    padder = padding.PKCS7(128).padder()
    data = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend()).encryptor()
    return cipher.update(data) + cipher.finalize()


def decrypt(data):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend()).decryptor()
    data = cipher.update(data) + cipher.finalize()
    padder = padding.PKCS7(128).unpadder()
    return padder.update(data) + padder.finalize()


@app.route('/')
def get_index():
    return send_from_directory('website', 'index.html')


@app.route('/api/encrypt', methods=["POST"])
def post_encrypt():
    username = request.get_json().get('username')
    data = ("username=" + username + "&is_admin=false").encode('utf-8')
    return base64.b64encode(encrypt(data))


@app.route('/api/verify', methods=["POST"])
def verify_token():
    try:
        token = request.get_json().get('token')
        token = decrypt(base64.b64decode(token.encode('utf-8'))).decode('utf-8')
        token = urllib.parse.parse_qs(token)
        if len(token.get('is_admin')) == 1 and token.get('is_admin')[0] == "true":
                return "You won!"
        else:
            return "This token is not admin!"
    except:
        return "Your token is invalid!"


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
