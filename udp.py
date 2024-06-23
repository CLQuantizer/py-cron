import socket

def udp_server(host='127.0.0.1', port=12345):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the server address and port
    server_socket.bind((host, port))
    
    print(f"UDP server up and listening on {host}:{port}")
    
    while True:
        # Receive message from client
        message, client_address = server_socket.recvfrom(1024)  # Buffer size is 1024 bytes
        print(f"Received message from {client_address}: {message.decode('utf-8')}")
        
        # Optionally, send a response to the client
        response = "Message received"
        server_socket.sendto(response.encode('utf-8'), client_address)

if __name__ == "__main__":
    udp_server()
