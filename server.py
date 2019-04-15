import select
import socket
import framing

CODING_FORMAT = 'utf-8'
count = 0
framing_funcs = framing.Framing()

def round_robin_events(poll_obj):
    while True:
        for fd, event in poll_obj.poll():
            yield fd, event

def handle_connections(listener):
    fd_to_sock_dict = {listener.fileno() : listener}
    fd_to_addr_dict = {}

    poll_obj = select.poll()
    poll_obj.register(listener, select.POLLIN)

    for fd, event in round_robin_events(poll_obj):
        sock = fd_to_sock_dict[fd]

        if sock is listener:
            inc_sock, address = sock.accept()
            print('Accepted connection from {}'.format(address))
            inc_sock.setblocking(False)
            fd_to_sock_dict[inc_sock.fileno()] = inc_sock
            fd_to_addr_dict[inc_sock.fileno()] = address
            ## inc_sock.send("HI".encode(CODING_FORMAT))
            poll_obj.register(inc_sock, select.POLLOUT)
            if len(fd_to_addr_dict.keys()) == 2:
                fds = list(fd_to_addr_dict.keys())
                sock_to_send = fd_to_sock_dict[fds[0]]
                addr_to_send = str(fd_to_addr_dict[fds[1]]).encode(CODING_FORMAT)
                framing_funcs.put_block(sock_to_send,addr_to_send)
                sock_to_send.close()
                sock_to_send = fd_to_sock_dict[fds[1]]
                addr_to_send = str(fd_to_addr_dict[fds[0]]).encode(CODING_FORMAT)
                framing_funcs.put_block(sock_to_send,addr_to_send)
                sock_to_send.close()

        elif event & (select.POLLERR | select.POLLHUP | select.POLLNVAL):
            addr = fd_to_addr_dict.pop(fd)
            print("Closing connection with {}".format(addr))
            ## Some code I do not understand
            poll_obj.unregister(fd)
            del fd_to_sock_dict[fd]

        elif event & select.POLLIN:
            data = framing_funcs.get_block(sock)
            if not data:
                sock.close()
                continue
           
            print("Recieved {} from {}".format(
                    data.decode(CODING_FORMAT), str(fd_to_addr_dict[fd])
                ))
           

def get_listener_socket(address):
    """Build and return a listening server socket."""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(64)
    print('Listening at {}'.format(address))
    return listener


if __name__ == "__main__":
    listener = get_listener_socket(('0.0.0.0',15000))
    handle_connections(listener)
