:: Chaine de traitement globale
:: Prétraitement: conversion des scans en las et ajout d'un id a chaque point selon la station d'origine. Gestion du dossier
:: Partie 1: segmentation du sol puis du sursol
:: Partie 2: segmentation du sursol
:: Partie 3: classification des objets mobiles dans le sursol
:: Partie 4: classification du sursol


:: Activation de l'environnement PDAL
call F:\mmorin\pdal_activate.bat

:: ##########Pretraitement: attribution à chaque point d'un id selon sa station d'origine##########
::::::::::: Des modifs à faire dans le fichier: chemins à mettre à jour::::::::::
call F:\mmorin\ndp_tests\codes\0_pretraitement\marquage_DOS.bat

REM #############FIN Pretraitement#############
pause

:: ##########Partie 1##########

pdal pipeline F:\mmorin\ndp_tests\codes\1_seg_sol_sursol\Seg_sol_sursol.json
::suppression des fichiers nodes générés par le filtres CSF
DEL *.txt
REM #############FIN PARTIE 1#############
pause

:: ##########Partie 2##########

call F:\mmorin\ndp_tests\codes\2_seg_sursol\seg_sursol.bat
REM #############FIN PARTIE 2#############
pause

:: ##########Partie 3##########

pdal pipeline F:\mmorin\ndp_tests\codes\3_classif_objets_mobiles\classification_objets_mobiles.json
REM #############FIN PARTIE 3#############
pause


:: ##########Partie 4##########

pdal pipeline F:\mmorin\ndp_tests\codes\4.1_classif_veget\calcul_scattering_anisotropy.json
pdal pipeline F:\mmorin\ndp_tests\codes\4.2_classif_sursol\classification_sursol.json
REM #############FIN PARTIE 4#############
::pause
