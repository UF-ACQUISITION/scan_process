import numpy as np

#Pour modifier la classe des points appartenant a des clusters non reliés au sol: cl=15
def flying_cluster(ins,outs):
    #liste ordonnée des clusters
    Cluster_set = set(ins['ClusterID'])
    Clusters = list(Cluster_set)
    Clusters.sort()
    
    #nombre de points dans le nuage
    n_points = len(ins['X'])
    
    #####format [key][array]#####
    #####print(ins['X'][0])#####
    
    #array destiné à contenir les hag min des clusters
    HAG_min_cluster = np.ones(Clusters[-1]+1)
    
   
    #boucle pour extraire le HeightAboveGround minimum de chaque cluster, stocké dans HAG_min_cluster
    for i in range (0,n_points):
        if (ins['ClusterID'][i] != 0):
            if ins['HeightAboveGround'][i] < HAG_min_cluster[ins['ClusterID'][i]]:
                HAG_min_cluster[ins['ClusterID'][i]] = ins['HeightAboveGround'][i]
        
    
    #boucle pour changer la classe des points appartenant aux clusters répondant au critère d'HAG
    for i in range (0,n_points):
        if (ins['ClusterID'][i] != 0):
            if HAG_min_cluster[ins['ClusterID'][i]] > 0.50:
                ins['Classification'][i] = 32
                
                 
    outs['Classification'] = ins['Classification']
    
    return True