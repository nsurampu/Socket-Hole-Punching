import argparse, socket


def startup():
    node_list = [('127.0.0.1',7474), ('127.0.0.1',9897), ('127.0.0.1',1833)]

    i = 0
    for nodex in node_list:
        try:
            if(i == 0):
                print("try if"+ str(i))
                pseudo_server(nodex[0],nodex[1])
                break
            else:
                print("try else "+ str(i))
                node(nodex[0],nodex[1],node_list[0][1])
                break
        except BaseException as e:
            print("excepting"+ str(i))
            print(e)
            i += 1
            continue

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data

def pseudo_server(interface, port):
    list_node = []
    sock_list = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())
    while True:
        print('Waiting to accept a new connection')
        sc, sockname = sock.accept()
        sock_list.append(sc)
        # list_node.append(sc.getpeername())
        # print(sock_list)
        print('We have accepted a connection from', sockname)
        print('  Socket name:', sc.getsockname())
        print('  Socket peer:', sc.getpeername())

        message = recvall(sc, 16)
        print(' Incomming request from node:', repr(message))
        sc.sendall(b'Farewell, node')
        # sc.close()
        # print('  Reply sent, socket closed')

def node(host,in_port, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, in_port))
    sock.connect((host, port))
    print('Node has been assigned socket name', sock.getsockname())
    sock.sendall(b'Hello pseudo_server')
    reply = recvall(sock, 19)
    print('Message from a electoral pseudo_server: ', repr(reply))
    # sock.close()
    while True:
        if (input() == "exit"):
            break
        continue

if __name__ == '__main__':
    startup()
