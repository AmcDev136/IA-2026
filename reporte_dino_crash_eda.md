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
(respuestas a 3 preguntas + leakage + i.i.d.)

## 4. Interpretación de resúmenes (Misión 4)
(desbalance, métricas, dist_obstacle)

## 5. Elección de modelo (Misiones 5–6)
(tabla P1/P2/P3 + contraejemplos)

## Síntesis (5 líneas)
¿Qué dataset pedirías primero y qué modelo *solo después* del EDA?