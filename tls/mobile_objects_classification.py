import numpy as np
from math import *

def init_clusters(ins_clusters_id):
    #initialisation d'une liste qui contient les ID de clusters par ordre croissant
    
    Cluster_set = set(ins_clusters_id)
    Clusters_list = list(Cluster_set)
    Clusters_list.sort()

    return Clusters_list    

def init_dict_clusters_link(cluster_list):
        
    cluster_dict = {}
    for i in range (0, len(cluster_list)):
        cluster_dict[cluster_list[i]] = i
            
    return cluster_dict

def mobile_objects_classification(ins, outs):
    
    #print(ins)
    
    #Classification à 66 des clusters conteant des points provenant d'une seule source
    
    #liste ordonnée des clusters du sursol dunuage
    Clusters = init_clusters(ins['ClusterID'])

    #dictionnaire qui associe le num du cluster à son indice dans la liste
    dict_num_indice = init_dict_clusters_link(Clusters)
    #print(dict_num_indice)
    
    #nombre de points dans le nuage
    n_points = len(ins['X'])
    
    #array qui contient la première source d'un cluster, et 1 si elle est unique
    sources = np.zeros((len(Clusters),3))
    
	
    for i in range (0,len(Clusters)):
        sources[i][0] = Clusters[i]

        
    for i in range (0, n_points):
       
        if sources[int(dict_num_indice[ins['ClusterID'][i]])][1] != ins['OriginId'][i]:
            sources[int(dict_num_indice[ins['ClusterID'][i]])][1] = ins['OriginId'][i]
            sources[int(dict_num_indice[ins['ClusterID'][i]])][2] += 1
    
    #print(sources)
    for i in range (0, n_points):
    
        if sources[int(dict_num_indice[ins['ClusterID'][i]])][2] == 1:
            ins['Classification'][i] = 66
        
    
    outs['Classification'] = ins['Classification']
    
    
    return True