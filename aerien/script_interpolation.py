from grass.pygrass.modules import Module
from grass.pygrass.gis.region import Region
from grass.script import core as grass
from multiprocessing import Process, Pool
import json
import time

import queue

with open("D:\\Documents\\GitHub\\scan_process\\aerien\\config_dev.json") as jsonFile:
    config = json.load(jsonFile)
    jsonFile.close()

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
    grass.create_location(config_location.get("gisdbase"), config_location.get("location_name"), config_location.get("epsg"))
    Module("g.mapset",
           flags="c",
           mapset=config_location.get("g.mapset").get("mapset_name"),
           location=config_location.get("location_name"),
           overwrite=True
          )

#Permet d'importer le jeu de donnees a traiter, ici, on importe un nuage de points qui va etre stocke sous la forme d'un vecteur
def import_file():
    config_import = config.get("import_file").get("v.in.lidar")
    Module("v.in.lidar",
           flags="tboe",
           input=config_import.get("input"),
           output=config_import.get("output"),
           class_filter=config_import.get("class_filter"),
           overwrite=True
          )


def enQueue_regions(regions, i, nRegion, queue):
    config_region = config.get("interpolation").get("g.region")
    config_surf = config.get("interpolation").get("v.surf.rst")
    config_gdal = config.get("interpolation").get("r.out.gdal")

    r = Region()

    xDist = r.east - r.west
    yDist = r.north - r.south
    name = "region_" + str(nRegion)

    regions = config.get("parallel").get("regions")

    #Partie superieure du jeu de donnees
    if(nRegion < regions/2):
        #Decoupage de la region
        region = Module(
            "g.region",
            flags = "u",
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

    #Partie inferieure du jeu de donnees
    else:
        #Decoupage de la region
        region = Module(
            "g.region",
            flags = "u",
            vector = config_region.get("vector"), 
            res3 = config_region.get("res"),
            n = r.north - yDist/2,
            s = r.south,
            e = r.east - (((regions/2 - 1)-i) * (xDist/(regions/2))),
            w = r.west + i * (xDist/(regions/2)),
            grow = config_region.get("grow"),
            save = name,
            overwrite = True
        )

    queue.put(name)

def interpolation(nomRegion):
    config_region = config.get("interpolation").get("g.region")
    config_surf = config.get("interpolation").get("v.surf.rst")
    config_gdal = config.get("interpolation").get("r.out.gdal")


    regions = config.get("parallel").get("regions")


    r = Region()

    xDist = r.east - r.west
    yDist = r.north - r.south

    Module(
        "g.region",
        flags = "du",
        region = nomRegion
    )

    #Interpolation
    Module(
        "v.surf.rst",
        input = config_surf.get("input"),
        elevation = nomRegion + "_elevation",
        smooth = config_surf.get("smooth"),
        segmax = config_surf.get("segmax"),
        npmin = config_surf.get("npmin"),
        overwrite = True
    )

    #Enregistrement des regions interpolees en .tif
    Module(
        "r.out.gdal",
        input = nomRegion + "_elevation",
        output = config_gdal.get("output") + nomRegion + "_output.tif",
        format = config_gdal.get("format"),
        overwrite = True
    )

if __name__ == "__main__":
    valuesOk = check_values()
    if(valuesOk):
        #create_new_location()
        #import_file()

        regions = config.get("parallel").get("regions")
        nbProcesses = config.get("parallel").get("nbProcesses")
        processes = []
        i = 0

        q = queue.Queue()

        for r in range(regions):
            enQueue_regions(regions, i, r, q)
            if i < (regions / 2) - 1:
                i += 1
            else:
                i = 0

        while not q.empty():
            for i in range(nbProcesses):
                p = Process(target=interpolation, args=(q.get(),))
                processes.append(p)
                p.start()

            for p in processes:
                p.join()