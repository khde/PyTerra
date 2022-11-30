try:
    import ujson as json
    print("ujson ist vorhanden und wurde geladen!")
except:
    print("Build-in json Modul importiert!")
    import json
import os

import welt
import spieler


# Muss mit Fehlermeldungen noch besser gemacht werden, anstatt leeres dict zurück zu geben
def spielstand_laden(pfad):
    if os.path.isfile(pfad):
        with open(pfad, "r") as datei:
            spielstand  = json.load(datei)
            spielerObj = json_zu_spieler(spielstand["spieler"])
            weltObj = json_zu_welt(spielstand["welt"])
            
            return {"spieler": spielerObj, "welt": weltObj}

    else:
        print("Welt nicht vorhanden!")  # Das Hauptmenu sollte das zuerst überprüfen
        return {}


def json_zu_spieler(spDict):
    sp = spieler.Spieler(spDict["x"], spDict["y"])
    return sp


def json_zu_welt(wtDict):
    wt = welt.Welt()
    for feld in wtDict["felder"]:
        fx, fy, fnr = feld.split(":")
        wt.neues_feld(int(fx), int(fy), int(fnr))
    print("Felder: ", len(wt.felder))
    wt.init_welt()
    return wt


def spielstand_speichern(spielablauf):
    spielstand = {}
    spielerDict = spieler_zu_json(spielablauf.spieler)
    weltDict = welt_zu_json(spielablauf.welt)
    
    spielstand.update({"spieler": spielerDict})   
    spielstand.update({"welt": weltDict})
    
    jsonSpielstand = json.dumps(spielstand, indent=4)
    
    with open(spielablauf.pfad, "w") as datei:
        datei.write(jsonSpielstand)


def spieler_zu_json(spieler):
    spielerDict = {}
    spielerDict["x"] = spieler.x
    spielerDict["y"] = spieler.y
    
    return spielerDict


def welt_zu_json(welt):
    weltDict = {}
    
    weltDict["felder"] = []
    for feld in welt.felder:
        f = "{}:{}:{}".format(feld.x, feld.y, feld.nr)
        weltDict["felder"].append(f)
    
    return weltDict


