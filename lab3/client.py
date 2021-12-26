import socket
import json
import merkle_hellman as mh
import utils
import solitaire
import stream_crypter

KS_HOST = 'localhost'
KS_PORT = 8000

HOST = 'localhost'
PORT = 8001

def make_socket(port = 0):
    """
    Open a socket on the specified port. If no port is specified, an arbirtary free one is used.
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if port != 0:
        s.bind((HOST, port))

    return s

def send_json(s, obj):
    print('Sending raw object:', obj)
    s.sendall(json.dumps(obj).encode('ascii'))

def send_mh(s, msg, pk):
    """
    Send a string `msg` through socket `s`, encrypted using Merkle-Hellman using the public key `pk`.
    """
    
    msg = [ord(c) for c in msg]
    send_json(s, mh.encrypt_mh(msg, pk))

def rec_mh(s, sk):
    """
    Receive a string through socket `s`, encrypted using Merkle-Hellman. It is decrypted using the private (secret) key `sk`.
    """

    msg = json.loads(s.recv(4096).decode('ascii'))
    return "".join([chr(i) for i in mh.decrypt_mh(msg, sk)])

def connect_ks():
    """
    Open a socket and connect it to the key server.
    """
    
    s = make_socket()
    s.connect((KS_HOST, KS_PORT))

    return s

def register_pub_key(s, pk):
    """
    Register the public key `pk` to the key server that can be accessed through the socket `s`.
    """

    cmd = {'action': 'register', 'data': pk, 'id': PORT}
    send_json(s, cmd)

    #wait for ack
    s.recv(1024)

def get_pub_key(s, id):
    """
    Get the public key of client with id `id` from the key server that can be accessed through the socket `s`.
    """

    cmd = {'action': 'get', 'data': id, 'id': PORT}
    
    print('Getting the other client\'s public key...')

    #repeatedly try fetching the public key until a non-empty response is received
    while True:
        send_json(s, cmd)

        pk = json.loads(s.recv(1024).decode('ascii'))
        if len(pk) != 0:
            print('Getting public key successful.\n')
            return pk

def disconnect_ks(s):
    """
    Disconnect from the key server that can be accessed through the socket `s`. The socket is then closed.
    """

    cmd = {'action': 'exit', 'id': PORT}
    send_json(s, cmd)
    s.close()

def key_exchange(s, id, start = True):
    """
    Exchange public keys with another client (with id of `id`) accessible through socket `s`.
    """

    def compare_msg(msg, expected_msg):
        if msg == expected_msg:
            print('Key exchange complete.\n')
            return True
        else:
            print('Key exchange failed.')
            return False

    other_pk = get_pub_key(key_server, id)
    
    if start:
        send_mh(s, 'hello', other_pk)
        #wait for ack
        ack = rec_mh(s, sk)

        if compare_msg(ack, 'ack'):
            return other_pk
    else:
        #wait for hello
        hello = rec_mh(s, sk)

        if compare_msg(hello, 'hello'):
            send_mh(s, 'ack', other_pk)
            return other_pk

    return None

def common_secret(s, other_pk, start=True):
    """
    Establish a common secret with another client accessible through socket `s`, with public key `other_pk`.
    """

    if start:
        #generate the swaps to shuffle the first half of the deck and send it
        first_half = utils.shuffle_sequence(0, 54 // 2, 54)
        send_mh(s, json.dumps(first_half), other_pk)

        #receive the swaps to shuffle the second half of the deck
        second_half = json.loads(rec_mh(s, sk))
    else:
        #receive the swaps to shuffle the first half of the deck
        first_half = json.loads(rec_mh(s, sk))

        #generate the swaps to shuffle the second half of the deck and send it
        second_half = utils.shuffle_sequence(54 // 2, 54, 54)
        send_mh(s, json.dumps(second_half), other_pk)

    #combine the swaps and shuffle the deck using them
    sequence = first_half + second_half

    print('\nAcquired sequence of swaps:', sequence)

    deck = list(range(1, 55))

    for i, j in sequence:
        deck[i], deck[j] = deck[j], deck[i]

    print('Established common secret. Deck after applying swaps:', deck, '\n')

    return deck

def solitaire_chat(deck, s, start = True):
    sol = solitaire.Solitaire(deck)
    sc = stream_crypter.StreamCrypter(sol)

    print('Communication has started. You can type in messages now. Send \'exit\' to stop (from both clients).')

    if start:
        msg = input('Type in your message:')
        s.sendall(bytes(sc.encrypt(msg.encode('ascii'))))

    while True:
        print('Waiting for message...')

        #receive a message
        msg = s.recv(1024)
        msg = sc.to_string(sc.decrypt(msg))
        print('New message:', msg)

        #send a message
        msg = input('Type in your message:')
        s.sendall(bytes(sc.encrypt(msg.encode('ascii'))))

        if msg == 'exit':
            return

def start():
    print('Starting communication. My id is', PORT)

    while True:
        try:
            id = int(input('Specify the id of the recipient:'))
            
            if id <= 0:
                print('The id must be a positive number!')
                continue
            break
        except:
            print('The id must be a number!')
            pass

    s = make_socket(PORT)
    s.connect((HOST, id))
    
    print('Connection established. Starting key exchange.\n')

    other_pk = key_exchange(s, id, True)
    if other_pk == None:
        return

    print('\nEstablishing common secret...')
    deck = common_secret(s, other_pk, True)

    solitaire_chat(deck, s, True)

def respond():
    s = make_socket(PORT)

    print('Responding to communication, my id is', PORT)
    print('Waiting for connection...\n')

    s.listen()
    conn, addr = s.accept()
    _, id = addr
    
    print('Connection established with client', id, ', starting key exchange.\n')

    other_pk = key_exchange(conn, id, False)
    if other_pk == None:
        return

    print('\nEstablishing common secret...')
    deck = common_secret(conn, other_pk, False)

    solitaire_chat(deck, conn, False)


key_server = connect_ks()

sk = mh.generate_private_key()
pk = mh.generate_public_key(sk)

register_pub_key(key_server, pk)
print('Successfully registered public key.\n')

while True:
    cmd = input('[S]tart the communication or wait for one to [R]espond to?')
    if cmd == 's' or cmd == 'S':
        start()
        break
    if cmd == 'r' or cmd == 'R':
        respond()
        break

disconnect_ks(key_server)