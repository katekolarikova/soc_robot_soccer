# Katerina Kolarikova
# SOC - fotbal robotu 2019
"""
28_10_18 dvě funkce, kdy první vrací listy x_train a y_train, druhá pal x_test a y_test;
soubory ke zpracovani dostavaji z 'menu_network'

30_10_18 hodnoty jsou normalizovany - nachayeji se v intervalu 0-1, tj x-souradnice/6, y-souradnice/4; pravidla se
nachazeji v intervalu 0-15, tj pravidlo-1

14_11_18 zobrazeni tri po sobe jdoucich hernich situaci v jednom poli

24_11_18 upravy : parametr pro velikost historie; parametr pro velikost deleni dat;
y-data maji podobu souradnic, kam se maji roboti premistit;rozdeleni na vice funkci

"""
import os

#vytvoreni herniho pole
def mapcrt():
    game_field = [] # aktualni herni situace
    for y in range(24):
        game_field.append([0] * 3)

    return game_field

#funkce,rozdeleni dat na trenovaci a testovaci
def data_split(x_data,y_data):
    split_size=round(len(x_data)/4)

    x_train = x_data[:-split_size]
    x_test = x_data[-split_size:]
    y_train = y_data[:-split_size]
    y_test = y_data[-split_size:]

    return x_train,y_train,x_test,y_test

#funkce, zpracovani  logu na trenovaci data
def data(path, history_size=1):

    x_data = []
    y_data = []
    history=[] # x po sobě jdoucí situace na hřišti

    #prochazeni souboru v adresari
    for file in os.listdir(path):

        if file.endswith('.log'):
            training_log = path + '\\' + file
            print(file)

            #zpracovani logu
            with open(training_log) as log:
                heading=log.readline()

                for line in log:

                    if line == '\n':  # ošetření výskytu prázdných řádků v souboru
                        pass
                    else:

                     # aktualni pozice na hristi
                        game_field = mapcrt()

                        lsplit = line.split(';')

                        rule = int(lsplit[0]) - 1

                        if lsplit[2] == '7':
                            lsplit[2]='6'

                        ball_x = int(lsplit[2])
                        ball_y = int(lsplit[3])

                        index = (ball_y - 1) * 6 + ball_x - 1  # zjisteni indexu, ktery odpovida danemu hernimu poli

                        game_field[index][0] += 1  # pridani pozice mice do game_field

                        position_x = 4
                        position_y = 5

                        # nacteni pozic robotu do gamefield
                        while position_x < 13:
                            x_lteam = int(lsplit[position_x])
                            y_lteam = int(lsplit[position_y])

                            x_rteam = int(lsplit[position_x + 10])
                            y_rteam = int(lsplit[position_y + 10])

                            index_l = (y_lteam - 1) * 6 + x_lteam - 1  # index pro robota leveho tymu
                            index_r = (y_rteam - 1) * 6 + x_rteam - 1  # index pro robota praveho tymu

                            game_field[index_l][1] += 1/4  # pridani poyice leveho robota do game_field
                            game_field[index_r][2] += 1/4  # pridani pozice praveho robota do game_field

                            position_x += 2
                            position_y += 2

                        history.append(game_field) # pridani herni situce do historie

                        # pridani history do trenovacich dat vzdy po urcitem poctu opakovani (history_size)
                        if len(history)%history_size==0:
                            if history not in x_data:  # pokud game_field neni v trenovacich datech, prdej ho
                                x_data.append(history)
                                y_data.append(rule)
                                history=[]

                            else:
                                history=[]

        x_train, y_train, x_test, y_test=data_split(x_data,y_data)

    return x_train,y_train,x_test,y_test