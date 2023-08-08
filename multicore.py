import time
from utils import getArray, getStartPoints, toHex
from secp256k1 import add, subtract, multiply, double, g, hash160
from multiprocessing import Process, Event

def worker(startPoints, pows, target, stop_event):


    startPoint = multiply(g, startPoints[0])

    if startPoint['y'] % 2 == 0:
        prefix = "02"
    else:
        prefix = "03"

    hash = hash160(prefix + toHex(startPoint['x']))

    if(hash == target):
        print('Found!')
        print(prefix + toHex(startPoint['x']))
        stop_event.set()
    
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
            stop_event.set()
            break
    

def main():
    target = "d39c4704664e1deb76c9331e637564c257d68a08"

    KEY_SIZE = 30
    ONES = 16
    DISTANCE_POINTS = 100

    num_processes = 10

    stop_event = Event()

    pows = [g]

    _1 = g

    # init a array of pows of points
    for i in range(KEY_SIZE - 1):
        _1 = double(_1)
        pows.append(_1)

    startKey = getArray(KEY_SIZE - ONES, ONES)

    start_time = time.time()

    while not stop_event.is_set():  # Continue as long as stop_event is not set

        processes = []

        for _ in range(num_processes):
            startPoints = getStartPoints(startKey, KEY_SIZE, DISTANCE_POINTS)

            process = Process(target=worker, args=(startPoints, pows, target, stop_event))
            processes.append(process)

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        if stop_event.is_set():
            for process in processes:
                process.terminate()

    end_time = time.time()
    execution_time_seconds = end_time - start_time

    hours = int(execution_time_seconds // 3600)
    minutes = int((execution_time_seconds % 3600) // 60)
    seconds = int(execution_time_seconds % 60)

    print(f"Time: {hours} h, {minutes} m, {seconds} s")

if __name__ == '__main__':
    main()