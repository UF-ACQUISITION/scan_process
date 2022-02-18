from grass.pygrass.modules import Module
from grass.pygrass.gis.region import Region
from grass.script import core as grass
from multiprocessing import Process, Lock
import json

with open(input("Entrez le chemin vers votre fichier de config : ")) as jsonFile:
    config = json.load(jsonFile)
    jsonFile.close()

#Verification des valeurs donnees dans le fichier de config
#Retourne True si les valeurs sont coherente
#Retourne False avec un message d'erreur sinon
def check_values():
    config_region = config.get("interpolation").get("g.region")
    config_surf = config.get("interpolation").get("v.surf.rst")

    buffer = config_region.get("grow")
    npmin = config_surf.get("npmin")
    dmin = config_surf.get("dmin")
    segmax = config_surf.get("segmax")
    res3 = config_region.get("res3")

    if(buffer * res3 < npmin):
        print("La valeur grow n'est pas coherente.")
        return False
    elif(segmax > npmin):
        print("La valeur segmax doit etre inferieur a la valeur npmin.")
        return False
    elif(buffer * res3 < npmin * dmin):
        print("La valeur grow doit etre superieure ou egale au produit npmin * dmin.")
        return False
    else:
        return True

#Permet de creer une nouvelle une nouvelle location et un nouveau mapset dans WinGRASS
def create_new_location():
    config_location = config.get("create_new_location")

    #Creation de la location, on passe la base, le nom de la location et la projection souhaitee
    grass.create_location(config_location.get("gisdbase"), config_location.get("location_name"), config_location.get("epsg"))

    #Creation du jeu de carte de la location
    Module("g.mapset",
           flags="c",
           mapset=config_location.get("g.mapset").get("mapset_name"),
           location=config_location.get("location_name"),
           overwrite=True
          )

#Permet d'importer le jeu de donnees a traiter, ici, on importe un nuage de points qui va etre stocke sous la forme d'un vecteur

def import_file():
    config_import = config.get("import_file").get("v.in.lidar")

    #Le flag e permet de mettre la region correspondante a la donnee importee en region par defaut, de ce fait, inutile de recharger la region dans la suite du code
    Module("v.in.lidar",
           flags="tboe",
           input=config_import.get("input"),
           output=config_import.get("output"),
           class_filter=config_import.get("class_filter"),
           overwrite=True
          )

def interpolation(regions, i, nRegion, r, lock):
    config_region = config.get("interpolation").get("g.region")
    config_surf = config.get("interpolation").get("v.surf.rst")

    #On recupere la region par defaut et on calcule la distance entre le nord et le sud et l'est et l'ouest
    xDist = r.east - r.west
    yDist = r.north - r.south

    regions = config.get("parallel").get("regions")

    name = "region_" + str(nRegion)
    elevation = name + "_elevation"

    #Si cette condition est verifiee, la region se trouvera dans la partie haute du jeu de donnees. On ramene donc le sud vers le nord
    if(nRegion < regions/2):
        #Decoupage de la region
        region = Module(
            "g.region",
            vector = config_region.get("vector"), 
            res3 = config_region.get("res3"),
            n = r.north,
            s = r.south + yDist/2,
            e = r.east - (((regions/2 - 1)-i) * (xDist/(regions/2))),
            w = r.west + i * (xDist/(regions/2)),
            grow = config_region.get("grow"),
            save = name,
            overwrite = True
        )

    #Sinon la region se trouvera dans la partie basse du jeu de donnees. On ramene donc le nord vers le sud
    else:
        #Decoupage de la region
        region = Module(
            "g.region",
            vector = config_region.get("vector"), 
            res3 = config_region.get("res"),
            n = r.north - yDist/2,
            s = r.south,
            e = r.east - (((regions/2 - 1)-i) * (xDist/(regions/2))),
            w = r.west + i * (xDist/(regions/2)),
            save = name,
            overwrite = True
        )

    #Interpolation
    Module(
        "v.surf.rst",
        input = config_surf.get("input"),
        elevation = elevation,
        smooth = config_surf.get("smooth"),
        segmax = config_surf.get("segmax"),
        npmin = config_surf.get("npmin"),
        overwrite = True
    )

if __name__ == "__main__":
    valeursOk = check_values()
    #Si les valeurs sont coherentes on execute le code sinon on ne fait rien
    if(valeursOk):
        create_new_location()
        import_file()

        regions = config.get("parallel").get("regions")
        nbProcesses = config.get("parallel").get("nbProcesses")
        processes = []
        decalage = 0
        region = Region()
        lock = Lock()

        #La variable decalage represente le decalage pour obtenir un decoupage de regions qui ont la meme taille
        for r in range(regions):
            if len(processes) < nbProcesses:

                p = Process(target=interpolation, args=(regions, decalage, r, region, lock))
                processes.append(p)
                p.start()

            if decalage < (regions / 2) - 1:
                decalage += 1
            else:
                decalage = 0

            for p in processes:
                if not p.is_alive():
                    processes.remove(p)
                    break