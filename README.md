# supplychain_blockchain_database_qrcode
SupplyChain database with blockchain steroids


### Set up BigChainDB (client)
- pip3 install bigchaindb-driver
- pip3 install --upgrade setuptools
- sudo apt-get update
- sudo apt-get install python3-dev libssl-dev libffi-dev
http://docs.bigchaindb.com/projects/py-driver/en/latest/quickstart.html

### Set up BigChainDB and RUN docker container (server)
https://docs.bigchaindb.com/projects/server/en/latest/appendices/all-in-one-bigchaindb.html

### Run script 
```python3 code.py```

### Create and SCAN QRCODE

Install all python packages from requirements.txt 

```python3 -m pip install -r requirements.txt```

When you run script, qrcode will be created (png format) with an asset id description

Run scan.py to scan your qrcode with```python3 scan.py``` 
Webcam will automatically closed if qr code scan successfully and all metadata from asset id blockchain database will printed in your terminal.
 
