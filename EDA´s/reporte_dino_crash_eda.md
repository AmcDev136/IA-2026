# Reporte EDA — Operación Dino Crash
**Analista:** Fernando Amilcar Rodriguez Ramirez / 22121370

## 1. Problema y dataset (Misión 1)
### P1 — Muerte en el siguiente frame
- Y: La columna seria jump (de las propuestas) y de tipo binaria 0/1.
- X (mínimo 5 variables):
    * ```Obstacle_type```: Saber el tipo de obstáculo y adaptar el salto al mismo.
    * ```Frame```: Para contar los frames y tener registro de las acciones realizadas y las acciones a realizar.
    * ```Time_ms```: Para saber el tiempo de partida y si llega a perder saber cuanto duró la misma.
    * ```Speed```: Para medir la velocidad del juego y planear mejor los saltos y/o saber en que velocidad empieza a subir la dificultad.
    * ```Dist_obstacle```: Medir el próximo salto y saber el tipo de salto (largo o corto), a su vez, saber si es un salto posible (que evite el objeto).
- Granularidad: Necesito un frame cada 16ms (puede cambiar dependiendo de la velocidad inicial y la velocidad de los obstáculos).
- Tamaño mínimo de dataset: El tamaño minimo considero que serían entre 10 partidas como mínimo y 50 partidas (prueba y error) para podeer confiar.
- Riesgo si el dataset está mal definido: El riesgo es bastante, ya que si el dataset no contiene los saltos efectuados o un mal diseño, siempre perderá el juego.

### P2 — Puntos por partida
- Y: Numérico.
- X (mínimo 5 variables):
    * ```time_ms```: Saber cuanto tiempo lleva jugando para predecir el número de puntos.
    * ```score```: La puntuacion en la pantalla indica como va el progreso de la misma, ayuda a la variable anterior.
    * ```obstacle_type```: Suponiendo que cada tipo de obstáculo tiene diferentes puntajes al momento de ser superados.
    * ```died```: Saber si el juego ha concluido (sirve para no hacer mediciones en vano).
    * ```speed```: Sirve para saber que tan avanzado va en el juego, se ayuda con la primera y segunda variable.
- Granularidad: Resumen por partida.
- Tamaño mínimo de dataset: Se necesita alrededor de 100 partidas para poder empezar a medir los resultados sin demasiado sesgo.
- Riesgo si el dataset está mal definido: No es un riesgo tan grande, únicamente observo que se podría equivocar en las predicciones de los puntajes.

### P3 — Tipo de obstáculo siguiente
- Y: Categórica.
- X (mínimo 5 variables):
    * ```time_ms```: Sirve para observar el tiempo desde que se inició el juego y los tipos de obstaculos dependiendo del tiempo.
    * ```score```: Sirve para analizar el puntaje en pantalla y a su vez predecir la dificultad y/o consistencia en que saldrán los próximos obstáculos.
    * ```speed```: Al igual que la primera variable, analizar la velocidad y predecir los objetos que saldrán, por ejemplo, si los cactus largos salen a partir de cierta velocidad en adelante.
    * ```obstacle_type```: Sirve para saber los tipos de obstáculos y que no prediga o diga un obstáculo que no existe.
    * ```frame```: Analizar frame por frame, ayuda con las tres primeras variables.
- Granularidad: frame cada salto.
- Tamaño mínimo de dataset: Tamaño minimo a considerar, alrededor de 70 partidas, para analizar todos los objetos que existen.
- Riesgo si el dataset está mal definido: Si el dataset está mal definido, se puede encontrar con que la precisión a la hora de predecir el siguiente obstáculo sea erróneo.

## 2. Diccionario y muestra (Misión 2)
1. ¿Qué patrón ves en la fila donde ```died=1``` (frame 82)?
Al analizar la fila, observo que hay dos opciones de muerte, la primera, que el usuario dio por terminado el juego (cierre del mismo intencional o accidental), segunda, que fue error del usuario, ya que al ver el frame anterior, se observa que el objeto todavia estaba considerablemente lejos.
2. ¿```score``` es buena variable para predecir muerte en el siguiente frame? ¿Por qué sí o no? Si bien, puede ser de ayuda para predecir, no garantiza que sea clave para la prediccion, ya que al tener mayor puntaje (score) hay más probabilidades de perder ya que el juego se hace cada vez más dificil.
3. ¿Falta alguna columna crítica para P1? (pista: altura del dino, agachado, lag de reacción del jugador…) Si, faltaría el tiempo en el que reacciona el jugardor.
4. ¿```died``` tal como está definida sirve para P1 o solo describe el final de la partida? Solo describe el final de la partida.

