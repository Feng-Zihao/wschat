

import websocket
import threading
import sys
import traceback
import socket


class AccessDeniedError(Exception):
    pass


class Channel(object):

    def __init__(self, encrypted_key=None):
        self.encrypted_key = encrypted_key
        self.pipes = {}  # dict of {conn: [addr, user, seq]}
        self.msgs = []  # list of (seq, data)

    def push_tunnel(self, conn):
        try:
            while True:
                seq = self.pipes[conn][2]
                for msg in filter(lambda m: m[0] > seq, self.msgs):
                    conn.send(websocket.reply(str(msg[0]) + msg[1]))
                    self.pipes[conn][2] = msg[0]
        except (KeyError, socket.error):
            pass
        finally:
            self.close_tunnel(conn)

    def recv_tunnel(self, conn):
        try:
            while True:
                data = websocket.get_data_frame(conn)
                if data[0] == '\x08' or data[0] == '\x88':
                    return
                else:
                    data = websocket.payload_data(data)
                    print len(self.msgs), data
                    self.msgs.append((len(self.msgs) + 1, data))
        except (KeyError, socket.error):
            pass
        finally:
            self.close_tunnel(conn)

    def close_tunnel(self, conn):
        try:
            conn.close()
            addr = self.pipes[conn][0]
            self.pipes.pop(conn)
            self.msgs.append((len(self.msgs), str(addr) + 'offline'))
        except KeyError:
            pass

    def accept(self, conn, addr, handshake_frame):
        l = handshake_frame.split('GET')[1].split('HTTP/1.1')[0].strip()[1:]
        user = l.split('/')[1]
        if not user.startswith('user'):
            raise AccessDeniedError
        try:
            self.pipes[conn] = [addr, user, len(self.msgs)]
            conn.send(websocket.accept_handshake(handshake_frame))
            self.msgs.append((len(self.msgs), str(addr) + ' log in'))
            recv_thread = threading.Thread(target=self.recv_tunnel, args=(conn,))
            recv_thread.daemon = True
            recv_thread.start()
            push_thread = threading.Thread(target=self.push_tunnel, args=(conn,))
            push_thread.daemon = True
            push_thread.start()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=10, file=sys.stdout)
