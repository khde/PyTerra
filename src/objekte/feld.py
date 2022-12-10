from .objekt import Objekt

FELDDIM = 32

"""
Renewable 	

Yes
Stackable 	

Yes (64)
Tool 	

Blast resistance 	

1,200
Hardness 	

50
Luminant 	

No
Transparent 	

No
Flammable 	

No
Catches fire from lava 	

"""


class Feld(Objekt):
    def __init__(self, x, y, nr, textur=None):
        super().__init__(x, y, FELDDIM, FELDDIM, textur)
        self.nr = nr
        self.kollision = False
