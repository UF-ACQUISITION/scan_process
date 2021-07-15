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

def mean_dimensions(ins, outs):
    
    #print(ins)
    
    #Calcul de la moyenne d'une dimensions pour un cluster
    
    #liste ordonnée des clusters du sursol dunuage
    Clusters = init_clusters(ins['ClusterID'])

    #dictionnaire qui associe le num du cluster à son indice dans la liste
    dict_num_indice = init_dict_clusters_link(Clusters)
    #print(dict_num_indice)
    
    #nombre de points dans le nuage
    n_points = len(ins['X'])
	
	#array qui contient la moyenne d'anisotropie du cluster
    calcul_mean_anisotropy = np.zeros((len(Clusters),3))
    mean_anisotropy = np.zeros((len(Clusters),2))
    #array qui contient la moyenne de surf_var du cluster
    calcul_mean_surf_var = np.zeros((len(Clusters),3))
    mean_surf_var = np.zeros((len(Clusters),2))


    for i in range (0,len(Clusters)):
        calcul_mean_anisotropy[i][0] = Clusters[i]
        mean_anisotropy[i][0] = Clusters[i]
        
        calcul_mean_surf_var[i][0] = Clusters[i]
        mean_surf_var[i][0] = Clusters[i]
        

    for i in range (0, n_points):
       
        calcul_mean_anisotropy[int(dict_num_indice[ins['ClusterID'][i]])][1] += ins['Anisotropy'][i]
        calcul_mean_anisotropy[int(dict_num_indice[ins['ClusterID'][i]])][2] += 1
            
        calcul_mean_surf_var[int(dict_num_indice[ins['ClusterID'][i]])][1] += ins['SurfaceVariation'][i]
        calcul_mean_surf_var[int(dict_num_indice[ins['ClusterID'][i]])][2] += 1

    #print(calcul_mean)
 
    for i in range(0,len(Clusters)):
        mean_anisotropy[i][1] = calcul_mean_anisotropy[i][1]/calcul_mean_anisotropy[i][2]
        mean_surf_var[i][1] = calcul_mean_surf_var[i][1]/calcul_mean_surf_var[i][2]
    
    for i in range (0,n_points):
        ins['mean_anisotropy'][i] = mean_anisotropy[int(dict_num_indice[ins['ClusterID'][i]])][1]
        ins['mean_surf_var'][i] = mean_surf_var[int(dict_num_indice[ins['ClusterID'][i]])][1]
    
    outs['mean_anisotropy'] = ins['mean_anisotropy']
    outs['mean_surf_var'] = ins['mean_surf_var']
    
    return True