## 3. Checklist EDA (Misión 3)
2. ¿Hay valores faltantes? Si, hay 3% de NA por columna, trato de evitar respuestas con NA, ademas le digo al modelo que interprete el NA como nulo o 0.
6. ¿Distribucion de speed? En el caso del juego, no hay tope o limite claro, sigue subiendo, en esos casos, utilizo la velocidad máxima en el dataset como limite.
7. ¿Outliners? Hay pocos, en ese caso trato de limpiarlos manualmente, si no, creo un algoritmo que busque y limpie automaticamente.

8. ¿Datos i.i.d.? Es un error ya que el modelo se puede confundir y pensar que esta analizando datos duplicados.
4. Leakage: Puede haber un caso especifico en el que el tiempo de partida es corto, es decir, apenas va iniciando, pero el puntaje (score) es alto, existe una redundancia ya que no puede tener un puntaje alto con un tiempo que apenas va empezando, o alrevés, que apenas vaya empezando la partida con un puntaje alto

## 4. Interpretación de resúmenes (Misión 4)
1. ¿El problema P1 (muerte en siguiente frame) está desbalanceado? Cuantifica con los números dados. Si, está notoriamente desbalanceado.
2. ¿Qué implica eso para la métrica que usarías? (accuracy vs precision/recall/F1). Usaría recall para medir la cantidad de muertes que logra detectar, precision para evitar falsos positivos y f1 para equilibrar las dos anteriores
3. ¿```dist_obstacle``` parece útil como predictor? Argumenta con la fila de muertes. Dependiendo de la clase o tipo de predicción que se necesite, por ejemplo, si se quiere saber si va a morir en el siguiente frame no es útil, ya que no serviria de mucho saber la distancia, si no, el tiempo de respuesta del jugador. 
4. ¿La distribución de score sugiere regresión simple o necesitas transformación / otro enfoque? Sugiere regresión simple. La distribucion muestra que no es simetrica, por lo cual, convendría aplicar una transformación o un enfoque más especifico.

## 5. Elección de modelo (Misiones 5–6)
| Escenario | Tras tu EDA, ¿qué fila de la guía aplica? | Modelo que propondrías | 2 condiciones del dataset que deben cumplir |
| --------- | --------- | --------- | --------- |
| P1    | Secuencia de frames por sesión | LTSM/GRU | El dataset debe contener todas las partidas completas y calcular la probabilidad de dificultad del obstáculo |
| P2    | Y numérica | Regresión lineal | El dataset debe contener varias partidas con los puntajes finales, debe contener el valor númerico de los objetos (valor por esquivar) y cuantos obstáculos se esquivaron |
| P3    | Categórica multiclase | Árbol | El dataset debe contener los tipos de obstaculos que existe y la probabilidad en que apareciero en partido y/o el número de los obstáculos aparecidos |


## Contraejemplo — Cuando no usar un modelo
### 1. Escenario con árbol profundo
En primer lugar parecería buena idea usar un árbol de decisión profundo ya que podría segmentar las opciones de forma jerárquica para reglas especificas, sin embargo, el eda lo desestima por dos problemas:
    + La variable ```distancia_obstaculo``` disminuye estrictamente de manera lineal conforme para el tiempo (milisegundos), mientras que el árbol divide el espacio en forma de bloques rígidos, quiere decir, que el árbol tendría que tener una profundida exagerado.
    + El EDA revela que en pequeñas variaciones en el retardo de ```tiempo__presion_tecla``` cambia drásticamente el resultado. Al cambiar minimamente la velocidad de testeo, el modelo falla debido a la rigidez de sus hojas terminales con pocos datos.

### 2. Escenario con red neuronal
El mapa de la matriz de pixeles en una direccion requiere extraer patrones especiales y temporales que no son linealmente separables manualmente.
#### Que deberiamos ver en el EDA para justificar:
1. Si tomamos una muestra de imagenes del juego y aplanamo los pixeles en un vector, el análisis de componentes mostraria que los datos no se agrupan de manera limpia, es decir, la varianza requeriria cientos de componentes ppara poder explicarla.
2. Un análisis de correlación entre el valor de pixeles individuales y la variable objetivo (```acción```) daria valores cercanos a 0. Esto demuestra que la información no reside en pixeles aislados, sino, en la interacción compleja y jerárquica de bloques de pixeles próximos.

### 3. P1 con reglas fijas vs modelo aprendido
Pregunta: ¿Es viable usar una regla fija como ```si dist_obstacle < X y jump=0 entonces muerte``` en lugar de un modelo de machine learning?
**Comparativa**
| Criterio | Reglas fijas | Modelo Aprendido |
| --------- | --------- | --------- |
| Ventajas | -**Determinista y rapido**: Cero coste computacional en tiempo de ejecución. <br> -**Explicabilidad**: 100% transparente con el desarrollador | -**Adaptabilidad**: Capacidad de generalizar ante escenarios no previstos. <br> -**Manejo de incertidumbre**: Devuelve probabilidades en lugar de decisiones rígidas. |
| Limites | -**Rígidez dinámica**: El juego acelera constantemente. Un rango de X fijo que funciona con velocidad inicial provocará muerte muerte a velocidad máxima debido al cambio en el tiempo de reacción. <br> -**Fragilidad en multivariables**: Si se añade el factor de las aves (pterodáctilos con altura variable), el número de reglas manuales crece, volviendose complicado de manejar. | -**Costo de datos**: Requiere un dataset representativo de la curva de velocidad del juego. <br> -**Latencia**: La inferencia del modelo consume más ciclos de CPU/GPU que una condicional. |

