import pygame


class PromotionScene:
    def __init__(self, ui, engine, board):
        self.ui = ui
        self.engine = engine
        self.board = board

        self.square_size = min(self.ui.screen.get_width(), self.ui.screen.get_height()) / 8

        self.white_square_c = (230, 230, 230)
        self.black_square_c = (100, 100, 100)
        self.selected_piece_c = (200, 100, 100)

    def button_press(self, event):
        """Action on button press"""
        pass

    def button_release(self, event):
        """Action on button release"""
        mouse_pos = pygame.mouse.get_pos()
        if event.button == 1:
            self.define_pawn_promotion(mouse_pos)

        elif event.button == 3:
            self.ui.clear_pawn_promotion()

    def draw_window(self, mouse_pos):
        """Display promotion window"""
        border_proportion = 0.2

        # Draw frame
        border_colour_out = (20, 20, 20)
        border_width = round(self.square_size * border_proportion)
        rect = pygame.Rect(self.ui.screen.get_width() / 2 - (2 * self.square_size + border_width),
                           self.ui.screen.get_height() / 2 - (self.square_size / 2 + border_width),
                           4 * self.square_size + 2 * border_width,
                           self.square_size + 2 * border_width)
        pygame.draw.rect(self.ui.screen, border_colour_out, rect, border_width)

        # Draw squares
        for square_i in range(4):
            rect = pygame.Rect(self.ui.screen.get_width() / 2 + self.square_size * (-2 + square_i),
                               self.ui.screen.get_height() / 2 - self.square_size / 2,
                               self.square_size, self.square_size)
            if (square_i % 2) != 0:
                square_colour = self.black_square_c
            else:
                square_colour = self.white_square_c

            pygame.draw.rect(self.ui.screen, square_colour, rect, border_width)

        # Highlight square
        if mouse_pos:
            square_i = self.define_square(mouse_pos)
            if square_i is not None:
                if square_i in range(4):
                    border_width = round(self.square_size * 0.1)
                    rect = pygame.Rect(self.ui.screen.get_width() / 2 + self.square_size * (-2 + square_i),
                                       self.ui.screen.get_height() / 2 - self.square_size / 2,
                                       self.square_size, self.square_size)
                    pygame.draw.rect(self.ui.screen, self.selected_piece_c, rect, border_width)

    def define_square(self, mouse_pos):
        """Define which square is mouse on"""
        x, y = mouse_pos
        if y in range(int((self.ui.screen.get_height() - self.square_size) / 2),
                      int((self.ui.screen.get_height() + self.square_size) / 2)):
            square_index = int((x - (self.ui.screen.get_width() / 2 - 2 * self.square_size)) / self.square_size)
        else:
            square_index = None

        return square_index

    def draw_pieces(self):
        """Display pieces on the scene"""
        # Get pieces available for promotion
        promotion_pieces = self.engine.possible_pawn_promotions(self.board.current_colour())
        # Draw pieces
        for square_i, piece in enumerate(promotion_pieces):
            image = piece.get_image()
            rect = image.get_rect()
            # place squares
            rect.centery = self.ui.screen.get_height() / 2
            rect.centerx = self.ui.screen.get_width() / 2 + self.square_size * (-1.5 + square_i)
            self.ui.screen.blit(image, rect)

    def define_pawn_promotion(self, mouse_pos):
        """Choose piece promote to"""
        # Define click location
        piece_index = self.define_square(mouse_pos)
        if piece_index:
            promotion_pieces = self.engine.possible_pawn_promotions(self.board.current_colour())
            if (piece_index >= 0) and (piece_index < len(promotion_pieces)):
                # Set previous move
                self.ui.previous_move = self.engine.promotion_move
                # Set previous location
                self.ui.previous_location = self.engine.promotion_location
                # Promote pawn
                self.engine.promote_pawn(self.board, promotion_pieces[piece_index])
                # Reset flag
                self.ui.clear_pawn_promotion()

    def draw(self, mouse_pos=None):
        """Display scene"""
        self.draw_window(mouse_pos)
        self.draw_pieces()
