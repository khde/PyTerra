import pygame
import sys

import conf

# TODO
"""
PRIO:
    -Kamera
    -Spieler mit Gravitation und verbessertem springen (eigene Methode)
        -> Soll alles in Wesen passieren. Der Spieler soll ein Wesen sein das kontrolliert -> Testwesen mit anderer Textur in Welt platzieren
    -Speichern wieder implementieren

-Ich hatte noch nie ein Projekt mit so vielen Namespace Problemen 
-Für den anfang soll der game state so sein, dass das letze Element in der liste self.zustand ist, nur das wird akktualisiert ?? oder variable aktiv beim state ->  gibt an ob dieser state bearbeitet und akktualisiert, gerendert wird
-in ui sollen text und menu und buttons definiert werden usw.
-Es soll zuerst eine Welt in spielstand.py erfoglreich geladen werden und dann eine Instanz eines von zustand.Zustand erschaffen werden (big brain!)
-Instanz von Zustand soll eine Methode für das verlassen haben def on_exit -> Bei spielablauf.py könnte dann das Spiel z.B gespeichert werden
oder ein Menu soll erscheinen
 angezeigt werden
-Texturmanager soll missing texture anzeigen anstatt abzukraten
-Speichern muss vereinfacht werden -> einfach alle Attribute von spieler oder welt klasse die benötigt werden automatisiert irgendwie in json format bringen?
-Kamera soll spieler folgen -> https://www.youtube.com/watch?v=lCcKgUkFwSw
-Eigenschaften wie Springen und Kollisionsberechnung der Spieler-Klasse sollen in die Wesen-Klasse übertragen werden, damit in Zukunft K.I. auch Springen usw. kann
 --> ggf. sollte der Quelltext ungeschrieben werden -> Mehr funktionen die unabhängig nicht in der akktualisieren-Methode sind
-ARTIKEL ZU GAME STATES: http://blog.nuclex-games.com/tutorials/cxx/game-state-management/comment-page-1/
-Texturen: https://api.arcade.academy/en/latest/api/texture.html
-Eigenschaften wie Leben, Position usw. sollte in dict in Wesen-Klasse zusammengefasst werden, damit beliebig viel geladen und gespeichert werden kann egal was es ist
 wahrscheinlich auch in der Objekt-Klasse von Grund auf einfügen
-Kamera soll tatsächlichen differenzwert zurückgeben, damit ich nicht immer Minus dran machen muss -.- (Methode?)

-CHUNKS UNBEDINGT IMPLEMENTIEREN: ES IST EINFACHER DIE CHUCKS ZU FINDEN DIE AUF DEM FENSTER SIND ALS ALLE KACHELN ZU BETRACHTEN !!!111!!
-CHUNKs mit arrays machen? schneller?

-einstellungsmodul für unterschiedliche werte Pfade fensterhoehe, breite usw
-Sollte nich das spiel (PyTerra) das Spiel starten anstatt das Hauptmenu??? neue funktion in PyTerra ajaja
-Zustandsmaschine muss auch dringend überarbeitet werden -> bessere Kontrolle, bessere Verwaltung
-Texturen sollen nur noch über eine Methode vom Textur Manager geholt werden, er gibt bild oder missing bild zurück (try-except ist hier perfekt)
-Welten .json-Dateien sollen komprimiert werden (gzip, bz2, lzma, zlib, tarfile)
Kollision usw Optimieren Berechnung der Distanz zwischen kollidierenden Objekt nicht nötig, da Restbetrag der Bewegung einfach Position des Objekts 
 + oder - Eins ist
-starte pyterra mit Parametern (argparse) wie Welt direkt laden
-Beendent von Pyterra (Klasse) soll besser werden (die self.beenden Variable wird nicht einmal benutzt)
Problem: menu.py importiert spielablauf.py, welches ui.interface importiert, welches menu.py importiert -.-, Denke das ist der Grund für den ImportError Bug mit 
 menu not found
"""

class PyTerra():
    """
    Instanz dieser Klasse ist soll eine Zustandsmaschine sein, die die akktualisieren() 
    und zeichnen()-Methode eines Zustands automatisch aufruft.
    Alle Zustände mit self.aktiv = True werden akktualisiert, nicht nur der oberste 
    auf dem Stapel.
    Ist kein Zustand aktiv, beendet sich das Programm..
    """
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 18)
        self.beenden = False
        self.hoehe = conf.fensterhoehe
        self.breite = conf.fensterbreite
        self.titel = conf.fenstertitel
        self.fps = conf.fps
        self.zustaende = []
        
        self.fenster = pygame.display.set_mode((self.breite, self.hoehe))
        pygame.display.set_caption(self.titel)
        self.clock = pygame.time.Clock()
        
    def start(self):
        while not self.beenden:
            self.fenster.fill((0, 0, 0))
            
            eingaben = pygame.event.get()
            zustandVorhanden = False
            for zustand in self.zustaende:
                if zustand.aktiv:
                    zustand.akktualisieren(eingaben)
                    zustand.zeichnen(self.fenster)
                    zustandVorhanden = True
            
            if not zustandVorhanden:
                print("Kein Zustand vorhanden: -> Verlasse PyTerra")
                self.stop()
            
            self.clock.tick(self.fps) 
            self.zeige_fps()
            pygame.display.update()
    
    def stop(self):
        pygame.quit()
        sys.exit(0)
        
    def neuer_zustand(self, zustand):
        self.zustaende.append(zustand)
    
    def starte_spielablauf(self):
        pass
    
    def zeige_fps(self):
        fps_text = self.font.render(str(self.clock.get_fps()), 1, pygame.Color("coral"))
        self.fenster.blit(fps_text, (10,0))       

