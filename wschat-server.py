
import socket
import websocket


def worker_handler(conn, addr):
    try:
        frame = websocket.get_handshake_frame(conn, addr, 4096)
        conn.send(websocket.accept_handshake(frame))
        frame = websocket.get_data_frame(conn, addr, 4096)
        websocket.data_frame_info(frame)
        for i in range(2):
            conn.send(websocket.make_data_frame_reply(frame))
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
