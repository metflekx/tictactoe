"""
Version 1.0.0 (Initial Release):
- Implemented Tic Tac Toe game using Python and Pygame.
- Created a Game class to manage the game state and logic.
- Defined players (Player X and Player O) with associated markers.
- Implemented AI using the Minimax algorithm for player moves.
- Added functionality to check for a winner or a draw.
- Integrated Pygame for graphical display of the game board.

TODO:
- write better main() function to run the game.
- Add a proper GUI for the game.

"""

from enum import Enum
import time


import pygame


# __Global scope__ 

def utility(terminal_state):
    """
    given a terminal state, returns which player wins the game.

    args:
        terminal_state (list): list of lists of 3x3

    returns:
        winner (Player): player who won the game
    """

    # to avoid writing the same code again, 
    # we initialize an instance of game class and set the board to
    # terminal_state and after calling game.is_terminal(True), with a true
    # arg, game.winner gets populated and we can retrive the winner

    g = Game()
    g.set_board(terminal_state)
    winner = g.get_winner()
    del g

    # return the Marker.winner
    if not winner:
        return 0
    elif winner.is_max:
        return 1
    else:
        return -1

# initialize pygame
pygame.init()

# sets to false at first move so we can keep track of frist player
starting_player_marker = None

# __End global scope__

