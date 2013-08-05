
import socket
import re
import sha
import base64

class HandshakeError(Exception):
    pass


class DataFrameError(Exception):
    pass


def validate_handshake_frame(handshake_frame):
    return handshake_frame.endswith('\r\n\r\n')


def accept_handshake(handshake_frame):
    MAGIC_UUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    accept_handshake_tmpl = ('HTTP/1.1 101 Switching Protocols\r\n' +
           'Upgrade: websocket\r\n' +
           'Connection: Upgrade\r\n' +
           'Sec-WebSocket-Accept: {accept_token}\r\n' +
           '\r\n\r\n')
    print handshake_frame
    key = re.findall('Sec-WebSocket-Key: [0-9a-zA-Z/=+]+\r\n', handshake_frame)[0].split(':')[1].strip()
    key += MAGIC_UUID
    accept_token = base64.standard_b64encode(sha.new(key).digest())
    return accept_handshake_tmpl.format(accept_token=accept_token)


def get_handshake_frame(conn, addr, length=4096):
    frame = ''
    while not validate_handshake_frame(frame):
        data = conn.recv(length)
        if not data:
            raise HandshakeError
        frame += data
    return frame


def get_mask_key(data_frame):
    pass


def get_payload_length(data_frame):
    if ord(data_frame[1]) < 126:
        return ord(data_frame[1])


def get_payload_data_start(data_frame):
    pass


def validate_data_frame(data_frame):
    pass


def worker_handler(conn, addr):
    try:
        frame = get_handshake_frame(conn, addr, 4096)
        conn.send(accept_handshake(frame))
    finally:
        conn.close()



#HOST = ''                 # Symbolic name meaning all available interfaces
#PORT = 50000              # Arbitrary non-privileged port
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((HOST, PORT))
#s.listen(1)
#while 1:
#    conn, addr = s.accept()
#    worker_handler(conn, addr)

with open('recv.dat', 'rb') as f:
    data_frame = f.read()
    print get_payload_length(data_frame)
