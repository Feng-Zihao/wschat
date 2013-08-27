
import socket
import websocket


class ValidationError(Exception):
    pass


channels = {
    'ch1': {
        'key': 'piapiapia',
        'users': ['user1', 'user2']}}


def validate_handshake(frame):
    l = frame.split('GET')[1].split('HTTP/1.1')[0].strip()[1:]
    ch = l.split('/')[0]
    user = l.split('/')[1]
    global channels
    print ch
    print user
    print channels
    try:
        if user in channels[ch]['users']:
            return
        else:
            raise ValidationError
    except KeyError:
        raise ValidationError


def push(msg):
    pass


def error(msg):
    pass


def worker_handler(conn, addr):
    try:
        frame = websocket.get_handshake_frame(conn, addr, 4096)
        print frame
        validate_handshake(frame)
        conn.send(websocket.accept_handshake(frame))
        frame = websocket.get_data_frame(conn, addr, 4096)
        for i in range(2):
            conn.send(websocket.make_data_frame_reply(frame))
    except ValidationError:
        conn.close()
    finally:
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
#data_frame_info(open('recv.dat', 'rb').read())