class Game:
    class Marker(Enum):
        """
        Marker class to represent the marker of a player
        """
    
        MINPLAYER = 0 # X
        MAXPLAYER = 1 # O
        EMPTY     = 2

    def __init__(self):
        """
        Initializes the game
        """

        # the state of the game, a 3 by 3 grid
        self.board = [[self.Marker.EMPTY for _ in range(3)] for _ in range(3)]
        # initialize players
        self.player_min = self.Player(False, self)
        self.player_max = self.Player(True, self)
        # populated once terminal
        self.winner = None

        self.is_game_started = False
        self.starting_player_marker = None

    class Player:
        def __init__(self, is_max, game_instance):
            """
            Initializes the player

            Args:
                is_max (bool): True if the player is the max player, 
                False otherwise
            """

            self.game_instance = game_instance
            if is_max:
                self.marker = self.game_instance.Marker.MAXPLAYER
            else:
                self.marker = self.game_instance.Marker.MINPLAYER
            self.AI = self.AI(is_max, self)
            self.is_max = is_max
            self.name_ = "Player O" if is_max else "Player X"

        class AI:
            def __init__(self, is_max, player_instance):
                """
                Initializes the AI
                """

                self.player_instance = player_instance
                self.is_max = is_max
                self.marker = self.player_instance.game_instance.Marker.EMPTY

            def min_value(self, board) -> tuple:
                if self.player_instance.game_instance.is_terminal(board):
                    return utility(board)

                v = float("inf")
                for a in self.player_instance.game_instance.actions(board):
                    v = min(v, self.max_value(
                        self.player_instance.game_instance.result(a, board, self.is_max)))

                return v

            def max_value(self, board) -> tuple:
                if self.player_instance.game_instance.is_terminal(board):
                    return utility(board)

                v = -float("inf")
                for a in self.player_instance.game_instance.actions(board):
                    v = max(v, self.min_value(
                        self.player_instance.game_instance.result(a, board, self.is_max)))

                return v

            def minimax(self, board) -> list:
                if self.is_max:
                    best = board
                    for a in self.player_instance.game_instance.actions(board):
                        result = self.player_instance.game_instance.result(
                                a, board, self.is_max)
                        if self.max_value(result) >= self.max_value(best):
                            best = result

                    return result

                else:
                    best = board
                    for a in self.player_instance.game_instance.actions(board):
                        result = self.player_instance.game_instance.result(
                                a, board, self.is_max)
                        if self.min_value(result) <= self.min_value(best):
                            best = result

                    return best

        def play(self, board):
            """
            Plays the game

            Args:
                board (list): the board to play on

            Returns:
                list: the updated board
            """

            if not self.game_instance.is_game_started:
                self.game_instance.starting_player_marker = self.marker
                self.game_instance.is_game_started = True

            return self.AI.minimax(board)

    def __marker_to_player(self, marker):
        """
        Converts a marker to a player

        Args:
            marker (Marker): the marker to convert

        Returns:
            Player (Player): the player that corresponds to the marker
        """

        # error check
        if not isinstance(marker, self.Marker):
            raise TypeError(
                    "::ERROR::GAME::MARKER MUST BE OF TYPE MARKER.")
        if marker == self.Marker.EMPTY:
            raise ValueError(
                    "::ERROR::GAME::MARKER CANNOT BE EMPTY.")

        if marker == self.Marker.MINPLAYER:
            return self.player_min
        else:
            return self.player_max

    def get_winner(self):
        """
        Returns:
            Player (Player): the winner of the game
        """

        self.is_terminal(self.board)

        if not self.winner:
            return None

        return self.winner

    def set_board(self, board):
        """
        Sets the board to the given board

        Args:
            board (list): the board to set
        """

        self.board = board

    def set_cell(self, cell, marker):
        """
        Sets the cell to the marker

        Args:
            cell (tuple): the cell to set
            marker (Marker): the marker to set the cell to
        """

        if not isinstance(cell, tuple):
            raise TypeError("::ERROR::GAME::CELL MUST BE OF TYPE TUPLE.")
        if not isinstance(marker, self.Marker):
            raise TypeError("::ERROR::GAME::MARKER MUST BE OF TYPE MARKER.")
        if marker == self.Marker.EMPTY:
            raise ValueError("::ERROR::GAME::MARKER CANNOT BE EMPTY.")

        i, j = cell
        self.board[i][j] = marker

    def actions(self, board) -> list:
        """
        Returns:
            list: list of all possible actions
        """

        sample_space = list() # to store all possible actions

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == self.Marker.EMPTY:
                    sample_space.append((i, j))

        return sample_space

    def result(self, action, board, is_max) -> list:
        """
        Returns:
            list: the resulting board after taking action
        """

        i, j = action

        # copy the board
        board_clone = [row[:] for row in board]

        board_clone[i][j] = self.Marker.MAXPLAYER if is_max else self.Marker.MINPLAYER

        return board_clone

    def is_terminal(self, board, assign_winner=False):
        """ 
        Checks if the game is over
        sets the winner of the game, stores it in self.winner

        Returns:
            bool: True if the game is over, False otherwise
        """

        # check for rows
        if board[0][0] != self.Marker.EMPTY:
            # access the marker from first cell in row
            marker = board[0][0] 
            if board[0][0] == board[0][1] == board[0][2]:
                marker = board[0][0]
                if assign_winner:
                    self.winner = self.__marker_to_player(marker)
                return True
    
        if board[1][0] != self.Marker.EMPTY:
            if board[1][0] == board[1][1] == board[1][2]:
                if assign_winner:
                    marker = board[1][0]
                    self.winner = self.__marker_to_player(marker)
                return True

        if board[2][0] != self.Marker.EMPTY:
            if board[2][0] == board[2][1] == board[2][2]:
                if assign_winner:
                    marker = board[2][0]
                    self.winner = self.__marker_to_player(marker)
                return True

        # check for columns
        if board[0][0] != self.Marker.EMPTY:
            if board[0][0] == board[0][1] == board[0][2]:
                if assign_winner:
                    marker = board[0][0]
                    self.winner = self.__marker_to_player(marker)
                return True
            
        if board[0][1] != self.Marker.EMPTY:
            if board[0][1] == board[1][1] == board[2][1]:
                if assign_winner:
                    marker = board[0][1]
                    self.winner = self.__marker_to_player(marker)
                return True

        if board[0][2] != self.Marker.EMPTY:
            if board[0][2] == board[1][2] == board[2][2]:
                if assign_winner:
                    marker = board[0][2]
                    self.winner = self.__marker_to_player(marker)
                return True

        # check for diagonals
        if board[0][0] != self.Marker.EMPTY:
            if board[0][0] == board[1][1] == board[2][2]:
                if assign_winner:
                    marker = board[0][0]
                    self.winner = self.__marker_to_player(marker)
                return True

        if board[0][2] != self.Marker.EMPTY:
            if board[0][2] == board[1][1] == board[2][0]:
                if assign_winner:
                    marker = board[0][2]
                    self.winner = self.__marker_to_player(marker)
                return True

        # check for draw
        for row in board:
            for cell in row:
                if cell == self.Marker.EMPTY:
                    return False

        # if we get here, the game is a draw
        self.winner = None
        return True

    def display(self, board):
        """
        Displays the board using pygame
        """

        # draw a grid
        screen = pygame.display.set_mode((300, 300))
        pygame.display.set_caption("Tic Tac Toe")
        screen.fill((255, 255, 255))

        # draw a white line
        pygame.draw.line(screen, (0, 0, 0), (100, 0), (100, 300), 2)
        pygame.draw.line(screen, (0, 0, 0), (200, 0), (200, 300), 2)
        pygame.draw.line(screen, (0, 0, 0), (0, 100), (300, 100), 2)
        pygame.draw.line(screen, (0, 0, 0), (0, 200), (300, 200), 2)

        # draw the markers
        for i in range(3):
            for j in range(3):
                if board[i][j] == self.Marker.MINPLAYER:
                    # set parameters for pyame.draw.line()
                    line_color = (0.0, 0.0, 0.0, 1.0)
                    line_start_pos =  [20 + 100 * j, 20 + 100 * i]
                    line_end_pos = 80 + 100 * j, 80 + 100 * i
                    # draw
                    pygame.draw.line(screen, line_color, 
                                     line_start_pos, line_end_pos,
                                     width=2)

                    line_color = (0.0, 0.0, 0.0, 1.0)
                    line_start_pos = [80 + 100 * j, 20 + 100 * i]
                    line_end_pos = [20 + 100 * j, 80 + 100 * i]

                    pygame.draw.line(screen, line_color, 
                                     line_start_pos, line_end_pos,
                                     width=2)

                elif board[i][j] == self.Marker.MAXPLAYER:
                    circle_color = (0.0, 0.0, 0.0, 1.0)
                    circle_center = [50 + 100 * j, 50 + 100 * i]

                    pygame.draw.circle(screen, circle_color,
                                       circle_center, radius=40, 
                                       width=2)

        pygame.display.flip()

    def main(self):
        """
        Main game loop
        """

        running = True
        do = True
        while running:
            if self.is_terminal(self.board, assign_winner=True):
                running = False

            while do:
                self.board = self.player_max.play(self.board)
                self.display(self.board)
                do = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.is_terminal(self.board, assign_winner=True):
                    running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.board[0][0] = self.Marker.MINPLAYER
                    do = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    self.board[0][1] = self.Marker.MINPLAYER
                    do = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    self.board[0][2] = self.Marker.MINPLAYER
                    do = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    self.board[1][0] = self.Marker.MINPLAYER
                    do = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                    self.board[1][1] = self.Marker.MINPLAYER
                    do = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                    self.board[1][2] = self.Marker.MINPLAYER
                    do = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                    self.board[2][0] = self.Marker.MINPLAYER
                    do = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_8:
                    self.board[2][1] = self.Marker.MINPLAYER
                    do = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_9:
                    self.board[2][2] = self.Marker.MINPLAYER
                    do = True

        winner = self.winner
        if not winner:
            print("draw")
        elif winner.is_max:
            print("winner is: O")
        else:
            print("winner is: X")


if __name__ == "__main__":
    game = Game()
    game.main()
