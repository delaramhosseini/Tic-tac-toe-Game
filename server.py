# Importing necessary modules and libraries
import socket  # Module for network communication
import pickle  # Module for object serialization
import time   # Module for time-related operations
import numpy as np  # Module for numerical computing with arrays

# Creating a socket object
s = socket.socket()

# Host and port configuration
host = ""  # Empty string indicates the server will listen on all available interfaces
port = 9999  # Port number for communication

# Asking the user for the size of the board
n = int(input("Enter the size of the board: "))

# Default value of winning condition
k= 3 

# Adjusting the winning condition based on the size of the board
if n > 4 : 
    k = n-1

# Initializing the game board matrix with zeros
matrix = [[0]*n for _ in range(n)] 

# Constants representing player identifiers
playerOne = 1
playerTwo = 2

# Lists to store connections and addresses of players
playerConn = list()
playerAddr = list()       


def get_input(currentPlayer):
    # Determine which player's turn it is and retrieve their connection
    if currentPlayer == playerOne:
        player = "Player One's Turn"
        conn = playerConn[0]
    else:
        player = "Player Two's Turn"
        conn = playerConn[1]
    
    # Print whose turn it is
    print(player)
    
    # Send a message to both players indicating whose turn it is
    send_common_msg(player)
    
    try:
        # Send a message to the player indicating to provide input
        conn.send("Input".encode())
        
        # Receive data from the player's connection
        data = conn.recv(2048 * 10)
        
        # Set a timeout for the connection
        conn.settimeout(20)
        
        # Decode the received data and split it into x and y coordinates
        dataDecoded = data.decode().split(",")
        x = int(dataDecoded[0])
        y = int(dataDecoded[1])
        
        # Update the game matrix with the player's move
        matrix[x][y] = currentPlayer
        
        # Send a common message indicating the updated game matrix to both players
        send_common_msg("Matrix")
        send_common_msg(str(matrix))
    except:
        # If an error occurs during communication with the player, send an error message
        conn.send("Error".encode())
        print("Error occured! Try again..")


def check_rows():
    # Print a message indicating that rows are being checked
    print("Checking rows")
    
    # Initialize counters for player one (F) and player two (S) to zero
    F = 0 
    S = 0
    
    # Iterate over possible starting positions of consecutive rows of length k
    for j in range(n-k+1):
        # Iterate over each row
        for ii in range(n):
            # Iterate over each cell within the row
            for jj in range (k):
                # Check if the cell contains a mark for player one
                if matrix[ii ] [ jj + j] == 1 : F+=1
                
                # Check if the cell contains a mark for player two
                if matrix[ii ] [ jj + j] == 2 : S+=1
                
            # Check if player one has a winning sequence of length k in the current row
            if F == k : return 1
            
            # Check if player two has a winning sequence of length k in the current row
            if S == k : return 2
            
            # Reset counters for the next row
            F = 0
            S = 0
            
    # Return 0 if no player has a winning sequence in any row
    return 0



def check_columns():
    # Initialize counters for player one (F) and player two (S) to zero
    F = 0 
    S = 0
    
    # Iterate over possible starting positions of consecutive columns of length k
    for j in range(n-k+1):
        # Iterate over each column
        for ii in range(n):
            # Iterate over each cell within the column
            for jj in range (k):
                # Check if the cell contains a mark for player one
                if matrix[jj + j] [ii] == 1 : F+=1
                
                # Check if the cell contains a mark for player two
                if matrix[jj + j] [ii] == 2 : S+=1
            
            # Check if player one has a winning sequence of length k in the current column
            if F == k : return 1
            
            # Check if player two has a winning sequence of length k in the current column
            if S == k : return 2
            
            # Reset counters for the next column
            F = 0
            S = 0
            
    # Return 0 if no player has a winning sequence in any column
    return 0




