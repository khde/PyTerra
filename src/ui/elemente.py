import pygame

class Element():
    def __init__(self, x, y, h, b, funk=None, args=None, kwargs=None):
        self.x = x
        self.y = y
        self.h = h
        self.b = b
        
        self.funk = funk
        self.args = args
        self.kwargs = kwargs
        
    def aktion(self, menu):
        if self.funk:
            self.funk(*self.args, **self.kwargs)
    
    def setze_aktion(self, funk, *args, **kwargs):
        self.funk = funk
        self.args = args
        self.kwargs = kwargs
    
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
    """
    Die x-y-Koordinaten von eines Instanz werden automatisch berechnet, sodass diese die Koordinaten vom Zentrum des Bildes sind
    """
    def __init__(self, x, y, bild, h=None, b=None, funk=None):
        h = h if h else bild.get_height()
        b = b if b else bild.get_width()
        
        x -= b / 2
        y -= h / 2
        
        super().__init__(x, y, h, b, funk)
        self.bild = bild
    
    def zeichnen(self, fenster):
        fenster.blit(self.bild, (self.x, self.y))


class FarbeElement(Element):
    def __init__(self, x, y, h, b, farbe):
        super().__init__(x, y, h, b)
        self.farbe = farbe
        self.r = pygame.Rect(self.x, self.y, self.b, self.h)
    
    def zeichnen(self, fenster):
        pygame.draw.rect(fenster, self.farbe, self.r)
