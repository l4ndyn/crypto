#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: <YOUR NAME>
SUNet: <SUNet ID>

Replace this with a description of the program.
"""
import utils
import math

# Caesar Cipher

period = ord('Z') - ord('A') + 1
uppercase_offset = ord('A')
lowercase_offset = ord('a')

def shift_by(char, num):
    offset = lowercase_offset if char.islower() else uppercase_offset
    return chr((ord(char) - offset + num) % period + offset)

def encrypt_caesar(plaintext):
    return ''.join([shift_by(c, 3) if c.isalpha() else c for c in plaintext])

def decrypt_caesar(ciphertext):
    return ''.join([shift_by(c, -3) if c.isalpha() else c for c in ciphertext])


# Vigenere Cipher

def letter_value(letter):
    return ord(letter) - lowercase_offset if letter.islower() else ord(letter) - uppercase_offset

def check_keyword(keyword):
    if len(keyword) == 0:
            raise utils.Error('The keyword can\'t be empty!')
    if not keyword.isalpha():
        raise utils.Error('The keyword may only contain letters!')

def encrypt_vigenere(plaintext, keyword):
    check_keyword(keyword)

    return ''.join([shift_by(c, letter_value(keyword[i % len(keyword)]))
        if c.isalpha() else c for (i, c) in enumerate(plaintext)])

def decrypt_vigenere(ciphertext, keyword):
    check_keyword(keyword)

    return ''.join([shift_by(c, -letter_value(keyword[i % len(keyword)]))
        if c.isalpha() else c for (i, c) in enumerate(ciphertext)])


# Scytale Cipher

def check_circumference(circumference):
    if circumference != int(circumference):
        raise utils.Error('The circumference must be an integer!')
    if circumference <= 0:
        raise utils.Error('The circumference must greater than zero!')

def encrypt_scytale(plaintext, circumference):
    check_circumference(circumference)

    return ''.join([''.join([plaintext[i * circumference + offset] 
        for i in range(math.ceil((len(plaintext) - offset) / circumference))])
        for offset in range(circumference)])

def decrypt_scytale(ciphertext, circumference):
    check_circumference(circumference)

    return encrypt_scytale(ciphertext, math.ceil(len(ciphertext) / circumference))


# Railfence Cipher

def stride(size):
        if size == 1:
            return 1
        return 2 * (size - 1)

def encrypt_railfence(plaintext, circumference):
    check_circumference(circumference)

    cipher = ''
    
    for offset in range(circumference):
        i = offset
        use_lower_stride = (offset != circumference - 1)

        while i < len(plaintext):
            cipher += plaintext[i]

            i += stride(circumference - offset) if use_lower_stride else stride(offset + 1)
            if offset != 0 and offset != circumference - 1:
                use_lower_stride = not use_lower_stride

    return cipher

def decrypt_railfence(ciphertext, circumference):
    check_circumference(circumference)

    plaintext = [0] * len(ciphertext)
    cipher_i = 0

    for offset in range(circumference):
        text_i = offset
        use_lower_stride = (offset != circumference - 1)

        while text_i < len(ciphertext):
            plaintext[text_i] = ciphertext[cipher_i]
            text_i += stride(circumference - offset) if use_lower_stride else stride(offset + 1)

            if offset != 0 and offset != circumference - 1:
                use_lower_stride = not use_lower_stride

            cipher_i += 1

    return ''.join(plaintext)

# Merkle-Hellman Knapsack Cryptosystem

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    raise NotImplementedError  # Your implementation here

def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    raise NotImplementedError  # Your implementation here


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    raise NotImplementedError  # Your implementation here

def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    raise NotImplementedError  # Your implementation here

