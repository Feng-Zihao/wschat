

import websocket
import threading
import sys
import traceback
import socket
import json
import math
import time


class AccessDeniedError(Exception):
    pass


def get_epoch_miliseconds():
    return int(math.floor(time.time() * 1000))


class Channel(object):

    def __init__(self, encrypted_key=None):
        self.encrypted_key = encrypted_key
        self.pipes = {}  # dict of {conn: [addr, user, last-time]}
        self.msgs = []   # list of (time, data)

    def push_tunnel(self, conn):
        try:
            while True:
                last_time = self.pipes[conn][2]
                for msg in filter(lambda m: m[0] > last_time, self.msgs):
                    conn.send(websocket.reply(str(msg[0]) + msg[1]))
                    self.pipes[conn][2] = msg[0]
        except (KeyError, socket.error):
            pass
        finally:
            self._close_tunnel(conn)

    def recv_tunnel(self, conn):
        try:
            while True:
                data = websocket.get_data_frame(conn)
                if data[0] == '\x08' or data[0] == '\x88':
                    return
                else:
                    data = websocket.payload_data(data)
                    self.msgs.append((get_epoch_miliseconds(), data))
        except (KeyError, socket.error):
            pass
        finally:
            self._close_tunnel(conn)

    def accept(self, conn, addr, handshake_frame):
        l = handshake_frame.split('GET')[1].split('HTTP/1.1')[0].strip()[1:]
        user = l.split('/')[1]
        if not user.startswith('user'):
            raise AccessDeniedError
        try:
            self.pipes[conn] = [addr, user, get_epoch_miliseconds()]
            conn.send(websocket.accept_handshake(handshake_frame))

            self.msgs.append((get_epoch_miliseconds(), str(user) + ' online'))

            recv_thread = threading.Thread(target=self.recv_tunnel, args=(conn,))
            recv_thread.daemon = True
            recv_thread.start()

            push_thread = threading.Thread(target=self.push_tunnel, args=(conn,))
            push_thread.daemon = True
            push_thread.start()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=10, file=sys.stdout)
            self._close_tunnel(conn)

    def _close_tunnel(self, conn):
        try:
            user = self.pipes[conn][1]
            self.msgs.append((get_epoch_miliseconds(), str(user) + ' offline'))
            conn.close()
            self.pipes.pop(conn)
        except KeyError:
            pass
