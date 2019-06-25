import hashlib
import random
import string
import json
import binascii
#import numpy as np 
#import pylab as pl 
#import pandas as pd 
import logging
#import pyotp
from fstrings import f


def encode(message):
	m = hashlib.sha256(message.encode('ascii')).hexdigest()
	return m
print ("Simplicity Blockchain")
message = ("hello welcome to our blockchain")
print (message)
print(encode(message))


from time import time
import urllib3
from uuid import uuid4
from urllib3.util import parse_url
import requests


class Blockchain:
	def __init__(self):
		self.current_transaction = []
		self.chain = []
		self.nodes = set()
		#new block
		self.new_block(previous_hash='1',proof=100)

	def register_node(self, address):
		#link or ip
		parsed_url = parse_url(address)
		if parsed_url.netloc:
			self.nodes.add(parsed_url.netloc)
		elif parsed_url.path:
			self.nodes.add(parsed_url.path)
		else:
			raise ValueError('Invalid URL')
	def valid_chain(self, chain):
		last_block = chain[0]
		current_index = 1
		while current_index < len(chain):
			block = chain[current_index]
			print(f('{last_block}'))
			print(f('{block}'))
			print("\n ------ \n")
			last_block_hash = self.hash(last_block)
			if block['previous_hash'] != last_block_hash:
				return False
			# validate proof of work
			if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
				return False
			last_block = block
			current_index +=1
		return True
	def resolve_conflicts(self):
		neighbours = self.nodes
		new_chain = None
		max_length = len(self.chain)

		for node in neighbours:
			response = requests.get(f('http://{node}/chain'))
			if response.status_code == 200:
				length = response.json()['length']
				chain = response.json()['chain']
				if length > max_length and self.valid_chain(chain):
					max_length = length
					new = chain
		if new_chain:
			self.chain = new_chain
			return True
		return False
	def new_block(self, proof, previous_hash):
		
		self.current_transactions = []
		block = {
		'index' : len(self.chain) + 1,
		'timestamp' : time(),
		'transactions' : self.current_transactions,
		'proof': proof,
		'previous_hash': previous_hash or self.hash(self.chain[-1])
		}
		self.current_transactions = []
		self.chain.append(block)
		return block

	def new_transaction(self, sender, recipent, amount):
		self.current_transactions.append({
		'sender': sender,
		'recipent' : recipent,
		'amount' : amount,
		})
		return self.last_block['index'] + 1

	@property
	def last_block(self):
		return self.chain[-1]
	@staticmethod
	def hash(block):
		block_string = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()
	def proof_of_work(self, last_block):
		last_proof = last_block['proof']
		last_hash = self.hash(last_block)
		proof = 0
		while self.valid_proof(last_proof, proof, last_hash) is False:
			proof +=1
		return proof
	@staticmethod
	def valid_proof(last_proof, proof, last_hash):
		guess = f('{last_proof}{proof}{last_hash}').encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"
from flask import Flask, jsonify, request
app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()
@app.route('/mine', methods=['GET'])
def mine():
	last_block = blockchain.last_block
	proof = blockchain.proof_of_work(last_block)
	blockchain.new_transaction(
		sender="0",
		recipent=node_identifier,
		amount=1,
	)
	previous_hash = blockchain.hash(last_block)
	block = blockchain.new_block(proof, previous_hash)
	response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
	return jsonify(response), 200
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
	values = request.get_json()
	required = ['sender', 'recipient', 'amount']
	if not all(k in values for k in required):

		
		return 'Missing values', 400
	index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

	response = {'message': f('Transaction will be added to Block {index}')}
	return jsonify(response), 201
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)

