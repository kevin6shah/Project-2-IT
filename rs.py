import socket as mysoc
import threading
import sys

# ROOT DNS SERVER
rootTable = {}

# Initialize the topLevelTable table by reading query
# lines from PROJI-DNSRS.txt
def initTable():
    file = open("PROJI-DNSRS.txt", "r")
    nameServer = ""
    for line in file:
        split = line.split()
        if split[2] == "NS":
            nameServer = split[0] + " " + split[1] + " " + split[2]
        else:
            rootTable[split[0].lower()] = [split[1], split[2]]
    file.close()
    return nameServer


# Root Server Procedure
def server():
    nameServer = initTable()
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

    # Accept Connection
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at" + str(addr))

    while True:
        # Message recieed from Client
        query = csockid.recv(200).decode("utf-8").lower()
        if query == "/end":
            break
        print("[S]: Query from Client: " + query)
        try:
            ip, types = rootTable[query]
            csockid.send((query + " " + ip + " " + types).encode("utf-8"))
        except:
            csockid.send(nameServer.encode("utf-8"))

    # Close the server socket
    ss.close()
    exit()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:\tpython rs.py <rsListenPort>")
        print("Ex:\tpython rs.py 8080")
    else:
        t1 = threading.Thread(name="server", target=server)
        t1.start()
