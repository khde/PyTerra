import pygame
import sys

import zustand
import spielstand
import kamera
from ui import interface
from textur import textur

import spieler
import welt


class Spielablauf(zustand.Zustand):
    def __init__(self, spiel, vZustand, pfad):
        super().__init__(spiel, vZustand)
        self.pfad = pfad
        self.kamera = kamera.Kamera(0, 0, spiel.hoehe, spiel.breite)
        
        #sp = spielstand.spielstand_laden(pfad)
        #self.welt = sp["welt"]
        self.welt = welt.Welt(self.spiel.fenster, self.kamera)
        self.spieler = spieler.Spieler(100, 8300, textur.spieler["spieler"],  self.welt)
        
        self.kamera.setze_position(self.spieler.x, self.spieler.y)
        self.kamera.setze_ziel(self.spieler)
        
        self.interface = interface.InterfaceSpieler(self.spiel, self, self.spieler)
        self.spiel.neuer_zustand(self.interface)
        
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
                    if not self.spieler.springen:
                        self.spieler.yaMomentan = self.spieler.yaMax
                        self.spieler.springen = True
                if event.key == pygame.K_s:
                    self.spieler.y += 150
                if event.key == pygame.K_a:
                    self.spieler.links = True
                if event.key == pygame.K_d:
                    self.spieler.rechts = True            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.spieler.links = False
                if event.key == pygame.K_d:
                    self.spieler.rechts = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                links, mitte, rechts = pygame.mouse.get_pressed()
                if links:
                    self.spieler.aktionLinks = True
                if rechts:
                    self.spieler.aktionRechts = True
            if event.type == pygame.MOUSEBUTTONUP:
                links, mitte, rechts = pygame.mouse.get_pressed()
                if not links:
                    self.spieler.aktionLinks = False
                if not rechts:
                    self.spieler.aktionRechts = False
                pass
        
        self.spieler.akktualisieren(self.kamera)
        self.welt.akktualisieren()
        self.kamera.akktualisieren()
        self.interface.akktualisieren(eingabe)
    
    def zeichnen(self, fenster):
        self.welt.zeichnen()
        self.spieler.zeichnen(fenster, self.kamera)
        self.interface.zeichnen(fenster)
    
    def beenden(self):
        self.spiel.zustaende.remove(self.interface)
        super().beenden()

