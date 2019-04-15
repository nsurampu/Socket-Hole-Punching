import socket
import framing
import ast
import time
CODING_FORMAT = 'utf-8'
framing_funcs = framing.Framing()
server_addr = ('139.59.61.2',110)

def make_peer_sock(address):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect(address)
    to_bind = sock.getsockname()
    other_addr_str = framing_funcs.get_block(sock)
    other_addr_str = other_addr_str.decode(CODING_FORMAT)
    print("PEER Address = ",other_addr_str)
    sock.close()
    ## Processing other address
    other_sock = ast.literal_eval(other_addr_str)
    addr = other_sock[0]
    port = other_sock[1]

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(to_bind)
    sock.connect((addr,port))
    
    return sock


if __name__ == "__main__":
    sock = make_peer_sock(server_addr)
    #handle_connection(sock, 0.1)
    while True:
        framing_funcs.put_block(sock,b"Test")
        time.sleep(1)
        data = framing_funcs.get_block(sock)
        print(data)
