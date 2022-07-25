import unittest
from block import Block
from blockchain import Blockchain


class TestBlock(unittest.TestCase):
    def test_block(self):
        blk1 = Block(1, [1, 2, 3], 12345678, "0", Blockchain.pow_difficulty, 0)
        blk1_hash = blk1.calculate_hash()
        blk1_hash2 = blk1.calculate_hash()

        self.assertEqual(blk1_hash, blk1_hash2)

        blk1_copy = Block(1, [1, 2, 3], 12345678, "0", Blockchain.pow_difficulty, 0)
        blk1_copy_hash = blk1_copy.calculate_hash()

        self.assertEqual(blk1_hash, blk1_copy_hash)

        blk1_tampered = Block(1, [1, 2, 4], 12345678, "0", Blockchain.pow_difficulty, 0)
        blk1_tampered_hash = blk1_tampered.calculate_hash()

        self.assertNotEqual(blk1_hash, blk1_tampered_hash)


class TestBlockchain(unittest.TestCase):
    def test_blockchain(self):
        Blockchain.pow_difficulty = 1
        Blockchain.blockchain_persistance = ""

        blockchain = Blockchain()
        print(blockchain.chain)
        self.assertEqual(1, len(blockchain.chain))

        blockchain.add_data([1, 2, 3])
        blockchain.mine_block()
        self.assertEqual(2, len(blockchain.chain))
        self.assertEqual(blockchain.last_block.previous_hash, blockchain.prelast_block.hash)
