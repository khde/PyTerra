import pygame
import os

from objekte import feld
from textur import textur


class Welt():
    def __init__(self):
        self.felder = []
        self.wesen = []
        
    def laden(self):
        pass
    
    def init_welt(self):
        for feld in self.felder:
            self.setze_feldtextur(feld)
    
    def akktualisieren(self):
        pass
    
    def zeichnen(self, fenster, kamera):
        fenster.blit(textur.hintergrund, (0, 0))
        
        for feld in self.felder:
            fenster.blit(feld.textur, (feld.x + kamera.x, feld.y + kamera.y))
    
    def setze_feldtextur(self, feld):
        if feld.nr == 0:
            feld.textur = textur.feld["fehlend"]
        elif feld.nr == 1:
            feld.textur = textur.feld["gras"]
        elif feld.nr == 2:
            feld.textur = textur.feld["dreck"]
        
    def neues_feld_platzieren(self, x, y, nr):
        """
        Platziert ein neues Feld in die Welt, welches ein Vielfaches
        von FELDDIM ist und nur wenn an dieser Position kein anderes 
        Feld ist. Bei Erfolg gibt True zurück, anderenfalls False.
        """
        x = (x // feld.FELDDIM) * feld.FELDDIM
        y = (y // feld.FELDDIM) * feld.FELDDIM
        
        for f in self.felder:
            if f.x == x and f.y == y:
                print("Platzieren kollision: {}:{} und {}:{}".format(f.x, f.y, x, y))
                return False
        
        self.neues_feld(x, y, nr)
        return True
    
    def neues_feld(self, x, y, nr):
        """
        !!! GEFAHR !!!
        Erstellt ein neues Feld an der x-y-Koordinate.
        Sollte nur beim Laden benutzt werden, da nicht auf ein Vielfaches
        von FELDDIM geprüft wird.
        """
        fd = feld.Feld(x, y, nr)
        self.setze_feldtextur(fd)
        self.felder.append(fd)
        
        # print("Neues Feld {}|{}".format(x, y))
    
    def entferne_feld(self, x, y):
        """
        Entfernt ein Feld mit angegebener x-y-Position.
        Bei Erfolg gibt True zurück, anderenfalls False.
        """
        x = (x // feld.FELDDIM) * feld.FELDDIM
        y = (y // feld.FELDDIM) * feld.FELDDIM
        
        for f in self.felder:
            if f.x == x and f.y == y:
                self.felder.remove(f)
                return True
            
        return False


class Chunk():
    def __init__(self):
        pass
    
