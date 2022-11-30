from .objekt import Objekt

FELDDIM = 32

FELD_LEER = 0
FELD_GRAS = 1
FELD_DRECK = 2


class Feld(Objekt):
    def __init__(self, x, y, nr, textur=None):
        super().__init__(x, y, FELDDIM, FELDDIM, textur)
        self.nr = nr
