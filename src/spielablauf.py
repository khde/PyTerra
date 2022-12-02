import pygame
import sys

import zustand
import spielstand
import kamera
from ui import interface


# Sollte die Steuerung für den Spieler in den Spieler ausgelagert werden?
class Spielablauf(zustand.Zustand):
    def __init__(self, spiel, vZustand, pfad):
        super().__init__(spiel, vZustand)
        self.pfad = pfad
        self.kamera = kamera.Kamera(self.spiel)
        
        sp = spielstand.spielstand_laden(pfad)
        self.welt = sp["welt"]
        
        self.spieler = sp["spieler"]
        self.spieler.setze_welt(self.welt)
        
        # Nur Temporär, bis eine bessere Lösung gefunden wird
        self.mausLinks = False
        self.mausRechts = False
        
        self.kamera.setze_zielobjekt(self.spieler)
        self.interface = interface.InterfaceSpieler(self.spiel, self)
    
    def __str__(self):
        return "Spielstand " + self.pfad
        
    def akktualisieren(self, eingabe):
        for event in eingabe:
            if event.type == pygame.QUIT:
                self.beende = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.beenden()
                if event.key == pygame.K_r:
                    spielstand.spielstand_speichern(self)
                if event.key == pygame.K_a:
                    self.spieler.links = True
                if event.key == pygame.K_d:
                    self.spieler.rechts = True
                if event.key == pygame.K_w:
                    if not self.spieler.springen:
                        self.spieler.yaMomentan = self.spieler.yaMax
                        self.spieler.springen = True
                if event.key == pygame.K_1:
                    self.spieler.auswahl = 1
                if event.key == pygame.K_2:
                    self.spieler.auswahl = 2
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.spieler.links = False
                if event.key == pygame.K_d:
                    self.spieler.rechts = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                links, mitte, rechts  = pygame.mouse.get_pressed()
                self.spieler.aktionLinks = links
                self.spieler.aktionRechts = rechts
                
            if event.type == pygame.MOUSEBUTTONUP:
                links, mitte, rechts  = pygame.mouse.get_pressed()
                self.spieler.aktionLinks = links
                self.spieler.aktionRechts = rechts
                
        self.spieler.akktualisieren(self.kamera)
        self.welt.akktualisieren()
        self.kamera.akktualisieren()
        self.interface.akktualisieren(eingabe, self.spieler)
    
    def zeichnen(self, fenster):
        self.welt.zeichnen(fenster, self.kamera)
        self.spieler.zeichnen(fenster, self.kamera)
        self.interface.zeichnen(fenster)
