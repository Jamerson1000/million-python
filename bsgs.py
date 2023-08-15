import time
from utils import toHex
from secp256k1 import add, subtract, multiply, g

count = 1

run = True

distance = 10_000

start = 0x8000000000

target = {
    'x': 0xa2efa402fd5268400c77c20e574ba86409ededee7c4020e4b9f0edbee53de0d4,
    'y': 0x7ba1a987013e78aef5295bf842749bdf97e25336a82458bbaba8c00d16a79ea7
}

base = multiply(g, start)
stride = multiply(g, distance)

point = g

points = []

start_time = time.time()

print('creating points...')

for i in range(round(distance / 2)):
    point = add(point, g)
    points.append(point['x'])

print('searching...')

while(run):

    base = add(base, stride)

    p = subtract( base, target)

    if(p['x'] in points):
        i = points.index(p['x']) + 2

        pk = start + (count * distance) + i
        print('Found', toHex(pk))
        run = False

    count+=1

end_time = time.time()
execution_time_seconds = end_time - start_time

hours = int(execution_time_seconds // 3600)
minutes = int((execution_time_seconds % 3600) // 60)
seconds = int(execution_time_seconds % 60)
print(f"Total time: {hours} h, {minutes} m, {seconds} s")