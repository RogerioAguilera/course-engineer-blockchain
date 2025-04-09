import datetime
import hashlib
import json
from flask import Flask, jsonify
import requests
from uuid import uuid4
from urllib.parse import urlparse

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash} 

        self.transactions=[]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # A operação de hash deve ser consistente com a validação em is_chain_valid
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        # Garante que o dicionário esteja ordenado para hashes consistentes
        encoded_block = json.dumps(block, sort_keys=True).encode() # Correção 4: Typo corrigido
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # Verifica se o hash do bloco anterior corresponde ao previous_hash do bloco atual
            if block['previous_hash'] != self.hash(previous_block):
                return False
            # Verifica se a prova de trabalho é válida
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest() # Correção 5: Lógica/Typo corrigido
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

# Parte 2: Minerar a Blockchain (Aplicação Web com Flask)
# Correção 2: Mover a configuração do Flask para fora da classe

# Criar a Aplicação Web
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False # Opcional: desabilita a formatação "bonita"

# Criar uma instância da Blockchain
blockchain = Blockchain()

# Rota para minerar um novo bloco
@app.route('/mine_block', methods=['GET']) # Correção 8: Adicionar '/'
def mine_block():
    # Obter o último bloco e sua prova
    previous_block_dict = blockchain.get_previous_block() # Correção 6: Manter o dict do bloco anterior
    previous_proof = previous_block_dict['proof']

    # Encontrar a nova prova
    proof = blockchain.proof_of_work(previous_proof)

    # Obter o hash do bloco anterior
    previous_hash = blockchain.hash(previous_block_dict) # Correção 6: Calcular hash do dict

    # Criar o novo bloco
    block = blockchain.create_block(proof, previous_hash)

    # Preparar a resposta
    response = {'message': 'Parabéns, você minerou um bloco!',
                'index': block['index'], # Correção 7: Usar string como chave
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# Rota para obter a chain completa
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Rota para verificar a validade da chain
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'Tudo certo. O Blockchain é válido.'}
    else:
        response = {'message': 'Houston, temos um problema. O Blockchain não é válido.'}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)