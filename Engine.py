from Piece import Piece
from itertools import product


class Engine:
    def __init__(self, board, pieces, app):
        self.pieces = pieces
        self.board = board
        self.app = app
        self.ui = None

        self.promotion_location = None
        self.promotion_move = None

        self.__set_pawn_promotions()
        self.compute_legal_moves(board)

    def set_ui(self, ui):
        """Create UI object"""
        self.ui = ui

    def __set_pawn_promotions(self):
        """Define available pawn promotions"""
        self.pawn_promotions = {'white': [], 'black': []}

        promotion_names_white = ['w_knight', 'w_bishop', 'w_rook_moved', 'w_queen']
        # promotion_names_white = ['w_rook_moved', 'w_rook_moved', 'w_rook_moved', 'w_rook_moved']
        for piece_name in promotion_names_white:
            piece = self.pieces.get_by_name(piece_name)
            self.pawn_promotions['white'].append(piece)

        promotion_names_black = ['b_knight', 'b_bishop', 'b_rook_moved', 'b_queen']
        # promotion_names_black = ['b_rook_moved', 'b_rook_moved', 'b_rook_moved', 'b_rook_moved']
        for piece_name in promotion_names_black:
            piece = self.pieces.get_by_name(piece_name)
            self.pawn_promotions['black'].append(piece)

    def process_move(self, board, location, move):
        """Calculate move for given board and location"""
        move_done = False
        attacking_moves, position_moves = self.board.get_piece_legal_moves(location)
        piece_moves = attacking_moves + position_moves
        if move in piece_moves:
            if not self.__pawn_promotion(board, location, move):
                move_done = True
                self.__move_piece(board, location, move)
                self.compute_legal_moves(self.board)
                if self.check_mate(self.board):
                    self.ui.set_mate()

            else:
                self.promotion_location = location
                self.promotion_move = move
                self.ui.set_pawn_promotion()

        return move_done

    def __move_piece(self, board, location, move):
        """Move piece to another square"""
        piece = board.get_piece(location)

        # Place piece
        board.place_piece(piece, move)

        #  and get flag if un passant will be available
        consider_un_passant = board.update_parameters(piece, move)
        board.clear_location(location)

        if consider_un_passant:
            # Save un passant square and piece for take
            self.__compute_un_passant(board, piece, location, move)
        else:
            # Delete un passant squares
            self.__clear_un_passant(board, move)

        if self.__castling_move(piece, location, move):
            self.__castle_rook(board, move)

        board.change_colour()

    def __castling_move(self, piece, location, move):
        """Castling"""
        its_castling = False
        if self.pieces.is_king(piece):
            if abs(location[1] - move[1]) == 2:
                its_castling = True

        return its_castling

    @staticmethod
    def __castle_rook(board, move):
        """Move rook when castling"""
        # king side castling
        if move[1] == 6:
            rook_location = (move[0], 7)
            rook_move = (move[0], 5)
        # queen side castling
        elif move[1] == 2:
            rook_location = (move[0], 0)
            rook_move = (move[0], 3)
        # internal error
        else:
            rook_location = None
            rook_move = None

        board.place_piece(board.get_piece(rook_location), rook_move)
        board.clear_location(rook_location)

    def compute_legal_moves(self, board):
        """Compute legal moves for each piece on a given board"""
        legal_moves = [[[] for _ in range(board.length())]
                       for _ in range(board.length())]

        # For each square
        for rank, file in product(range(board.length()), range(board.length())):
            location = (rank, file)
            piece = board.get_piece(location)

            if piece:
                # if piece belong to moving side
                if piece.get_colour() == board.current_colour():
                    # get piece moves by its moving rules
                    piece_attacking_moves, piece_position_moves = piece.get_moves(board, location)

                    legal_attacks = []
                    for move in piece_attacking_moves:
                        if self.__move_legal(board, location, move):
                            legal_attacks.append(move)

                    legal_positions = []
                    for move in piece_position_moves:
                        if self.__move_legal(board, location, move):
                            legal_positions.append(move)

                    legal_moves[rank][file] = [legal_attacks, legal_positions]

        castling_moves = self.__compute_castling(board)
        # if castling is possible add it to king's legal moves
        if castling_moves:
            king_rank, king_file = board.king_location_by_colour(board.current_colour())
            # if castling is possible, then at least 1 move for the king is possible
            legal_attacks, legal_positions = legal_moves[king_rank][king_file]
            for castle_location in castling_moves:
                legal_positions.append(castle_location)
            legal_moves[king_rank][king_file] = [legal_attacks, legal_positions]

        board.set_legal_moves(legal_moves)

    def __simulate_move(self, board, location, move):
        """Create board and simulate a move"""
        # Create copy of board
        computational_board = board.copy()

        # Simulate move on the copy
        self.__move_piece(computational_board, location, move)

        return computational_board

    def __move_legal(self, board, location, move):
        """Check if move is legal"""
        # simulate move on the copy of the board
        computational_board = self.__simulate_move(board, location, move)
        # if king won't be in check
        king_location = computational_board.king_location_by_colour(board.current_colour())
        # then move is legal
        return not self.__square_under_attack(computational_board, king_location, board.opposite_colour())

    @staticmethod
    def __square_under_attack(board, square, attacker_colour):
        """Compute attacking moves for given board, side to move and check if king in check"""
        check = False
        for rank, file in product(range(board.length()), range(board.length())):
            location = (rank, file)
            piece = board.get_piece(location)
            piece: Piece
            if piece:
                # move is simulated, so next to move is opponent
                if piece.get_colour() == attacker_colour:
                    piece_attacking_moves, piece_position_moves = piece.get_moves(board, location)
                    if square in piece_attacking_moves:
                        check = True
                        break

        return check

    @staticmethod
    def check_mate(board):
        """Check if it is mate in position"""
        mate = True
        # For each square
        for rank, file in product(range(board.length()), range(board.length())):
            # get legal moves for a piece
            piece_moves = board.get_piece_legal_moves((rank, file))
            if piece_moves:
                attacking_moves, position_moves = piece_moves
                # and if there is any
                if attacking_moves + position_moves:
                    # it's not mate
                    mate = False
                    break

        return mate

    def __compute_castling(self, board):
        """Computation of castling moves"""
        castle = []
        # Get king location and piece
        king_rank, king_file = board.king_location_by_colour(board.current_colour())
        king = board.get_piece((king_rank, king_file))

        # King can't be in check
        king_under_attack = self.__square_under_attack(board, (king_rank, king_file), board.opposite_colour())
        # King didn't move
        king_moved = king.is_moved()

        if not king_moved and not king_under_attack:
            castle_k, castle_q = king.castling((king_rank, king_file))
            k_rook = board.get_piece((king_rank, 7))
            if k_rook:
                if not k_rook.is_moved():
                    # if squares between rook and king are not under attack
                    if not self.__square_under_attack(board, (king_rank, king_file + 1), board.opposite_colour()) and \
                       not self.__square_under_attack(board, (king_rank, king_file + 2), board.opposite_colour()):
                        castle.append(castle_k)
            q_rook = board.get_piece((king_rank, 0))
            if q_rook:
                if not q_rook.is_moved():
                    # if squares between rook and king are not under attack
                    if not self.__square_under_attack(board, (king_rank, king_file - 1), board.opposite_colour()) and \
                       not self.__square_under_attack(board, (king_rank, king_file - 2), board.opposite_colour()):
                        castle.append(castle_q)
        return castle

    @staticmethod
    def __compute_un_passant(board, piece, location, move):
        """Compute and set un passant parameters"""
        rank, file = move

        # If pawn have made double forward move
        if abs(location[0] - move[0]) == 2:

            # Make un passant available
            if piece.get_colour() == "white":
                un_passant = (rank - 1, file)
            elif piece.get_colour() == "black":
                un_passant = (rank + 1, file)
            else:
                # internal error
                un_passant = None

            # Save location of piece available for un passant take
            board.set_un_passant(un_passant, move)

        else:
            # Make un passant unavailable
            board.clear_un_passant()

    @staticmethod
    def __clear_un_passant(board, location):
        """Clear un passant"""
        # If piece was taken un passant
        if board.get_un_passant_attack() == location:
            # Clear victim square
            board.clear_location(board.get_un_passant_victim_location())

        # Make un passant unavailable
        board.clear_un_passant()

    def possible_pawn_promotions(self, colour):
        """Get possible pawn promotions for given colour"""
        return self.pawn_promotions[colour]

    def __pawn_promotion(self, board, location, move):
        """Check if move is pawn promotion"""
        promotion = False
        piece = board.get_piece(location)
        # if piece is a pawn
        if self.pieces.is_pawn(piece):
            # and if it's on last rank for its colour
            rank, file = move
            if rank in [0, 7]:
                promotion = True

        return promotion

    def promote_pawn(self, board, piece):
        """Promote pawn"""
        # Place piece
        board.place_piece(piece, self.promotion_move)

        #  and get flag if un passant will be available
        board.update_parameters(piece, self.promotion_move)
        board.clear_location(self.promotion_location)
        # Delete un passant squares
        self.__clear_un_passant(board, self.promotion_move)

        self.promotion_location = None
        self.promotion_move = None

        board.change_colour()

        self.compute_legal_moves(self.board)
        if self.check_mate(self.board):
            self.ui.set_mate()
