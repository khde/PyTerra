

class Kamera():
    def __init__(self, spiel, zielobjekt=None):
        self.spiel = spiel
        self.zielobjekt = zielobjekt
        
        objekthalbx = 0
        objekthalby = 0
        
        if zielobjekt:
            objekthalbx = int(zielobjekt.breite / 2)
            objekthalby = int(zielobjekt.hoehe / 2)
        
        self.fenstermittex = int(self.spiel.breite / 2)  + objekthalbx
        self.fenstermittey = int(self.spiel.hoehe / 2) + objekthalby
        
        self.x = 0
        self.y = 0
    
    def setze_zielobjekt(self, zielobjekt):
        self.zielobjekt = zielobjekt
        
        objekthalbx = int(zielobjekt.b / 2)
        objekthalby = int(zielobjekt.h / 2)
        
        self.fenstermittex = int(self.spiel.breite / 2) - objekthalbx
        self.fenstermittey = int(self.spiel.hoehe / 2) - objekthalby
    
    def akktualisieren(self):
        if self.zielobjekt:
            self.x = -self.zielobjekt.x + self.fenstermittex
            self.y = -self.zielobjekt.y + self.fenstermittey
