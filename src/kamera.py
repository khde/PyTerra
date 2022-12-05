

class Kamera():
    def __init__(self, x, y, h, b):
        self.x = x
        self.y = y
        
        # Vorherige Koordinaten
        self.vx = self.x
        self.vy = self.y
        
        self.h = h
        self.b = b
    
    def akktualisieren(self):
        self.vx = self.x
        self.vy = self.y
    
    def in_sicht(self, x, y, h, b):
        pass
    
    def differenz(self):
        return not (self.x == self.vx and self.y == self.vy)
        
