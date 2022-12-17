

class Zustand():
    def __init__(self, spiel, vZustand):
        self.spiel = spiel
        self.vZustand = vZustand  # Vorheriger Zustand
        self.aktiv = True
        self.beende = False  # Wird momentan nicht benötigt, muss unbedingt benutzt werden
    
    def akktualisieren(self, eingabe):
        pass
    
    def zeichnen(self, fenster):
        pass
    
    def aktivieren(self):
        self.aktiv = True
    
    def deaktivieren(self):
        self.aktiv = False
    
    def beenden(self):
        self.spiel.zustaende.remove(self)
        self.beende = True
        if self.vZustand:
            self.vZustand.aktiv = True
