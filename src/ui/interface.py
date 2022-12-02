import pygame

import zustand
from . import elemente
from textur import textur
import conf


class Interface(zustand.Zustand):
    """
    Ein Quasi umbenanntes Menu, damit es keine ImportError gibt
    """
    def __init__(self, spiel, vZustand):
        super().__init__(spiel, vZustand)
        self.elemente = []
    
    def __str__(self):
        return "Menu"
    
    def neues_element(self, ele):
        self.elemente.append(ele)
    
    def akktualisiere_elemente(self):
        mx, my = pygame.mouse.get_pos()
        
        for ele in self.elemente:
            if ele.click_check(mx, my):
                ele.aktion(self)
    

class InterfaceSpieler(Interface):
    def __init__(self, spiel, vZustand):
        super().__init__(spiel, vZustand)
    
    def akktualisieren(self, eingabe, spieler):
        pass
    
    def zeichnen(self, fenster):
        fenster.blit(textur.feld["fehlend"], (0, 0))


class InterfaceEditor(Interface):
    def __init__(self, spiel, vZustand):
        super().__init__(spiel, vZustand)

