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
        return "Interface"
    
    def neues_element(self, ele):
        self.elemente.append(ele)
    
    def akktualisiere_elemente(self):
        mx, my = pygame.mouse.get_pos()
        
        for ele in self.elemente:
            if ele.click_check(mx, my):
                ele.aktion(self)
    

class InterfaceSpieler(Interface):
    def __init__(self, spiel, vZustand, spieler):
        super().__init__(spiel, vZustand)
        self.spieler = spieler
        
        self.testf = elemente.FarbeElement(550, 20, 50, 350, (102, 102, 102))
        self.neues_element(self.testf)
        
        self.lebensleiste = Lebensleiste(50, 20, 30, 150)
        self.neues_element(self.lebensleiste)
        
    def __str__(self):
        return "Interface Spieler"
    
    def akktualisieren(self, eingabe):
        pass
    
    def zeichnen(self, fenster):
        for ele in self.elemente:
            ele.zeichnen(fenster)


class InterfaceEditor(Interface):
    def __init__(self, spiel, vZustand):
        super().__init__(spiel, vZustand)


class Lebensleiste(elemente.Element):
    def __init__(self, x, y, h, b):
        super().__init__(x, y, h, b)
        self.hg = elemente.FarbeElement(x, y, h, b, (20, 20, 20))
        self.fllng = elemente.FarbeElement(x+5, y+5, h-10, b-10, (255, 255, 255))
        self.fg = elemente.FarbeElement(x+5, y+5, h-10, b-10, (0, 128, 0))
    
    def zeichnen(self, fenster):
        self.hg.zeichnen(fenster)
        self.fllng.zeichnen(fenster)
        self.fg.zeichnen(fenster)

class Inventar(elemente.Element):
    pass

