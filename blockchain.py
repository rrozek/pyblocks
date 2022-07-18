import json
import time
import typing

from block import Block


class Blockchain:
    pow_difficulty = 2
    blockchain_persistance = "blockchain.txt"

    def __init__(self):
        self.pending_data = []
        self.chain = []
        try:
            self.load_chain()
        except FileNotFoundError:
            self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
        self.store_block(genesis_block)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, block: Block, proof: str) -> bool:
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_pow_valid(block, proof):
            return False
        block.hash = proof
        print(f"add_block: {block.height} hash: {block.hash}")
        self.chain.append(block)
        self.store_block(block)
        return True

    def consensus_pow(self, block: Block) -> str:
        block.nonce = 0
        computed_hash = block.calculate_hash()
        while not computed_hash.startswith("0" * Blockchain.pow_difficulty):
            block.nonce += 1
            computed_hash = block.calculate_hash()
            if block.nonce % 1000 == 0:
                print(f"calculated {block.nonce} PoW for block {block.height} without success")
        return computed_hash

    def is_pow_valid(self, block: Block, block_hash: str) -> bool:
        return block_hash.startswith("0" * Blockchain.pow_difficulty) and block_hash == block.calculate_hash()

    def mine_block(self) -> int:
        if not self.pending_data:
            print("nothing to mine. don`t waste enerty")
            return False

        print(f"mine new block")
        last_block = self.last_block

        new_block = Block(
            height=last_block.height + 1, data=self.pending_data, timestamp=time.time(), previous_hash=last_block.hash
        )

        proof = self.consensus_pow(new_block)
        self.add_block(new_block, proof)
        self.pending_data = []

        return new_block.height

    def add_data(self, new_data: typing.Any):
        print(f"add_data: {new_data}")
        self.pending_data.append(new_data)

    def load_chain(self):
        with open(Blockchain.blockchain_persistance, "r") as chainfile:
            blocks = chainfile.readlines()
            for blockdata in blocks:
                blockdict = json.loads(blockdata)
                chainblock = Block(**{key: value for key, value in blockdict.items() if key != "hash"})
                chainblock.hash = blockdict["hash"]
                if chainblock.height == 0 or self.is_pow_valid(chainblock, chainblock.hash):
                    self.chain.append(chainblock)
                else:
                    raise Exception("corrupt data in chain file")

    def store_block(self, block: Block):
        with open(Blockchain.blockchain_persistance, "a") as chainfile:
            chainfile.write(json.dumps(block.as_dict()))
            chainfile.write("\n")
