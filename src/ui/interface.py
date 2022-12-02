import pygame

import zustand
from textur import textur
from . import elemente
import conf

class Interface(zustand.Zustand):
    def __init__(self, spiel, vZustand):
        super().__init__(spiel, vZustand)
        
