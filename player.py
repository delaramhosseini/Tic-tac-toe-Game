import pygame  # Import the pygame library for creating the game interface
import socket  # Import the socket library for network communication
import time    # Import the time module for introducing delays
import threading  # Import the threading module for managing concurrent execution
import numpy as np  # Import the numpy library for array manipulation

# Create a socket object
s = socket.socket()

# Define the host (IP address or hostname) to bind the socket
host = "localhost"

# Define the size of the board (n x n grid)
n = 3

# Initialize the game matrix to represent the game board
matrix = [[0]*n for _ in range(n)]

# Define the port number for socket communication
port = 9999

# Define player identifiers
playerOne = 1
playerTwo = 2

# Define player colors for rendering
playerOneColor = (255, 0, 0)  # Red
playerTwoColor = (0, 0, 255)  # Blue

# Initialize message variables for game status and communication
bottomMsg = ""   # Message displayed at the bottom of the game window
msg = "Waiting for peer"  # Initial message displayed during peer connection
currentPlayer = 0  # Variable to keep track of the current player's turn
xy = (-1, -1)  # Variable to store the selected grid position by a player
allow = 0  # Flag to control player input


def create_thread(target):
    # Create a new thread with the given target function
    t = threading.Thread(target=target)
    
    # Set the thread as a daemon thread, which will terminate when the main program exits
    t.daemon = True
    
    # Start the thread
    t.start()



# Initialize the Pygame library
pygame.init()

# Define the size of the game board
nBoard = 100 * n

# Set the width and height of the Pygame window
width = nBoard + 300
height = nBoard + 250

# Create the game screen with the specified dimensions
screen = pygame.display.set_mode((width, height))

# Load the game icon
icon = pygame.image.load("tictactoe.png")

# Define fonts for text rendering
bigfont = pygame.font.Font('freesansbold.ttf', 64)  # Large font for titles
smallfont = pygame.font.Font('freesansbold.ttf', 32)  # Smaller font for messages

# Define colors for rendering
backgroundColor = (255, 255, 255)   # Background color of the game screen
titleColor = (0, 0, 0)               # Color for title text
subtitleColor = (128, 0, 255)       # Color for subtitle text
lineColor = (0, 0, 0)                # Color for grid lines


def initialize(n):
    # Initialize the Pygame library
    pygame.init()

    # Declare global variables to be used and modified within the function
    global nBoard
    global width
    global height
    global screen

    # Set the caption of the Pygame window to indicate the size of the Tic Tac Toe board
    pygame.display.set_caption(f"Tic Tac Toe {n} x {n}")

    # Define the size of the game board
    nBoard = 100 * n

    # Set the width and height of the Pygame window
    width = nBoard + 300
    height = nBoard + 250

    # Create the game screen with the specified dimensions
    screen = pygame.display.set_mode((width, height))

    # Set the window icon to the previously loaded icon image
    pygame.display.set_icon(icon)




def buildScreen(bottomMsg, string, playerColor=subtitleColor):
    # Fill the screen with the background color
    screen.fill(backgroundColor)
    
    # Determine player color based on the string provided
    if "One" in string or "1" in string:
        playerColor = playerOneColor
    elif "Two" in string or "2" in string:
        playerColor = playerTwoColor

    # Draw grid lines for the Tic Tac Toe board
    for i in range(1, n):
        pygame.draw.line(screen, lineColor, (150 + (nBoard/n)*i - 2, 150), (150 + (nBoard/n)*i - 2, 150 + nBoard), 4)
        pygame.draw.line(screen, lineColor, (150, 150 + (nBoard/n)*i - 2), (150 + nBoard, 150 + (nBoard/n)*i - 2), 4)

    # Render and display the title "TIC TAC TOE" at the center of the screen
    title = bigfont.render("TIC TAC TOE", True, titleColor)
    screen.blit(title, (nBoard/2 - 40, 0))
    
    # Render and display the subtitle (e.g., player's turn) at the center of the screen
    subtitle = smallfont.render(str.upper(string), True, playerColor)
    screen.blit(subtitle, (nBoard/2 - 20, 70))
    
    # Display the bottom message with specified color
    centerMessage(bottomMsg, playerColor)



def centerMessage(msg, color=titleColor):
    # Declare global variable to access nBoard
    global nBoard
    
    # Calculate the position to center the message
    pos = ((nBoard - 100) / 2, nBoard + 180)
    
    # Determine the color based on the message content
    if "One" in msg or "1" in msg:
        color = playerOneColor
    elif "Two" in msg or "2" in msg:
        color = playerTwoColor
    
    # Render the message with the specified color
    msgRendered = smallfont.render(msg, True, color)
    
    # Display the rendered message at the calculated position
    screen.blit(msgRendered, pos)




def printCurrent(current, pos, color):
    # Render the current player indicator text
    currentRendered = bigfont.render(str.upper(current), True, color)
    
    # Display the rendered text at the specified position on the screen
    screen.blit(currentRendered, pos)



def printMatrix(matrix):
    # Iterate over each row of the matrix
    for i in range(n):
        # Calculate the y-coordinate for displaying the current row
        y = int((i * nBoard / n) + 150 + nBoard / (n * 4))
        
        # Iterate over each column of the matrix
        for j in range(n):
            # Calculate the x-coordinate for displaying the current column
            x = int((j * nBoard / n) + 150 + nBoard / (n * 4))
            
            # Initialize variables for the current cell content and color
            current = " "
            color = titleColor
            
            # Determine the content and color based on the value in the matrix
            if matrix[i][j] == playerOne:
                current = "X"  # 'X' represents Player One's move
                color = playerOneColor  # Use Player One's color
            elif matrix[i][j] == playerTwo:
                current = "O"  # 'O' represents Player Two's move
                color = playerTwoColor  # Use Player Two's color
            
            # Print the current cell content at the calculated position with the specified color
            printCurrent(current, (x, y), color)




