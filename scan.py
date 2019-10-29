import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from time import gmtime, strftime

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

d = [None]
while True:
    _, frame = cap.read()

    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        d.append(obj.data)
        break
    if len(d) > 1:
        break
       
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    
    if key == 27:
        break

#BigChainDB query instead of mongoDB
from bigchaindb_driver import BigchainDB
bdb_root_url = 'http://localhost:9984'
bdb = BigchainDB(bdb_root_url)
creation_tx = bdb.transactions.get(asset_id=d[1])
track = creation_tx[-1]["metadata"]
print(track)

