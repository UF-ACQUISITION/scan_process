import numpy as np

def cluster_to_ground(ins,outs):
    #liste ordonnée des clusters dans le nuage en entrée
    Cluster_set = set(ins['ClusterID'])
    Clusters = list(Cluster_set)
    Clusters.sort()

    #nombre de points dans le nuage en entrée
    n_points = len(ins['X'])
    
    #####format ins: [key][array]#####
    #####ex: ins['X'][0]#####
    
    #array destiné à contenir les HAG_max de chaque cluster de pts
    HAG_max_cluster = np.zeros(len(Clusters))

    #boucle pour extraire le HeightAboveGround maximum de chaque cluster, stocké dans HAG_max_cluster
    for i in range (0,n_points):
        if (ins['ClusterID'][i] != 0):
            if ins['HeightAboveGround'][i] > HAG_max_cluster[ins['ClusterID'][i]]:
                HAG_max_cluster[ins['ClusterID'][i]] = ins['HeightAboveGround'][i]
        
    
    #boucle pour changer la classe des points appartenant aux clusters répondant au critère d'HAG
    for i in range (0,n_points):
        if (ins['ClusterID'][i] != 0):
            if HAG_max_cluster[ins['ClusterID'][i]] < 0.30:
                ins['Classification'][i] = 2
                 
    
    #modification des classe des points de l'output
    outs['Classification'] = ins['Classification']
    
    return True