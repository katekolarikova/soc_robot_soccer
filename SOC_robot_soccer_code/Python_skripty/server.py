#Katerina Kolarikova
# SOC - fotbal robotu 2019
# vznik serveru, zajistujici komunikaci mezi neuronovou siti a simultorem

import json
import pickle
import socket
import numpy as np

from tensorflow.python.keras.models import load_model

PORT = 1234

path='test_sit.strg' # soubor se strategii

#vytvoreni seznamu prislusnych pozic Move za kazde pravidlo
def move(path):
    with open(path) as log:
        rule_list = []
        move_list = []
        for line in log:
            lsplit = line.split('\t')
            if lsplit[0] == ".Move":

                split_move = lsplit[1][:-1].split('  ')
                for prvek in split_move:
                    move_list.append(int(prvek[0]))
                    move_list.append(int(prvek[2]))
                rule_list.append(move_list)
                move_list = []

    return rule_list


moves = move(path)
net = load_model("test_sit.h5") # nacteni site z disku

# priprava na ulozeni dat
def save_data(file, data):
    with open(file, "w") as f:
        pickle.dump(data, f)

# priprava na nacteni dat
def load_data(file):
    with open(file) as f:
        return pickle.load(f)

history=[]

def handle_message(msg):
    """
    msg jsou data ze hry
    vratit se stejna zprava, ve ktere budou aktualizovane pohyby (move) pro hrace
    """

    def mapcrt(): # vytvoreni herniho pole
        stav_hry = []  # aktualni herni situace
        for y in range(24):
            stav_hry.append([0] * 3)

        return stav_hry

    stav_hry=mapcrt()

    #pozice mice
    ball_x=int(msg["Ball"]["Position"]["X"])
    ball_y=int(msg["Ball"]["Position"]["Y"])

    pozice_ball=int((ball_y - 1) * 6 + ball_x - 1)

    stav_hry[pozice_ball][0]+=1

    # nacteni pozic mych robotu do "stav hry"
    for i in range(5):
        x_my=int(msg["myRobots"][i]["Position"]["X"])
        y_my=int(msg["myRobots"][i]["Position"]["Y"])
        position_my=(y_my - 1) * 6 + x_my - 1
        stav_hry[position_my][1]+=1/4

    # nacteni pozic souperovych robotu do stavu hry
    for i in range(5):
        x_opp=int(msg["oppntRobots"][i]["Position"]["X"])
        y_opp=int(msg["oppntRobots"][i]["Position"]["Y"])
        position_opp=(y_opp - 1) * 6 + x_opp - 1
        stav_hry[position_opp][2]+=1/4

    history.append(stav_hry)

    while len(history) < 4:
        history.append(stav_hry)

    if len(history) > 4:
        history.pop(0)

    rule = np.argmax(net.predict(np.array([[stav_hry]]))[0]) # vrati cislo pravidla doporuceneho siti

    input = moves[rule]
    #instrukce pro pohyb
    for i in range(4):
        msg["myRobots"][i]["PositionMove"]["X"] =input[i * 2]
        msg["myRobots"][i]["PositionMove"]["Y"] =input[i * 2 + 1]


    msg["ruleNumber"]=int(rule)

    return msg

#spusteni serveru
def run_server():
    # vytvoreni socketu - spojeni mezi dvema body
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', PORT))
    sock.listen(10) # ocekavni vstupu od klienta
    print("start")
    client, addr = sock.accept()

    buffer = ""
    while True: # neustale cteni zprav od klienta
        data = client.recv(512)
        if not data:
            print("Client exited")
            break
        buffer += data.decode()
        while '\n' in buffer:
            index = buffer.index('\n')
            msg = buffer[:index]

            result = handle_message(json.loads(msg)) # zpracovani udaju  ze hry

            client.sendall("{}\n".format(json.dumps(result)).encode()) # predani JSON zpravy s instrukcemi pro pohyb
            buffer = buffer[index + 1:]

run_server()
