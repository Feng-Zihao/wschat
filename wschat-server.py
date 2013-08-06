
import socket
import re
import sha
import base64
import struct


class HandshakeError(Exception):
    pass


class DataFrameError(Exception):
    pass


def validate_handshake_frame(handshake_frame):
    return handshake_frame.startswith('GET') and handshake_frame.endswith('\r\n\r\n')


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


def get_data_frame(conn, addr, length=4096):
    frame = ''
    while len(frame) > 2 and payload_length(frame) + payload_data_start(frame) < len(frame):
        data = conn.recv(length)
        if not data:
            raise DataFrameError
        frame += data
    if payload_length(frame) + payload_data_start(frame) != len(frame):
        raise DataFrameError
    return frame


def make_data_frame_reply(reply_data):
    frame = '0x7'


def mask_key(data_frame):
    if ord(data_frame[1]) & 0x80 == 0:
        return
    plen = ord(data_frame[1]) & 0x7f
    if plen < 126:
        return bytes(data_frame[2:6])
    if plen == 126:
        return bytes(data_frame[4:8])
    if plen == 127:
        return bytes(data_frame[10:14])


def payload_length(data_frame):
    plen = ord(data_frame[1]) & 0x7f
    if plen < 126:
        return plen
    if plen == 126:
        return struct.unpack('>H', data_frame[2:4].encode('hex'))
    if plen == 127:
        return struct.unpack('>Q', data_frame[2:10].encode('hex'))


def payload_data_start(data_frame):
    plen = ord(data_frame[1]) & 0x7f
    if plen < 126:
        start = 2
    if plen == 126:
        start = 4
    if plen == 127:
        start = 10
    if mask_key:
        return start + 4
    return start


def is_final_frame(data_frame):
    return ord(data_frame[1]) & 0x80 != 0


def payload_data(data_frame):
    mask = mask_key(data_frame)
    start = payload_data_start(data_frame)
    data = bytearray(data_frame[start:start + payload_length(data_frame)])
    for i in range(len(data)):
        data[i] = chr(ord(chr(data[i])) ^ ord(mask[i % 4]))
    return bytes(data)


## for debug only
def data_frame_info(data_frame):
    print payload_length(data_frame)
    print payload_data_start(data_frame)
    print len(data_frame)
    print is_final_frame(data_frame)
    print mask_key(data_frame).encode('hex')
    print len(mask_key(data_frame))
    payload_data(data_frame)


def worker_handler(conn, addr):
    try:
        frame = get_handshake_frame(conn, addr, 4096)
        conn.send(accept_handshake(frame))
        frame = get_data_frame(conn, addr, 4096)
        print str(payload_data(frame))
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
#data_frame_info(open('recv.dat', 'rb').read())
