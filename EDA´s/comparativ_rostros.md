# Reporte comprativo técnico
## Eigenfaces vs Fisherfaces vs LBPH
Este reporte técnico analiza en profundida los tres algoritmos clásicos más utilizados en la visión por computadora para el reconocimiento facial: **Eigenfaces, Fisherfaces y LBPH** (Local Binary Patterns Histograms). A continuación se desglosa sus fundamentos, capacidades, limitaciones y sensibilidad ante variaciones del entorno.

## 1. Fundamentos teóricos y enfoque
Para comprender el comportamiento de cada algoritmo ante factores externos, es crucial analizar cómo modelan y extraen la información de un rostro.

### A. Eigenfaces
+ **Enfoque:** Utiliza el Análisis de Componentes Principales (PCA). Su objetivo es reducir la dimensionalidad del espacio de imágenes de rostros encontrando los vectores (autovectores o eigenvectors) que maximizan la varianza total de los datos.

+ **Mapeo:** Construye un "espacio de rostros" (face space). Cada rostro nuevo se proyecta en este espacio y se representa como una combinación lineal de las caras base (las eigenfaces).

### B. Fisherfaces
+ **Enfoque:** Holístico y supervisado (clasificación por clases/identidades).

+ **Fundamento:** Utiliza el Análisis Discriminante Lineal (LDA) de Fisher. A diferencia de PCA, que busca la variación global sin importar a quién pertenece la foto, LDA busca componentes que maximicen la separación entre diferentes personas (varianza entre clases) y minimicen la separación entre fotos de la misma persona (varianza dentro de la clase).

+ **Mapeo:** Proyecta las imágenes en un espacio donde las identidades forman grupos (clusters) claramente separados y compactos.

### C. LBPH (Local Binary Patterns Histogram)
+ **Enfoque:** Local y basado en texturas microestructurales.

+ **Fundamento:** No analiza la imagen globalmente de forma matricial directa. Divide la imagen en subregiones (celdas) y aplica el operador LBP (Patrón Binario Local) en cada píxel, comparándolo con sus 8 vecinos. Si el vecino es mayor o igual al centro, se marca con ``1``, de lo contrario con ``0``. Esto genera un código binario de 8 bits por píxel que representa texturas como bordes, esquinas o líneas.

+ **Mapeo:** Se genera un histograma de frecuencias de texturas para cada celda y se concatenan todos en un único vector de características que representa la huella digital del rostro.

## 2. Tabla comparativa de rendimiento
| Criterio | Eigenfaces | Fisherfaces | LBPH |
| --------- | --------- | --------- | --------- |
| **Técnica Matemática** | Reducción de dimensión no supervisada (PCA). | Reducción y clasificación supervisada (LDA). | Operaciones lógicas locales y análisis frecuencial (Histogramas). |
| **Sensibilidad lumínica** | **Muy alta**. El brillo domina la varianza principal. | **Moderada**. Tiende a ignorar componentes debidos a la luz si se fue entrenado con ella. | **Muy baja**. El contraste relativo local permanece invariante. |
| **Sensibilidad a poses/expresiones** | **Alta**. Requiere alineación matemática estricta. | **Moderada**. Tolera variaciones si están representadas en el entrenamiento. | **Baja-moderada**. La división por celdas tolera ligeros desplazamientos espaciales. |
| **Minimo de fotos para entrenar** | 1 foto por persona puede bastar para un espacio básico. | **Requisito crítico:** Múltiples fotos por persona (``N > clases``). | 1 foto por persona es suficiente para crear su histograma base. |
| **Carga computacional (Entrenamiento)** | Media (Cálculo de la matriz de covarianza y autovalores). | Alta (inversión de matrices de dispersión complejas). | Muy baja/nula. No requiere un entrenamiento matricial global costoso. |
| **Sensibilidad al ruido/calidad** | Baja (PCA filtra el ruido de alta frecuencia de forma nativa). | Baja (LDA se enfoca en rasgos macro discriminantes). | Alta. El ruido de pixeles individuales altera los códigos binarios locales. |

