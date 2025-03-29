import datetime
import hashlib
import json
import flask import Flask, jsonify

#Parte 1 , create Blockchain

class Blockchain:
    def __init__(self):
        self.chain=[]
        self.create_block(proof = 1, previous_hash='0')