def validate_input(x, y):
    # Check if the input coordinates are within the bounds of the game board
    if x >= n or y >= n:
        print("\nOut of bounds! Please enter valid coordinates.\n")
        return False
    # Check if the selected cell is already occupied
    elif matrix[x][y] != 0:
        print("\nAlready occupied! Please select an empty cell.\n")
        return False
    # Return True if the input is valid
    return True


    
def handleMouseEvent(pos):
    # Extract the x and y coordinates from the mouse position
    x = pos[0]
    y = pos[1]
    
    # Declare global variables to be used and modified within the function
    global currentPlayer
    global xy
    global nBoard
    global n
    
    # Check if the mouse position is outside the game board area
    if x < 150 or x > (nBoard + 150) or y < 150 or y > (nBoard + 150):
        xy = (-1, -1)  # Set xy to indicate an invalid position
    else:
        # Calculate the column and row indices based on the mouse position
        col = int((x - 150) / (nBoard / n))
        row = int((y - 150) / (nBoard / n))
        print("({}, {})".format(row, col))  # Print the selected row and column
        
        # Validate the input coordinates
        if validate_input(row, col):
            # If the input is valid, update the game matrix with the current player's mark
            matrix[row][col] = currentPlayer
            xy = (row, col)  # Set xy to indicate the selected position




def start_player():
    # Declare global variables to be used and modified within the function
    global currentPlayer
    global bottomMsg
    global n
    global matrix

    try:
        # Connect to the server
        s.connect((host, port))
        print("Connected to:", host, ":", port)
        
        # Receive initial data from the server
        recvData = s.recv(2048 * 10)
        
        # Decode the received data to update the bottom message and board size
        bottomMsg = recvData.decode()
        n = int(bottomMsg[-1])
        print(n)
        print(bottomMsg)
        
        # Remove the board size information from the bottom message
        bottomMsg = bottomMsg[:-16]
        
        # Update the game matrix based on the new board size
        matrix = [[0] * n for _ in range(n)]
        
        # Initialize the game screen with the updated board size
        initialize(n)

        # Determine the current player based on the received data
        if "1" in bottomMsg:
            currentPlayer = 1
        else:
            currentPlayer = 2
        
        # Start the game
        start_game()
        
        # Close the socket connection
        s.close()
    
    except socket.error as e:
        print("Socket connection error:", e)




def start_game():
    # Declare variables and set up the game loop
    running = True
    global msg
    global matrix
    global bottomMsg
    
    # Create a separate thread to handle incoming messages from the server
    create_thread(accept_msg)
    
    # Main game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            # Quit event: Exit the game loop
            if event.type == pygame.QUIT:
                running = False
            
            # Mouse button up event: Handle mouse click on the game board
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()  # Get the mouse position
                if allow:  # Check if input is allowed
                    handleMouseEvent(pos)  # Handle the mouse click
        
        # Break out of the loop if no message is received
        if msg == "":
            break
        
        # Build and update the game screen
        buildScreen(bottomMsg, msg)  # Build the game screen with current messages
        printMatrix(matrix)  # Print the current game matrix onto the screen
        pygame.display.update()  # Update the display




flag = True
def accept_msg():
    # Declare global variables to be used and modified within the function
    global matrix
    global msg
    global bottomMsg
    global allow
    global xy
    global flag

    while True:
        try:
            # Receive data from the server
            recvData = s.recv(2048 * 10)
            
            # Decode the received data
            recvDataDecode = recvData.decode()
            
            # Update the game screen based on the received data
            buildScreen(bottomMsg, recvDataDecode)

            # Handle different types of received data
            if recvDataDecode == "Input":
                failed = 1
                allow = 1
                xy = (-1, -1)
                # Keep trying to send input coordinates until successful
                while failed:
                    try:
                        # If valid input coordinates are available, send them to the server
                        if xy != (-1, -1):
                            coordinates = str(xy[0]) + "," + str(xy[1])
                            s.send(coordinates.encode())
                            failed = 0
                            allow = 0
                    except:
                        print("Error occurred....Try again")

            elif recvDataDecode == "Error":
                print("Error occurred! Try again..")
            
            elif recvDataDecode == "Matrix":
                # Receive the updated game matrix from the server
                matrixRecv = s.recv(2048 * 100)
                matrixRecvDecoded = matrixRecv.decode("utf-8")
                matrix = eval(matrixRecvDecoded)  # Update the local game matrix
                # Print the received matrix if it's the first time
                flag and print(matrix)
                flag = False

            elif recvDataDecode == "Over":
                # Receive the game over message from the server
                msgRecv = s.recv(2048 * 100)
                msgRecvDecoded = msgRecv.decode("utf-8")
                bottomMsg = msgRecvDecoded
                msg = "~~~Game Over~~~"
                break  # Break out of the loop to end the game
                
            else:
                # Update the message to be displayed on the screen
                msg = recvDataDecode

        except KeyboardInterrupt:
            print("\nKeyboard Interrupt")
            time.sleep(1)
            break

        except:
            print("Error occurred")
            break


start_player()