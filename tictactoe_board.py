class TicTacToeBoard:
    def __init__(self):
        self.board = {
            'A1': ' ', 'A2': ' ', 'A3': ' ',
            'B1': ' ', 'B2': ' ', 'B3': ' ',
            'C1': ' ', 'C2': ' ', 'C3': ' '
        }
        self.player1 = 'O'
        self.player2 = 'X'
        self.player1_turn = True  # True if player1 turn, False if player2 turn
        self.move_count = 0
        
    def print_board(self):
        """
        prints the current state of the board.
        """
        print("\n")
        print("     1   2   3")
        print("   +---+---+---+")
        print(f" A | {self.board['A1']} | {self.board['A2']} | {self.board['A3']} |")
        print("   +---+---+---+")
        print(f" B | {self.board['B1']} | {self.board['B2']} | {self.board['B3']} |")
        print("   +---+---+---+")
        print(f" C | {self.board['C1']} | {self.board['C2']} | {self.board['C3']} |")
        print("   +---+---+---+")
        print("\n")
    
            
    def reset_board(self):
        """
        resets the board to the initial empty state.
        """
        for key in self.board:
            self.board[key] = ' '
        self.player1_turn = True
        
    def get_board(self):
        """
        returns the current state of the board.
        """
        return self.board

    def make_move(self, position):
        """
        places a piece on the board.
        Makes sure the position is valid and not already taken.
        uses self.current_player_turn to determine whose turn it is.
        """
        if position not in self.board:
            print("Invalid position! Does not exist.")
            return False
        if position != ' ':
            print("Invalid position! Already taken.")
            return False
        
        if self.player1_turn:
            self.board[position] = self.player1
        else:
            self.board[position] = self.player2

        self.move_count += 1
        return True

    def check_game_state(self):
        """
        check if game has a winner, draw, or is ongoing.
        """
        game_state = {
            'status': 'ongoing',
            'winner': None,
            'winner_text': None
        }
        
        winner = self.check_winner()
        if winner:
            # if there is a winner
            game_state['status'] = 'win'
            game_state['winner'] = winner
            game_state['winner_text'] = 'P1' if winner == self.player1 else 'P2'
            return game_state

        # board is full, it's a draw
        if self.check_board_full():
            game_state['status'] = 'draw'
            game_state['winner_text'] = 'Draw'
        
        # game is ongoing
        return game_state
    
    def check_winner(self):
        """
        checks the board horizontally, vertically, and diagonally for a winner.
        returns 'O' if player1 wins, 'X' if player2 wins, or False if no winner yet.
        """
        # check if all rows are same and not empty
        for row in ['A', 'B', 'C']:
            if self.board[f"{row}1"] == self.board[f"{row}2"] == self.board[f"{row}3"] != ' ':
                return self.board[f"{row}1"]
        
        # check if column sequences are the same and not empty
        for col in ['1', '2', '3']:
            if self.board[f"A{col}"] == self.board[f"B{col}"] == self.board[f"C{col}"] != ' ':
                return self.board[f"A{col}"]
            
        # check diagonals
        if self.board["A1"] == self.board["B2"] == self.board["C3"] != ' ':
            return self.board["A1"]
        if self.board["A3"] == self.board["B2"] == self.board["C1"] != ' ':
            return self.board["A3"]
        
        return False

    
    def check_board_full(self):
        """
        checks if the board is full, no empty spaces
        """
        return all(value != ' ' for value in self.board.values())
    
    
    def is_valid_move(self, position: str) -> bool:
        """
        checks if position is valid, checks if empty and in board
        
        position: Position to check ('A1', 'B2', 'C2')
        """
        return position in self.board and self.board[position] == ' '

    def get_empty_positions(self):
        return [pos for pos, val in self.board.items() if val == ' ']


    def switch_player(self):
        """
        change the current player's turn
        """
        self.player1_turn = not self.player1_turn

    def get_move_count(self):
        """
        Get the number of pieces on the board.
        
        Returns:
            int: Number of non-empty positions
        """
        return len([val for val in self.board.values() if val != ' '])