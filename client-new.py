#All this thing does is send stuff to ls

import socket as mysoc
import threading
import sys


def loadfile(filename):
    with open(filename) as file_in:
        lines = []
        for line in file_in:
            lines.append(line.rstrip())
    return lines


# Client function that connects to the RS and TS DNS servers to
# identify the ipaddress of a given hostname.
def client():

    # Create the Sockets
    tsBinded = False
    try:
        ls = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print(err + "\n socket open error ")

    # Define the port on which you want to connect to the server
    port = int(sys.argv[2])
    sa_sameas_myaddr = mysoc.gethostbyname(sys.argv[1])

    # connect to the ls here
    server_binding = (sa_sameas_myaddr, port)
    ls.connect(server_binding)

    # Initialize/prepare the I/O files
    file = loadfile("PROJI-HNS.txt")
    outputFile = open("RESOLVED.txt", "w")

    for query in file:
        # Send query to the server
        ls.send(query.encode("utf-8"))
        print("[C]: Message sent to server: " + query)

        # Recieve a response from Root Server
        data = ls.recv(100).decode("utf-8")
        print("[S]: Message from Root Server: " + data)
        split = data.split()

        # This is if the RS server does not have the hostname, it will have to connect with the TS server
        if split[2] == "NS" and tsBinded == False:
            port = int(sys.argv[3])
            ts_add = mysoc.gethostbyname(split[0])
            ts_binding = (ts_add, port)
            ts.connect(ts_binding)
            tsBinded = True
        # at this point server is bound to client (now to receive and send messages)

        # Procedure to send query to Top-Level Server if NS flag is seen
        if split[2] == "NS":
            ts.send(query.encode("utf-8"))
            data = ts.recv(100).decode("utf-8")
            if data == "Error:HOST NOT FOUND":
                outputFile.write(query + " - " + data + "\n")
            else:
                outputFile.write(data + "\n")
            print("[S]: Message from Top-Level Server: " + data)
        else:
            outputFile.write(data + "\n")

        print

    rs.send("/End".encode("UTF-8"))
    ts.send("/End".encode("UTF-8"))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage:\tpython client.py <rsHostname> <rsListenPort> <tsListenPort>")
        print("Ex:\tpython client.py localhost 8080 15002")
        print("\tpython client.py 179.123.13.4 5023 1002")
    else:
        t2 = threading.Thread(name="client", target=client)
        t2.start()