## 3. Análisis detallado de sensibilidad y limitaciones
### Sensibilidad de iluminación
+ **Eigenfaces:** Es extremadamente vulnerable. Dado que PCA busca la mayor variación matemática en los píxeles, los cambios drásticos de luz (por ejemplo, una sombra que oscurece la mitad del rostro) alteran los valores numéricos globales mucho más que las sutiles diferencias entre las identidades de dos personas. El algoritmo clasificará los rostros basándose en el patrón de luz en lugar de en la identidad.

+ **Fisherfaces:** Mitiga el problema de la luz modelándolo como una variación "dentro de la clase". Si el set de entrenamiento incluye fotos de la misma persona con diferentes luces, LDA aprenderá a ignorar las dimensiones de la iluminación porque no ayudan a distinguir entre identidades. Si no cuenta con esas muestras, su precisión disminuye.

+ **LBPH:** Es el más robusto. Al calcular la relación del píxel central con sus vecinos (I( x<sub>c</sub>) > I( x<sub>n</sub> )), si la iluminación de la escena cambia uniformemente, el valor de todos los píxeles de la zona sube o baja proporcionalmente, pero el orden relativo (mayor o menor) se mantiene idéntico. Por ende, el código binario resultante y su histograma apenas se alteran.

### Sensibilidad a expresiones y cambios de pose
+ **Eigenfaces:** Al depender de la superposición matricial perfecta del rostro completo, una sonrisa amplia, ojos cerrados o una leve rotación de la cabeza desplazan la posición de los ojos, nariz y boca en los vectores de entrada, destruyendo la correspondencia matemática con el espacio de rostros entrenado.

+ **Fisherfaces:** Al igual que con la luz, si el algoritmo ve suficientes variaciones de expresión de cada persona durante el entrenamiento, puede encontrar un subespacio donde las expresiones se minimicen y la estructura ósea de la identidad prevalezca.

+ **LBPH:** Al dividir el rostro en una cuadrícula independiente (ej. celdas de <code>8 x 8</code> píxeles), si una persona sonríe, las alteraciones en los histogramas ocurren principalmente en las celdas de la boca y mejillas, pero las celdas de los ojos, cejas y frente permanecen idénticas. Esto le permite mantener una tasa de reconocimiento aceptable frente a expresiones moderadas.

### Impacto de la resolucion y el ruido
+ **Eigenfaces y Fisherfaces:** Tienen un rendimiento decente con imágenes de baja resolución o desenfocadas, ya que capturan la estructura geométrica macro del rostro. El ruido blanco aleatorio suele cancelarse durante la reducción de componentes.

+ **LBPH:** Es altamente sensible al ruido digital o granulado de la cámara. Un solo píxel ruidoso puede cambiar por completo el patrón binario de 8 bits de su vecindario, alterando la frecuencia del histograma local. Requiere filtros previos de suavizado (como el filtro Gaussiano) si las condiciones de captura no son limpias.

## 4. Conclusiones y aplicación
1. **Selecciona eigenfaces si:** Dispone de un entorno de captura industrial completamente controlado (iluminación fija, posición frontal obligatoria), bases de datos pequeñas y busca una implementación matemática sencilla de compresión de características.

2. **Selecciona fisherfaces si:** Cuenta con una base de datos robusta con múltiples fotografías por persona tomadas bajo diferentes condiciones (luz, expresiones) y necesita un sistema con alta tasa de discriminación entre una gran cantidad de usuarios.

3. **Selecciona LBPH si:** Su aplicación se desplegará en entornos del mundo real con iluminación impredecible (cámaras web en interiores, smartphones al aire libre), tiene pocas imágenes de muestra por persona (incluso solo una) y necesita un algoritmo rápido que pueda actualizarse dinámicamente agregando nuevos usuarios sin reentrenar todo el sistema.
