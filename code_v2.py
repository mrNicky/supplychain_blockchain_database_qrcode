import os
import qrcode
from bigchaindb_driver import BigchainDB

bdb_root_url = 'http://localhost:9984'

bdb = BigchainDB(bdb_root_url)

from bigchaindb_driver.crypto import generate_keypair
production, packaging, logistic, warehousing, retailer = generate_keypair(), generate_keypair(), generate_keypair(), generate_keypair(), generate_keypair()

metadata = {}
def creation(date, type, lot, site):
    metadata[site] = date
    type = {
            'data': {
                f"{type}": {
                    'lot': f"{lot}",
                    'site': f"{site}",
                },
            },
        }
    prepared_creation_tx = bdb.transactions.prepare(
            operation='CREATE',
            signers=production.public_key,
            asset=type,
            metadata=metadata,
            )

    fulfilled_creation_tx = bdb.transactions.fulfill(
            prepared_creation_tx, private_keys=production.private_key,)

    print(f"----- > sent over to a BigchainDB node from {site}------- ")
    sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)
    print(sent_creation_tx, "\n")
    return fulfilled_creation_tx

def transfer(etape_data, date, etape, sender, tx, first):
        metadata[etape_data] = date
        fulfilled_creation_tx = tx
        txid = fulfilled_creation_tx['id']
        creation_tx = bdb.transactions.retrieve(txid)
        output_index = 0
        output = creation_tx['outputs'][output_index]

        asset_id =  creation_tx['id'] if first==True else fulfilled_creation_tx['asset']['id']
        transfer_asset = {'id': asset_id}

        transfer_input = {
            'fulfillment': output['condition']['details'],
            'fulfills': {
                'output_index': output_index,
                'transaction_id': creation_tx['id'],
                },
            'owners_before': (output['public_keys'] if first==True else [sender.public_key]),
            }

        prepared_transfer_tx = bdb.transactions.prepare(
                operation='TRANSFER',
                asset=transfer_asset,
                inputs=transfer_input,
                recipients=etape.public_key,
                metadata=metadata,
                )
#FULFILL
        fulfilled_transfer_tx = bdb.transactions.fulfill(
                prepared_transfer_tx,
                private_keys=sender.private_key,
                )

        print(f"---------- FULFILL TO {etape_data} ---------")
        print(fulfilled_transfer_tx, "\n")
        #SEND IT
        sent_transfer_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)
        return fulfilled_transfer_tx

#Production
step1 = creation("26 octobre 2019 - 12:05", "pièce_moteur_p18", "124", "production")

#packaging
step2 = transfer("packaging", "26 octobre 2019 - 14:05", packaging, production, step1, True)

#logistic
step3 = transfer("logistic", "26 octobre 2019 - 16:05", logistic, packaging, step2, False)

#warehousing
step4 = transfer("warehousing", "26 octobre 2019 - 18:05", warehousing, logistic, step3, False)

#retailer
step5 = transfer("retailer", "26 octobre 2019 - 22:05", retailer, warehousing, step4, False)

print("METADATA OF ASSET: ", "\n", step5["metadata"], "\n")
id = step5["asset"]["id"]
print("ASSET ID : ", "\n", id)

#Create and save qrcode in your current directory (with python script)
img = qrcode.make(id)
path = os.getcwd()
img.save(f'{path}/{id}.png')
