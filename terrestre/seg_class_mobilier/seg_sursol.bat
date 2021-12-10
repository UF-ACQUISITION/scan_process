:: calcul du nb de voisins sous Cloudcompare puis clustering spatial sous PDAL

::::::::::::::::MODIF::::::::::::::::
:::::::::nom du fichier Las à ouvrir::::::::::
:: ligne de commande cloudcompare  //\\-o nuage en entrée//\\
:: calcul du nombre de voisins d'un point dans une sphere de 0.3m de diamètre
F:\applications\cloudcompare\v2.12.alpha_bin_x64\CloudCompare.exe -SILENT -AUTO_SAVE OFF -o "__tmp__.las" -DENSITY 0.3 -TYPE KNN -C_EXPORT_FMT LAS -SAVE_CLOUDS FILE "__tmp__.las"


:: pipeline qui permet de faire le clustering spatial avec prise en coimpte de la densité (materialisee par le nb de voisin dans une sphere de rayon donne)
:: pipeline qui permet de modifier la classe des clusters non relies au sol a 32
pdal pipeline F:\mmorin\ndp_tests\codes\2_seg_sursol\pipe_seg_sursol.json --readers.las.filename=__tmp__.las --readers.las.extra_dims="Number of neighbors (r_0.3) = int64_t, OriginId = float" --filters.cluster.where="(Classification==1) && (Number_of_neighbors__r_0_3_ > 20)" --filters.cluster.tolerance="0.30" --filters.cluster.min_points="100" --filters.hag_nn.count="10" --filters.python.where="(ClusterID != 0)" --filters.python.script="F:/mmorin/ndp_tests/codes/filtres.python/flying_cluster.py" --filters.python.function="flying_cluster" --filters.python.module="anything" --writers.las.extra_dims="ClusterID = int64_t, OriginId = float, HeightAboveGround = double" --writers.las.filename="__tmp__.las" --writers.las.minor_version="4"