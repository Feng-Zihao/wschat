
import socket


class HandshakeError(Exception):
    pass


def validate_handshake_frame(handshake_frame):
    return handshake_frame.endswith('\r\n\r\n')


def accept_handshake(handshake_frame):
    pass


def get_handshake_frame(conn, addr, length=4096):
    frame = ''
    while not validate_handshake_frame(frame):
        data = conn.recv(length)
        if not data:
            raise HandshakeError
        frame += data
    return frame


def worker_handler(conn, addr):
    try:
        frame = get_handshake_frame(conn, addr, 2)
        print frame
    finally:
        conn.close()


HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50000              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
while 1:
    conn, addr = s.accept()
    worker_handler(conn, addr)
