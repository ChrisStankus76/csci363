#Chat Server using UDP
import sys
import socket

def main(portNum):
    '''
    Creates a server connection
    Uses host computer's IP address and specified port number
    host IP printed
    '''
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Get the host computer's IP address
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("Server IP: " + str(IPAddr))
    server.bind((IPAddr, portNum))

    connClients = {}

    #Loops taking in messages and commands and sending responses
    while True:
        #get message and decodes the message
        message, addr = server.recvfrom(1024)
        message = message.decode("utf-8")

        '''
        Checks for Unconnected User
        If unconnected and less than 100 users
        Connects and sends message
        '''
        #check connected clients for the address
        if addr not in [i for i in connClients.keys()]:
            #ensures max of 100 users
            if len(connClients) < 100:
                print(f"{addr} connected to the chat")
                #sets the default nickname as "User"
                connClients[addr] = "User"
                messOut = f"<{connClients[addr]}> {message}"
                print(messOut)
                for i in connClients.keys():
                    server.sendto("<User Connected>\n".encode(), i)
                    server.sendto(messOut.encode(), i)
        else:
            '''
            Connected User 
            Checks for Command, if not found then sends the message
            '''
            #Changes your nickname on the server
            if message.startswith("/nick"):
                connClients[addr] = message.split()[1]
                continue
            #lists all connected users
            if message.startswith("/list"):
                activeUsers = []
                for i in connClients.values():
                    activeUsers.append(i)
                server.sendto((str(activeUsers) + "\n").encode(), addr)
                continue
            #quits - disconnects the currrent user
            if message.startswith("/quit"):
                connClients.pop(addr)
                continue
            
            #sends message to other users
            for i in connClients.keys():
                if i != addr:
                    messOut = f"<{connClients[addr]}> {message}"
                    print(messOut)
                    server.sendto(messOut.encode(), i)

'''
Runs Program on Launch
'''
if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        print("server.py [port number]")