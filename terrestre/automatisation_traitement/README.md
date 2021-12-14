# automatisation_scan_terrestre

Le but de ce script est d'automatiser une chaîne de traitement de nuages de points afin d'y enlever le bruit.

## Script

Le fichier automatisation_scan_terrestre.py contient le code exécutable. On y retrouve plusieurs fonctions qui remplissent des tâches précises.

##### e57tolas

La fonction e57tolas permet de convertir un fichier avec l'extension e57 en un fichier avec l'extension laz. Pour se faire, on utilise l'exécutable e572las et la bibliothèque subprocess qui permet d'effectuer des commandes bash directement depuis python. Ce fichier .laz sera ensuite utilisé pour le traitement du nuage.

##### removeNoise

La fonction removeNoise permet de retirer le bruit d'un nuage de points. On utilise dans celle ci la bibliothèque CloudComPy, une bibliothèque python pour le traitement de nuages de points. On utilise la fonction loadPointCloud pour charger le nuage, puis la fonction noiseFilter pour retirer le bruit de ce dernier. On sauvegarde ensuite le nuage qui vient d'être traité dans un fichier grâce à la fonction SavePointCloud.

## Configuration

Le fichier de configuration contient : 

- Les "inputs" : chemins vers les fichiers qui vont nous servir à exécuter les commandes (e572las.exe et fichier .e57).
- Les "outputs" : chemins vers les endroits où seront rangés les fichiers produits (le fichier converti en .laz et le fichier où le bruit a été filtré).
- "noiseFilter" : valeurs à entrer dans la fonction noiseFilter.

## Remarque

Le fichier de configuration est un fichier générique à modifier avec des valeurs personnelles.