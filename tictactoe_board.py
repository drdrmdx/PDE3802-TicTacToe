class TicTacToeBoard:
    def __init__(self):
        self.board = {
            'A1': ' ', 'A2': ' ', 'A3': ' ',
            'B1': ' ', 'B2': ' ', 'B3': ' ',
            'C1': ' ', 'C2': ' ', 'C3': ' '
        }
        self.current_player = 'X'
        self.dofbot = 'O'
        self.current_player_turn = True  # True if human's turn, False if Dofbot's turn

    def print_board(self):
        """
        prints the current state of the board.
        """
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)
            
    def reset_board(self):
        """
        resets the board to the initial empty state.
        """
        for key in self.board:
            self.board[key] = ' '
        self.current_player_turn = True
        
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
        
        if self.current_player_turn:
            self.board[position] = self.current_player
        else:
            self.board[position] = self.dofbot

        return True

    def check_winner(self):
        """
        checks the board horizontally, vertically, and diagonally for a winner.
        returns 'X' if human wins, 'O' if Dofbot wins, or None if no winner yet.
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
        
        return None