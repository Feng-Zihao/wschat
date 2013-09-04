

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


def get_epoch_milliseconds():
    return int(math.floor(time.time() * 1000))


class Channel(object):

    def __init__(self, encrypted_key=None):
        self.encrypted_key = encrypted_key
        self.pipes = {}  # dict of {conn: [addr, user, last-time]}
        self.msgs = []   # list of {'time': , 'user', 'text'}

    def _add_msg(self, msg_entity):
        m = msg_entity.copy()
        m['time'] = get_epoch_milliseconds()
        self.msgs.append(m)

    def _push_tunnel(self, conn):
        try:
            while True:
                last_time = self.pipes[conn][2]
                for msg in filter(lambda m: m['time'] > last_time, self.msgs):
                    conn.send(websocket.reply(json.dumps(msg)))
                    self.pipes[conn][2] = msg['time']
        except (KeyError, socket.error):
            pass
        finally:
            self._close_tunnel(conn)

    def _recv_tunnel(self, conn):
        try:
            user = self.pipes[conn][1]
            while True:
                data = websocket.get_data_frame(conn)
                if data[0] == '\x08' or data[0] == '\x88':
                    return
                else:
                    data = websocket.payload_data(data)
                    self._add_msg({'user': user, 'text': data})
        except (KeyError, socket.error):
            pass
        finally:
            self._close_tunnel(conn)

    def _close_tunnel(self, conn):
        try:
            user = self.pipes.pop(conn)[1]
            self._add_msg({'user': 'system', 'text': str(user) + ' offline'})
            conn.close()
        except KeyError:
            pass

    def accept(self, conn, addr, handshake_frame):
        l = handshake_frame.split('GET')[1].split('HTTP/1.1')[0].strip()[1:]
        user = l.split('/')[1]
        #if not user.startswith('user'):
        #    raise AccessDeniedError
        try:
            self.pipes[conn] = [addr, user, get_epoch_milliseconds()]
            conn.send(websocket.accept_handshake(handshake_frame))

            self._add_msg({'user': 'system', 'text': str(user) + ' online'})

            recv_thread = threading.Thread(target=self._recv_tunnel, args=(conn,))
            recv_thread.daemon = True
            recv_thread.start()

            push_thread = threading.Thread(target=self._push_tunnel, args=(conn,))
            push_thread.daemon = True
            push_thread.start()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=10, file=sys.stdout)
            self._close_tunnel(conn)
