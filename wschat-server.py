
import socket
import websocket
from channel import Channel


channels = {'ch1': Channel(None)}


def validate_handshake(conn, addr, handshake_frame):
    l = handshake_frame.split('GET')[1].split('HTTP/1.1')[0].strip()[1:]
    ch = l.split('/')[0]
    user = l.split('/')[1]
    print ch, user
    global channels
    channels[ch].accept(conn, addr, user)
    print len(channels[ch].pipes)


def worker_handler(conn, addr):
    try:
        frame = websocket.get_handshake_frame(conn, addr, 4096)
        validate_handshake(conn, addr, frame)
    except:
        conn.close()


HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50000              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
while 1:
    conn, addr = s.accept()
    conn.setblocking(0)
    worker_handler(conn, addr)
