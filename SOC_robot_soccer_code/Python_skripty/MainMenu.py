# Katerina Kolarikova
# SOC - fotbal robotu 2019
# hlavni modul, pro analzyu logu. Vola funkce pro tvorbu teplotnich map
# soucatsti je také complete_pict, která zkompletuje teplotni mapy do jednoho obrazku

# Import knihoven a funkcí
import ball_field
import robot_field
import complete_pict
import os

if __name__ == "__main__":
    # vstupni adresar s logy
    mydirectory=''
    print ("Robot Footbal Heatmap Creation")

    # nastavení, pro co vše se mají teplotní mapy generovat
    selection ="all"

    for filename in os.listdir(mydirectory): #prochazeni adesare
        path = mydirectory + '\\' + filename #cesta k logu

        if selection== "b":
             ball_field.ball_field(path,filename,mydirectory)

        if selection=="r":
                robot_field.robot_field(path,filename,mydirectory)

        if selection=="all":
            ball_field.ball_field(path,filename,mydirectory)
            robot_field.robot_field(path,filename,mydirectory)

    if selection=="all":
        complete_pict.complete(mydirectory) #zkompletovani obrazku
    print( "Complete map")




