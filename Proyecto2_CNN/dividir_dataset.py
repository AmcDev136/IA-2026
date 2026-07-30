"""
split_dataset.py
Divide "Caras/" en "Caras_split/train/" y "Caras_split/val/", evitando que
frames de la MISMA ráfaga/video queden repartidos entre ambos conjuntos.

Idea clave:
    Las imágenes se ordenan por fecha de modificación. Si el salto de tiempo
    entre una imagen y la siguiente es menor a GAP_SECONDS, se consideran parte
    de la MISMA sesión de captura (mismo video / misma ráfaga de webcam).
    Si el salto es mayor, se considera el inicio de una sesión NUEVA.

    Luego, sesiones COMPLETAS (nunca imágenes sueltas) se reparten entre
    train y validación, hasta acercarse al split deseado (80/20 por defecto).

Ejecuta este script UNA VEZ antes de entrenar, y luego apunta Entrenamiento.py
a "Caras_split/" en lugar de "Caras/".
"""
import os
import shutil
import random

# Config
SOURCE_DIR = "D:/Caras/"
OUTPUT_DIR = "D:/Caras_split/"
VAL_FRACTION = 0.2      # ~20% de las imágenes para validación
GAP_SECONDS = 2.0       # salto de tiempo (en segundos) que define una sesión nueva
SEED = 123

random.seed(SEED)

# Agrupar imagenes en sesiones por persona
def agrupar_sesiones(carpeta_persona):
    """
    Devuelve una lista de sesiones, donde cada sesion es una lista de rutas
    de archivo que pertenecen a la misma rafaga/video (ordenadas por tiempo)
    """
    archivos = [
        os.path.join(carpeta_persona, f)
        for f in os.listdir(carpeta_persona)
        if f.lower().endswith((".jpg", ".jepg", ".png"))
    ]
    # ordenamos por fecha de modificacion
    archivos.sort(key=lambda f: os.path.getmtime(f))

    sesiones = []
    sesion_actual = []
    tiempo_anterior = None

    for archivo in archivos:
        tiempo = os.path.getmtime(archivo)
        if tiempo_anterior is not None and (tiempo - tiempo_anterior) > GAP_SECONDS:
            #salto grande de tiempo = nueva sesion
            sesiones.append(sesion_actual)
            sesion_actual = []
        sesion_actual.append(archivo)
        tiempo_anterior = tiempo

    if sesion_actual:
        sesiones.append(sesion_actual)

    return sesiones

# Repartir sesiones completas entre train y validacion
def repartir_sesiones(sesiones, val_fraction):
    """
    Recibe lista de sesiones de persona y decide, sesion por sesion,
    si va completa a validacion o a entrenamiento, tratando de acercarse
    al porcentade deseado en numero de imagenes
    """
    sesiones = sesiones.copy()
    random.shuffle(sesiones)

    total_imagenes = sum(len(s) for s in sesiones)
    objetivo_val = total_imagenes * val_fraction

    val_sesiones = []
    train_sesiones = []
    acumulado_val = 0

    for sesion in sesiones:
        if acumulado_val < objetivo_val:
            val_sesiones.append(sesion)
            acumulado_val += len(sesion)
        else:
            train_sesiones.append(sesion)
    return train_sesiones, val_sesiones

# Copiar archivos a nueva estructura
def copiar_sesiones(sesiones, destino_carpeta):
    os.makedirs(destino_carpeta, exist_ok=True)
    for sesion in sesiones:
        for archivo in sesion:
            nombre = os.path.basename(archivo)
            shutil.copy2(archivo, os.path.join(destino_carpeta, nombre))

# Proceso principal
def main():
    personas = [
        d for d in os.listdir(SOURCE_DIR)
        if os.path.isdir(os.path.join(SOURCE_DIR, d))
    ]
    print(f"Personas encontradas: {personas}")

    for persona in personas:
        carpeta_persona = os.path.join(SOURCE_DIR, persona)
        sesiones = agrupar_sesiones(carpeta_persona)

        n_imagenes = sum(len(s) for s in sesiones)
        print(f"\n{persona}: {n_imagenes} imágenes en {len(sesiones)} sesiones detectadas")

        train_sesiones, val_sesiones = repartir_sesiones(sesiones, VAL_FRACTION)

        n_train = sum(len(s) for s in train_sesiones)
        n_val = sum(len(s) for s in val_sesiones)
        print(f"  -> Train: {n_train} imágenes ({len(train_sesiones)} sesiones)")
        print(f"  -> Val:   {n_val} imágenes ({len(val_sesiones)} sesiones)")

        copiar_sesiones(train_sesiones, os.path.join(OUTPUT_DIR, "train", persona))
        copiar_sesiones(val_sesiones, os.path.join(OUTPUT_DIR, "val", persona))

    print(f"\nListo. Dataset dividido en: {OUTPUT_DIR}")
    print("Ahora apunta Entrenamiento.py a esta nueva estructura (ver instrucciones).")

if __name__ == "__main__":
    main()