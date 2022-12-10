import item


# Soll Methode bereitstellen, die sagt, ob Key an Stelle im Dict Item oder nichts ist
class Inventar():
    def __init__(self):
        self.items = {}
        self.maxItems = 50
    

class ItemPlatz():
    def __init__(self, nr, typ, anzahl=1):
        self.typ = typ
        self.nr = nr
        self.anzahl = 1