#### Conclusión
Para la versión base y estática del juego, una regla fija bien diseñada (que incluya la velocidad como variable, ej: $X = f(\text{velocidad})$) podría resolver el problema de forma óptima sin necesidad de IA.Sin embargo, si el EDA demuestra que la relación entre la velocidad, el tipo de obstáculo y la distancia segura es no-lineal o presenta anomalías (como lag), el modelo aprendido es mejor ya que ajustará las fronteras de decisión basándose en la experiencia real del dataset.

## Síntesis (5 líneas)
¿Qué dataset pedirías primero y qué modelo *solo después* del EDA?
El dataset inicial que pediria sería uno que deba contener las siguientes caracteristícas a lo largo de varias partidas: <br>
**Variables**:
+ ``velocidad_juego`` (númerica): La velocidad actual del scroll en pantalla.
+ ``distancia__obstaculo`` (númerica): Distancia en pixeles entre el obstáculo más cercano al eje X.
+ ``tipo_obstaculo`` (categorica multiclasificación): Tipo de obstáculo (cactus chico, cactus grande, ave alto, ave bajo).
+ ``altura_obstaculo`` (númerica): Altura en el eje Y (para aves).
+ ``estado_dino`` (categórica): Si el dino está corriendo, saltando o agachado en el instante.

Target:
+ ```accion_tomada``` (categorica multiclasificación): ``0 = nada``, ``1 = Salto``,  ``2 = agachado``.

### Después del EDA
Una vez ejecutado el EDA sobre el dataset tabular recolectado, la estrategia de modelado se divide en tres escenarios posibles según la estructura, relaciones y patrones que hayamos descubierto en los datos:

### Escenario A: Clasificación de Acción Inmediata
* **Si el EDA encuentra:** Que el dataset es de naturaleza puramente tabular ($N$ mediano), donde la variable objetivo es la acción (`Y` categórica multiclasificación: *Saltar, Agacharse, Nada*) y las fronteras de decisión entre las variables físicas (distancia, altura del obstáculo) están bien delimitadas.
* **Modelo Razonable:** **Logística Multinomial** o un **Árbol de Decisión** de baja profundidad. Permiten un mapeo directo y rápido de las características del entorno hacia la acción óptima.
* **Modelo Poco Razonable:** **Regresión lineal sobre códigos numéricos (1, 2, 3)**. Tratar las clases categóricas de las acciones como variables numéricas continuas induciría al modelo a asumir una falsa jerarquía o distancia matemática entre "saltar" y "agacharse" que no existe.

### Escenario B: Dependencia Temporal y Secuencial
* **Si el EDA encuentra:** Una fuerte autocorrelación temporal al analizar la **secuencia de frames por sesión**. Es decir, el análisis revela que la decisión óptima en el frame actual depende críticamente de la inercia, la aceleración acumulada o el ritmo de los obstáculos en los frames inmediatamente anteriores.
* **Modelo Razonable:** Extracción manual de **features temporales combinadas con un clasificador clásico**, o bien, el uso de redes **LSTM/GRU** (redes recurrentes) *únicamente* si el volumen de sesiones es lo suficientemente grande para mitigar el sobreajuste.
* **Modelo Poco Razonable:** Cualquier clasificador tradicional entrenado tras un particionamiento de datos que **ignore el orden temporal** (ej. *Shuffle Split*). Revolver los frames destruye la estructura de serie temporal que el EDA identificó como clave.

### Escenario C: Fronteras de Decisión Altamente Lineales
* **Si el EDA encuentra:** Que al cruzar las variables principales (como la relación matemática simple entre `distancia_obstaculo` y `velocidad_juego`), los diagramas de dispersión muestran una **relación clara, lineal y con muy pocas variables** para predecir la supervivencia (`Y` binaria: *Muerte / Vivo*).
* **Modelo Razonable:** **Regresión Logística**. Ofrece una solución matemática directa, con máxima interpretabilidad y coste computacional casi nulo en tiempo de ejecución.
* **Modelo Poco Razonable:** Un **Ensemble opaco sin necesidad** (como un Random Forest masivo o un XGBoost con cientos de estimadores). Añadir cajas negras ultra complejas solo incrementaría la latencia de inferencia en el juego sin aportar valor real sobre una simple frontera lineal.