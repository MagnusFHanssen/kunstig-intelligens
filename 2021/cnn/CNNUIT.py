# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 22:56:33 2021

@author: 47900
"""
#The essential resources
import numpy as np
import pandas as pd 
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.preprocessing import image
tf.compat.v1.set_random_seed(2019)

#The model with the different parts of the processing steps

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16,(3,3),activation = "relu" , input_shape = (180,180,3)) ,
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(32,(3,3),activation = "relu") ,  
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64,(3,3),activation = "relu") ,  
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128,(3,3),activation = "relu"),  
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(), 
    tf.keras.layers.Dense(550,activation="relu"),      #Adding the Hidden layer
    tf.keras.layers.Dropout(0.1,seed = 2019),
    tf.keras.layers.Dense(400,activation ="relu"),
    tf.keras.layers.Dropout(0.3,seed = 2019),
    tf.keras.layers.Dense(300,activation="relu"),
    tf.keras.layers.Dropout(0.4,seed = 2019),
    tf.keras.layers.Dense(200,activation ="relu"),
    tf.keras.layers.Dropout(0.2,seed = 2019),
    tf.keras.layers.Dense(16,activation = "softmax")   #Adding the Output Layer
])

#specifying the optimizer for error reduction in training
#Optimizer is used to reduce the cost calculated by cross-entropy
#The loss function is used to calculate the error
#The metrics term is used to represent the efficiency of the model

from tensorflow.keras.optimizers import RMSprop,SGD,Adam
adam=Adam(lr=0.001)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics = ['acc'])


#Getting the training images (which are lebeled)
#Getting the validation set (also lebeled for the purpose of verification)

bs=30         #Setting batch size
train_dir = "C:/Users/47900/Documents/images/archive/LEGObricks"   #Setting training directory
test_dir = "C:/Users/47900/Documents/images/archive/LEGObricks"   #Setting testing directory



from tensorflow.keras.preprocessing.image import ImageDataGenerator 
# All images will be rescaled by 1./255.
datagen = ImageDataGenerator(validation_split=0.2, rescale = 1.0/255. )
#test_datagen  = ImageDataGenerator( rescale = 1.0/255. )




# Flow training images in batches of 20 using train_datagen generator
#Flow_from_directory function lets the classifier directly identify the labels from the name of the directories the image lies in
train_generator=datagen.flow_from_directory(train_dir,subset='training', batch_size=bs,class_mode='categorical',target_size=(180,180))
validation_generator = datagen.flow_from_directory(train_dir,subset='validation', batch_size=bs, class_mode  = 'categorical',target_size=(180,180))


                                                  
#start training and validate
history = model.fit(train_generator,
                    validation_data=validation_generator,
                    steps_per_epoch=100 // bs,
                    epochs=250,
                    validation_steps=50 // bs,
                    verbose=2)

loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, color='red', label='Training loss')
plt.plot(epochs, val_loss, color='green', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

acc = history.history['acc']
val_acc = history.history['val_acc']
plt.plot(epochs, acc, color='red', label='Training acc')
plt.plot(epochs, val_acc, color='green', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

#testing

# Get test image ready

labels = ['Brick corner 1x2x2', 'Brick2x2', 'Brick1x2', 'Brick1x1','Plate2x2','Plate1x2', 
          'Plate1x1','Roof tile1x2x45deg','Flat tile1x2', 'Peg 2M',
          'Bush for cross axle', 'Plate 1x2 with knob','Technical lever3M', 'Bush 3M...',
          'Cross Axle 2M ...', 'half Brush']


def test():
    img_width, img_height = 180,180
    test_image = image.load_img('C:/Users/47900/Documents/images/archive2/peg.png', target_size=(img_width, img_height))
    test_image = image.img_to_array(test_image)
    test_image /= 255.
    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict(test_image, batch_size=1)
    print(result)
    df = pd.DataFrame(list(zip(labels, result[0])), columns =['Types', 'Classification']) 
    print(df) 

