import datetime
import json
import hashlib
from flask import Flask,jsonify,render_template,request
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(nonce=0, prev_hash="0",data={
            "data1":'Benyapa',
                "data2":"Thongsanga",
                "data3": "63105738"
        })
    
    def create_block(self, nonce, prev_hash, data):
        print(data)
        block = {
            "index": len(self.chain) +1,
            "timestamp": str(datetime.datetime.now()),
            "nonce": nonce,
            "previous_hash": prev_hash,
            "data" : data
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def hash(self, block):
        encode_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encode_block).hexdigest()
    
    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_proof = False
        while check_proof is False:
            hash_op = hashlib.sha256(str(new_nonce**2 - previous_nonce).encode()).hexdigest()
            if hash_op[:4] == "0000":
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce
    
    def isValid(self,chain): 
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
        
            if block['previos_hash'] != self.hash(prev_block):
                    return False
            
            prev_nonce = prev_block['nonce']
            nonce = block['nonce']
            hash_op = hashlib.sha256(str(nonce**2 - prev_nonce**2).encode()).hexdigest()
            if hash_op[:4] != "0000":
                return False
            
            prev_block = block
            block_index += 1
        return True
    
blockchain = Blockchain()


app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("home1.html")

@app.route('/get_chain', methods=["GET"])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'lenght': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/mining',methods=['POST'])
def mining_block():
    data = request.json
    prev_block = blockchain.get_previous_block()
    prev_nonce = prev_block['nonce']
    nonce = blockchain.proof_of_work(previous_nonce=prev_nonce)
    prev_hash = blockchain.hash(prev_block)
    blockchain.create_block(nonce=nonce, prev_hash=prev_hash, data=data)
    response = {
        "message": "mining complete",
        "new_block": blockchain.get_previous_block()
    }
    return jsonify(response), 200
    

if __name__== "__main__":
    app.run(debug=True)