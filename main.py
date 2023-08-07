import sys
argumentos = sys.argv

from utils import getArray, getStartPoints, toHex
from secp256k1 import add, subtract, multiply, double, g, hash160

target = 'd39c4704664e1deb76c9331e637564c257d68a08'

KEY_SIZE = 66
ONES = 33

# this is the number of powers that will be calculated for point addition.
# It will be used for parallel searches in the future.
DISTANCE_POINTS = 100

# init pows with point G
pows = [g]

_1 = g

# init a array of pows of points
for i in range(KEY_SIZE - 1):
    _1 = double(_1)
    pows.append(_1)

# get start key in array off bits
startKey = getArray(KEY_SIZE - ONES, ONES)

# search a public key that will be generate a hash160 of target
while(True):
    startPoints = getStartPoints(startKey, KEY_SIZE, DISTANCE_POINTS)

    startPoint = multiply(g, startPoints[0])

    if startPoint['y'] % 2 == 0:
        prefix = "02"
    else:
        prefix = "03"

    hash = hash160(prefix + toHex(startPoint['x']))
        
    if(hash == target):
        print('Found!')
        print(prefix + toHex(startPoint['x']))
        break
    
    found = False

    for i in range(len(startPoints[1])):
        p = startPoints[1][i]

        startPoint = add(startPoint, pows[p[0]])

        if(p[1] > 0):
            startPoint = add(startPoint, pows[p[1]])
            startPoint = subtract(startPoint, g)

        if startPoint['y'] % 2 == 0:
            prefix = "02"
        else:
            prefix = "03"
        hash = hash160(prefix + toHex(startPoint['x']))
        
        if(hash == target):
            print('Found!')
            print(prefix + toHex(startPoint['x']))
            break