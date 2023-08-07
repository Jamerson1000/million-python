import math

def getDistance(numero):
    potencia_de_dois = 1
    expoente = 0

    while potencia_de_dois * 2 <= numero:
        potencia_de_dois *= 2
        expoente += 1

    e = int(math.log2(potencia_de_dois))
    s = numero - potencia_de_dois

    return e, s

def getArray(zeros, uns):
    # All keys start with 1 to define the range limit.
    string = '1'
    array = list(string)

    while len(array) < (zeros + uns):
        if array.count("0") < zeros:
            array.append("0")
        elif array.count("1") < uns:
            array.append("1")

    return array

def getStartPoints(startKey, key_size, distance_points):

    run = True
    count_distance = 0
    pows_added = 0

    keys = []
    pows = []

    firstKey = int(''.join(startKey), 2)

    lastKey = int(''.join(startKey), 2)

    while run:
        count_distance += 1

        i = key_size - 2
        while i >= 0 and startKey[i] >= startKey[i + 1]:
            i -= 1

        if i < 0:
            break

        j = key_size - 1
        while j > i and startKey[j] <= startKey[i]:
            j -= 1

        temp = startKey[i]
        startKey[i] = startKey[j]
        startKey[j] = temp

        left = i + 1
        right = key_size - 1
        while left < right:
            temp = startKey[left]
            startKey[left] = startKey[right]
            startKey[right] = temp
            left += 1
            right -= 1

        key = int(''.join(startKey), 2)

        res = key - lastKey

        lastKey = key

        if distance_points == count_distance - 1:

            keys.append(key)

            count_results += 1
            count_distance = 0
        else:
            result = getDistance(res)

            e = result[0]
            s = result[1]

            if s > 0:
                s += 1

                s = int(getDistance(s)[0])

                pows.append([e, s])
            else:
                pows.append([e,0])

            pows_added += 1

        if pows_added == distance_points:
            run = False

    return firstKey, pows

def toHex(value):
    return format(value, '064x')

def toBinary(hexadecimal):
    decimal = int(hexadecimal, 16)
    binario = bin(decimal)
    return binario[2:] 

def toDecimal(hex):
    return int(hex, 16)
    