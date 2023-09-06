import numpy as np
import face_recognition
import cv2
import os
from datetime import datetime
from PIL import ImageGrab
import pyautogui
 
dirPath = 'images' 
jogadores = []
classNames = []

#myList = os.listdir(path)
#print(myList)]

imagens = os.listdir(dirPath)

for imagem in imagens:
    #percorrendo o diretorio e pegando uma imagem de cada vez
    imgPath = os.path.join(dirPath,imagem)
    imgAtual = cv2.imread(imgPath)
    #print(imgPath)
    #print(imgAtual)
    #adicionando a imagem atual na lista"images"
    jogadores.append(imgAtual)
    #(len(jogadores))
    #pegando o nome da foto ate o ".jpeg"
    classNames.append(os.path.splitext(imagem)[0])

#[jogadores] contém as imagens
#[classNames] os nomes do jogadores

#essa função vai retorna uma lista com multiplos valores extraindo caracteristicas únicas de cada imagem
def findEncodings(jogadores):
    encodeList = []
    for img in jogadores:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

#print(len(findEncodings(jogadores)))
 
#tioda vez que o reconhecimento facial for feito,vai salvar o nome e o horario do reconhecimento 
def markAttendance(name):
    with open('reconhecimento.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
        f   .writelines(f'n{name},{dtString}')
 
#### capturar a tela do computador
#bbox posição da captura
#transforar em array
#converter em bgr para fazer o decode
#pyautogui.position()
def captureScreen(bbox=(318,302,1067,799)):
     capScr = np.array(ImageGrab.grab(bbox))
     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
     return capScr
 
encodeListKnown = findEncodings(jogadores)
print('Encoding Complete')

while True:
    img = captureScreen()
    #reduzindo a imagem em 1/4 para acelerar o processp
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    #fazendo a localização das faces em cada frame
    facesCurFrame = face_recognition.face_locations(imgS)
    #fazendo o enconding das faces localizadas
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        #comparadno os encondings de do frame com os encondings na base de dados
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        # calculando a distancia entre a face sendo mostrada com a face armazenda
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #vai retornar uma lista com comparando o frame atual com as imagens que ja foram feitas os encodes
        matchIndex = np.argmin(faceDis)

        #vamos pegar qual a imagem mais parecida com o frame atual e "codar" a partir disso
        if matches[matchIndex]:
            #se a imagem mais parecida for a do bobe bryant,então o matchindex vai ter o valor de "0"
            #sabendo disso o nome que vai aparecer na captura vai ser o indice 0 da lista"classNAmes" no caso o propio kobe bryant
            name = classNames[matchIndex].upper()
            #print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
    
    cv2.imshow('tela',img)
    if cv2.waitKey(1) ==27:
        break