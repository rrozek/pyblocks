# pyblocks
minimal implementation of blockchain.  
For consensus algorithm it uses very simple string comparison of initial zeros in block hash.  
To find valid hash we're only updating nonce hoping it won't overflow python max integer.  
`example_blockchain.txt` shows how changing difficulty from 2 to 6 increases required amount of hash calculations exponentailly.

