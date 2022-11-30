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


class Hauptmenu(Menu):
    def __init__(self, spiel, vZustand):
        super().__init__(spiel, vZustand)
        self.neues_element(elemente.BildElement(spiel.breite - 80, 20, textur.beenden_kreuz))
        self.neues_element(elemente.BildElement(spiel.breite / 2, 250, textur.spielen_knopf))
    
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
                mx, my = pygame.mouse.get_pos()
        
                for ele in self.elemente:
                    if ele.click_check(mx, my):
                        ele.aktion(self)
    
    def zeichnen(self, fenster):
        fenster.blit(textur.hauptmenuBG, (0, 0))
        for ele in self.elemente:
            ele.zeichnen(fenster)
    
    def lade_spielmenu(self):
        self.spiel.neuer_zustand(Spielmenu(self.spiel, self))
        self.aktiv = False
    
    def beende_spiel(self):
        # Für den Beenden-Knopf
        pass


class Spielmenu(Menu):
    def __init__(self, spiel, vZustand):
        super().__init__(spiel, vZustand)
    
    def __str__(self):
        return "Spielmenu"
    
    def akktualisieren(self, eingabe):
        print("Spielmenu")
        for event in eingabe:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.beenden()
                if event.key == pygame.K_1:
                    self.starte_spiel(conf.weltenpfad + "testwelt1.json")
                if event.key == pygame.K_2:
                    self.starte_spiel(conf.weltenpfad + "testwelt2.json")
                if event.key == pygame.K_3:
                    self.starte_spiel(conf.weltenpfad + "testwelt3.json")
                if event.key == pygame.K_4:
                    self.starte_spiel(conf.weltenpfad + "testwelt4.json")

    def zeichnen(self, fenster):
        fenster.blit(textur.spielermenuBG, (0, 0))
    
    def starte_spiel(self, pfad):
        if os.path.isfile(pfad):
            self.spiel.neuer_zustand(spielablauf.Spielablauf(self.spiel, self, pfad))
            self.aktiv = False
        else:
            print("Welt existiert nicht!")

