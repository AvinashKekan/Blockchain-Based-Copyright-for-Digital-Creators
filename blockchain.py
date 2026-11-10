import hashlib
import json
from datetime import datetime

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data 
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Nayan's custom genesis block
        return Block(0, str(datetime.now()), "IP-Guard Genesis Block", "0")

    def add_new_block(self, data):
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain), str(datetime.now()), data, prev_block.hash)
        self.chain.append(new_block)

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].hash != self.chain[i].calculate_hash():
                return False
            if self.chain[i].previous_hash != self.chain[i-1].hash:
                return False
        return True