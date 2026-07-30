# Script de entrenamiento de cnn
import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models

# Configuración genera
DATASET_DIR = 'D:/Caras_split/'
TRAIN_DIR = DATASET_DIR + "train/"
VAL_DIR = DATASET_DIR + "val/"
IMG_HEIGHT = 150
IMG_WIDTH = 150
BATCH_SIZE = 32
EPOCHS = 20
SEED = 123

MODEL_OUTPUT_PATH = "modelo__caras.keras"
LABELS_OUTPUT_PATH = "clases.json"

# Carga de datos
# En lugar de usar validation_split (que reparte imágenes SUELTAS
# de forma aleatoria y puede filtrar frames casi idénticos entre train y val),
# cargamos train y validación desde carpetas YA separadas por split_dataset.py,
# el cual agrupa las imágenes por sesión de captura (ráfaga/video) antes de
# repartirlas. Así garantizamos que ninguna sesión quede partida entre ambos
# conjuntos, y la validación mide generalización real, no memorización.
#
# color_mode='grayscale' -> aunque tus imágenes estén guardadas A COLOR en disco,
# TensorFlow las decodifica y las convierte automáticamente a 1 solo canal
# (escala de grises) durante la carga. No hace falta convertirlas tú a mano.
#
# Tensores resultantes por batch:
#   images: (BATCH_SIZE, 150, 150, 1)
#   labels: (BATCH_SIZE,)  -> enteros (sparse), NO one-hot
train_ds = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    seed=SEED,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    color_mode="grayscale",
    label_mode="int" #Etiquetas enteras
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    VAL_DIR,
    seed=SEED,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    color_mode="grayscale",
    label_mode="int",
    shuffle=False
)

# class_names contiene el orden en el que Keras mapeó cada subcarpeta a un
# índice entero: class_names[0] -> primer label, etc.
class_names = train_ds.class_names
num_classes = len(class_names)
print(f"Clases encontradas ({num_classes}): {class_names}")

# Calculo de class_weight
# Si una persona tiene muchas más imágenes que otra (por ejemplo, porque se
# sacaron frames de varios videos), el modelo tiende a "apostar" por esa
# clase mayoritaria cuando no está seguro. class_weight le dice a Keras que
# penalice más fuerte los errores en las clases con MENOS imágenes, para
# que no queden en desventaja durante el entrenamiento.
conteo_clase = {
    nombre: len(os.listdir(os.path.join(TRAIN_DIR, nombre)))
    for nombre in class_names
}
print(f"Imagenes de entrenamiento por clase: {conteo_clase}")

total_imagenes = sum(conteo_clase.values())
class_weight = {
    i: total_imagenes / (num_classes * conteo_clase[nombre])
    for i, nombre in enumerate(class_names)
}
print(f"class_weight calculado: {class_weight}")

# Optimizacion del pipeline
# AUTOTUNE deja que tf.data decida dinámicamente cuántos elementos
# precargar en paralelo mientras la CPU/GPU entrena el batch actual.
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# Data augmentatio (activo para entrenamiento)
# Estas capas generan variaciones aleatorias de cada imagen EN CADA ÉPOCA
# (rotación leve, zoom, espejo horizontal, brillo/contraste). El objetivo es
# que el modelo deje de memorizar detalles fijos de cada sesión de captura
# (fondo, iluminación exacta, compresión del video) y en su lugar aprenda
# rasgos faciales que se mantengan bajo esas variaciones.
#
# IMPORTANTE: estas capas de Keras se desactivan automáticamente durante
# model.predict()/evaluación (solo aplican su efecto cuando training=True,
# lo cual ocurre internamente durante model.fit()). No hay que hacer nada
# especial en detect_webcam.py para "apagarlas".
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.06),      # (+- 20 grados máx)
    layers.RandomZoom(0.1),
    layers.RandomBrightness(0.15),
    layers.RandomContrast(0.15),
], name="data_augmentation")

# Normalizacion
# Rescaling(1./255) convierte los píxeles de rango [0, 255] a [0, 1].
# Se incluye como capa DENTRO del modelo (en vez de aplicarla al dataset)
# para que el mismo preprocesamiento quede "congelado" en el .keras
# y no haya que repetirlo manualmente en el script de inferencia.
normalization_layer = layers.Rescaling(1.0 / 255)

# Definicion de arquitectura CNN
# Flujo de tensores (entrada 150x150x1, tf convierte a gris)
# Input (150x150x1), Conv2D (32,3x3) = (148x148x32) + ReLU
# MaxPooling2D (74x74x32), Conv2D (64, 3x3) = (72x72x64) + ReLU
# MaxPooling2D (36x36x64), Conv2D (128, 3x3) = (34x34x128) + ReLU
# MaxPooling2D (17x17x128), Flatten (36992), Dense (128) + ReLU
# Dropout(0.5) = antioverfitting
# Dense(num_classes) = (num_classes) + softmax = distribucion de probabilidad
model = models.Sequential([
    layers.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 1)),
    normalization_layer,

    layers.Conv2D(32, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(128, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),

    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.5),
    layers.Dense(num_classes, activation="softmax")
])

model.summary()

# Compilacion
## sparse_categorical_crossentropy se usa porque las etiquetas son
# enteros y NO vectores one-hot.
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Callback
# Detiene el entrenamiento si la val_loss deja de mejorar y restaura
# los mejores pesos vistos, evitando entrenar de más (overfitting).
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=4,
    restore_best_weights=True
)

# Entrenamiento
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    callbacks=[early_stopping],
    class_weight=class_weight
)

# Guardado y etiquetas
model.save(MODEL_OUTPUT_PATH)
print(f"Modelo guardado en {MODEL_OUTPUT_PATH}")

# guardamos un diccionario para salida numerica del softmax
labels_dict = {str(i): name for i, name in enumerate(class_names)}
with open(LABELS_OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(labels_dict, f, ensure_ascii=False, indent=4)

print(f"Etiquetas guardadas en: {LABELS_OUTPUT_PATH}")
print("Entrenamiento finalizado")