import socket
import threading
import json

HOST = 'localhost'
PORT = 8000

public_keys = dict()

def send_json(s, obj):
    s.sendall(json.dumps(obj).encode('ascii'))

def serve(conn, addr):
    print('Connected by', addr)

    try:
        while True:
            msg = conn.recv(1024).decode('ascii')
            cmd = json.loads(msg)
            print('Message from', addr, ':', cmd)

            if cmd['action'] == 'register':
                print('Client with id', cmd['id'], 'has registered public key', cmd['data'])
                public_keys[cmd['id']] = cmd['data']

                send_json(conn, 'ack')

            if cmd['action'] == 'get':
                print('Client with id', cmd['id'], 'fetching public key of client with id', cmd['data'])

                if cmd['data'] in public_keys:
                    send_json(conn, public_keys[cmd['data']])
                    print('Sent public key of client with id', cmd['data'], 'to client with id', cmd['id'])
                else:
                    send_json(conn, [])
                    print('Public key of client with id', cmd['data'], 'not found')

            elif cmd['action'] == 'exit':
                print('Client with id', cmd['id'], 'has disconnected')
                conn.close()

                return
    except:
        print('A client has been dropped.')
        return

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    
    print('Listening on port', PORT)

    while True:
        s.listen()
        conn, addr = s.accept()
        host, port = addr

        t = threading.Thread(target=serve, args=(conn, addr))
        t.start()
