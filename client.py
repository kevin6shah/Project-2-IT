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
    file = loadfile("PROJ2-HNS.txt")
    outputFile = open("RESOLVED.txt", "w")

    for query in file:
        # Send query to the server
        ls.send(query.encode("utf-8"))
        print("[C]: Message sent to server: " + query)

        # Recieve a response from Load Server
        data = ls.recv(100).decode("utf-8")
        print ("[S]: Message from Load Server: " + data)
        outputFile.write(data + '\n')

        print

    ls.send("/end".encode("UTF-8"))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:\tpython client.py <ls Hostname> <ls ListenPort>")
        print("Ex:\tpython client.py localhost 8080")
        print("\tpython client.py 179.123.13.4 5023")
    else:
        t2 = threading.Thread(name="client", target=client)
        t2.start()