def check_diagonals():
    # Define a list of starting positions for diagonals based on the condition (n == k)
    ls = [0] if n == k else [0, 1]
    
    # Iterate over the list of starting positions
    for i in ls:
        # Initialize counters for player one (F) and player two (S) to zero
        S = F = 0
        
        # Check the diagonal from top-left to bottom-right
        for j in range(k):
            if matrix[j][j + i] == 1:
                F += 1
            if matrix[j][j + i] == 2:
                S += 1
        if S == k:
            return 2 
        if F == k:
            return 1

        # Check the diagonal from bottom-left to top-right
        S = F = 0
        for j in range(k):
            if matrix[-j - 1][-1 - j - i] == 1:
                F += 1
            if matrix[-j - 1][-1 - j - i] == 2:
                S += 1
        if S == k:
            return 2 
        if F == k:
            return 1

        # Check the diagonal from bottom-right to top-left
        S = F = 0
        for j in range(k):
            if matrix[-1 - j][j + i] == 1:
                F += 1
            if matrix[-1 - j][j + i] == 2:
                S += 1
        if S == k:
            return 2 
        if F == k:
            return 1

        # Check the diagonal from top-right to bottom-left
        S = F = 0
        for j in range(k):
            if matrix[j][-1 - j - i] == 1:
                F += 1
            if matrix[j][-1 - j - i] == 2:
                S += 1
        if S == k:
            return 2 
        if F == k:
            return 1
    
    # Return 0 if no player has a winning sequence in any diagonal
    return 0


def check_winner():
    # Initialize the result variable to 0
    result = 0
    
    # Check for a winner by calling the check_rows function
    result = check_rows()
    
    # If no winner is found in rows, check for a winner in columns
    if result == 0:
        result = check_columns()
    
    # If no winner is found in rows or columns, check for a winner in diagonals
    if result == 0:
        result = check_diagonals()
    
    # Return the result indicating the winner (1 for player one, 2 for player two, or 0 for no winner)
    return result



def start_server():
    try:
        # Bind the socket to the host and port
        s.bind((host, port))
        
        # Print a message indicating that the server has started
        print("Tic Tac Toe server started \nBinding to port", port)
        
        # Listen for incoming connections (maximum 2 connections)
        s.listen(2) 
        
        # Call the function to accept player connections
        accept_players()
    
    # Handle socket binding errors
    except socket.error as e:
        print("Server binding error:", e)



def accept_players():
    try:
        # Iterate over two players
        for i in range(2):
            # Accept incoming connection and retrieve connection object and address
            conn, addr = s.accept()
            
            # Send a message to the player indicating their player number and board size
            msg = "<<< You are player {} >>> board size is {}".format(i + 1, n)
            conn.send(msg.encode())

            # Store player connection and address in lists
            playerConn.append(conn)
            playerAddr.append(addr)
            
            # Print player connection information
            print("Player {} - [{}:{}]".format(i + 1, addr[0], str(addr[1])))
        
        # Start the game after both players have connected
        start_game()
        
        # Close the server socket after the game ends
        s.close()
    
    # Handle socket errors during player connection
    except socket.error as e:
        print("Player connection error", e)
    
    # Handle KeyboardInterrupt (Ctrl+C) to gracefully exit the program
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt")
        exit()
    
    # Handle other exceptions
    except Exception as e:
        print("Error occurred:", e)



def start_game():
    # Initialize variables to track the game progress and the number of moves
    result = 0
    i = 0
    
    # Continue the game loop until there's a winner or the game board is full
    while result == 0 and i < n ** 2:
        # Determine which player's turn it is based on the number of moves
        if i % 2 == 0:
            get_input(playerOne)  # Player One's turn
        else:
            get_input(playerTwo)  # Player Two's turn
        
        # Check for a winner after each move
        result = check_winner()
        
        # Increment the move counter
        i += 1
    
    # Inform both players that the game is over
    send_common_msg("Over")

    # Determine the final outcome of the game
    if result == 1:
        lastmsg = "Player One is the winner!!"
    elif result == 2:
        lastmsg = "Player Two is the winner!!"
    else:
        lastmsg = "Draw game!! Try again later!"
    
    # Send the final message to both players
    send_common_msg(lastmsg)
    
    # Delay for 10 seconds before closing player connections
    time.sleep(10)
    
    # Close connections with both players
    for conn in playerConn:
        conn.close()

    

def send_common_msg(text):
    # Send the same message to both players
    playerConn[0].send(text.encode())
    playerConn[1].send(text.encode())
    
    # Introduce a delay of 1 second between sending messages to avoid flooding the network
    time.sleep(1)


start_server()