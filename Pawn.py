from Piece import Piece


class Pawn(Piece):
    def __init__(self, colour, picture, moved):
        super().__init__(colour, picture, moved)

    def __calculate_position_moves(self, position):
        """"Return piece moves"""
        colour = self.get_colour()
        rank, file = position
        if colour == "white":
            position_moves = ((rank + 1, file),
                              (rank + 2, file))
        elif colour == "black":
            position_moves = ((rank - 1, file),
                              (rank - 2, file))

        else:
            position_moves = None

        return position_moves

    def __calculate_attacking_moves(self, position):
        """"Return piece position after taking piece to the right"""
        colour = self.get_colour()
        rank, file = position

        if colour == "white":
            attacking_moves = [(rank + 1, file + 1),
                               (rank + 1, file - 1)]

        elif colour == "black":
            attacking_moves = [(rank - 1, file + 1),
                               (rank - 1, file - 1)]

        else:
            attacking_moves = None

        return attacking_moves

    @staticmethod
    def __position_is_possible(board, next_location):
        move_available = False
        # is there board
        if board.on_board(next_location):
            piece_on = board.get_piece(next_location)
            # is there a piece
            if not piece_on:
                move_available = True

        return move_available

    def __attack_is_possible(self, board, next_location):
        """"Add attacking move to the list"""
        move_available = False
        # is there board
        if board.on_board(next_location):
            piece_on = board.get_piece(next_location)
            # is there a piece
            if piece_on:
                # is it of different colour
                if piece_on.get_colour() != self.get_colour():
                    move_available = True
            elif board.get_un_passant_attack() == next_location:
                move_available = True

        return move_available

    def get_moves(self, board, location):
        """"Compute piece possible position moves"""
        position_moves = []
        attacking_moves = []

        forward_position, double_forward_position = self.__calculate_position_moves(location)
        possible_attacking_moves = self.__calculate_attacking_moves(location)

        # Add possible position moves
        if self.__position_is_possible(board, forward_position):
            position_moves.append(forward_position)

            # Double forward available if pawn didn't move
            if not self.is_moved() and self.__position_is_possible(board, double_forward_position):
                position_moves.append(double_forward_position)

        # Add possible attacking moves
        for attack in possible_attacking_moves:
            if self.__attack_is_possible(board, attack):
                attacking_moves.append(attack)

        return attacking_moves, position_moves
