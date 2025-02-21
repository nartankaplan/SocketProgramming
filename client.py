import socket  # Importing the socket module for client-server communication


def main():
    try:
        # Create a client socket and connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8888))  # Connect to server on localhost:8888

        # Receive the initial message from the server (stock info)
        message = client_socket.recv(1024).decode()
        print("Server:", message)

        while True:
            # Prompt the user to enter their price prediction or type 'END' to quit
            guess = input("Enter your price prediction (or type 'END' to quit): ")

            # Send the guess to the server
            client_socket.send(guess.encode())
            print(f"Sent guess to server: {guess}")

            # Check if the user wants to end the connection
            if guess.upper() == "END":
                print("Ending the connection.")
                break  # Exit the loop if 'END' is entered

            # Try to receive the response from the server
            try:
                response = client_socket.recv(1024).decode()  # Receive feedback from the server
                print("Server:", response)  # Print the server's response directly
            except ConnectionAbortedError:
                print("Connection was aborted by the server.")
                break  # Exit the loop if connection was aborted
            except ConnectionResetError:
                print("Connection was reset by the server.")
                break  # Exit the loop if connection was reset

            # End session if the response contains success or game-over messages
            if "Correct" in response or "Too many attempts" in response:
                print("Ending session based on server response.")
                break  # Exit the loop based on server's feedback

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    finally:
        # Closes the client socket upon ending the connection
        client_socket.close()
        print("Client socket closed.")

# Run the client if this script is executed directly
if __name__ == '__main__':
    main()
