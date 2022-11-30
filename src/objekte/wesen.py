from .objekt import Objekt


class Wesen(Objekt):
    def __init__(self, x, y, h, b, textur=None, welt=None):
        super().__init__(x, y, h, b, textur)
        self.welt = welt
        self.geschwindigkeit = 0
    
    def setze_welt(self, welt):
        self.welt = welt
    
    def akktualisieren(self):
        pass
    
    def zeichnen(self):
        pass
