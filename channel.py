

import websocket
import thread
import sys
import traceback


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
                for msg in filter(lambda m: m[1] > seq, self.msgs):
                    conn.send(websocket.reply(msg[1]))
                    self.pipes[conn][2] = msg[1]
        finally:
            try:
                conn.close()
            except:
                pass

    def recv_tunnel(self, conn):
        try:
            while True:
                self.msgs.append((len(self.msgs), websocket.get_data_frame(conn)))
        finally:
            try:
                conn.close()
            except:
                pass

    def accept(self, conn, addr, handshake_frame):
        l = handshake_frame.split('GET')[1].split('HTTP/1.1')[0].strip()[1:]
        user = l.split('/')[1]
        if not user.startswith('user'):
            raise AccessDeniedError
        try:
            self.pipes[conn] = [addr, user, 0]
            conn.send(websocket.accept_handshake(handshake_frame))
            self.msgs.append((len(self.msgs), str(addr) + ' log in'))
            thread.start_new_thread(self.recv_tunnel, (conn,))
            thread.start_new_thread(self.push_tunnel, (conn,))
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=10, file=sys.stdout)
