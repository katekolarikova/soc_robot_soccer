#Katerina Kolarikova
# SOC - fotbal robotu 2019
#funkce, ktera zajisti natrenovani a vytvoreni neuronove site

import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.python.keras.layers import Flatten, Dense

def neural_network(x_train,y_train,x_test,y_test):

    model = tf.keras.models.Sequential([
    Flatten(input_shape=x_train[0].shape), # vstupni vrstva
    Dense(512, activation=tf.nn.relu),# "husta vrstva", 512-neurony
    Dense(15, activation=tf.nn.softmax) #activation - aktivacni funkce, upravuje hodnoty
    # neuron pro každou číslici, hodnota udává pravděpodobnost
    ])

    # konfigurace modelu
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(x_train, y_train, epochs=25) # fit == train
    print(model.evaluate(x_test, y_test))

    # tisk grafu popisujicich uceni
    plt.plot(history.history['acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')

    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

    plt.plot(history.history['loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

    model.save('neuronova_sit.h5') # ulozeni site na disk

