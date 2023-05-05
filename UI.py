import sys
import pygame

from GameScene import GameScene
from PromotionScene import PromotionScene


class UI:
    def __init__(self, app, engine, board):
        self.app = app
        self.engine = engine
        self.board = board

        self.screen = None
        self.screen_width = 120  # 120 or 480
        self.screen_height = 120  # 120 or 480
        self.bg_color = (0, 0, 0)

        self.scenes = {}
        self.active_scenes = []

        self.previous_move = None
        self.previous_location = None

        self.initialize_screen()
        self.initialize_scenes()

    def initialize_screen(self):
        """"Initialize Pygame and screen"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Chess")

    def initialize_scenes(self):
        """"Create scenes to use during game"""
        self.scenes['game'] = GameScene(self, self.engine, self.board)
        self.scenes['promotion'] = PromotionScene(self, self.engine, self.board)

        self.active_scenes.append(self.scenes['game'])

    def check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.button_press(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.button_release(event)

    def update_screen(self):
        """Update images on the screen and flip to the new screen."""
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.bg_color)

        # Draw underlying scenes
        if len(self.scenes) > 1:
            for scene in self.active_scenes[:-1]:
                scene.draw()

        # Draw input scene
        self.active_scenes[-1].draw(pygame.mouse.get_pos())

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def button_press(self, event):
        """"Respond to key press"""
        self.active_scenes[-1].button_press(event)

    def button_release(self, event):
        """"Respond to key release"""
        self.active_scenes[-1].button_release(event)

    def set_pawn_promotion(self):
        """"Add promotion scene to active scenes"""
        self.active_scenes.append(self.scenes['promotion'])

    def clear_pawn_promotion(self):
        """"Remove promotion scene from active scenes"""
        self.active_scenes.remove(self.scenes['promotion'])

    def set_mate(self):
        """"End of the game"""
        self.app.set_mate()
