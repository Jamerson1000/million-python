import hashlib
import binascii

a = 0
b = 7

# prime modulus
p = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1

n = 115792089237316195423570985008687907852837564279074904382605163141518161494337

g = {
    'x': 55066263022277343669578718895168534326250603453777594175500187360389116729240,
    'y': 32670510020758816978083085130507043184471273380659243275938904335757337482424,
}

def double(point):
    slope = ((3 * point['x'] ** 2) * pow(2 * point['y'], -1, p)) % p

    x = (slope ** 2 - (2 * point['x'])) % p

    y = (slope * (point['x'] - x) - point['y']) % p
    return {'x': x, 'y': y}


def add(point1, point2):
    if point1 == point2:
        return double(point1)

    slope = ((point1['y'] - point2['y']) *
             pow(point1['x'] - point2['x'], -1, p)) % p

    x = (slope ** 2 - point1['x'] - point2['x']) % p

    y = ((slope * (point1['x'] - x)) - point1['y']) % p

    return {'x': x, 'y': y}


def divide(point1, point2):
    if point2['x'] is None and point2['y'] is None:
        raise ValueError("It's not possible to divide by infinity.")

    x2_inverse = pow(point2['x'], -1, p)

    return add({'x': point1['x'], 'y': point1['y']}, {'x': -point2['x'], 'y': -point2['y']})


def subtract(point1, point2):
    negated_point2 = {'x': point2['x'], 'y': -point2['y']}
    return add(point1, negated_point2)


def divideByScalar(point, scalar):
    inverse_scalar = pow(scalar, -1, n)
    return multiply(point, inverse_scalar)

def multiply(point, scalar):
    result = {'x': None, 'y': None}
    current = point

    while scalar:
        if scalar & 1: 
            if result['x'] is None:
                result = current
            else:
                result = add(result, current)

        current = double(current)
        scalar >>= 1

    return result

def hash160(public_key):
    sha256 = hashlib.sha256(binascii.unhexlify(public_key)).digest()
    
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256)
    hash160 = ripemd160.digest()
    
    return binascii.hexlify(hash160).decode()

def compare_points(point1, point2):
    if point1['y'] > point2['y']:
        return "Maior"
    elif point1['y'] < point2['y']:
        return "Menor"
    else:
        return "Igual"