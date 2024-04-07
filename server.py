# IMporting libraries
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 # you can use any port between 0 to 65535
LISTENER_LIMIT = 5
active_clients = []

# Function to listen for upcoming massages from client
def listen_for_massages(client,username):

    while True:
        message = client.recv(2048).decode('utf-8')
        if message != '':

            final_msg = username + '~' + message
            send_massages_to_all(final_msg)

        else:
            print(f"The message send from the client {username} is empty")
def send_message_to_client(client,message):
    client.sendall(message.encode())

# Function to send any new messages to all the clients that
# are currently connected to the server
def send_massages_to_all(message):
    for user in active_clients:

        send_message_to_client(user[1],message)


# Fumction to handle client
def client_handler(client):

    # Server will listen for client massage that will
    # contain the Username
    while True :
        username = client.recv(2048).decode('utf-8')
        if username !=  '':
            active_clients.append((username,client))
            break
        else :
            print("Client username is empty")
    threading.Thread(target=listen_for_massages,args=(client,username,)).start()
#main function
def main():
    # Creating the socket class object
    # AF_INET : indicates that we are going to use IPV4 addresses
    # SOCK_STREAM: Indicates that we are using TCP Package for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block
    try:
        # Provide the server with an address in the form of
        # Host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server {HOST}:{PORT}")
    except Exception as e:  # Catching specific exception
        print(f"Unable to bind to host {HOST} and Port {PORT}")
        print(e)  # Print the exception for debugging purposes
        return  # Exit the function if binding fails

    # Set server limit
    server.listen(LISTENER_LIMIT)
    # This while loop will keep listening to client connection
    while True:  # Changed '1' to 'True' for clarity
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler,args=(client,)).start()





if __name__=='__main__':
    main()