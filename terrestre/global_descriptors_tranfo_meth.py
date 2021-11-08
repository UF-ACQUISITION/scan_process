import numpy as np
from math import *

#from math import sqrt as sqrt
#from math import pi as pi

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
  
def proba_sur_1(valeur):
    #print(valeur)
    proba = 0
    if (valeur <= 1) and (valeur > 0.5):
        proba = valeur
    
    if (valeur > 1) and ((1/valeur) > 0.5):
        proba = (1/valeur)
    
    if valeur < 0.33 or valeur > 3:
        proba = -5
    
    return proba

def score_cluster(cluster_desc_array):
    #Etape 1: recherche de la vegetation et du bati
    cluster_veget_basse = []
    cluster_veget_inter = []
    cluster_veget_haute = []
    cluster_bati = []
    
    
    for i in range (0, len(cluster_desc_array)):
        
        if (cluster_desc_array[i][1] < 1) and (cluster_desc_array[i][2] > (cluster_desc_array[i][1]/2)) and (cluster_desc_array[i][5] < 0.7):
        #if (cluster_desc_array[i][1] < 1) and (cluster_desc_array[i][5] < 0.7):
            cluster_veget_basse.append(cluster_desc_array[i][0])
        
        if (cluster_desc_array[i][1] < 3) and (cluster_desc_array[i][1] > 1) and (cluster_desc_array[i][2] < 3) and (cluster_desc_array[i][3] < 3) and (cluster_desc_array[i][2] > 0.5) and (cluster_desc_array[i][3] > 0.5) and (cluster_desc_array[i][5] < 0.7) and (cluster_desc_array[i][6] > 3):
        #if (cluster_desc_array[i][1] < 3) and (cluster_desc_array[i][1] > 1) and (cluster_desc_array[i][5] < 0.7) and (cluster_desc_array[i][6] > 3):
            cluster_veget_inter.append(cluster_desc_array[i][0])
        
        if (cluster_desc_array[i][1] > 3) and (cluster_desc_array[i][2] > 2.5) and (cluster_desc_array[i][3] > 2.5) and (cluster_desc_array[i][5] < 0.7) and (cluster_desc_array[i][6] > 3):
            cluster_veget_haute.append(cluster_desc_array[i][0])
           
        if (cluster_desc_array[i][1] > 5) and (cluster_desc_array[i][2] > 10) and (cluster_desc_array[i][5] > 0.7) and (cluster_desc_array[i][2] > 5*cluster_desc_array[i][3]):
            cluster_bati.append(cluster_desc_array[i][0])
    
    #Etape 2: classification des clusters restants
    
    #dimensions idéales [H L l L/l L/H]
    #[potelet
    # panneau agglo
    # panneau hors agglo
    # panneau rue
    # panneau pub
    # lampadaire
    # feu 1
    # feu 2]

    cluster_ref = np.array([[0.9, 0.15, 0.15, 1, 0.17],
    [3.15, 0.7, 0.2, 3.5, 0.22],
    [1.85, 0.7, 0.2, 3.5, 0.38],
    [2.70, 0.5, 0.1, 5.0, 0.18],
    [5.0, 3.5, 0.9, 3.9, 0.7],
    [9.0, 3.0, 0.6, 5.0, 0.33],
    [3.5, 0.7, 0.5, 1.4, 0.2],
    [7.5, 5.9, 0.9, 6.55, 0.79]])
    
    #[ClusterID score_dans_les_différentes_classes]
    cluster_score = np.zeros((len(cluster_desc_array),len(cluster_ref)+1))

    for i in range (1, len(cluster_desc_array)):
        
        cluster_score[i][0] = cluster_desc_array[i][0]
        
        for j in range (0,len(cluster_ref)):

            score = (3*proba_sur_1((cluster_desc_array[i][1] / cluster_ref[j][0])) + proba_sur_1((cluster_desc_array[i][2] / cluster_ref[j][1])) + proba_sur_1((cluster_desc_array[i][3] / cluster_ref[j][2])) + proba_sur_1(((cluster_desc_array[i][2]/cluster_desc_array[i][3]) / cluster_ref[j][3])) + proba_sur_1(((cluster_desc_array[i][2]/cluster_desc_array[i][1]) / cluster_ref[j][4]))) / 7
            
            cluster_score[i][j+1] = score
            
    return cluster_veget_basse, cluster_veget_inter, cluster_veget_haute, cluster_bati, cluster_score
 
 
