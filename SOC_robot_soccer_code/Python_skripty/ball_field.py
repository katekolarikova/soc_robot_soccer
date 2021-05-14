# Katerina Kolarikova
# # SOC - fotbal robotu 2019
# funkce, s jejiz pomoci jsou generovany teplotni mapy pro vyskyt mice

import print_field
import os

def ball_field(selected_log,filename,mydirectory,slideNumber=5):
    score='0:0'

    # Vytvoreni adresare pro ukladani map
    newpath = mydirectory + '\\ball_map'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    #vytvoreni herniho pole
    def mapcrt():
        heatmap = []
        for y in range(4):
            heatmap.append([0] * 6)

        return heatmap

    # log otevreni
    heatmap_1 = mapcrt()
    heatmap_2 = mapcrt()

    if selected_log.endswith('.txt'):
        with open(selected_log) as log:
            sumline = 0
            id="b"
            printselection = 1
            heading = log.readline() #nacteni zahlavi

            for line in log:
                sumline+=1

                # rozdeleni radku
                lsplit = line.split(';')
                score = lsplit[24]
                y_position = int(lsplit[3])  # y ball position
                x_position = int(lsplit[2])  # x ball position

                # pridani pozice do teplotn mapy
                heatmap_1[-(y_position )][x_position - 1] += 1
                heatmap_2[-(y_position )][x_position - 1] += 1

                # tisk pomoci sliding window
                if sumline % slideNumber==0:

                    if printselection == 1:
                        print_field.printing(heatmap_1, filename, str(sumline), score, id, newpath)
                        heatmap_1 = mapcrt()
                        printselection = 3

                    if printselection == 2:
                        print_field.printing(heatmap_2, filename, str(sumline), score, id, newpath)
                        heatmap_2 = mapcrt()
                        printselection = 2

                    printselection-=1

            # vytisteni konce hry
            print_field.printing(heatmap_1, filename, str(sumline), score, id, newpath)
            print_field.printing(heatmap_2, filename, str(sumline), score, id, newpath)

    return

