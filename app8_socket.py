"""
Socket client and server 
test redirect client to socket 
"""
from socket import *
import datetime, time
import sys
import _thread
import select


def server_simple(host='127.0.0.1', port=50008):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    while True:
        conn,addr = sock.accept()
        print(f'new connection :{addr}')
        while True:
            data = conn.recv(1024)
            msg = data.decode()
            if not data: 
                break 
            print(f'received : {msg}')
            echo_byte = f'{datetime.datetime.now()} server received : "{msg}"'.encode()
            conn.send(echo_byte)
        conn.close()
        print ('connection closed')

def server_select(host='127.0.0.1', port=50008):
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((host,port))
    server.listen(5)
    inputs,outputs,[] = [server],[],[]
    q=[] # messages 
    clients=[] # array of connections 
    running = True
    def run():
        while running:
            readable, writable, exp = select.select(inputs, outputs, [])
            for s in readable:
                if s is server:
                    conn,addr = s.accept()
                    #conn.setblocking(0)
                    print(f'[{datetime.datetime.now()}] new connection: {addr}')
                    inputs.append(conn)
                    clients.append(conn)
                    outputs.append(conn)
                else:
                    try:
                        data_byte = s.recv(1024)
                        #client disconnected
                        if not data_byte:
                            inputs.remove(s)
                            clients.remove(s)
                            outputs.remove(s)
                            s.close()
                        else:
                            msg = data_byte.decode()
                            print(f'[{datetime.datetime.now()}] received: from client - {msg}')
                            q.append(msg)
                    except:
                        inputs.remove(s)
                        clients.remove(s)
                        outputs.remove(s)

            # broadcasting message to all socket connections
            while len(q) > 0:
                msg = q.pop(0)
                for w in writable:
                    w.send(('[Broadcast From server]: '+msg).encode())
                
    _thread.start_new_thread(run,())

    while True:
        print("Server started. press q to exit")
        if(input() == 'q'):
            running = False
            break

def server_epoll(host='127.0.0.1', port=50008):
    """
        Referenced from http://scotdoyle.com/python-epoll-howto.html
    """
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversocket.bind((host, port))
    serversocket.listen(1)
    serversocket.setblocking(0)

    ep = select.epoll() # not available on windows
    ep.register(serversocket.fileno(), select.EPOLLIN)

    try:
        connections = {}
        requests = {}
        responses = {}
        while True:
            events = ep.poll(1)
            for fileno, event in events:
                if fileno == serversocket.fileno(): # new connection
                    print ('New connection.')
                    try:
                        while True:
                            connection, address = serversocket.accept()
                            connection.setblocking(0)
                            ep.register(connection.fileno(), select.EPOLLIN | select.EPOLLET)
                            connections[connection.fileno()] = connection
                            requests[connection.fileno()] = b''
                            responses[connection.fileno()] = f'server time: {time.time()}'.encode()
                    except :
                        pass
                elif event & select.EPOLLIN: # read client input
                    try:
                        while True:
                            requests[fileno] += connections[fileno].recv(1024)
                    except :
                        pass
                    ep.modify(fileno, select.EPOLLOUT | select.EPOLLET)
                    print(f'Received : {requests[fileno].decode()}')
                elif event & select.EPOLLOUT: # write output to client
                    try:
                        while len(responses[fileno]) > 0:
                            byteswritten = connections[fileno].send(responses[fileno])
                            responses[fileno] = responses[fileno][byteswritten:]
                    except :
                        pass
                    if len(responses[fileno]) == 0:
                        ep.modify(fileno, select.EPOLLET)
                        connections[fileno].shutdown(SHUT_RDWR)
                    print('Shutdown client connection')
                elif event & select.EPOLLHUP: # close connection
                    ep.unregister(fileno)
                    connections[fileno].close()
                    del connections[fileno]
                    print('Deleted client connection')
    finally:
        ep.unregister(serversocket.fileno())
        ep.close()
        serversocket.close()

def client_simple(msg, host='127.0.0.1', port=50008):
    sock = socket(AF_INET, SOCK_STREAM)
    conn = sock.connect((host,port))
    byte_arr = msg.encode(encoding='utf-8')
    sock.send(byte_arr)
    buff = sock.recv(1024)
    print(f'Client received: "{buff.decode()}"')
    sock.close()
    print ("connection closed")

def client_keyboard(host='127.0.0.1', port=50008):
    sock = socket(AF_INET, SOCK_STREAM)
    conn = sock.connect((host,port))
    def listen_server():
        try:
            while True:
                try:
                    buff = sock.recv(1024)
                    print(f'Client received: "{buff.decode()}"')
                except:
                    print("server disconnected")
                    break
        except:
            print('error!')

    _thread.start_new_thread(listen_server, ())

    def listen_keyboard():
        while True:
            print('key in message :')
            msg = input()
            if msg.lower() == 'q':
                break
            
            byte_arr = msg.encode(encoding='utf-8')
            sock.send(byte_arr)
    listen_keyboard()

    sock.close()
    print ("connection closed")



def run_simple(mode):
    if mode ==1 :
        server_simple()
    elif mode == 2:
        msg = input('key in message :')
        client_simple(msg)
    elif mode == 3:
        server_select()
    elif mode == 4:
        server_epoll()
    elif mode ==5:
        client_keyboard()

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ['1','2','3','4', '5']:
        print('invalid arguments !')
        exit()

    run_simple(int(sys.argv[1]))