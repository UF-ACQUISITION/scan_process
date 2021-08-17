:: Activation de l'environnement PDAL
::call F:\mmorin\pdal_activate.bat


::ouverture du e57 structuré et export en n nuages e57
::::::::::::::::MODIF::::::::::::::::
:::::::::nom du fichier e57 structuré à ouvrir::::::::::
F:
cd F:\applications\cloudcompare\v2.12.alpha_bin_x64
CloudCompare.exe -SILENT -AUTO_SAVE OFF -o "F:\mmorin\ndp_tests\kennedy\kennedy.e57" -C_EXPORT_FMT E57 -SAVE_CLOUDS 

::suppression du nuage structuré
::::::::::::::::MODIF::::::::::::::::
:::::::::nom du fichier e57 structuré à supprimer::::::::::
DEl F:\mmorin\ndp_tests\kennedy\kennedy.e57

::vers le dossier contenant les scans bruts issus de Trimble RW
::::::::::::::::MODIF::::::::::::::::
:::::::::nom du repertoire dans lequels les e57 ont été écrits::::::::::
F:
cd F:\mmorin\ndp_tests\kennedy

::conversion des n nuages e57 en n nuages Las1.4
find -type f -name "*.e57" | F:\applications\rush.exe --jobs 20 "pdal pipeline F:\mmorin\ndp_tests\codes\0_pretraitement\open_e57_write_las.json --readers.e57.filename={} --writers.las.filename={.}.las --writers.las.minor_version=4"

::suppression des nuages e57
DEL *.e57

::attribution d'un id unique à chaque point en fonction de son scan dans la dimension OriginId
find -type f -name "*.las" | F:\applications\rush.exe --jobs 20 "pdal pipeline F:/mmorin/ndp_tests/codes/0_pretraitement/open_las_create_OriginID_dimension.json --readers.las.filename={}  --filters.python.script=F:/mmorin/ndp_tests/codes/filtres.python/marquage_obj_mobiles.py --filters.python.function=marquage --filters.python.module=anything --filters.python.add_dimension=OriginId --writers.las.extra_dims="all" --writers.las.minor_version=4 --writers.las.filename={.}.las"

mkdir base_cloud

::::::::::::::::MODIF::::::::::::::::
:::::::::nom du repertoire dans lequels se trouve \base_cloud::::::::::
pdal pipeline F:\mmorin\ndp_tests\codes\0_pretraitement\merge_in_one_las.json

::suppression des nuages las
DEL *.las
cd base_cloud
