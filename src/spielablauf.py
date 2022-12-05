import pygame
import sys

import zustand
import spielstand
import kamera
from ui import interface

import spieler
import welt


class Spielablauf(zustand.Zustand):
    def __init__(self, spiel, vZustand, pfad):
        super().__init__(spiel, vZustand)
        self.pfad = pfad
        self.kamera = kamera.Kamera(4000, 4000, spiel.hoehe, spiel.breite)
        
        #sp = spielstand.spielstand_laden(pfad)
        #self.welt = sp["welt"]
        self.welt = welt.Welt(self.spiel.fenster, self.kamera)
        
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
                if event.key == pygame.K_w:
                    self.kamera.y -= 150
                if event.key == pygame.K_s:
                    self.kamera.y += 150 
                if event.key == pygame.K_a:
                    self.kamera.x -= 150
                if event.key == pygame.K_d:
                    self.kamera.x += 150
        
        #self.spieler.akktualisieren(self.kamera)
        self.welt.akktualisieren()
        self.kamera.akktualisieren()
        #self.interface.akktualisieren(eingabe, self.spieler)
    
    def zeichnen(self, fenster):
        self.welt.zeichnen()
        #self.spieler.zeichnen(fenster, self.kamera)
        #self.interface.zeichnen(fenster)
