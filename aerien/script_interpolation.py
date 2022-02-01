from grass.pygrass.modules import Module

from grass.script import core as grass



import json

with open(input("Veuillez entrer le chemin de votre fichier de configuration : ")) as jsonFile:

    config = json.load(jsonFile)

    jsonFile.close()


def create_new_location():

    config_location = config.get("create_new_location")


    grass.create_location(config_location.get("gisdbase"), config_location.get("location_name"), config_location.get("epsg"))

    Module("g.mapset",
           flags="c",
           mapset=config_location.get("g.mapset").get("mapset_name"),
           location=config_location.get("location_name")
          )

def import_file():

    config_import = config.get("import_file").get("v.in.lidar")


    Module("v.in.lidar",
           flags="tbo",
           input=config_import.get("input"),
           output=config_import.get("output"),
           class_filter=config_import.get("class_filter"),
           overwrite=True
          )

def interpolation():

    config_region = config.get("interpolation").get("g.region")

    config_surf = config.get("interpolation").get("v.surf.rst")

    config_gdal = config.get("interpolation").get("r.out.gdal")


    Module("g.region",
           vector=config_region.get("vector"),
           res=config_region.get("res")
          )


    Module("v.surf.rst",
           input=config_surf.get("input"),
           elevation=config_surf.get("elevation"),
           smooth=config_surf.get("smooth"),
           dmin=config_surf.get("dmin"),
           segmax=config_surf.get("segmax"),
           npmin=config_surf.get("npmin"),

           overwrite=True
          )


    Module("r.out.gdal",
           input=config_gdal.get("input"),
           output=config_gdal.get("output"),
           format=config_gdal.get("format"),

           overwrite=True
          )

if __name__ == "__main__":
    create_new_location()
    import_file()
    interpolation()