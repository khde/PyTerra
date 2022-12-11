import pygame

from objekte.wesen import Wesen
from objekte.projektil import Projektil, einheitsvektor
from textur import textur
from item import Items, Typ
import inventar

# Einige Werte sollten in Wesen direkt geschrieben werden
# und viel Code in akktualisieren sollte in Funktionen
# ausgelagert werden, die auch in Wesen sind
# Das Drehen der Textur sollte vielleicht nur einmal passieren in __init__ ?a?
### Spieler soll eigene Hitbox haben, Textur soll nicht Kollision bestimmen
# Springen soll durch eine quadratische Funktion dargestellt werden
class Spieler(Wesen):
    def __init__(self, x, y, textur, welt):
        super().__init__(x, y, 60, 30, textur, welt)
        self.links = False
        self.rechts = False
        self.drehen = False
        self.auswahl = 1
        self.aktionLinks = False
        self.aktionRechts = False
        
        self.springen = False
        self.fallen = False
        self.geschwindigkeit = 18
        self.yaMomentan = 0
        self.yaMax = 20
        
        self.inventar = inventar.Inventar()
        self.auswahl = 1
        self.inventar.items[1] = inventar.ItemPlatz(Items.GRAS, Typ.FELD)
        self.inventar.items[2] = inventar.ItemPlatz(Items.DRECK, Typ.FELD)
        self.inventar.items[3] = inventar.ItemPlatz(Items.STEIN, Typ.FELD)
        self.inventar.items[4] = inventar.ItemPlatz(Items.HOLZ, Typ.FELD)
        self.inventar.items[5] = inventar.ItemPlatz(Items.HOLZBRETTER, Typ.FELD)
        self.inventar.items[6] = inventar.ItemPlatz(Items.LAUB, Typ.FELD)
        
        self.datenSpeicherung = {
            "x": self.x,
            "y": self.y,
            "inventar": self.inventar,
            "auswahl": self.auswahl
        }
    
    def akktualisieren(self, kamera):
        dx = 0
        dy = 0
        
        if self.aktionLinks:
            self.aktion_links(kamera.x, kamera.y)
            
        if self.aktionRechts:
            self.aktion_rechts(kamera.x, kamera.y)   
            
        if self.links:
            dx -= self.geschwindigkeit
            self.drehen = True
        if self.rechts:
            dx += self.geschwindigkeit
            self.drehen = False
            
        if self.springen:
            dy -= self.yaMomentan
            self.yaMomentan -= 2
            if self.yaMomentan <= -self.yaMax:
                self.springen = False
        else:
            dy += 10
        
        for feld in self.welt.aktive_felder():
            if feld.nr == 0:
                continue
            # Kollision in x-Richtung
            if self.objektkollision(feld, dx=dx):
                if self.x > feld.x + feld.b:
                    dx = -(self.x - (feld.x + feld.b))
                elif self.x + self.b < feld.x:
                    dx = feld.x - (self.x + self.b)
                else:
                    dx = 0
                    
            # Kollision in y-Richtung
            if self.objektkollision(feld, dy=dy):
                if self.y > feld.y + feld.h:
                    dy = -(self.y - (feld.y + feld.h))
                elif self.y + self.h < feld.y:
                    dy = feld.y - (self.y + self.h)
                else:
                    dy = 0
                    self.springen = False
        
        self.x += dx
        self.y += dy
    
    def zeichnen(self, fenster, kamera):
        tx = pygame.transform.flip(self.textur, self.drehen, False)
        fenster.blit(tx, (self.x - kamera.x , self.y - kamera.y))
    
    def aktion_links(self, dx, dy):
        mx, my = pygame.mouse.get_pos()
        mx += dx
        my += dy
        
        # Nur zu Testzwecken
        aw = self.inventar.items.get(self.auswahl)
        if aw:
            if aw.typ == Typ.FELD:
                self.welt.setze_feld(mx, my, aw.nr)
            
    def aktion_rechts(self, dx, dy):
        mx, my = pygame.mouse.get_pos()
        mx += dx
        my += dy
        
        self.welt.entferne_feld(mx, my)
    
    def spring(self):
        pass
    
    def shoot(self):
        mausX, mausY = pygame.mouse.get_pos()
        
        projektil = Projektil(*self.mitte(), 10, 10, textur.emoji, self.welt)
        ex, ey = einheitsvektor(self.x - self.welt.kamera.x, self.y - self.welt.kamera.y, mausX, mausY)
        projektil.setze_steigung(ex, ey)
        
        self.welt.projektile.append(projektil)

