import socket as mysoc
import threading
import sys

# TOP-LEVEL DNS SERVER
topLevelTable = {}

# Initialize the topLevelTable table by reading query
# lines from PROJI-DNSTS.txt
def initTable():
    file = open("PROJ2-DNSTS1.txt", "r")
    for line in file:
        split = line.split()
        topLevelTable[split[0].lower()] = [split[1], split[2]]
    file.close()

# Top-Level Server Procedure
def server():
    initTable()
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

    while True:
        # Message recieved from Client
        query = csockid.recv(200).decode("utf-8").lower()
        if query == "/end":
            break
        print("[S]: Query from Client: " + query)
        try:
            ip, types = topLevelTable[query]
            csockid.send((query + " " + ip + " " + types).encode("utf-8"))
        except:
            #csockid.send("Error:HOST NOT FOUND".encode("utf-8"))
            #do nothing hahaha
            a = 1
        

    # Close the server socket
    ss.close()
    exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:\tpython ts1.py <ts1 ListenPort>")
        print("Ex:\tpython ts1.py 8080")
    else:
        t1 = threading.Thread(name="server", target=server)
        t1.start()