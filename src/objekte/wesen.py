from .objekt import Objekt


class Wesen(Objekt):
    def __init__(self, x, y, h, b, textur, welt):
        super().__init__(x, y, h, b, textur)
        self.welt = welt
        self.geschwindigkeit = 0
    
    def akktualisieren(self):
        pass
    
    def zeichnen(self):
        pass

