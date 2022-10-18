import sys
import pygame
from itertools import product


class PrevUI:
    def __init__(self, app, engine, board):
        self.app = app
        self.engine = engine
        self.board = board

        self.screen_width = 120
        self.screen_height = 120
        self.screen = None

        self.bg_color = (0, 0, 0)
        self.white_square_c = (230, 230, 230)
        self.black_square_c = (100, 100, 100)
        self.selected_piece_c = (200, 100, 100)
        self.move_c = (150, 50, 50)
        self.prev_location_c = (0, 0, 0)
        self.prev_move_c = (60, 60, 60)
        self.square_size = min(self.screen_width, self.screen_height) / 8

        self.selected_piece_location = None
        self.previous_location = None
        self.previous_move = None

        self.pawn_promoting = False

        self.initialize_screen()

    def initialize_screen(self):
        """"Initialize Pygame and screen"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Chess")

    def check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.button_press(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.button_release(event)

    def square_index_by_position(self, mouse_pos):
        """"Convert mouse coordinates to rank and file"""
        x, y = mouse_pos
        file = int(x / self.square_size)
        rank = int(y / self.square_size)
        # Convert rank so indexes start from bottom
        rank_inverse = (7 - rank)
        return rank_inverse, file

    def draw_board(self):
        """"Draw board on the screen"""
        for rank, file in product(range(self.board.length()), range(self.board.length())):
            rect = pygame.Rect(file * self.square_size, (7 - rank) * self.square_size,
                               self.square_size, self.square_size)
            indexes_sum = rank + file

            # if sum of a square's indexes is even, then the square is black
            if (indexes_sum % 2) == 0:
                pygame.draw.rect(self.screen, self.black_square_c, rect)
            else:
                pygame.draw.rect(self.screen, self.white_square_c, rect)

            if (rank, file) == self.selected_piece_location:
                self.highlight_square(rank, file, self.selected_piece_c, 0.1)

            if (rank, file) == self.previous_location:
                self.highlight_square(rank, file, self.prev_location_c, 0.1)

            if (rank, file) == self.previous_move:
                self.highlight_square(rank, file, self.prev_move_c, 0.1)

            if not self.pawn_promoting and (rank, file) == self.square_index_by_position(pygame.mouse.get_pos()):
                self.highlight_square(rank, file, self.move_c, 0.1)

    def highlight_square(self, rank, file, colour, border_width_to_size):
        """"Highlight square"""
        border_width = round(self.square_size * border_width_to_size)
        rect = pygame.Rect(file * self.square_size, (7 - rank) * self.square_size,
                           self.square_size, self.square_size)
        pygame.draw.rect(self.screen, colour, rect, border_width)

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
                self.screen.blit(image, rect)

    def update_screen(self):
        """Update images on the screen and flip to the new screen."""
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.bg_color)

        self.draw_board()
        self.draw_pieces()

        if self.pawn_promoting:
            self.display_pawn_promotion_menu()

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def button_press(self, event):
        """"Respond to key presses"""
        # if left click
        if event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if not self.pawn_promoting:
                click_square = self.square_index_by_position(mouse_pos)
                # if no piece to move
                if self.selected_piece_location is None:
                    # take piece
                    self.take_piece(click_square)
                # elif clicking same piece
                elif click_square == self.selected_piece_location:
                    # forget piece to move
                    self.selected_piece_location = None

    def button_release(self, event):
        """"Respond to key release"""
        if not self.pawn_promoting:
            self.game_button_release(event)
        else:
            self.promotion_menu_button_release(event)

    def game_button_release(self, event):
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

    def set_pawn_promotion(self):
        self.pawn_promoting = True

    def clear_pawn_promotion(self):
        self.pawn_promoting = False

    def promotion_menu_button_release(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.button == 1:
            self.define_pawn_promotion(mouse_pos)

        elif event.button == 3:
            self.pawn_promoting = False

    def take_piece(self, location):
        """"Choose piece to move and save it"""
        if self.board.get_piece_legal_moves(location):
            # save location of piece
            self.selected_piece_location = location

    def put_piece(self, new_location):
        """"Change chosen piece location"""
        # if move possible
        attacking_moves, position_moves = self.board.get_piece_legal_moves(self.selected_piece_location)
        piece_moves = attacking_moves + position_moves
        if new_location in piece_moves:
            self.engine.__move_piece(self.board, self.selected_piece_location, new_location)
            self.previous_location = self.selected_piece_location
            self.previous_move = new_location
            self.engine.compute_legal_moves(self.board)
            if self.engine.check_mate(self.board):
                self.app.set_mate()

        # forget moving piece
        self.selected_piece_location = None

    def draw_promotion_window(self):
        border_proportion = 0.4
        border_colour_out = (200, 200, 200)
        border_colour_in = (100, 100, 100)

        # Draw frame
        border_width = round(self.square_size * border_proportion)
        rect = pygame.Rect(self.screen_height / 2 - self.square_size / 2,
                           self.screen_width / 2 - self.square_size * (2 + border_proportion),
                           self.square_size, self.square_size)
        pygame.draw.rect(self.screen, border_colour_out, rect, border_width)

        border_width = round(self.square_size * border_proportion / 2)
        rect = pygame.Rect(self.screen_height / 2 - self.square_size / 2,
                           self.screen_width / 2 - self.square_size * (2 + border_proportion / 2),
                           self.square_size, self.square_size)
        pygame.draw.rect(self.screen, border_colour_in, rect, border_width)

        # Draw squares
        for square_i in range(4):
            rect = pygame.Rect(self.screen_height / 2 - self.square_size / 2,
                               self.screen_width / 2 + self.square_size * (-2 + square_i),
                               self.square_size, self.square_size)
            if (square_i % 2) == 0:
                square_colour = self.black_square_c
            else:
                square_colour = self.white_square_c

            pygame.draw.rect(self.screen, square_colour, rect, border_width)

    def draw_promotion_pieces(self):
        # Get pieces available for promotion
        promotion_pieces = self.engine.possible_pawn_promotions(self.board.current_colour())
        # Draw pieces
        for square_i, piece in promotion_pieces:
            image = piece.get_image()
            rect = image.get_rect()
            # place squares
            rect.centery = self.screen_height / 2
            rect.centerx = self.screen_width / 2 + self.square_size * (-2 + square_i)
            self.screen.blit(image, rect)

    def display_pawn_promotion_menu(self):
        """"Draw promotion options"""
        self.draw_promotion_window()
        self.draw_promotion_pieces()
        #   Highlight piece if mouse on it

    def define_pawn_promotion(self, mouse_pos):
        """"Choose piece promote to"""
        # Define click location
        x, y = mouse_pos
        if y in range(int(self.screen_height / 2 - self.square_size), int(self.screen_height / 2 + self.square_size)):
            piece_index = int((x - 2 * self.square_size) / self.square_size)
            promotion_pieces = self.engine.possible_pawn_promotions(self.board.current_colour())
            if (piece_index >= 0) and (piece_index < len(promotion_pieces)):
                # Promote pawn
                self.engine.promote_pawn(promotion_pieces[piece_index])
                # Reset flag
                self.pawn_promoting = False
