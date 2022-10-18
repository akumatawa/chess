from Piece import Piece


class King(Piece):
    def __init__(self, colour, picture, moved):
        super().__init__(colour, picture, moved)

    @staticmethod
    def __calculate_moves(location):
        """"Return piece moves"""
        rank, file = location
        possible_moves = [(rank + 1, file),
                          (rank - 1, file),
                          (rank, file + 1),
                          (rank, file - 1),
                          (rank + 1, file + 1),
                          (rank + 1, file - 1),
                          (rank - 1, file + 1),
                          (rank - 1, file - 1)]

        return possible_moves

    @staticmethod
    def castling(location):
        rank, file = location
        castle = [(rank, file + 2),
                  (rank, file - 2)]

        return castle

    def get_moves(self, board, location):
        """"Compute piece possible moves"""
        position_moves = []
        attacking_moves = []

        available_moves = self.__calculate_moves(location)

        for next_position in available_moves:
            # MAY BE ADDED TO _MOVES()
            # does square exists on board
            if board.on_board(next_position):
                piece_on = board.get_piece(next_position)
                # is there a piece
                if piece_on is None:
                    position_moves.append(next_position)
                # is it another colour
                elif piece_on.get_colour() != self.get_colour():
                    attacking_moves.append(next_position)

        return attacking_moves, position_moves
