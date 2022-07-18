from blockchain import Blockchain

block_data = [
    "some sort of significant data",
    {"complex": {"object": "with children"}},
    ["more", "data", "whatsoever", 1, 2, 3],
    "last block",
]

if __name__ == "__main__":
    print(f"initializing blockchain...")
    blockchain = Blockchain()
    for data in block_data:
        blockchain.add_data(data)
        blockchain.mine_block()
        print(
            f"last_block: {blockchain.last_block.height} "
            f"hash: {blockchain.last_block.hash} "
            f"data: {blockchain.last_block.data}"
        )
