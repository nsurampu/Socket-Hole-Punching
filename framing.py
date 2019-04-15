import socket, struct
from argparse import ArgumentParser

class Framing:

    def __init__(self):
        # Using struct for network with packet size of 8
        self.HEADER = struct.Struct("!Q")

    def put_block(self, sock, message):
        block_length = len(message)
        sock.send(self.HEADER.pack(block_length))
        sock.send(message)

    def recvall(self, sock, length):
        blocks = []
        while length:
            block = sock.recv(length)
            if not block:
                raise EOFError("EOF Error")
            length -= len(block)
            blocks.append(block)
        return b''.join(blocks)

    def get_block(self, sock):
        data = self.recvall(sock, self.HEADER.size)
        (block_length,) = self.HEADER.unpack(data)
        return self.recvall(sock, block_length)

    def send_framed(self, sc, message):
        ## sock.shutdown(socket.SHUT_RD)
        self.put_block(sc, message)
        self.put_block(sc, b'')
        ## sock.close()

    def recv_framed(self, sc):
        # sock.listen(1)
        # print('Listening at', sock.getsockname())
        # sc, sockname = sock.accept()
        # print('Accepted connection from', sockname)
        # sc.shutdown(socket.SHUT_WR)
        while True:
            block = self.get_block(sc)
            if not block:
                break


"""
FOR TESTING
framing = Framing()

def server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    framing.recv_framed(sock)

def client(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    framing.send_framed(sock, b'Hello')

if __name__ == '__main__':
    parser = ArgumentParser(description='Transmit & receive blocks over TCP')
    parser.add_argument('hostname', nargs='?', default='127.0.0.1',
                         help='IP address or hostname (default: %(default)s)')
    parser.add_argument('-c', action='store_true', help='run as the client')
    parser.add_argument('-p', type=int, metavar='port', default=1060,
                         help='TCP port number (default: %(default)s)')
    args = parser.parse_args()
    function = client if args.c else server
    function((args.hostname, args.p))
    """
