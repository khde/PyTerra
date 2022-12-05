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
-Nur nach neuen Chunks suchen, wenn Kamera oder was auch die Sicht beeinflusst verändert wird.
 Sonst nur andere Weltenlogik machen, aber nach keinen neuen Chunks suchen
"""

class Welt():
    def __init__(self, fenster, kamera):
        self.fenster = fenster
        self.kamera = kamera
        
        self.chunks = {}
        self.chunksAktiv = []
        self.wesen = []
        
        ### Test
        for y in range(0, WELTCHUNKHOEHE):
            for x in range(0, WELTCHUNKBREITE):
                xc = x * CHUNKBREITE
                yc = y * CHUNKHOEHE
                
                chunk = ChunkTest(xc, yc)
                self.neuer_chunk(chunk)
                
                if chunk.in_kamera(self.kamera):
                    self.chunksAktiv.append(chunk)
        ### Testcode ende
        
        print("CHUNKS: ", len(self.chunks))
        print("FELDER: ", anzahlFelder)
        
    def akktualisieren(self):
        neueChunks = []
        
        # Suche nach Chunks für die aktive Gruppe
        if self.kamera.differenz():
            if self.chunksAktiv:
                for chunk in self.chunksAktiv:
                    if not chunk.in_kamera(self.kamera):
                        self.chunksAktiv.remove(chunk)
                        continue
                    
                    neueChunks.append(self.chunks.get((chunk.x+CHUNKBREITE, chunk.y)))
                    neueChunks.append(self.chunks.get((chunk.x-CHUNKBREITE, chunk.y)))
                    neueChunks.append(self.chunks.get((chunk.x, chunk.y+CHUNKHOEHE)))
                    neueChunks.append(self.chunks.get((chunk.x, chunk.y-CHUNKHOEHE)))
                    neueChunks.append(self.chunks.get((chunk.x+CHUNKBREITE, chunk.y+CHUNKHOEHE)))
                    neueChunks.append(self.chunks.get((chunk.x-CHUNKBREITE, chunk.y-CHUNKHOEHE)))
                    neueChunks.append(self.chunks.get((chunk.x+CHUNKBREITE, chunk.y-CHUNKHOEHE)))
                    neueChunks.append(self.chunks.get((chunk.x-CHUNKBREITE, chunk.y+CHUNKHOEHE)))
                    
                    for chunk in neueChunks:
                        if chunk:
                            if chunk.in_kamera(self.kamera) and chunk not in self.chunksAktiv:
                                self.chunksAktiv.append(chunk)
            else:
                chunks = self.chunks.values()
                for chunk in chunks:
                    if chunk.in_kamera(self.kamera):
                        self.chunksAktiv.append(chunk)
        
    def zeichnen(self):
        self.fenster.blit(textur.hintergrund, (0, 0))
        for chunk in self.chunksAktiv:
            chunk.zeichnen(self.fenster, self.kamera)
    
    def neuer_chunk(self, chunk):
        if chunk.x % CHUNKBREITE == 0 and chunk.y % CHUNKHOEHE == 0:
            self.chunks[(chunk.x, chunk.y)] = chunk
        else:
            print("Chunk: Fehlerhafte x-y-Koordinaten")
    
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
                self.felder.append(feld.Feld(x, y, 0, textur.feld["gras"]))
                anzahlFelder += 1
    
