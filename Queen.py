from Piece import Piece


class Queen(Piece):
    def __init__(self, colour, picture, moved):
        super().__init__(colour, picture, moved)

    @staticmethod
    def __calculate_moves(board, position):
        """"Return piece moves"""
        rank, file = position
        possible_moves = [[], [], [], [], [], [], [], []]

        i = 1
        while True:
            next_position = (rank + i, file)
            if board.on_board(next_position):
                possible_moves[0].append(next_position)
                i += 1
            else:
                break

        i = -1
        while True:
            next_position = (rank + i, file)
            if board.on_board(next_position):
                possible_moves[1].append(next_position)
                i -= 1
            else:
                break

        j = 1
        while True:
            next_position = (rank, file + j)
            if board.on_board(next_position):
                possible_moves[2].append(next_position)
                j += 1
            else:
                break

        j = -1
        while True:
            next_position = (rank, file + j)
            if board.on_board(next_position):
                possible_moves[3].append(next_position)
                j -= 1
            else:
                break

        i = 1
        j = 1
        while True:
            next_position = (rank + i, file + j)
            if board.on_board(next_position):
                possible_moves[4].append(next_position)
                i += 1
                j += 1
            else:
                break

        i = -1
        j = 1
        while True:
            next_position = (rank + i, file + j)
            if board.on_board(next_position):
                possible_moves[5].append(next_position)
                i -= 1
                j += 1
            else:
                break

        i = 1
        j = -1
        while True:
            next_position = (rank + i, file + j)
            if board.on_board(next_position):
                possible_moves[6].append(next_position)
                i += 1
                j -= 1
            else:
                break

        i = -1
        j = -1
        while True:
            next_position = (rank + i, file + j)
            if board.on_board(next_position):
                possible_moves[7].append(next_position)
                i -= 1
                j -= 1
            else:
                break

        return possible_moves

    def get_moves(self, board, location):
        """"Compute piece possible moves"""
        position_moves = []
        attacking_moves = []

        available_moves = self.__calculate_moves(board, location)

        for direction in available_moves:
            for next_position in direction:
                piece_on = board.get_piece(next_position)
                # is there a piece
                if piece_on is None:
                    position_moves.append(next_position)
                    continue
                # is it another colour
                elif piece_on.get_colour() != self.get_colour():
                    attacking_moves.append(next_position)
                break

        return attacking_moves, position_moves
