import socket
import solitaire
import bbs
import stream_crypter
import json
import threading

HOST = '127.0.0.1'
PORT = 65432

def load_rng(path):
    f = open(path, "r")
    file = f.read()

    config = json.loads(file)

    if config['algorithm'] == 'solitaire':
        return solitaire.Solitaire(config['key'])
    else:
        return bbs.Bbs(*config['key'])

sc = stream_crypter.StreamCrypter(load_rng("config_b.json"))

def get_msg(conn):
    msg = b''

    while True:
        data = conn.recv(1024)
        if not data:
            break

        msg += data

    return msg

def send(conn, sc):
    while True:
        msg = input()
        conn.sendall(bytes(sc.encrypt(msg.encode('ascii'))))

        if msg == 'exit':
            return

def receive(conn, sc):
    while True:
        msg = conn.recv(1024)
        msg = sc.to_string(sc.decrypt(msg))
        print(msg)

        if msg == 'exit':
            return

def host():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        
        print('Listening on port', PORT)

        s.listen()
        conn, addr = s.accept()

        print('Connected by', addr)

        return conn


def join():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    return s

while True:
    cmd = input('[H]ost or [J]oin?')
    if cmd == 'h' or cmd == 'H':
        conn = host()
        break
    if cmd == 'j' or cmd == 'J':
        conn = join()
        break

send_t = threading.Thread(target=send, args=(conn, sc))
rec_t = threading.Thread(target=receive, args=(conn, sc))

send_t.start()
rec_t.start()

print('You can type in messages now. Send \'exit\' to stop (from both clients).')

send_t.join()
rec_t.join()