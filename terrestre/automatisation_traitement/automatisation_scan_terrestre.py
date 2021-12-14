import distutils.util
import json
import subprocess
import cloudComPy as cc


with(open(input("Veuillez renseigner le chemin de votre fichier de configuration : \n"))) as jsonFile:
    config = json.load(jsonFile)
    jsonFile.close()


def e57tolas():
    command = config.get("inputs").get("e572las") + " -v -i " + config.get("inputs").get("e57") + " -o " + \
              config.get("outputs").get("lazFile")

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    process.communicate()

    process.terminate()

    print("\nLa conversion du fichier e57 en laz est terminée.\n")


def removeNoise():
    cc.initCC()
    filter = config.get("noiseFilter")

    cloud = cc.loadPointCloud(config.get("outputs").get("lazFile"))

    print("Début du traitement du nuage de point.\n")

    noise = cc.CloudSamplingTools.noiseFilter(cloud, filter.get("kernelRadius"), filter.get("nSigma"), distutils.util.strtobool(filter.get("removeIsolatedPoints")),
                                              distutils.util.strtobool(filter.get("useKnn")), filter.get("knn"), distutils.util.strtobool(filter.get("useAbsoluteError")), filter.get("absoluteError"))
    pointCloud, clone = cc.ccPointCloud.partialClone(cloud, noise)
    cc.SavePointCloud(pointCloud, config.get("outputs").get("lazFiltered"))


if __name__ == "__main__":
    e57tolas()
    removeNoise()
