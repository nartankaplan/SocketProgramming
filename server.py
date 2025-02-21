import socket  # Importing the socket module for network communication
import pandas as pd  # Importing pandas for handling Excel files
import os  # Importing os for handling file paths
import time  # Importing time to make delays to use in some cases (I've got many errors at the beggining)
                #also wrote try catch blocks to prevent them

# Function to handle the client's prediction
def handle_request(client_connection, stock_name, actual_price):
    attempts = 1  # Initialize the number of attempts
    tolerance = 0.05  # Set 5% tolerance for correct predictions

    # Allow up to 3 attempts for the client to guess
    while attempts < 3:
        try:
            # Receive guess from the client
            guess = client_connection.recv(1024).decode()
            print(f"Received guess from client: {guess}")

            # Check if client wants to end the session
            if guess.upper() == "END":
                print("Client has ended the connection.")
                client_connection.send("Connection closed by client.".encode())
                return  # Exit the function to end the session

            # Attempt to convert the client's guess to a float for comparison
            try:
                guess = float(guess)
                print(f"Processed guess as float: {guess}")
            except ValueError:
                client_connection.send("Invalid input. Please enter a valid number.".encode())
                continue  # Skip to the next iteration if input is invalid

            # Check if the guess is within the tolerance range
            if abs(guess - actual_price) / actual_price <= tolerance:
                client_connection.send("*********************----Correct! Your guess is within the tolerance range.----*********************".encode())
                print("Correct guess received. Ending session.")
                return  # End function as the guess was correct
            else:
                # Increment attempt count if guess is incorrect
                attempts += 1
                # Provide a hint to the client based on the guess
                if guess > actual_price:
                    client_connection.send("Lower".encode())
                else:
                    client_connection.send("Higher".encode())
                print(f"Attempt {attempts}: Sent hint to client.")

        # Handle cases where connection is reset or aborted by the client
        except (ConnectionResetError, ConnectionAbortedError):
            print("Connection error.")
            return  # End function on connection error
        except Exception as e:
            print(f"Unexpected error: {e}")
            client_connection.send("Server error. Please try again.".encode())
            return  # End function for other errors

    # After 3 incorrect attempts, send the correct price to the client
    final_message = f"*********************----Game Over. Too many attempts. Correct price: {actual_price} *********************----"
    client_connection.send(final_message.encode())
    print(f"Too many attempts. Sent correct price: {actual_price}")

    # Add a delay to ensure client receives the final message before closing
    time.sleep(1)  # Wait 1 second

# Function to start the server and load stock data
def serve_forever():
    # Load the stock data from the Excel file
    file_path = os.path.join(os.path.dirname(__file__), 'stock.xlsx')
    stock_data = pd.read_excel(file_path)

    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8888))  # Bind to localhost on port 8888
    server_socket.listen(1)  # Listen for incoming connections
    print("Server has been started on local and listening on port 8888.")

    while True:  # Infinite loop to keep the server running
        try:
            client_connection, client_address = server_socket.accept()  # Accept new client connections
            print(f"Connected by {client_address}")

            # Randomly select a stock from the loaded data
            stock = stock_data.sample()
            stock_name = stock['Stock Symbol'].values[0]  # Get stock symbol
            actual_price = stock['Price'].values[0]  # Get stock price

            # Send stock info to the client for prediction
            client_connection.send(f"Predict the price for {stock_name}".encode())
            print(f"Sent stock information to client: {stock_name} with price {actual_price}")

            # Handle the client's prediction
            handle_request(client_connection, stock_name, actual_price)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close the client connection after each session
            client_connection.close()
            print(f"Connection with {client_address} closed.")

# Run the server if this script is executed directly
if __name__ == '__main__':
    serve_forever()
