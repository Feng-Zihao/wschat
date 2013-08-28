

import websocket

class AccessDeniedError(Exception):
    pass


class Channel(object):

    def __init__(self, encrypted_key=None):
        self.encrypted_key = encrypted_key
        self.pipes = []  # list of (conn, user, user)

    def push(self):
        pass

    def recv(self):
        pass

    def accept(self, conn, addr, user):
        if user.startswith('user'):
            self.pipes.append((conn, addr, user))
            conn.send(websocket.accept_handshake(frame))
            for i in range(2):
                conn.send(websocket.make_data_frame_reply(frame))
        else:
            raise AccessDeniedError

