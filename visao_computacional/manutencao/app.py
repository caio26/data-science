import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import cv2
import random
from skimage import io
import tensorflow as tf
import sklearn
from tensorflow.keras import layers, optimizers
from tensorflow.keras.layers import Dense, Input, AveragePooling2D, Flatten, Dropout, MaxPooling2D,GlobalAveragePooling2D
from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, Add, UpSampling2D, Concatenate
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from pathlib import Path
import os

imagens_com_ou_sem_defeito=pd.read_csv('D:\manutenção\Departamento de manutenção\defect_and_no_defect.csv')
mascara_imagens = pd.read_csv("D:\manutenção\Departamento de manutenção/train.csv")

#Temos 12997 imagens nessa base de dados
imagens_com_ou_sem_defeito.shape

#Dessas 12997 imagens temos um total de 12568 imagens únicas,429 são imagens que aparecem mais de uma vez.
imagens_com_ou_sem_defeito['ImageID'].nunique()

#Nesse dataframe temos 7095 peças com defeitos e 5902 peças sem defeito
imagens_com_ou_sem_defeito.label.value_counts()

#todas as imagens repetidas são imagens que apresentam algum tipo de problema(6666+429=7095)
imagens_com_ou_sem_defeito[imagens_com_ou_sem_defeito['label'] == 1]['ImageID'].nunique()

#5748 mascaras foram encontradas
mascara_imagens.shape

#Criando um bloco de código para saber quantos erros diferentes podem ter na mesma imagem
mascara_imagens['mask'] = mascara_imagens['ClassId'].map(lambda x: 1)
defect_type = mascara_imagens.groupby(['ImageId'])['mask'].sum()
#1-5201
#2-272
#3-1
defect_type.value_counts()
#diretório que contem a pasta com as imagens
train_images = Path("D:/manutenção/Departamento de manutenção/train_images")

for i in range(10):
  #aqui estamos juntando o caminho da pasta que contem as imagens,junto com o nome da imagem
  img = io.imread(os.path.join(train_images,mascara_imagens['ImageId'][i]))
  plt.figure()
  #e colocando com titulo a classe da imagem
  plt.title(mascara_imagens['ClassId'][i])
  plt.imshow(img)

#importando a função que vai transformar os encoded pixels em mascaras para as imagens
from utilities import rle2mask

for i in range(10):
  #aqui estamos juntando o caminho da pasta que contem as imagens,junto com o nome da imagem
  img = io.imread(os.path.join(train_images,mascara_imagens['ImageId'][i]))
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  mask = rle2mask(mascara_imagens['EncodedPixels'][i], img.shape[0], img.shape[1])

  plt.figure() 
  img[mask == 1,1] = 255
  #e colocando com titulo a classe da imagem
  plt.title(mascara_imagens['ClassId'][i])
  plt.imshow(img)
  

#como nao veio um dataset de teste e um dataset de treino vamos separar o dataset original em dois
train, test = train_test_split(imagens_com_ou_sem_defeito, test_size = 0.15)

datagen = ImageDataGenerator(rescale=1./255,validation_split=0.15)

# Definindo o tamanho do lote e outras opções de pré-processamento
batch_size = 32
#a rede resnet foi treinada com imagens 256X256
target_size = (256,256)

train['label'] = train['label'].astype(str)


