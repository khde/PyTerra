

class Objekt():
    def __init__(self, x, y, h, b, textur=None):
        self.x = x
        self.y = y
        self.h = h
        self.b = b
        self.textur = textur
    
    def __str__(self):
        return ("Objekt[{}:{}]".format(self.x, self.y))
        
    def objektkollision(self, objekt, dx=0, dy=0):
        return not (self.x + dx >= objekt.x + objekt.b 
                or self.x + self.b + dx <= objekt.x 
                or self.y + dy >= objekt.y + objekt.h 
                or self.y + self.h + dy <= objekt.y)
    
    def punktkollision(self, x, y):
        pass
        
