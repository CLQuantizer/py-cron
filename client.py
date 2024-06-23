import socket


def udp_client(message, host='127.0.0.1', port=12345):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send message to server
    client_socket.sendto(message.encode('utf-8'), (host, port))

    # Receive response from server
    response, server_address = client_socket.recvfrom(1024)  # Buffer size is 1024 bytes
    print(f"Received response from server: {response.decode('utf-8')}")

    # Close the socket
    client_socket.close()


if __name__ == "__main__":
    message = "Hello, UDP server!"
    udp_client(message)
