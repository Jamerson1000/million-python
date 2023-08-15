import time
from utils import toHex
from secp256k1 import add, subtract, multiply, g
from multiprocessing import Process, Event, cpu_count

def worker( points, start, pointsPerCore, distance, stop_event):
    count = 1

    target = {
        'x': 0xa2efa402fd5268400c77c20e574ba86409ededee7c4020e4b9f0edbee53de0d4,
        'y': 0x7ba1a987013e78aef5295bf842749bdf97e25336a82458bbaba8c00d16a79ea7
    }

    base = multiply(g, start)
    stride = multiply(g, distance)

    for i in range(pointsPerCore):

        base = add(base, stride)

        p = subtract( base, target)

        if(p['x'] in points):
            i = points.index(p['x']) + 2

            pk1 = start + (count * distance) + i
            pk2 = start + (count * distance) - i

            #one key is negative and another is positive
            #one is the correct key
            print('Found', toHex(pk1))
            print('Found', toHex(pk2))
            stop_event.set()

        count+=1

def main():

    stop_event = Event()

    n_cores = cpu_count()
    print('Init', n_cores, 'cores')
    num_processes = n_cores

    start = 0x8000000000
    distance = 20_000

    pointsPerCore = 20_000

    step = 0

    point = g

    points = []


    for i in range(round(distance / 2)):
        point = add(point, g)
        points.append(point['x'])

    while not stop_event.is_set():

        processes = []

        for _ in range(num_processes):
            
            startPoint = start + (pointsPerCore * (distance * step))

            step += 1

            process = Process(target=worker, args=( points, startPoint, pointsPerCore, distance, stop_event))
            processes.append(process)

        for process in processes:
            process.start()

        for process in processes:
            process.join()


if __name__ == '__main__':
    start_time = time.time()

    main()
    
    end_time = time.time()
    execution_time_seconds = end_time - start_time

    hours = int(execution_time_seconds // 3600)
    minutes = int((execution_time_seconds % 3600) // 60)
    seconds = int(execution_time_seconds % 60)
    print(f"Total time: {hours} h, {minutes} m, {seconds} s")