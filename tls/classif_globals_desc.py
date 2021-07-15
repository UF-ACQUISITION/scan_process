import numpy as np
from math import sqrt as sqrt

def dist_D1(X,Y,xc,yc,n,ClusterID, cl_id):
    #plus grande distance horizonte dans le nuage en partant du centre de la bounding box
    
    dist_max = 0
    x_p = 0
    y_p = 0
    
    for i in range (0, n):
        if ClusterID[i] == cl_id:
            d = sqrt((X[i]-xc)**2 + (Y[i]-yc)**2)
        
            if d > dist_max:
                dist_max = d
                x_p = X[i]
                y_p = Y[i]
    
    return x_p, y_p, dist_max
    
def dist_D2(X,Y,xp,yp,xc,yc,hyp,n,ClusterID, cl_id):
    #plus grande distance horizonte dans le nuage orthogonale a D1
    #formule de Héron
    
    hmax = 0
    h = 0
    for i in range (0, n):
        if ClusterID[i] == cl_id:
            a = sqrt((X[i] - xp)**2 + (Y[i] - yp)**2)
            b = sqrt((X[i] - xc)**2 + (Y[i] - yc)**2)
            s = ( a + b + hyp)/2
        
        #print(a,b,hyp,s)
    
            A = sqrt(s*(s-a)*(s-b)*(s-hyp))
    
            h = 2*A/hyp
    
    if h > hmax:
        hmax = h
    
    return h
    
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

    #######################
    #####Main function#####
    #######################
    
def classif_gobals_desc(ins, outs):
    #Calcul de descripteurs globaux

    #liste ordonnée des clusters du sursol dunuage
    Clusters = init_clusters(ins['ClusterID'])
    
    #dictionnaire qui associe le num du cluster à son indice dans la liste
    dict_num_indice = init_dict_clusters_link(Clusters)

    #nombre de points dans le nuage
    n_points = len(ins['X'])
    
    #[clusterID Cluster_class Xm XM Ym YM Zm ZM Xc Yc Zc] -> stocker les caractéristiques de chaque cluster
    cluster_signature = np.zeros((len(Clusters),11))

    #[clusterID X Y Z] -> stocker les coord du point le plus loin
    cluster_point_D2 = np.zeros((len(Clusters),3))
    
    #[clusterID H D1 D2 class] -> stocker les descripteurs de chaque cluster
    cluster_descriptors = np.zeros((len(Clusters),5))
    
    #initialisation de la matrice signature
    
        #Initialisation du critère d'arret de la boucle while -> pour ne pas parcourir inutilement tous les points du nuage
    stop = len(Clusters)
    
    #initialisation de l'array cluster_signature
    i = 0
    ###print(dict_num_indice[8])
    ###print(ins['ClusterID'][0])
    ###print(cluster_signature[int(dict_num_indice[ins['ClusterID'][0]])][0])
   
    while (stop != 0):
        if cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][0] == 0:
            
            cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][0] = ins['ClusterID'][i]
            cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][1] = ins['Classification'][i]
            cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][2] = ins['X'][i]
            cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][3] = ins['X'][i]
            cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][4] = ins['Y'][i]
            cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][5] = ins['Y'][i]
            cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][6] = ins['Z'][i]
            cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][7] = ins['Z'][i]
             
            stop -= 1
                
        i+=1
    

    #remplissage de l'array cluster_signature
    #cluster_signature
    for i in range (0,n_points):
        if (ins['ClusterID'][i] != 0):
            if ins['X'][i] < cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][2]:
                cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][2] = ins['X'][i]
            
            if ins['X'][i] > cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][3]:
                cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][3] = ins['X'][i]
            
            if ins['Y'][i] < cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][4]:
                cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][4] = ins['Y'][i]
            
            if ins['Y'][i] > cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][5]:
                cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][5] = ins['Y'][i]
            
            if ins['Z'][i] < cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][6]:
                cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][6] = ins['Z'][i]
            
            if ins['Z'][i] > cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][7]:
                cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][7] = ins['Z'][i]
     

    #remplissage des centres des bounding box des clusters
       
    for i in range (0, len(Clusters)):
        cluster_signature[i][8] = (cluster_signature[i][2] + cluster_signature[i][3])/2
        cluster_signature[i][9] = (cluster_signature[i][4] + cluster_signature[i][5])/2
        cluster_signature[i][10] = (cluster_signature[i][6] + cluster_signature[i][7])/2
    
       
       
    for i in range (0, len(Clusters)):
        cluster_descriptors[i][0] = cluster_signature[i][0]
        cluster_point_D2[i][0] = cluster_signature[i][0]
        
        cluster_descriptors[i][1] = cluster_signature[i][7] - cluster_signature[i][6]
        
        cluster_point_D2[i][1], cluster_point_D2[i][2], cluster_descriptors[i][2] = dist_D1(ins['X'], ins['Y'], cluster_signature[i][8], cluster_signature[i][9], n_points, ins['ClusterID'],i+1)
        
        #num cluster a corr
        cluster_descriptors[i][3] = dist_D2(ins['X'], ins['Y'], cluster_point_D2[i][1], cluster_point_D2[i][2], cluster_signature[i][8], cluster_signature[i][9], cluster_descriptors[i][2], n_points, ins['ClusterID'],i+1)
    
    #print(cluster_signature, cluster_point_D2,cluster_descriptors)
    
    np.savetxt('cluster_global_dec.csv', cluster_descriptors, delimiter=',',fmt='%f')
    
    
    return True