# Criando um gerador de lotes de imagens a partir do diretório de treinamento
train_generator = datagen.flow_from_dataframe(dataframe=train,
        directory=train_images,
        x_col='ImageID',
        y_col='label',
        subset='training',
        shuffle=True,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary')

#criando lotes de imagens para validação a avaliação do treinamento
valid_generator = datagen.flow_from_dataframe(dataframe=train,
        directory=train_images,
        x_col='ImageID',
        y_col='label',
        subset='validation',
        shuffle=True,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary')

test_datagen = ImageDataGenerator(rescale=1./255)

#criando lotes de imagens para teste do modelo
test_generator = test_datagen.flow_from_dataframe(dataframe=test,
        directory=train_images,
        x_col='ImageID',
        class_mode=None,
        y_col=None,
        shuffle=False,
        target_size=target_size,
        batch_size=batch_size
        )

#Usando a rede pre-treinada Resnet50 como base para nosso modelo de classificação
base_model = ResNet50(weights='imagenet', include_top=False,input_tensor=Input(shape=(256, 256, 3)))

# congela as primeiras 10 camadas do modelo pré-treinado 
for layer in base_model.layers[:10]:
  layer.trainable = False

# adiciona as suas camadas personalizadas
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.2)(x)
x = Dense(1, activation='sigmoid')(x)

# juntando o modoelo base (resnet) com a parte da classficação das imagens(x)
model = Model(inputs=base_model.input, outputs=x)

# compilando o modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

#se o parametro val_loss não abaxiar depois de 20 consecutivas
earlystopping = EarlyStopping(monitor='val_loss', mode='min', patience=20)

#vai salvar os pesos(weights.hdf5) que obtiveram os melhores resultados no val_loss
checkpointer = ModelCheckpoint(filepath='weights.hdf5', save_best_only=True)

#colocando o modelo em produção
history = model.fit_generator(train_generator, epochs = 40, 
                              validation_data= valid_generator, 
                              callbacks=[checkpointer, earlystopping])
#salvando o modelo
model_json = model.to_json()
with open("resnet-classifier-model.json","w") as json_file:
  json_file.write(model_json)

#abrindo o modelo
with open('D:\manutenção\Departamento de manutenção/resnet-classifier-model.json', 'r') as json_file:
  json_saved_model = json_file.read()

model = tf.keras.models.model_from_json(json_saved_model)
model.load_weights('D:\manutenção\Departamento de manutenção\weights.hdf5')
model.compile(loss = 'binary_crossentropy', optimizer='Nadam', metrics=['accuracy'])

#fazenmdo as predições com o modelo
predictions = model.predict(test_generator)

# Arredonda as previsões para obter as classes preditas (0 ou 1)
predicted_classes = np.round(predictions)
predicted_classes=predicted_classes.astype(np.int64)
predicted_classes = predicted_classes.flatten()

# Obtém as classes reais dos dados de teste
true_classes = test['label'].values

# criando uma lista com os IDs das imagens
image_ids = test['ImageID'].tolist()

# Criar o DataFrame a partir das arrays
df = pd.DataFrame({'image_ids':image_ids,'Classe_predicted':predicted_classes , 'classe_certa': true_classes})
df['previsoes'] = np.where(df['Classe_predicted'] == df['classe_certa'], 'certo', 'errado')
#1872 previsões foram corretas contra 78 imagens que foram classificadas de forma incorreta
df['previsoes'].value_counts()

df_prevesioes_incorretas = df[df['previsoes']=='errado']
df_prevesioes_incorretas['resultado'] = np.where(df_prevesioes_incorretas['Classe_predicted'] - df_prevesioes_incorretas['classe_certa'] > 0, 'falso_positivo', 'falso_negativo')
#das 76 previsões incorretas metade delas são falsos positivios e a outra metade falso negativo(38/38)
df_prevesioes_incorretas['resultado'].value_counts()

#separando as imagens de teste
imagens_para_teste=os.listdir(train_images)

# Selecionar 10 imagens aleatórias
imagens_aleatorias = random.sample(imagens_para_teste, 10)

# Criar uma figura para as imagens
fig, axs = plt.subplots(2, 5, figsize=(15, 10))
fig.subplots_adjust(wspace=0.2, hspace=0.2)

for i, file in enumerate(imagens_aleatorias):
    # carregar a imagem
    img = io.imread(os.path.join(train_images, file))

    # Redimensionar a imagem para o tamanho correto (256x256) e normalizá-la
    img = cv2.resize(img, (256, 256))
    img = img / 255.0

    # Adicionar uma dimensão extra para a imagem
    img = np.expand_dims(img, axis=0)

    # Fazer a previsão com o modelo
    pred = model.predict(img)

    # Arredondar a previsão para obter a classe predita (0 ou 1)
    pred_class = np.round(pred)[0][0]

    # Obter a classe real da imagem
    true_class = imagens_com_ou_sem_defeito.loc[imagens_com_ou_sem_defeito['ImageID'] == file, 'label'].item()

    # Plotar a imagem com o título contendo a classe real e a classe predita
    row = i // 5
    col = i % 5
    axs[row, col].imshow(img[0])
    axs[row, col].set_title(f"Classe real: {true_class}, Classe prevista: {pred_class}",fontsize=8)
    
# Exibir a figura
plt.show()
