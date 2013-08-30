import re
import sha
import base64
import struct
import socket


class HandshakeError(Exception):
    pass


class DataFrameError(Exception):
    pass


def validate_handshake_frame(handshake_frame):
    return handshake_frame.startswith('GET') and handshake_frame.endswith('\r\n\r\n')


def validate_data_frame(data_frame):
    try:
        return len(data_frame) >= payload_length(data_frame) + payload_data_start(data_frame)
    except:
        return False


def accept_handshake(handshake_frame):
    MAGIC_UUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    accept_handshake_tmpl = ('HTTP/1.1 101 Switching Protocols\r\n' +
        'Upgrade: websocket\r\n' +
        'Connection: Upgrade\r\n' +
        'Sec-WebSocket-Accept: {accept_token}\r\n' +
        '\r\n')
    key = re.findall('Sec-WebSocket-Key: [0-9a-zA-Z/=+]+\r\n', handshake_frame)[0].split(':')[1].strip()
    key += MAGIC_UUID
    accept_token = base64.standard_b64encode(sha.new(key).digest())
    return accept_handshake_tmpl.format(accept_token=accept_token)


def get_handshake_frame(conn, addr, length=4096):
    frame = ''
    while not validate_handshake_frame(frame):
        data = conn.recv(length)
        frame += data
    return frame


def get_data_frame(conn, length=4096):
    frame = ''
    while not validate_data_frame(frame):
        data = conn.recv(length)
        frame += data
    return frame


def reply(reply_data):
    frame = '\x81' + '\x05' + 'hello'
    return bytes(frame)


def mask_key(data_frame):
    if ord(data_frame[1]) & 0x80 == 0:
        return None
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
    if mask_key(data_frame) is not None:
        return start + 4
    return start


def is_final_frame(data_frame):
    return ord(data_frame[0]) & 0x80 != 0


def payload_data(data_frame):
    mask = mask_key(data_frame)
    start = payload_data_start(data_frame)
    data = bytearray(data_frame[start:start + payload_length(data_frame)])
    if mask is not None:
        for i in range(len(data)):
            data[i] = chr(ord(chr(data[i])) ^ ord(mask[i % 4]))
    return bytes(data)


## for debug only
def data_frame_info(data_frame):
    print payload_length(data_frame)
    print payload_data_start(data_frame)
    print len(data_frame)
    print is_final_frame(data_frame)
    if mask_key(data_frame) is not None:
        print mask_key(data_frame).encode('hex')
        print len(mask_key(data_frame))
    else:
        print 'unmasked'
    print str(payload_data(data_frame))
