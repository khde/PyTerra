import pygame
import pygame.font

import pyterra
import ui.menu


def main():
    pygame.init()
    pygame.font.init()
    
    spiel = pyterra.PyTerra()
    spiel.neuer_zustand(ui.menu.Hauptmenu(spiel, None))
    
    spiel.start()


if __name__ == "__main__":
    main()
