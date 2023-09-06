import zipfile
import tensorflow as tf
import cv2
import os
import numpy as np
import random
from tensorflow import keras
from  keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization


path = 'train'
#zip_object = zipfile.ZipFile(file=path,mode = 'r')
#zip_object.extractall('./')
#zip_object.close()

gerador_treinamento = ImageDataGenerator(rescale=1./255,
                                         rotation_range=7,
                                         horizontal_flip=True,
                                         zoom_range=0.2,)
dataset_treinamento = gerador_treinamento.flow_from_directory(path,
                                                              target_size = (48, 48),
                                                              batch_size = 16,
                                                              class_mode = 'categorical',
                                                              shuffle = True)

dataset_treinamento.classes

np.unique(dataset_treinamento.classes, return_counts=True)

#gerador_teste = ImageDataGenerator(rescale=1./255)
#dataset_teste = gerador_teste.flow_from_directory('/content/fer2013/validation',
                                                  #target_size = (48, 48),
                                                  #batch_size = 1,
                                                  #class_mode = 'categorical',
                                                  #shuffle = False)

#np.unique(dataset_teste.classes, return_counts=True)


numero_detectores = 32
numero_classes = 7
largura, altura = 48, 48
epocas = 80
 
network = Sequential()

#detector de caracteristicas = kernel_size,mapas de caracteristicas gerados =32,padding ="same" para aproveitar ao maximo os pixels
network.add(Conv2D(filters=numero_detectores, kernel_size=(3,3), activation='relu', padding='same', input_shape=(largura, altura, 3)))
#BatchNormalization para normalizar os pixels de forma interna
network.add(BatchNormalization())
network.add(Conv2D(filters=numero_detectores, kernel_size=(3,3), activation='relu', padding='same'))
network.add(BatchNormalization())
#uma mapa com os pixels mais importantes da imagem
network.add(MaxPooling2D(pool_size=(2,2)))
#uma camada de dropout para evitar o overfitting
network.add(Dropout(0.1))

#64 neuronios na camada de convolução
network.add(Conv2D(filters=2*numero_detectores, kernel_size=(3,3), activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(Conv2D(filters=2*numero_detectores, kernel_size=(3,3), activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(MaxPooling2D(pool_size=(2,2)))
network.add(Dropout(0.1))

#128 neuronios na camada de convolução
network.add(Conv2D(filters=2*2*numero_detectores, kernel_size=(3,3), activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(Conv2D(filters=2*2*numero_detectores, kernel_size=(3,3), activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(MaxPooling2D(pool_size=(2,2)))
network.add(Dropout(0.1))
#256 neuronios na camada de convolução
network.add(Conv2D(filters=2*2*2*numero_detectores, kernel_size=(3,3), activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(Conv2D(filters=2*2*2*numero_detectores, kernel_size=(3,3), activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(MaxPooling2D(pool_size=(2,2)))
network.add(Dropout(0.1))

#Para colocar os dados em vetor
network.add(Flatten()) 
#primeira camada densa com 64 neuronios
network.add(Dense(units=2 * numero_detectores, activation='relu'))
network.add(BatchNormalization())
network.add(Dropout(0.2))

#segunda camada densa com 128 neuronios
network.add(Dense(units=2 * numero_detectores, activation='relu'))
network.add(BatchNormalization())
network.add(Dropout(0.2))

#softmax por ser um problema de mais de duas classes
network.add(Dense(units=numero_classes, activation='softmax'))
print(network.summary())

network.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

network.fit(dataset_treinamento, epochs=epocas)

modelo= network.to_json()
with open('modelo100_epochs.json','w') as json_file:
  json_file.write(modelo)

from keras.models import save_model
modelo_Salvo = save_model(network, '/content/pesos_emotions.hdf5')



#network.evaluate(dataset_teste)

#previsoes = network.predict(dataset_teste)
#previsoes

#previsoes = np.argmax(previsoes, axis = 1)
#previsoes

#from sklearn.metrics import confusion_matrix
#cm = confusion_matrix(dataset_teste.classes, previsoes)

#from sklearn.metrics import classification_report
#print(classification_report(dataset_teste.classes, previsoes))

