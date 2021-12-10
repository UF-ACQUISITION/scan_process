import numpy as np

#affichage
def marquage(ins,outs):

    n_points = len(ins['X'])

    identifiant_scan = ins['Intensity'][10] + ins['X'][10] + ins['Y'][10] + ins['Z'][10]

    
    for point in range(0, n_points):
        ins['OriginId'][point] = identifiant_scan
    
    outs['OriginId'] = ins['OriginId']
    
    return True