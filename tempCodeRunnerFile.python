import math
import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def modular_inverse(e, phi):
    def extended_gcd(a, b):
        if b == 0:
            return (a, 1, 0)
        gcd_val, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (gcd_val, x, y)
    gcd_val, x, y = extended_gcd(e, phi)
    if gcd_val != 1:
        return None
    else:
        return x % phi

def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal.')
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    d = modular_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

def decrypt(private_key, ciphertext):
    d, n = private_key
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)

# User Input
p = int(input("Enter a prime number (p): "))
q = int(input("Enter a different prime number (q): "))
try:
    public, private = generate_keypair(p, q)
    print(f"Public Key: {public}")
    print(f"Private Key: {private}")
    message = input("Enter message to encrypt: ")
    encrypted_msg = encrypt(public, message)
    print(f"Encrypted: {encrypted_msg}")
    decrypted_msg = decrypt(private, encrypted_msg)
    print(f"Decrypted: {decrypted_msg}")
except ValueError as ve:
    print(ve)