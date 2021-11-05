# Librairie qui permet de manipuler des dossiers et des fichiers
import os
# Librairie qui permet de manipuler différentes parties de l'environnement runtime de python
import sys

# On récupère grâce à "sys.argv" les arguments que l'on a passé en ligne de commande, et on enlève le premier élément de la liste (car c'est le nom de l'exécutable python. Ici, filtre.py)
sys.argv.pop(0)
args = sys.argv

# Constantes
FILE_SIZE = int(args[0])
DIR_PATH = args[1]


# Fonction qui permet de ne conserver que les fichiers ".las" dans le répertoire
def SupBinAndLazFiles():
    # On récupère tous les fichiers du dossier
    files = os.listdir(DIR_PATH)
    for file in files:
        filename, file_extension = os.path.splitext(DIR_PATH + "\\" + file)
        if file_extension != ".las":
            os.remove(filename + file_extension)
    SupSmallFiles(os.listdir(DIR_PATH))


# Fonction qui permet de supprimer les petits fichiers du répertoire. Le seuil de la taille du fichier est spécifié lors du lancement du programme (en ligne de commande) et est stocké dans la constante FILE_SIZE
def SupSmallFiles(files):
    for file in files:
        filename, file_extension = os.path.splitext(DIR_PATH + "\\" + file)
        # La taille est initialement donnée en byte, on la divise donc par 1024 pour l'avoir en Ko
        size = round(os.path.getsize(filename + file_extension) / 1024)
        if size < FILE_SIZE:
            os.remove(filename + file_extension)


SupBinAndLazFiles()