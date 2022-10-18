from Bishop import Bishop
from King import King
from Knight import Knight
from Pawn import Pawn
from Queen import Queen
from Rook import Rook


class PiecesCollection:
    def __init__(self):
        self.pieces = None

    def initialize_pieces(self):
        """"Create all pieces"""
        images_dir = "D:\\users\\akhmatov-nv\\PycharmProjects\\chess\\images\\"
        pieces = {"w_pawn": Pawn("white", images_dir + "w_pawn.png", False),
                  "w_pawn_moved": Pawn("white", images_dir + "w_pawn.png", True),
                  "b_pawn": Pawn("black", images_dir + "b_pawn.png", False),
                  "b_pawn_moved": Pawn("black", images_dir + "b_pawn.png", True),

                  "w_king": King("white", images_dir + "w_king.png", False),
                  "w_king_moved": King("white", images_dir + "w_king.png", True),
                  "b_king": King("black", images_dir + "b_king.png", False),
                  "b_king_moved": King("black", images_dir + "b_king.png", True),

                  "w_rook": Rook("white", images_dir + "w_rook.png", False),
                  "w_rook_moved": Rook("white", images_dir + "w_rook.png", True),
                  "b_rook": Rook("black", images_dir + "b_rook.png", False),
                  "b_rook_moved": Rook("black", images_dir + "b_rook.png", True),

                  "w_knight": Knight("white", images_dir + "w_knight.png", True),
                  "b_knight": Knight("black", images_dir + "b_knight.png", True),

                  "w_bishop": Bishop("white", images_dir + "w_bishop.png", True),
                  "b_bishop": Bishop("black", images_dir + "b_bishop.png", True),

                  "w_queen": Queen("white", images_dir + "w_queen.png", True),
                  "b_queen": Queen("black", images_dir + "b_queen.png", True)
                  }
        self.pieces = pieces

    def get_by_name(self, piece_name):
        return self.pieces[piece_name]

    def get_moved_version(self, piece):
        """Return moved instance of piece"""
        moved_piece = None
        if isinstance(piece, Pawn):
            piece_colour = piece.get_colour()
            if piece_colour == "white":
                moved_piece = self.pieces["w_pawn_moved"]
            elif piece_colour == "black":
                moved_piece = self.pieces["b_pawn_moved"]

        elif isinstance(piece, King):
            piece_colour = piece.get_colour()
            if piece_colour == "white":
                moved_piece = self.pieces["w_king_moved"]
            elif piece_colour == "black":
                moved_piece = self.pieces["b_king_moved"]

        elif isinstance(piece, Rook):
            piece_colour = piece.get_colour()
            if piece_colour == "white":
                moved_piece = self.pieces["w_rook_moved"]
            elif piece_colour == "black":
                moved_piece = self.pieces["b_rook_moved"]

        else:
            # No need to track this for other pieces
            moved_piece = piece

        return moved_piece

    @staticmethod
    def is_pawn(piece):
        return isinstance(piece, Pawn)

    @staticmethod
    def is_king(piece):
        return isinstance(piece, King)

    @staticmethod
    def is_rook(piece):
        return isinstance(piece, Rook)
