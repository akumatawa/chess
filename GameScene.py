import pygame
from itertools import product


class GameScene:
    def __init__(self, ui, engine, board):
        self.ui = ui
        self.engine = engine
        self.board = board

        self.square_size = min(self.ui.screen.get_height(), self.ui.screen.get_width()) / 8

        self.white_square_c = (230, 230, 230)
        self.black_square_c = (100, 100, 100)
        self.selected_piece_c = (200, 100, 100)
        self.move_c = (150, 50, 50)
        self.prev_location_c = (0, 0, 0)
        self.prev_move_c = (60, 60, 60)

        self.selected_piece_location = None

    def square_index_by_position(self, mouse_pos):
        """"Convert mouse coordinates to rank and file"""
        x, y = mouse_pos
        file = int(x / self.square_size)
        rank = int(y / self.square_size)
        # Convert rank so indexes start from bottom
        rank_inverse = (7 - rank)
        return rank_inverse, file

    def draw_board(self, mouse_pos):
        """"Draw board on the screen"""
        for rank, file in product(range(self.board.length()), range(self.board.length())):
            rect = pygame.Rect(file * self.square_size, (7 - rank) * self.square_size,
                               self.square_size, self.square_size)
            indexes_sum = rank + file

            # if sum of a square's indexes is even, then the square is black
            if (indexes_sum % 2) == 0:
                pygame.draw.rect(self.ui.screen, self.black_square_c, rect)
            else:
                pygame.draw.rect(self.ui.screen, self.white_square_c, rect)

            if (rank, file) == self.selected_piece_location:
                self.highlight_square(rank, file, self.selected_piece_c, 0.1)

            if (rank, file) == self.ui.previous_location:
                self.highlight_square(rank, file, self.prev_location_c, 0.1)

            if (rank, file) == self.ui.previous_move:
                self.highlight_square(rank, file, self.prev_move_c, 0.1)

            if mouse_pos:
                if (rank, file) == self.square_index_by_position(mouse_pos):
                    self.highlight_square(rank, file, self.move_c, 0.1)

    def highlight_square(self, rank, file, colour, border_width_to_size):
        """"Highlight square"""
        border_width = round(self.square_size * border_width_to_size)
        rect = pygame.Rect(file * self.square_size, (7 - rank) * self.square_size,
                           self.square_size, self.square_size)
        pygame.draw.rect(self.ui.screen, colour, rect, border_width)

    def draw_pieces(self):
        """Draw the pieces at its current location."""
        for rank, file in product(range(self.board.length()), range(self.board.length())):
            # Convert rank so indexes start from bottom
            position = (rank, file)
            piece = self.board.get_piece(position)
            rank_inverse = (7 - rank)
            if piece:
                image = piece.get_image()
                rect = image.get_rect()
                # place squares
                rect.centery = self.square_size / 2 + self.square_size * rank_inverse
                rect.centerx = self.square_size / 2 + self.square_size * file
                self.ui.screen.blit(image, rect)

    def button_release(self, event):
        """"Action when button released"""
        mouse_pos = pygame.mouse.get_pos()
        click_square = self.square_index_by_position(mouse_pos)
        # left click
        if event.button == 1:
            # if exists piece to move
            if self.selected_piece_location is not None:
                # if not clicking the same piece
                if self.selected_piece_location != click_square:
                    self.put_piece(click_square)

        # right click
        elif event.button == 3:
            # forget moving piece
            self.selected_piece_location = None

    def take_piece(self, location):
        """"Choose piece to move and save it"""
        if self.board.get_piece_legal_moves(location):
            # save location of piece
            self.selected_piece_location = location

    def put_piece(self, new_location):
        """"Change chosen piece location"""
        # if move made
        move_done = self.engine.process_move(self.board, self.selected_piece_location, new_location)
        if move_done:
            self.ui.previous_location = self.selected_piece_location
            self.ui.previous_move = new_location

        # forget moving piece
        self.selected_piece_location = None

    def button_press(self, event):
        """"Respond to key presses"""
        # if left click
        if event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            click_square = self.square_index_by_position(mouse_pos)
            # if no piece to move
            if self.selected_piece_location is None:
                # take piece
                self.take_piece(click_square)
            # elif clicking same piece
            elif click_square == self.selected_piece_location:
                # forget piece to move
                self.selected_piece_location = None

    def draw(self, mouse_pos=None):
        """"Display scene"""
        self.draw_board(mouse_pos)
        self.draw_pieces()
