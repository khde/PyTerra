import math

from .objekt import Objekt


class Projektil(Objekt):
    def __init__(self, x, y, h, b, textur, welt):
        super().__init__(x, y, h, b, textur)
        self.welt = welt
        self.geschwindigkeit = 4
        self.mx = 0
        self.my = 0
    
    def akktualisieren(self):
        print(self.x, self.y)
        self.x += self.mx * self.geschwindigkeit
        self.y += self .my * self.geschwindigkeit
    
    def setze_steigung(self, mx, my):
        self.mx += mx
        self.my += my
    

def einheitsvektor(x1, y1, x2, y2):
    x = x2 - x1
    y = y2 - y1
    
    l = math.sqrt(x ** 2 + y ** 2)
    
    ex = x / l
    ey = y / l
    
    return ex, ey
    