def global_descriptors_transfo_method(ins, outs):
       
    #Calcul de descripteurs globaux
    
    #liste ordonnée des clusters du sursol dunuage
    Clusters = init_clusters(ins['ClusterID'])
    
    
    #dictionnaire qui associe le num du cluster à son indice dans la liste
    dict_num_indice = init_dict_clusters_link(Clusters)
    #print(dict_num_indice)
    
    #nombre de points dans le nuage
    n_points = len(ins['X'])
    
    #[clusterID Cluster_class Xm XM Ym YM Zm ZM Xc Yc Zc] -> stocker les caractéristiques de chaque cluster
    cluster_signature = np.zeros((len(Clusters),11))
    
    #[p1 p2 p3 p4]
    cluster_pt_car = np.zeros((len(Clusters),8)) 

    #[clusterID X Y Z] -> stocker les centre géométriques de chaque cluster
    cluster_point_D2 = np.zeros((len(Clusters),3))
    
    #[clusterID Hauteur Lmax lmin Volume_approx anisotropy_mean surf_var_mean class] -> stocker les descripteurs de chaque cluster
    cluster_descriptors = np.zeros((len(Clusters),8))
    
    #initialisation de la matrice signature
    
    #Initialisation du critère d'arret de la boucle while -> pour ne pas parcourir inutilement tous les points du nuage
    stop = len(Clusters)
    
    #initialisation de l'array cluster_signature
    i = 0

   
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
            cluster_descriptors[int(dict_num_indice[ins['ClusterID'][i]])][5] = ins['mean_anisotropy'][i]
            cluster_descriptors[int(dict_num_indice[ins['ClusterID'][i]])][6] = ins['mean_surf_var'][i]
            
            stop -= 1
                
        i+=1
    
    
    #remplissage de l'array cluster_signature
    #cluster_signature
    for i in range (0,n_points):
        if (ins['ClusterID'][i] != 0):
            #Xmin
            if ins['X'][i] < cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][2]:
                cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][2] = ins['X'][i]
                cluster_pt_car[int(dict_num_indice[ins['ClusterID'][i]])][0] = ins['X'][i]
                cluster_pt_car[int(dict_num_indice[ins['ClusterID'][i]])][1] = ins['Y'][i]
            #XMax
            if ins['X'][i] > cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][3]:
                cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][3] = ins['X'][i]
                cluster_pt_car[int(dict_num_indice[ins['ClusterID'][i]])][2] = ins['X'][i]
                cluster_pt_car[int(dict_num_indice[ins['ClusterID'][i]])][3] = ins['Y'][i]
            #Ymin
            if ins['Y'][i] < cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][4]:
                cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][4] = ins['Y'][i]
                cluster_pt_car[int(dict_num_indice[ins['ClusterID'][i]])][4] = ins['X'][i]
                cluster_pt_car[int(dict_num_indice[ins['ClusterID'][i]])][5] = ins['Y'][i]
            #YMax
            if ins['Y'][i] > cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][5]:
                cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][5] = ins['Y'][i]
                cluster_pt_car[int(dict_num_indice[ins['ClusterID'][i]])][6] = ins['X'][i]
                cluster_pt_car[int(dict_num_indice[ins['ClusterID'][i]])][7] = ins['Y'][i]
            #Zmin
            if ins['Z'][i] < cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][6]:
                cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][6] = ins['Z'][i]
            #ZMax
            if ins['Z'][i] > cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][7]:
                cluster_signature[int(dict_num_indice[ins['ClusterID'][i]])][7] = ins['Z'][i]
     

    #remplissage des centres des bounding box des clusters
       
    for i in range (0, len(Clusters)):
        #Xcentre
        cluster_signature[i][8] = (cluster_signature[i][2] + cluster_signature[i][3])/2
        #Ycentre
        cluster_signature[i][9] = (cluster_signature[i][4] + cluster_signature[i][5])/2
        #Zcentre
        cluster_signature[i][10] = (cluster_signature[i][6] + cluster_signature[i][7])/2
        
    #print(cluster_signature)
    #print(cluster_pt_car)
    
    
    #Calcul de la bounding box min
    for i in range (0, len(Clusters)):
    #for i in range (0,1):    
        LM = cluster_signature[i][3] - cluster_signature[i][2]
        lm = cluster_signature[i][5] - cluster_signature[i][4]
        
        surface =  LM * lm
        
        alpha = 0
        while alpha < pi:
        
            point_transformes = np.zeros((1,8))
            for j in range (0,4):
                point_transformes[0][2*j] = cluster_pt_car[i][2*j]*cos(alpha) - cluster_pt_car[i][2*j+1]*sin(alpha)
                point_transformes[0][2*j+1] = cluster_pt_car[i][2*j]*sin(alpha) + cluster_pt_car[i][2*j+1]*cos(alpha)
            
            x = [point_transformes[0][0],point_transformes[0][2],point_transformes[0][4],point_transformes[0][6]]
            x.sort()
            y = [point_transformes[0][1],point_transformes[0][3],point_transformes[0][5],point_transformes[0][7]]
            y.sort()
            cotes = [abs(x[-1] - x[0]), abs(y[-1] - y[0])]
            cotes.sort()
            L = cotes[1]
            l = cotes[0]
     
            s = l*L
            #print(s)
            if s < surface:
                surface = s
                LM = L
                lm = l
                #print(s)
            
            alpha += pi/20
                
        cluster_descriptors[i][0] = cluster_signature[i][0]
        cluster_descriptors[i][1] = cluster_signature[i][7] - cluster_signature[i][6]
        cluster_descriptors[i][2] = LM
        cluster_descriptors[i][3] = lm
        cluster_descriptors[i][4] = surface * cluster_descriptors[i][1]
            
    
    veget_basse, veget_inter, veget_haute, bati, prob_class = score_cluster(cluster_descriptors)
    #print(prob_class)
    
    for i in range (0, len(prob_class)):
        probas = prob_class[i][1:]
        maximum = np.max(probas)
        
        #print("Cluster n ", cluster_descriptors[i][0])
        #print(probas)
        for j in range (0,len(probas)):
            if (probas[j] > 0.5) and (probas[j] == maximum):
                cluster_descriptors[i][-1] = 67+j
                #print("Cluster n ", cluster_descriptors[i][0])
                #print(probas)
                #print(67+j)
                #print(cluster_descriptors[i][0], cluster_descriptors[i][-1], probas[j])
        
    
    #np.savetxt('cluster_geom_desc.csv', cluster_descriptors, delimiter=',',fmt='%f')
    #print(cluster_descriptors[int(dict_num_indice[14])][:])
    
    for i in range (0,n_points):
        if cluster_descriptors[int(dict_num_indice[ins['ClusterID'][i]])][-1] != 0:
            ins['Classification'][i] = cluster_descriptors[int(dict_num_indice[ins['ClusterID'][i]])][-1]
    
    for i in range (0,n_points):
        if ins['ClusterID'][i] in veget_basse:
            ins['Classification'][i] = 3
        if ins['ClusterID'][i] in veget_inter:
            ins['Classification'][i] = 4
        if ins['ClusterID'][i] in veget_haute:
            ins['Classification'][i] = 5
        if ins['ClusterID'][i] in bati:
            ins['Classification'][i] = 6
    
    outs['Classification'] = ins['Classification']
        
    return True