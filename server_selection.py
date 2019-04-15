import socket
import time
import hashlib

class Distributed_Elect:

    def __init__():
        CURRENT_LEADER = None
        PING = "PING!"
        ELECT_REQ = "ELEQ!"
        NODE_LIST = ['127.0.0.1:7474', '127.0.0.1:9897', '127.0.0.1:1833']

    def first_run(self):
        #Contain the list of nodes and its hashes.
        hash_list = list()
        for node in self.NODE_LIST:
            hash_list.append(tuple(node,hashlib.md5(node.encode('ascii')))
        hash_list.sort(key=lambda x: x[1])
        i = 0
        for node in hash_list:
            sel = i % len(self.NODE_LIST)
            real_node = hash_list[0][sel]
            if node == real_node:
                continue
            received_conf = self.inform_server(real_node, node)
            if received_conf:
                self.CURRENT_LEADER = real_node
                break
            else:
                i = i + 1
                continue

    def inform_server(self, real_node, node):
        #self.PING him that he is the server you need. (But not the one you deserve)
        #self.PING him on a different port maybe? (Use TCP)
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(node)
        sock.connect(real_node)
        sock.sendall(self.PING_pack)
        sock.shutdown(socket.SHUT_RD)

        return True

    def server_creation(self):
        #if I currently am the server, then process the request, else pass it to the real server.
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.listen(len(self.NODE_LIST)-1)
        num_of_informs = 0
        prev_leader = self.CURRENT_LEADER
        potential_nodes = [node for node in self.NODE_LIST if node != self.CURRENT_LEADER]
        potential_leader = potential_nodes[random.randint(len(potential_nodes))]

        for node in self.NODE_LIST:
            sock.connect(node)
            sock.sendall(self.ELECT_REQ)
            self.server_election(node, potential_leader)

        while True:
            incoming = sock.recv_until(sock, b'!')
            if incoming == self.PING:
                num_of_informs = num_of_informs + 1
                acceptance = self.server_acceptance(len(self.NODE_LIST), num_of_informs)
                if acceptance:
                    self.CURRENT_LEADER = potential_leader
                else:
                    self.CURRENT_LEADER = prev_leader
            for node in self.NODE_LIST:
                sock.connect(node)
                sock.sendall(self.CURRENT_LEADER)

    def server_election(self, some_node, leader_eleq):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(some_node)
        sock.connect(leader_eleq)
        message = sock.recv_until(sock, b'!')
        if message = self.ELECT_REQ:
            sock.sendall(self.PING)

    def handle_server_conversation(self, sock, address):
        """Converse with a client over `sock` until they are done talking."""
        try:
            while True:
                self.handle_sever_request(sock)
        except EOFError:
            print('Client socket to {} has closed'.format(address))
        except Exception as e:
            print('Client {} error: {}'.format(address, e))
        finally:
            sock.close()

    def handle_server_request(self, sock):
        """Receive a single client request on `sock` and send the answer."""
        incoming = recv_until(sock, b'.')
        sock.sendall("OKAY.")

    def server_acceptance(self, total_nodes,num_of_informs):
        if(num_of_informs > total_nodes/2):
            return True
        else:
            return False
