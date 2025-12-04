class Piece:
    """
    Piece used in the game to represent a marker on the board.
    Attributes:
        color: Color of the piece (e.g., 'W' or 'B')
        name: eg: King, Queen, Rook, etc.
        symbol: Symbol representing the piece (e.g., 'WK' for White King)
    """
    def __init__(self, color, name, symbol):
        self.color = color
        self.name = name
        self.symbol = symbol
        self.current_pos = None # current position on board eg: A1, B1, C3
        self.coordinates = None
        
    def __str__(self):
        return self.symbol