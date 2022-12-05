import pygame
import os
import sys
import random

from objekte import feld
from textur import textur

# Chunks: 8192
# Felder: 8388608

CHUNKREIHEN = 32
CHUNKSPALTEN = 32
CHUNKHOEHE = CHUNKREIHEN * feld.FELDDIM
CHUNKBREITE = CHUNKSPALTEN * feld.FELDDIM

WELTCHUNKHOEHE = 5
WELTCHUNKBREITE = 8

#WELTCHUNKHOEHE = 32
#WELTCHUNKBREITE = 256

anzahlFelder = 0

"""
WICHTIG NOCH MACHEN:
WENN CHUNK IN SICHT WÄRE DORT ABER KEINER GELADEN IST, SOLL EIN NEUER GENERIERT WERDEN -> DAS IMPLEMENTIEREN
UND DANN SOLLTE ALLES ANDERE AUCH KLAPPEN (DER CHUNK SOLL MIT DEM NICHT BLOCK AUFGEFÜLLT WERDEN)
"""

class Welt():
    def __init__(self, fenster, kamera, seed=None):
        self.fenster = fenster
        self.kamera = kamera
        
        self.seed = seed
        self.chunks = {}
        self.chunksAktiv = []
        self.wesen = []
        
        self.chunks[(0, 0)] = ChunkTest(0, 0)
        
        print("CHUNKS: ", len(self.chunks))
        print("FELDER: ", anzahlFelder)
        
    def akktualisieren(self):
        neueChunksPos = []
        
        # Suche nach Chunks für die aktive Gruppe
        if self.kamera.differenz():
            for chunk in self.chunksAktiv:
                if not chunk.in_kamera(self.kamera):
                    self.chunksAktiv.remove(chunk)
                    continue
                
            zx, zy = self.chunk_position(self.kamera.x, self.kamera.y)
            
            neueChunksPos.append((zx+CHUNKBREITE, zy))
            neueChunksPos.append((zx-CHUNKBREITE, zy))
            neueChunksPos.append((zx, zy+CHUNKHOEHE))
            neueChunksPos.append((zx, zy-CHUNKHOEHE))
            
            print(zx, zy)
            print(neueChunksPos)
            for chunkPos in neueChunksPos:
                if self.kamera.in_sicht(chunkPos[0], chunkPos[1], CHUNKHOEHE, CHUNKBREITE):
                    print("Chunk in Sicht: ", chunkPos[0], chunkPos[1])
                    #self.lade_chunk(chunkPos[0], chunkPos[1])
                            
    def zeichnen(self):
        #self.fenster.blit(textur.hintergrund, (0, 0))
        for chunk in self.chunksAktiv:
            chunk.zeichnen(self.fenster, self.kamera)
 
    def lade_chunk(self, x, y):
        if x % CHUNKBREITE == 0 and y % CHUNKHOEHE == 0:
            chunk = self.chunks.get((x, y))
            if chunk:
                return chunk
            else:
                print("Chunk nicht in Dict: generiere")
                return self.generiere_chunk(x ,y)   
        
    def generiere_chunk(self, x, y):
        chunk = Chunk(x, y)
        
        for y in range(0, WELTCHUNKHOEHE):
            for x in range(0, WELTCHUNKBREITE):
                xc = x * CHUNKBREITE
                yc = y * CHUNKHOEHE
                
                chunk = ChunkTest(xc, yc)
                
                if chunk.in_kamera(self.kamera):
                    self.chunksAktiv.append(chunk)
        
        return chunk
    
    def chunk_position(self, x, y):
        nx = (x // CHUNKBREITE) * CHUNKBREITE
        ny = (y // CHUNKBREITE) * CHUNKBREITE
        return nx, ny
    
    def neues_feld(self, x, y, feld):
        pass
    
    def setze_feld(self, x, y, feld):
        pass
    
    def entferne_feld(self, x, y):
        pass


class Chunk():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.felder = []
    
    def __str__(self):
        return "Chunk [{}:{}]".format(self.x, self.y)
    
    def akktualisieren(self):
        pass
    
    def zeichnen(self, fenster, kamera):
        for feld in self.felder:
            fenster.blit(feld.textur, (feld.x-kamera.x, feld.y-kamera.y))
        
    def in_kamera(self, kamera):
        return not (self.x >= kamera.x + kamera.b 
                or self.x + CHUNKBREITE <= kamera.x 
                or self.y >= kamera.y + kamera.h 
                or self.y + CHUNKHOEHE <= kamera.y)


class ChunkTest(Chunk):
    def __init__(self, x, y):
        global anzahlFelder
        super().__init__(x, y)
        for y in range(CHUNKSPALTEN):
            y *= feld.FELDDIM
            y += self.y
            for x in range(CHUNKREIHEN):
                x *= feld.FELDDIM
                x += self.x
                self.felder.append(feld.Feld(x, y, 0, textur.feld["fehlend"]))
                anzahlFelder += 1
    
