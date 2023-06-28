import time
from multiprocessing import Process
import socket

def f(x):
    sock = socket.socket()
    sock.connect(('localhost', 9090))

    for i in range(10):
        time.sleep(1)
        result = str(i*x)
        sock.send(result.encode())
        data = sock.recv(1024)
        print(data)
        if not data:
            continue
    conn.close()

if __name__ == '__main__':
    p = Process(target=f, args=(2,))
    p.start()
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(2)
    conn, addr = sock.accept()

    while True:
        data = conn.recv(1024)
        print(data.decode(),  ' ')
        conn.send(b'ok')
        if not data:
            break

    conn.close()
    p.join()

