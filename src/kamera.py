

class Kamera():
    def __init__(self, x, y, h, b):
        self.x = x
        self.y = y
        
        # Vorherige Koordinaten
        self.vx = self.x
        self.vy = self.y
        
        self.h = h
        self.hhalb = h // 2
        
        self.b = b
        self.bhalb = b // 2
        
    def akktualisieren(self):
        self.vx = self.x
        self.vy = self.y
    
    def in_sicht(self, x, y, h, b):
        return not (self.x >= x + b 
                or self.x + b <= x 
                or self.y >= y + h 
                or self.y + h <= y)
    
    def differenz(self):
        return not (self.x == self.vx and self.y == self.vy)
    
    def mitte(self):
        return self.x + self.bhalb, self.y + self.hhalb
