#Katerina Kolarikova
# SOC - fotbal robotu 2019
""""
28.10.18 - menu pro neuronovou síť; navolení adresářů s logy pro tréninková i testovací data; import funkcí, ktéré
vrátí x_test,y_test,x_train,y_train
"""

import training_data
import neural_network
import training_data_kuba
import numpy as np

training_directory= '' # adresar s logy pro trenink

train=training_data_kuba.data(training_directory) # vrati hodnoty x_train a y_train v jednom listu

# prevedeni testovacich dat na numpy pole
x_train=np.array(train[0])
y_train=np.array(train[1])

x_test=np.array(train[2])
y_test=np.array(train[3])

neural_network.neural_network(x_train,y_train,x_test,y_test)





