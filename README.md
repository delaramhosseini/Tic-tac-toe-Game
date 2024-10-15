# Tic Tac Toe Game Server and Client

This project implements a **Tic Tac Toe** game using Python, allowing two players to connect and play over a network. The project includes both server and client-side code, with functions for handling player connections, managing game logic, and rendering the game board using **Pygame** for the client. Additionally, the code is well-documented with comments explaining each section for ease of understanding.

## Server Overview

The server is responsible for handling player connections, managing the game state, and facilitating communication between the two players during the Tic Tac Toe game. It listens for incoming player connections, processes their moves, checks for a winner after each move, and sends game state updates to both players.

### Key Features:
- Accepts two players to connect to the game server.
- Receives player input and updates the game state.
- Checks for a winner after each move by evaluating rows, columns, and diagonals.
- Sends game state updates and messages to both players.

### Import Statements:
- **`socket`**: Provides access to the BSD socket interface for network communication, enabling client-server applications.
- **`pickle`**: Used to serialize and deserialize Python objects, allowing complex data structures to be transmitted over a network.
- **`time`**: Provides time-related functions, such as delays for controlling the flow of the program.
- **`numpy as np`**: Supports operations on large, multi-dimensional arrays, which is useful for managing the Tic Tac Toe game board.

### Server Functions:

1. **`get_input`**:
   - Manages player input during each turn.
   - Sends turn information to both players.
   - Updates the game matrix with the current player's move.
   - Handles communication errors gracefully.

2. **`check_rows`**:
   - Checks for a winning sequence in any row of the game matrix.
   - Iterates through each row to identify if either player has achieved a sequence of length `k`.

3. **`check_columns`**:
   - Checks for a winning sequence in any column of the game matrix.
   - Iterates through each column, identifying possible winning sequences for both players.

4. **`check_diagonals`**:
   - Checks for winning sequences in both main and anti-diagonals.
   - Iterates through all possible diagonal starting positions to detect a winner.

5. **`check_winner`**:
   - Combines the results from `check_rows`, `check_columns`, and `check_diagonals` to determine if there's a winner.
   - Returns the corresponding player identifier (1 for Player One, 2 for Player Two) if a winner is found; otherwise, returns 0.

6. **`start_server`**:
   - Binds the server socket to a specified host and port.
   - Listens for incoming player connections with a maximum queue size of 2.
   - Handles socket binding errors.

7. **`accept_players`**:
   - Waits for two players to connect.
   - Sends each player their player number and board size.
   - Starts the game once both players are connected.
   - Handles errors such as socket issues and keyboard interrupts.

8. **`start_game`**:
   - Manages the game loop, alternating between Player One and Player Two.
   - Checks for a winner after each move and sends game state updates to both players.
   - Closes player connections at the end of the game.

9. **`send_common_msg`**:
   - Sends a message to both players simultaneously.
   - Introduces a short delay to prevent network flooding.

---

## Player Overview

The player (client) side is responsible for connecting to the server, receiving game updates, and rendering the game interface using **Pygame**. It also handles user input and sends the player's move to the server.

### Key Features:
- Connects to the Tic Tac Toe server and receives game state updates.
- Renders the game board and player turns using Pygame.
- Handles player input, including clicks and move validation.

### Player Functions:

1. **`create_thread`**:
   - Creates and starts a new thread to handle concurrent tasks, such as listening for server messages.

2. **`initialize`**:
   - Initializes the Pygame environment, sets up the game window, and loads necessary assets (like the game icon).

3. **`buildScreen(bottomMsg, string, playerColor)`**:
   - Builds and updates the game screen.
   - Renders the game grid, title, and player turn information.

4. **`centerMessage`**:
   - Renders a message in the center of the game screen.
   - Calculates the position to ensure the message is centered both horizontally and vertically.

5. **`printCurrent`**:
   - Displays the current player's turn on the screen with appropriate colors.

6. **`printMatrix`**:
   - Renders the current state of the game board matrix, displaying 'X' for Player One, 'O' for Player Two, or an empty space.

7. **`validate_input`**:
   - Validates the player's input to ensure it corresponds to a valid, empty cell on the game board.

8. **`handleMouseEvent`**:
   - Handles mouse click events, determining which cell the player clicked and updating the game state if the move is valid.

9. **`start_player`**:
   - Initializes the client-side game setup, connects to the server, and starts receiving game data.

10. **`start_game`**:
   - Contains the main game loop, which updates the game screen, handles user input, and checks for game events like quitting or mouse clicks.

11. **`accept_msg`**:
   - Continuously listens for messages from the server.
   - Updates the game board and screen based on the messages received.
   - Handles game-over conditions and updates the game status.

