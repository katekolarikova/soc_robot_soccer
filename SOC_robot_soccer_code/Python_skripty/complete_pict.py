# Katerina Kolarikova
# SOC - fotbal robotu
# modul, ktery slozi trojci teplotnich map

import numpy as np
import PIL.Image
import os

def complete(path):

    ball=os.listdir(path+'\\ball_map')
    team_r=os.listdir(path+'\\robot_map_right')
    team_l=os.listdir(path+'\\robot_map_left')

    size=len(ball)
    x=0
    newpath = path + '\\all_maps'  # slozka pro ulozeni map
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    for picture in range (size):
        name=ball[x]
        pict1=path+'\\ball_map\\'+ball[x]
        pict2=path+'\\robot_map_left\\'+ team_l[x]
        pict3=path + '\\robot_map_right\\' + team_r[x]

        list_im = [pict1, pict2, pict3]
        imgs    = [ PIL.Image.open(i) for i in list_im ]
        # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

        # save picture
        imgs_comb = PIL.Image.fromarray( imgs_comb)
        imgs_comb.save(newpath+'\\'+ name+'.png' )

        x+=1

    return
