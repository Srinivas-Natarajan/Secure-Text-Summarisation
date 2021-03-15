# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 06:19:02 2020

@author: nsrin
"""
import collections
import hashlib
import random
import binascii
import sys
from Crypto.Cipher import AES
import Padding



def enc_long(n):            #Encoding large number to a sequence of bytes
    s = ""
    while n > 0:
        s = chr(n & 0xFF) + s
        n >>= 8             #Shifting 8bits i.e. 1 byte
    return s


############################################################# Padding for Data

BLOCK_SIZE = 16  # Bytes                      (128 bits per block)
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

##############################################################################


def encrypt(plaintext,key, mode):
	encobj = AES.new(key,mode)             #256-bit
	return(encobj.encrypt(plaintext))

def decrypt(ciphertext,key, mode):
	encobj = AES.new(key,mode)
	return(encobj.decrypt(ciphertext))


EllipticCurve = collections.namedtuple('EllipticCurve', 'name p a b g n h')         #Defining the curve

curve = EllipticCurve(                          
    'secp256k1',
    # Field characteristic.
    p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    # Curve coefficients.
    a=0,
    b=7,
    # Base point.
    g=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
       0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    # Subgroup order.
    n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    # Subgroup cofactor.
    h=1,
)

############################  y^2 = x^3 +ax + b is the curve used


########################################################### Modular arithmetic 

def inverse_mod(k, p):                                                          
    """Returns the inverse of k modulo p.
    This function returns the only integer x such that (x * k) % p == 1.
    k must be non-zero and p must be a prime.
    """
    if k == 0:
        raise ZeroDivisionError('Division by zero')

    if k < 0:
        # k ** -1 = p - (-k) ** -1  (mod p)
        return p - inverse_mod(-k, p)

    # Extended Euclidean algorithm.
    s, prev_s = 0, 1
    t, prev_t = 1, 0
    r, prev_r = p, k

    while r != 0:
        quo = prev_r // r
        prev_r, r = r, prev_r - quo * r
        prev_s, s = s, prev_s - quo * s
        prev_t, t = t, prev_t - quo * t

    gcd, x, y = prev_r, prev_s, prev_t

    assert gcd == 1
    assert (k * x) % p == 1

    return x % p


 ########################################## Functions that work on curve points

def is_on_curve(point):
    """Returns True if the given point lies on the elliptic curve."""
    if point is None:
        # None represents the point at infinity.
        return True

    x, y = point

    return (y * y - x * x * x - curve.a * x - curve.b) % curve.p == 0


def point_neg(point):                              #Mirror image allong x axis
    """Returns -point."""
    assert is_on_curve(point)                   #Should be a point on the curve to continue

    if point is None:
        # -0 = 0
        return None

    x, y = point
    result = (x, -y % curve.p)

    assert is_on_curve(result)                  #Result should lie on the curve as well

    return result


def point_add(point_a, point_b):
    """Returns the result of point_a + point_b according to the group law."""
    assert is_on_curve(point_a)
    assert is_on_curve(point_b)

    if point_a is None:                      # 0 + point_b = point_b
        return point_b
    if point_b is None:                      # point_a + 0 = point_a
        return point_a

    x1, y1 = point_a
    x2, y2 = point_b

    if x1 == x2 and y1 != y2:              # point_a + (-point_a) = 0
        return None

    if x1 == x2:                            #  point_a == point_b.
        m = (3 * x1 * x1 + curve.a) * inverse_mod(2 * y1, curve.p)
    else:
        # This is the case point_a != point_b.
        m = (y1 - y2) * inverse_mod(x1 - x2, curve.p)

    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)
    result = (x3 % curve.p,
              -y3 % curve.p)

    assert is_on_curve(result)

    return result


def scalar_mult(k, point):
    """Returns k * point computed using the double and point_add algorithm."""
    assert is_on_curve(point)

    if k % curve.n == 0 or point is None:
        return None

    if k < 0:
        # k * point = -k * (-point)
        return scalar_mult(-k, point_neg(point))

    result = None
    addend = point

    while k:
        if k & 1:
            # Add.
            result = point_add(result, addend)

        # Double.
        addend = point_add(addend, addend)

        k >>= 1

    assert is_on_curve(result)

    return result


################################################ # Keypair generation and ECIES

def make_keypair():
    """Generates a random private-public key pair."""
    private_key = random.randrange(1, curve.n)              #Generate Random Key
    public_key = scalar_mult(private_key, curve.g)          #Make Public key

    return private_key, public_key

"""                     (Still not complete)
def verify_signature(public_key, message, signature):
    z = hash_message(message)

    r, s = signature

    w = inverse_mod(s, curve.n)                 #Creating the field on which we operate
    u1 = (z * w) % curve.n
    u2 = (r * w) % curve.n

    x, y = point_add(scalar_mult(u1, curve.g),
                     scalar_mult(u2, public_key))

    if (r % curve.n) == (x % curve.n):
        return 'signature matches'
    else:
        return 'invalid signature'
"""


################################################################## Test Code

message="Hello"
if (len(sys.argv)>1):
	message=str(sys.argv[1])


dA, Qa = make_keypair()
print("Private key:", hex(dA))                      #Making keys
print(("Public key: (0x{:x}, 0x{:x})".format(*Qa)))


print("\n\n=========================")

r = random.randint(0, 2**128)                      # Random initialisation

rG = scalar_mult(r,curve.g)
S = scalar_mult(r,Qa)

print("Random value: " , r)
print("rG: " , rG)

print("\n\n======Symmetric key========")

print("Encryption key:",str(S[0]))

key = hashlib.sha256(str(S[0]).encode()).digest()

message = Padding.appendPadding(message,blocksize=Padding.AES_blocksize,mode=0)

ciphertext = encrypt(message.encode(),key,AES.MODE_ECB)


print("Encrypted:\t",binascii.hexlify(ciphertext))


Snew = scalar_mult(dA,rG)
key = hashlib.sha256(str(Snew[0]).encode()).digest()

text = decrypt(ciphertext,key,AES.MODE_ECB)


print("Decrypted:\t",Padding.removePadding(text.decode(),mode=0))