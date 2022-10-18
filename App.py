from Board import Board
from Engine import Engine
from PiecesCollection import PiecesCollection
from UI import UI


class App:
    def __init__(self):
        self.pieces = None
        self.board = None
        self.engine = None
        self.ui = None
        self.mate = False

    def __initialize_pieces(self):
        """"Create pieces"""
        self.pieces = PiecesCollection()
        self.pieces.initialize_pieces()

    def __initialize_board(self):
        """"Create Board, pieces and place them"""
        self.board = Board()
        self.__initialize_pieces()
        self.board.set_pieces_collection(self.pieces)
        self.board.configure_pieces()

    def __initialize_engine(self):
        self.engine = Engine(self.board, self.pieces, self)

    def __initialize_ui(self):
        """"Create UI"""
        self.ui = UI(self, self.engine, self.board)
        self.engine.set_ui(self.ui)

    def __initialize_game(self):
        """"Initialize all objects"""
        self.__initialize_board()
        self.__initialize_engine()
        self.__initialize_ui()

    def set_mate(self):
        self.mate = True

    def run_game(self):
        """"Loop for screen and key events"""
        self.__initialize_game()
        while not self.mate:
            self.ui.update_screen()
            self.ui.check_events()
        print('mate')
