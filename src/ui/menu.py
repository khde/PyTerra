import pygame
import os
import sys

import zustand
import spielablauf
from textur import textur
from . import elemente
import conf


class Menu(zustand.Zustand):
    def __init__(self, spiel, vZustand):
        super().__init__(spiel, vZustand)
        self.elemente = []
    
    def __str__(self):
        return "Menu"
    
    def neues_element(self, ele):
        self.elemente.append(ele)
    
    def akktualisiere_elemente(self):
        mx, my = pygame.mouse.get_pos()
        
        for ele in self.elemente:
            if ele.click_check(mx, my):
                ele.aktion(self)


class Hauptmenu(Menu):
    def __init__(self, spiel, vZustand):
        super().__init__(spiel, vZustand)
        
        beendenBtn = elemente.BildElement(spiel.breite - 40, 40, textur.beenden_kreuz)
        beendenBtn.setze_aktion(self.beenden)
        self.neues_element(beendenBtn)
        
        spielenBtn = elemente.BildElement(spiel.breite / 2, 300, textur.spielen_knopf)
        spielenBtn.setze_aktion(self.lade_spielmenu)
        self.neues_element(spielenBtn)
    
    def __str__(self):
        return "Hauptmenu"
    
    def akktualisieren(self, eingabe):
        for event in eingabe:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.beenden()
                if event.key == pygame.K_SPACE:
                    self.lade_spielmenu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                links, mitte, rechts = pygame.mouse.get_pressed()
                if links:
                    self.akktualisiere_elemente()
    
    def zeichnen(self, fenster):
        fenster.blit(textur.hauptmenuBG, (0, 0))
        for ele in self.elemente:
            ele.zeichnen(fenster)
    
    def lade_spielmenu(self):
        self.spiel.neuer_zustand(Spielmenu(self.spiel, self))
        self.deaktivieren()
    
    def beende_spiel(self):
        # Für den Beenden-Knopf
        pass


class Spielmenu(Menu):
    def __init__(self, spiel, vZustand):
        super().__init__(spiel, vZustand)
        
        beendenBtn = elemente.BildElement(spiel.breite - 40, 40, textur.beenden_kreuz)
        beendenBtn.setze_aktion(self.beenden)
        self.neues_element(beendenBtn)
        
        weltenpfade = os.listdir(conf.weltenpfad)
        for k, pfad in enumerate(weltenpfade, start=1):
            weltBtn = elemente.BildElement(spiel.breite / 2, 50 + k * 40, textur.feld["fehlend"])
            weltBtn.setze_aktion(self.starte_spiel, conf.weltenpfad + pfad)
            self.neues_element(weltBtn)
            
        neuesSpielBtn = elemente.BildElement(100, 100, textur.emoji)
        neuesSpielBtn.setze_aktion(self.neues_spiel)
        self.neues_element(neuesSpielBtn)
        
        
            
    def __str__(self):
        return "Spielmenu"
    
    def akktualisieren(self, eingabe):
        for event in eingabe:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.beenden()
            if event.type == pygame.MOUSEBUTTONDOWN:
                links, mitte, rechts = pygame.mouse.get_pressed()
                if links:
                    self.akktualisiere_elemente()
    
    def zeichnen(self, fenster):
        fenster.blit(textur.spielermenuBG, (0, 0))
        for ele in self.elemente:
            ele.zeichnen(fenster)
    
    # Sollte lade_spiel heißen
    def starte_spiel(self, pfad):
        if os.path.isfile(pfad):
            self.spiel.neuer_zustand(spielablauf.Spielablauf(self.spiel, self, pfad))
            self.aktiv = False
        else:
            print("Welt existiert nicht: ", pfad)
    
    def neues_spiel(self):
            # Neuem Spiel sollte Name (also pfad) gegeben werden
            pfad = None
            self.spiel.neuer_zustand(spielablauf.Spielablauf(self.spiel, self, pfad))
            self.deaktivieren()

