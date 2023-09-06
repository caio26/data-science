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


#carregando o modelo
with open('modelo100_epochs.json', 'r') as json_file:
  json_saved_model = json_file.read()
json_saved_model

network_loaded = tf.keras.models.model_from_json(json_saved_model)
network_loaded.load_weights('pesos_emotions.hdf5')
network_loaded.compile(loss = 'categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])


emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']


#utilizando o detector de faces
detector_face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

while True:
# Lê um frame da câmera
    success, img = cap.read()

    # Detecta faces na imagem utilizando o detector pré-treinado
    deteccoes = detector_face.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))

    # Verifica se pelo menos uma face foi detectada
    if len(deteccoes) > 0:

        # Percorre todas as faces detectadas
        for (x, y, w, h) in deteccoes:

            # Desenha um retângulo em volta da face detectada
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Extrai a região de interesse (ROI) da imagem
            roi = img[y:y + h, x:x + w]

            # Converte a imagem para o formato RGB
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)

            # Redimensiona a imagem para as dimensões esperadas pelo modelo
            roi = cv2.resize(roi, (48, 48))

            # Normaliza os valores dos pixels para o intervalo [0, 1]
            roi = roi / 255

            # Adiciona uma dimensão extra para indicar o tamanho do batch
            roi = np.expand_dims(roi, axis=0)

            # Realiza a classificação da imagem utilizando o modelo pré-treinado
            previsao = network_loaded.predict(roi)

            # Verifica se a classificação obteve sucesso
            if previsao is not None:

                # Obtém o índice da emoção com maior probabilidade
                resultado = np.argmax(previsao)

                # Escreve o nome da emoção sobre o retângulo em volta da face detectada
                cv2.putText(img, emotions[resultado], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    # Exibe a imagem na janela com o nome "tela"
    cv2.imshow('tela', img)

    # Verifica se a tecla "Esc" foi pressionada
    if cv2.waitKey(1) == 27:
        break  # Encerra o loop e finaliza o programa



