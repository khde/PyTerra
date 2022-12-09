import pygame


class TexturManager():
    """
    TexturManager lädt alle benötigten Texturen (hoffentlich), sodass Modul nur noch importiert werden muss,
    damit auf die Textur zugegriffen werden kann
    """
    def __init__(self):
        self.hauptmenuBG = pygame.image.load("ressourcen/hauptmenu-bg.png")
        self.spielermenuBG = pygame.image.load("ressourcen/spielermenu-bg.png")
        self.beenden_kreuz = pygame.image.load("ressourcen/beenden-kreuz.png")
        self.spielen_knopf = pygame.image.load("ressourcen/spielen-knopf.png")
        
        self.feld = {}
        self.spieler = {}
        self.feld["fehlend"] = pygame.image.load("ressourcen/felder/fehlend.png")
        self.feld["gras"] = pygame.image.load("ressourcen/felder/gras.png")
        self.feld["dreck"] = pygame.image.load("ressourcen/felder/dreck.png")
        self.feld["stein"] = pygame.image.load("ressourcen/felder/stein.png")


        self.spieler["spieler"] = pygame.image.load("ressourcen/spieler1.png")
        self.hintergrund = pygame.image.load("ressourcen/himmel.png")
        
        self.emoji = pygame.image.load("ressourcen/emoji.png")

textur = TexturManager()
