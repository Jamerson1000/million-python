import time
from utils import toHex
from secp256k1 import add, subtract, multiply, g
from multiprocessing import Process, Event, cpu_count, Queue, Array
# import cProfile

def worker( points, start, target, stride, pointsPerCore, stop_event, result_queue):
    count = 1

    base = multiply(g, start)

    for i in range(pointsPerCore):
        base = add(base, stride)

        p = subtract( base, target)

        if p['x'] in points:
            result_queue.put([count, p['x'], start])
            stop_event.set()
            break
            

        count+=1

def main():
    start_time = time.time()

    stop_event = Event()
    result_queue = Queue()

    n_cores = cpu_count() - 7
    print('Init', n_cores, 'cores')
    num_processes = n_cores

    start = 0x40000000000000
    distance = 10_000_000
    pointsSize = round(distance / 2)

    pointsPerCore = 1_000_000

    stride = multiply(g, distance)

    step = 0

    point = g

    points1 = []

    # target = {
    #     'x': 0x6ecabd2d22fdb737be21975ce9a694e108eb94f3649c586cc7461c8abf5da71a,
    #     'y': 0xaa9a8c19d3626939f8f87d0c00c130d76a332fa99fda533bdf449a67407d11b6
    # }

    target = multiply(g, 0x6abe1f9b67e114)

    for i in range(pointsSize):
        point = add(point, g)
        points1.append(point['x'])

    end_time = time.time()
    execution_time_seconds = end_time - start_time

    hours = int(execution_time_seconds // 3600)
    minutes = int((execution_time_seconds % 3600) // 60)
    seconds = int(execution_time_seconds % 60)
    print(f"Creation points time: {hours} h, {minutes} m, {seconds} s")

    points = set(points1)

    search_time = time.time()

    while not stop_event.is_set():

        k = start + (pointsPerCore * (distance * step))

        print(toHex(k))

        processes = []

        for _ in range(num_processes):
            
            startPoint = start + (pointsPerCore * (distance * step))

            step += 1

            process = Process(target=worker, args=( points, startPoint, target, stride, pointsPerCore, stop_event, result_queue))
            processes.append(process)

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        if not result_queue.empty():
            result = result_queue.get()
            count = result[0]
            x = result[1]
            s = result[2]

            i = points1.index(x) + 2

            pk1 = s + (count * distance) + i
            pk2 = s + (count * distance) - i

            print('Found', toHex(pk1))
            print('Found', toHex(pk2))

            stop_event.set()

            for process in processes:
                process.terminate()

    end_time = time.time()
    execution_time_seconds = end_time - search_time

    hours = int(execution_time_seconds // 3600)
    minutes = int((execution_time_seconds % 3600) // 60)
    seconds = int(execution_time_seconds % 60)
    print(f"Search time: {hours} h, {minutes} m, {seconds} s")

    end_time = time.time()
    execution_time_seconds = end_time - start_time

    hours = int(execution_time_seconds // 3600)
    minutes = int((execution_time_seconds % 3600) // 60)
    seconds = int(execution_time_seconds % 60)
    print(f"Total time: {hours} h, {minutes} m, {seconds} s")


if __name__ == '__main__':
    # profiler = cProfile.Profile()
    # profiler.enable()

    main()

    # profiler.disable()
    # profiler.print_stats(sort='cumulative')