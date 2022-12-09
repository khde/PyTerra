import noise
import random
import time
import math

from objekte import feld
from textur import textur

# Chunks: 8192
# Felder: 8388608

CHUNKREIHEN = 32
CHUNKSPALTEN = 32

CHUNKBREITE = CHUNKSPALTEN * feld.FELDDIM
CHUNKHOEHE = CHUNKREIHEN * feld.FELDDIM

# Noch nicht benötigt
RENDERDISTANZ = 4096

WELTCHUNKBREITE = 256
WELTCHUNKHOEHE = 32

WELTCHUNKGRENZEX = WELTCHUNKBREITE * CHUNKBREITE
WELTCHUNKGRENZEY = WELTCHUNKHOEHE * CHUNKHOEHE

"""
WICHTIG! DREH DIE Y-ACHSE UM!!!1!1!!111 KA WIE ABER WICHTIG
https://www.redblobgames.com/maps/terrain-from-noise/
https://rtouti.github.io/graphics/perlin-noise-algorithm
https://accidentalnoise.sourceforge.net/minecraftworlds.html
Beginner friendly: https://gpfault.net/posts/perlin-noise.txt.html
"""


class Welt():
    def __init__(self, fenster, kamera, seed=None):
        self.fenster = fenster
        self.kamera = kamera
        
        random.seed(time.time())
        seed = random.randint(1, 100001)
        self.seed = seed
        
        self.chunks = {}
        self.chunksAktiv = []
        self.wesen = []
        self.projektile = []
        
        self.datenSpeicherung = {
            "chunks": self.chunks,
            "seed": self.seed
        }
        
    def akktualisieren(self):
        for projektil in self.projektile:
            projektil.akktualisieren()
        
        if self.kamera.differenz():
            self.chunksAktiv = []
            for chunk in self.chunksAktiv:
                if not chunk.in_sicht(self.kamera):
                    self.chunksAktiv.remove(chunk)
            
            zx, zy = self.chunk_position(*self.kamera.mitte())
            
            neueChunksPos = []
            neueChunksPos.append((zx, zy))
            neueChunksPos.append((zx+CHUNKBREITE, zy))
            neueChunksPos.append((zx-CHUNKBREITE, zy))
            neueChunksPos.append((zx, zy+CHUNKHOEHE))
            neueChunksPos.append((zx, zy-CHUNKHOEHE))
            neueChunksPos.append((zx+CHUNKBREITE, zy+CHUNKHOEHE))
            neueChunksPos.append((zx+CHUNKBREITE, zy-CHUNKHOEHE))
            neueChunksPos.append((zx-CHUNKBREITE, zy+CHUNKHOEHE))
            neueChunksPos.append((zx-CHUNKBREITE, zy-CHUNKHOEHE))
            
            for chunkPos in neueChunksPos:
                if self.kamera.in_sicht(chunkPos[0], chunkPos[1], CHUNKHOEHE, CHUNKBREITE):
                    self.lade_chunk(chunkPos[0], chunkPos[1])
    
    def zeichnen(self):
        self.fenster.blit(textur.hintergrund, (0, 0))
            
        for chunk in self.chunksAktiv:
            chunk.zeichnen(self.fenster, self.kamera)
            
        for projektil in self.projektile:
            self.fenster.blit(projektil.textur, (projektil.x - self.kamera.x, projektil.y - self.kamera.y))
    def suche_aktive_chunks(self):
        """
        Aktive Chunks sind die, die in Renderdistanz sind
        """
        pass
    
    def aktive_felder(self):
        felder = []
        for chunk in self.chunksAktiv:
            felder.extend(chunk.felder)
        
        return felder
    
    def lade_chunk(self, x, y):
        chunk = self.chunks.get((x, y))
        if chunk:
            self.chunksAktiv.append(chunk)
        else:
            chunk = self.neuer_chunk(x, y)
            if chunk:
                self.chunks[(x, y)] = chunk
    
    def neuer_chunk(self, x, y):
        if not (x < 0 or x >= WELTCHUNKGRENZEX or y < 0 or y >= WELTCHUNKGRENZEY):
            return self.generiere_chunk(x, y)
        else:
            return None
        
    def generiere_chunk(self, x, y):
        oktaven = 8
        amplitude = 15
        frequenz = 0.00022
        oktaven = 3
        
        lacunarity = 1.65
        persistance = 0.47
        
        chunk = Chunk(x, y)
        for y in range(CHUNKSPALTEN):
            yFeld = y * feld.FELDDIM + chunk.y
            for x in range(CHUNKREIHEN):
                # Absolute Position des Feldes in der Welt
                xFeld = x * feld.FELDDIM + chunk.x
                yFeld = y * feld.FELDDIM + chunk.y
                
                texturFeld = None
                nr = 0
                hoehe = 0
                a = amplitude
                f = frequenz
                pn = a * noise.pnoise1(xFeld * f + self.seed) 
                for k in range(1, oktaven+1):
                    # Kanten
                    if pn > 0.93:
                        a = math.pow(a, 1.07)
                    elif pn > 0.90:
                        a = math.pow(a, 1.04)
                        
                    hoehe += a * noise.pnoise1(xFeld * f + self.seed) 
                    hoehe += a * noise.pnoise1(xFeld * f + self.seed) 
                    
                    a *= persistance
                    f *= lacunarity                       
                    
                hoehe = int(round(hoehe))
                hoehe *= feld.FELDDIM
                
                if yFeld - 8 * CHUNKHOEHE >= CHUNKHOEHE - hoehe:
                   texturFeld = textur.feld["stein"]
                   nr = 1
                elif yFeld - 7 * CHUNKHOEHE - CHUNKHOEHE // 2 >= CHUNKHOEHE - hoehe:
                   texturFeld = textur.feld["gras"]
                   nr = 1
                else:
                    nr = 0
                feldNeu = feld.Feld(xFeld, yFeld, nr, texturFeld)
                chunk.felder.append(feldNeu)
            
        return chunk
    
    def chunk_position(self, x, y):
        nx = (x // CHUNKBREITE) * CHUNKBREITE
        ny = (y // CHUNKBREITE) * CHUNKBREITE
        return nx, ny
    
    def setze_feld(self, x, y, nr):
        x = (x // feld.FELDDIM) * feld.FELDDIM
        y = (y // feld.FELDDIM) * feld.FELDDIM
        
        for chunk in self.chunksAktiv:
            for f in chunk.felder:
                if f.x == x and f.y == y:
                    f.textur = textur.feld["stein"]
                    f.nr = nr
    
    def entferne_feld(self, x, y):
        x = (x // feld.FELDDIM) * feld.FELDDIM
        y = (y // feld.FELDDIM) * feld.FELDDIM
        
        for chunk in self.chunksAktiv:
            for f in chunk.felder:
                if f.x == x and f.y == y:
                    f.textur = None
                    f.nr = 0


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
            if feld.textur:
                fenster.blit(feld.textur, (feld.x-kamera.x, feld.y-kamera.y))
        
    def in_sicht(self, kamera):
        return not (self.x >= kamera.x + kamera.b 
                or self.x + CHUNKBREITE <= kamera.x 
                or self.y >= kamera.y + kamera.h 
                or self.y + CHUNKHOEHE <= kamera.y)

