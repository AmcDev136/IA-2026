# Reporte EDA — Detección de persona con una imagen
**Analista:** Fernando Amilcar Rodriguez Ramirez / 22121370

## 1. Definir procesamiento
### P1 — Detección facial
- Y: coordenadas de un cuadro delimitador y binario (Rostro = 1, No rostro= 0).
- X (mínimo 5 variables):
    * matriz de pixeles por rgb: Su función será que toda la imagen la convierta en una matrz rgb.
    * Ancho de la imagen: Detectar el ancho de la imagen de entrada original.
    * Alto de la imagen: Detectar el alto de la imagen de entrada original.
    * Relación de aspecto de la imagen.
    * Nivel de brillo de la imagen: Detectar si la imagen tiene un brillo muy bajo y no se puede detectar ningún rostro. 
- Granularidad: por imagen
- Tamaño mínimo de dataset: entre 10,000 y 50,000 imagenes de rostros.

### P2 — Identificación
- Y: ID único
- X (mínimo 5 variables):
    * Recorte de rostro
    * Puntos de referencia faciales (ojos, nariz, boca, cejas, etc.)
    * Ángulo de rotación de la imagen.
    * Porcentaje de visibilidad del rostro.
    * Distancia entre los dos ojos.
- Granularidad: Por rostro.
- Tamaño mínimo del dataset: entre 100 y 500 imagenes 

## 2. Diccionario y muestra (Misión 2)
- ¿Falta alguna columna? Si, es necesario agregar:
    * Split: Indicador que separe las imagenes de entrenamiento, validación y prueba para evitar filtración de datos.
    * Etiqueta_desarrollo: Etiqueta sobre el contexto para analizar si el modelo falla en ciertos entornos.
    * Img_flag: Valor booleano que indique si la imagen es original o es generada artificialmente.