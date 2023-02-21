# Python program to implement server side of chat room.
import socket
import sys
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

Port = None

#Sets a default port if it is not specified
if len(sys.argv) != 2:
	print ("Defaulting to Port 8890")
	Port = 8890

#Get the host computer's IP address
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("Server IP: " + str(IPAddr))

if Port == None:
	#Gets the port number to listen from
	Port = int(sys.argv[1])

server.bind((IPAddr, Port))

#listens for 100 active connections
server.listen(100)

list_of_clients = []
nicknames = {}

def clientthread(conn, addr):

	# sends a message to the client whose user object is conn
	welcomeMessage = "Welcome to the chat!\n"
	conn.send(welcomeMessage.encode())

	#sets the default nickname to the IP
	nicknames.update({addr[0]:addr[0]})

	while True:
			try:
				message = conn.recv(2048).decode()
				#print(message)
				if message:
					#handle commands
					if message.startswith("/nick"):
						name = message.split()
						name = name[1]
						nicknames.update({addr[0]:name})
						continue
					if message.startswith("/list"):
						broadcast(nicknames, conn)
						continue
					if message.startswith("/quit"):
						remove(conn)
						continue

					#format message
					message_to_send = "<" + nicknames[addr[0]] + "> " + message
					#send message to server terminal
					print(message_to_send)
					#send message to all users
					broadcast(message_to_send, conn)

			except:
				continue

"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def broadcast(message, connection):
	for clients in list_of_clients:
		#if clients!=connection:
		try:
			clients.send(message)
		except:
			clients.close()
			# if the link is broken, we remove the client
			remove(clients)

"""The following function simply removes the object
from the list that was created at the beginning of
the program"""
def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:

	"""Accepts a connection request and stores two parameters,
	conn which is a socket object for that user, and addr
	which contains the IP address of the client that just
	connected"""
	conn, addr = server.accept()

	"""Maintains a list of clients for ease of broadcasting
	a message to all available people in the chatroom"""
	list_of_clients.append(conn)

	# prints the address of the user that just connected
	print (addr[0] + " connected")

	# creates and individual thread for every user
	# that connects
	start_new_thread(clientthread,(conn,addr))	

conn.close()
server.close()