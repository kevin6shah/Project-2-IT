import socket as mysoc
import threading
import sys
import time

# Top-Level Server Procedure
def server():
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print(err + "\n socket open error ")

    # Bind and Listen
    server_binding = ("", int(sys.argv[1]))
    ss.bind(server_binding)
    ss.listen(1)
    host = mysoc.gethostname()

    print("[S]: Server host name is: " + host)
    localhost_ip = mysoc.gethostbyname(host)
    print("[S]: Server IP address is  " + localhost_ip)

    # Accept Connections
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at" + str(addr))

    #
    #CLIENT PART : CONNECTING TO TS's
    #
    # Create the Sockets to the TS
    try:
        ts1 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        ts2 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print(err + "\n socket open error ")

    # Define the port on which you want to connect to the server
    port_ts1 = int(sys.argv[3])
    port_ts2 = int(sys.argv[5])

    sa_sameas_myaddr_ts1 = mysoc.gethostbyname(sys.argv[2])
    sa_sameas_myaddr_ts2 = mysoc.gethostbyname(sys.argv[4])


    # bind to the ls here
    server_binding_ts1 = (sa_sameas_myaddr_ts1, port_ts1)
    server_binding_ts2 = (sa_sameas_myaddr_ts2, port_ts2)

    #connect to both
    ts1.connect(server_binding_ts1)
    ts2.connect(server_binding_ts2)
    ts1.settimeout(5)
    ts2.settimeout(5)

    while True:
        # Message recieved from Client
        query = csockid.recv(200).decode("utf-8").lower()
        if query == "/end":
            break
        print ("[S]: Query from Client: " + query)

        ts1.send(query.encode('utf-8'))
        ts2.send(query.encode('utf-8'))
        

    # Close the server socket
    ss.close()
    exit()


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage:\tpython ls.py <lsListenPort> <ts1 Hostname> <ts1 ListenPort> <ts2 Hostname> <ts2 ListenPort>")
        print("Ex:\tpython ls.py 8080 localhost 8090 localhost 9090")
    else:
        t1 = threading.Thread(name="server", target=server)
        t1.start()
