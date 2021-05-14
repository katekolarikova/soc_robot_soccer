# Katerina Kolarikova
# SOC - fotbal robotu 2019
# funkce, ktera vytvari teplotni mapy pro oba tymy robotu

import os
import print_field
def robot_field(selected_log,filename,mydirectory,slideNumber=5):

    # vytvoreni adresare pro ulozeni map leveho tymu
    newpath_left = mydirectory + '\\robot_map_left' # folder for left team
    if not os.path.exists(newpath_left):
        os.makedirs(newpath_left)

    # vytvoreni adresare pro ulozeni map praveho tymu
    newpath_right = mydirectory + '\\robot_map_right' # folder for right team
    if not os.path.exists(newpath_right):
        os.makedirs(newpath_right)

    #vytvoren herniho pole
    def mapcrt():
        heatmap = []
        for y in range(4):
            heatmap.append([0] * 6)

        return heatmap

    #zpracovani logu
    if selected_log.endswith('.txt') :
        with open(selected_log) as log:

            heatmapl_1 = mapcrt()
            heatmapr_1 = mapcrt()
            heatmapl_2= mapcrt()
            heatmapr_2= mapcrt()
            sumline=0
            id="l"
            id2="r"
            printselection=1

            #zpracovani radku
            heading = log.readline() # nacteni zahlavi
            for line in log:
                lsplit = line.split(';')

                score=lsplit[24]

                #pozice robotu
                x_field=4 # left team (right=14)
                y_field=5
                stop=13

                #pridani pozice robota do teplotni mapy
                while x_field < stop:
                    position_xl = int(lsplit[x_field])  # x position left
                    position_yl = int(lsplit[y_field])  # y position left

                    heatmapl_1[-(position_yl)][position_xl - 1] += 1
                    heatmapl_2[-(position_yl)][position_xl-1] +=1

                    position_xr = int(lsplit[x_field+10])  # x position right
                    position_yr = int(lsplit[y_field+10])  # y position right

                    heatmapr_1[-(position_yr)][position_xr - 1] += 1
                    heatmapr_2 [-(position_yr)][position_xr - 1]+=1

                    x_field+=2
                    y_field+=2

                #tisk pomoci sliding windov
                sumline+=1
                if sumline % slideNumber == 0:
                    if printselection == 1:
                        print_field.printing(heatmapl_1, filename, str(sumline), score, id, newpath_left)
                        print_field.printing(heatmapr_1, filename, str(sumline), score, id2, newpath_right)
                        heatmapl_1=mapcrt()
                        heatmapr_1=mapcrt()
                        printselection=3

                    if printselection == 2:
                        print_field.printing(heatmapl_2, filename, str(sumline), score, id, newpath_left)
                        print_field.printing(heatmapr_2, filename, str(sumline), score, id2, newpath_right)
                        heatmapl_2 = mapcrt()
                        heatmapr_2 = mapcrt()
                        printselection = 2

                    printselection-=1

        # vytisteni konce hry
        print_field.printing(heatmapl_1, filename, str(sumline), score, id, newpath_left)
        print_field.printing(heatmapr_1, filename, str(sumline), score, id2, newpath_right)
        print_field.printing(heatmapl_2, filename, str(sumline), score, id, newpath_left)
        print_field.printing(heatmapr_2, filename, str(sumline), score, id2, newpath_right)



    return