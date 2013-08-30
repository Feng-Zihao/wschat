
import socket
import websocket
from channel import Channel


channels = {'ch1': Channel(None)}


def join_channel(conn, addr, handshake_frame):
    l = handshake_frame.split('GET')[1].split('HTTP/1.1')[0].strip()[1:]
    ch = l.split('/')[0]
    global channels
    channels[ch].accept(conn, addr, handshake_frame)


def worker_handler(conn, addr):
    try:
        frame = websocket.get_handshake_frame(conn, addr, 4096)
        join_channel(conn, addr, frame)
    except:
        conn.close()


HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50000              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
while 1:
    conn, addr = s.accept()
    worker_handler(conn, addr)
