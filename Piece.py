import pygame
import abc


class Piece:

    def __init__(self, colour=None, image_filename=None, moved=None):
        self.colour = colour
        self.image = pygame.image.load(image_filename)
        self.moved = moved

    def get_colour(self):
        """"Get piece colour"""
        return self.colour

    def get_image(self):
        """"Get piece image"""
        return self.image

    def is_moved(self):
        """"Return information about has been piece moved or not"""
        return self.moved

    @abc.abstractmethod
    def get_moves(self, board, location):
        """"Get piece moves"""
        return
