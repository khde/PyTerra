import pygame
import pygame.font


class Element():
    def __init__(self, x, y, h, b):
        self.x = x
        self.y = y
        self.h = h
        self.b = b
        
    def aktion(self, menu):
        pass
    
    def click_check(self, mx, my):
        if mx > self.x and mx < self.x + self.b \
        and my > self.y and my < self.y + self.h:
            return True
        else:
            return False


class TextElement(Element):
    def __init__(self, x, y, h, b, text):
        super().__init__(x, y, h, b)
        self.text = text


class BildElement(Element):
    def __init__(self, x, y, bild, h=None, b=None):
        h = h if h else bild.get_height()
        b = b if b else bild.get_width()
        
        x -= b / 2
        y -= h / 2
        
        super().__init__(x, y, h, b)
        self.bild = bild
    
    def zeichnen(self, fenster):
        fenster.blit(self.bild, (self.x, self.y))

