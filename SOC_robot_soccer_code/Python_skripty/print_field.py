# Katrina Kolarikova
# SOC - fotbal robotu 2019
# funkce pro tisk teplotnich map

import matplotlib.pyplot as plt

def printing(heatmap,filename,sumline,score,id,path):
    plt.imshow(heatmap, cmap='hot',interpolation='nearest')
    plt.savefig(path+"\\"+filename+'_'+sumline+'_'+id+'.png')

    return

