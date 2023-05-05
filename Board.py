import Piece


class Board:
    def __init__(self):
        self.SQUARES_NUM = 8

        self.pieces = None

        self.locations = [[None for _ in range(self.SQUARES_NUM)] for _ in range(self.SQUARES_NUM)]

        # Track king position
        self.king_location = {"white": (0, 4), "black": (7, 4)}
        self.un_passant_attack = None
        self.un_passant_victim_location = None

        self.side_to_move = 'white'
        self.legal_moves = None

    def current_colour(self):
        """Get current side to move colour"""
        return self.side_to_move

    def opposite_colour(self):
        """Change side to move"""
        if self.side_to_move == "white":
            opponent = "black"
        elif self.side_to_move == "black":
            opponent = "white"
        else:
            opponent = None

        return opponent

    def change_colour(self):
        """Change side to move"""
        if self.side_to_move == "white":
            self.side_to_move = "black"
        elif self.side_to_move == "black":
            self.side_to_move = "white"
        else:
            self.side_to_move = None

    def set_pieces_collection(self, pieces):
        self.pieces = pieces

    def length(self):
        return self.SQUARES_NUM

    def on_board(self, piece_location):
        """Check if location exists on board"""
        rank, file = piece_location
        if (rank in range(self.length())) and (file in range(self.length())):
            on_board = True
        else:
            on_board = False

        return on_board

    def configure_pieces(self):
        """Place pieces if playing for white"""
        # Test case
        # self.locations[0] = [self.pieces.get_by_name("w_rook"),
        #                      None,
        #                      None,
        #                      None,
        #                      self.pieces.get_by_name("w_king"),
        #                      None,
        #                      None,
        #                      self.pieces.get_by_name("w_rook")]

        self.locations[0] = [self.pieces.get_by_name("w_rook"),
                             self.pieces.get_by_name("w_knight"),
                             self.pieces.get_by_name("w_bishop"),
                             self.pieces.get_by_name("w_queen"),
                             self.pieces.get_by_name("w_king"),
                             self.pieces.get_by_name("w_bishop"),
                             self.pieces.get_by_name("w_knight"),
                             self.pieces.get_by_name("w_rook")]
        self.locations[1] = [self.pieces.get_by_name("w_pawn") for _ in range(self.length())]
        self.locations[6] = [self.pieces.get_by_name("b_pawn") for _ in range(self.length())]
        self.locations[7] = [self.pieces.get_by_name("b_rook"),
                             self.pieces.get_by_name("b_knight"),
                             self.pieces.get_by_name("b_bishop"),
                             self.pieces.get_by_name("b_queen"),
                             self.pieces.get_by_name("b_king"),
                             self.pieces.get_by_name("b_bishop"),
                             self.pieces.get_by_name("b_knight"),
                             self.pieces.get_by_name("b_rook")]

        # Test case
        # self.locations[7] = [self.pieces.get_by_name("b_rook"),
        #                      None,
        #                      None,
        #                      None,
        #                      self.pieces.get_by_name("b_king"),
        #                      None,
        #                      None,
        #                      self.pieces.get_by_name("b_rook")]

    def get_piece(self, location) -> Piece:
        """Get piece by its location"""
        rank, file = location
        piece = self.locations[rank][file]
        return piece

    def place_piece(self, piece, location):
        """Place piece on square"""
        rank, file = location

        # If piece moved fo the first time
        if not piece.is_moved():
            # place moved instance instead
            piece = self.pieces.get_moved_version(piece)

        self.locations[rank][file] = piece

    def update_parameters(self, piece, location):
        """Update board parameters"""
        consider_un_passant = False

        if self.pieces.is_pawn(piece) and not piece.is_moved():
            # Should consider un passant
            consider_un_passant = True

        elif self.pieces.is_king(piece):
            # Save new king location
            self.king_location[piece.get_colour()] = location

        return consider_un_passant

    def clear_location(self, location):
        """Clear square"""
        rank, file = location
        self.locations[rank][file] = None

    def set_un_passant(self, location, victim_location):
        """Set un passant parameters"""
        self.un_passant_attack = location
        self.un_passant_victim_location = victim_location

    def clear_un_passant(self):
        """Clear un passant parameters"""
        self.un_passant_attack = None
        self.un_passant_victim_location = None

    def get_un_passant_attack(self):
        return self.un_passant_attack

    def get_un_passant_victim_location(self):
        return self.un_passant_victim_location

    def copy(self):
        """Returns copy of the board"""
        board_copy = Board()

        # Copy pieces locations and un passant attack square
        board_copy.locations = []
        for rank in self.locations:
            board_copy.locations.append(rank.copy())

        board_copy.un_passant_attack = self.un_passant_attack
        board_copy.un_passant_victim_location = self.un_passant_victim_location
        board_copy.king_location = self.king_location.copy()
        board_copy.side_to_move = self.side_to_move

        # Dictionary with pieces stay the same for optimization
        board_copy.pieces = self.pieces

        return board_copy

    def king_location_by_colour(self, king_colour):
        return self.king_location[king_colour]

    def set_legal_moves(self, legal_moves):
        self.legal_moves = legal_moves.copy()

    def get_piece_legal_moves(self, location):
        rank, file = location
        return self.legal_moves[rank][file]
