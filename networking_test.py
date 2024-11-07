import unittest
import socket
import threading

# Define constants for host and port
HOST = '127.0.0.1'  # localhost
PORT = 12345

def start_test_server():
    """A simple echo server that listens for connections, reads data, and echoes it back."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print("Server started, listening for connections...")

    conn, addr = server.accept()
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)  # Echo data back to the client
    conn.close()
    server.close()
    print("Server closed connection.")

class TestNetworking(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Start the server in a separate thread before running tests."""
        cls.server_thread = threading.Thread(target=start_test_server, daemon=True)
        cls.server_thread.start()

    def test_client_server_communication(self):
        """Test if the client can send data and receive the correct response from the server."""
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        
        # Send a message to the server
        test_message = b"Hello, Server!"
        client.sendall(test_message)
        
        # Receive the echoed message from the server
        received_message = client.recv(1024)
        
        # Check if the received message matches the sent message
        self.assertEqual(received_message, test_message)
        
        # Close the client connection
        client.close()

    @classmethod
    def tearDownClass(cls):
        """Any cleanup required after all tests (if necessary)."""
        # In a real scenario, we might send a shutdown command to the server or handle server cleanup here.

if __name__ == "__main__":
    unittest.main()
