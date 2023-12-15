# Tic-tac-toe AI

This project implements the classic game of tic-tac-toe where two agents compete to win. It's built using Python 3.11 and emphasizes minimal external library dependencies for the game logic.

## APIs and Tech Stack

- [Python](https://www.python.org/) - Version 3.11
- [NumPy](https://numpy.org/) - Utilizes data structures provided by NumPy for efficient array handling.
- [Pygame](https://www.pygame.org/) - Utilizes Pygame for visual representation and mapping of game data.

## Overview

The heart of the game resides in the `Game` class. The `Game.main()` method drives the game loop. During each iteration, the game checks for terminal states using `Game.is_terminal()`. Once a terminal state is detected, it populates the `Game.winner`. Meanwhile, the main loop continues until the game reaches a terminal state, allowing the agents to compete using the 'Minimax' algorithm.

### Implementation Details

The method `Game.is_terminal()` serves dual purposes. To prevent unnecessary iteration when finding the winner after the game concludes, the method takes a boolean argument `assign_winner`. Setting this argument to true populates the variable `Game.winner`. When calling `Game.is_terminal()` from within `Game.Player.AI.minimax()`, set this argument to false. This approach consolidates the functionalities of detecting terminal states and determining the winner to avoid extra iterations.

### Classes Hierarchy and Global Scope

#### Global Scope
The code contains elements noted with comments as `# __GLOBAL_SCOPE`, which denote calls or resources accessible from anywhere within the code.

#### Class Structure
The structure for each class is as follows:

- **Class:**
  - Constructor
  - Nested Classes
  - Private Methods (noted with `__` at the beginning of the method's name)
  - Static Methods
  - Getters
  - Setters
  - Public Methods

## Usage

To play the game, execute the main file `tictactoe.py`. The game interface is provided using Pygame, allowing players to interact with the game through key inputs (1-9) for their moves.

## Future Improvements

Potential future enhancements include:
- Adding a user interface for a more intuitive and interactive gameplay experience.
- Implementing more sophisticated AI algorithms or strategies for improved gameplay.

Feel free to contribute by forking this repository and submitting pull requests!

## License

This project is licensed under the [MIT License](LICENSE).

## Tutorial: Game Controls -- Specific for version

The game is played using the keyboard as controllers. Each cell on the tic-tac-toe grid is mapped to a numeric key on the keyboard (1-9). Players take turns by pressing the corresponding keys to make their moves.

### Key Mapping:

- `1`, `2`, `3`: Correspond to the cells in the first row from left to right.
- `4`, `5`, `6`: Correspond to the cells in the second row from left to right.
- `7`, `8`, `9`: Correspond to the cells in the third row from left to right.

### Gameplay Instructions:

1. Launch the game by running the main file `tictactoe.py`.
2. The initial display shows an empty tic-tac-toe grid.
3. Player X (represented by 'X') is the starting player, followed by Player O (represented by 'O').
4. To make a move:
   - Player X presses the corresponding key to place 'X' in an empty cell.
   - Player O then makes their move by pressing a key to place 'O' in an available cell.
5. The game continues until one player wins by forming a line of their marker (either horizontally, vertically, or diagonally) or until the grid is filled, resulting in a draw.
6. The game announces the winner or declares a draw at the end.

### Example:

- Player X's move:
  - Press key `1` to place 'X' in the top-left cell.
- Player O's move:
  - Press key `5` to place 'O' in the center cell.
- Players alternate turns until the game concludes.

### Note:

- Ensure only valid keys (1-9) are pressed to make moves. Invalid keys or attempts to place markers in non-empty cells will be disregarded.
- Pygame window must be in focus to receive key inputs.

Feel free to enjoy the game by competing against a friend or playing against the AI!
