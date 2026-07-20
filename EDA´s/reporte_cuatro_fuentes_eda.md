# Reporte EDA — Operación Cuatro Frentes
**Analista:** Fernando Amilcar Rodriguez Ramirez / 22121370

## Misión 1 — Semáforo Académico
- Pregunta de negocio: ¿Cómo saber el riesgo del alumno por reprobar al final de cada semestre?
- **Tipo propuesto:** Clasificar — justificación: La escuela está buscando organizar a sus alumnos por tipo de riesgo a reprobar, en este caso al ser 3 opciones, se necesita una clasificacion multiclase.
- Y / forma de Y: ``riesgo`` (categorica), (Verde = riesgo de reprobar, Amarillo = riesgo medio y Rojo = riesgo alto).
- X (mínimo 5):
    + ``asistencia``: Asistencias del alumno a lo largo del semestre.
    + ``materias_reprobadas``: Saber cuantas materias ha reprobado a lo largo del semestre.
    + ``porcentaje_tareas``: Porcentaje de tareas entregadas.
    + ``promedio_parciales``: Promedio por exámenes del parcial (númerica: 0 - 10).
    + ``historial``: Calificaciones de anteriores semestres. 
- Hallazgos EDA: 
+ **Patrón 1** (Fuerte relación inversa entre asistencia/calificaciones y riesgo): Existe una tendencia clara. Los alumnos etiquetados en "verde" mantienen promedios superiores a 8.0 y asistencias por encima del 85% (media de 91%). A medida que estas métricas decaen, el riesgo aumenta severamente. Un alumno con asistencia del ~50% y promedios cercanos a 5.0 cae invariablemente en rojo.

+ **Patrón 2** (El peso del historial académico): El indicador ``materias_reprobadas`` actúa como un fuerte factor agravante. Los estudiantes en riesgo "rojo" promedian 2.4 materias reprobadas anteriormente. En la muestra, ningún alumno con riesgo "verde" tiene más de cero materias previas reprobadas, lo que sugiere que el "pasado académico" arrastra el desempeño presente.

- Leakage evitado: **¿Usarías la calificación final como X?** No, la calificacion final aún no se conoce, es un dato del futuro. Si el modelo se entrena solo con un dato del futuro tendrá un entrenamiento del 100% eficas, siendo inutil en la vida real.

- Métricas coherentes con mi tipo: **Recall:** para evitar dejar alumnos sin atención o con "Falsos positivos" y un **F1-Score**.

- Modelo propuesto y condición:

## Misión 2 — Alerta de Churn
1. **Pregunta de negocio:** ¿Este alumno abandonará la materia?

2. **Tipo propuesto:** Clasificar — justificación: La escuela quiere saber si un alumno abandonará la materia, solo existen dos posibles resultados ``0 = permanece`` y ``1 = abandona``.

3. **Con N = 500 y 14% de abandona=1, calcula cuántos casos “positivos” hay. ¿Qué pasaría si alguien reportara “86% de aciertos” sin más contexto?**
    + Con una muestra total de N = 500 y un 14% de abandono, tenemos en total 70 casos positivos (donde los alumnos abandonan). A su vez, si alguien reporta 86% aciertos sin contexto, habría un desbalance en los datos, haciendo que el modelo falle.

4. **Tratamiento de NA:** Crear una variable bandera para los casos de tareas donde no se haya entregado (``NE``, "No entregado"). Después los NA originales pueden llenarse con un valor diferente para que el modelo separe los que sacaron cero de los que no entregaron.

5. **Leakage:** ¿incluirías “fecha de baja definitiva” o “nota final” como X? ¿Por qué sí/no? No, causaria fuga de información grave, haciendo que el modelo se vuelva inútil.

6. **Preguntas:**
    1. ¿Cómo está distribuida Y? Presenta un balance extremo, lo que quiere decir, que no podemos utilizar métricas de evaluación estándar.
    2. ¿Los casos abandona=1 se concentran en alumnos que trabajan?Revisando la muestra, de los 5 casos positivos, 4 de ellos tienen el flag ``trabaja=1``. Esto confirma la correlación detectada: los alumnos con carga laboral tienen mayor predisposición al abandono por falta de tiempo o presión externa.
    3. ¿Hay colinealidad sospechosa entre variables?
    Es altamente probable que ``dias_sin_login`` y ``avance_contenido_pct`` presenten multicolinealidad. Si el estudiante tiene 30 días sin conectarse, su avance de contenido inevitablemente será bajo o nulo.

7. **Compara con la Misión 1: ¿en qué se parecen y en qué se diferencian la forma de Y y el EDA que harías?** La misión 1 era un problema de clasificacion multiclase (3 estados), mientras que la misión 2 es clasificacion binaria (solo 2 estados). 
En la misión 1 era identificar rangos de promedios y asistencias que lo separaban en 3 clases, mientras que la misión 2 está centrado en manejo de balance de extremos y en interpretar los datos nulos (NA).

8. **Modelo propuesto:**

## Misión 3 — Pronóstico de Puntaje
1. **Pregunta de negocio:** ¿qué calificación final (escala 0–100) obtendrá el alumno?

2. **Tipo propuesto:** Predecir — justificación: La escuela quiere saber que calificacion final tendrá un alumno basandose en tareas, calificaciones de examenes y asistencia.

3. **Define Y y al menos 4 X. Señala cuál parece más relacionada con Y según las pistas.**
    - **Variable_Y:** ``calificaciofinal``
    - **Variables X:**
        + ``examen_1 (relacionada a Y):`` Correlaciono con ~0.85 con la **Y**, ya que se observa que los puntajes altos casi garantizan calificaiones fiales altas.
        + ``examen_2``: Similar a la anterior, se correlaciona fuertemente.
        + ``promedio_tareas``: Refleja constancia en el trabajo durante todo el semestre.
        + ``asisteciapct``: Indica nivel de exposición del alumno al material de la clase/materia. 

- Qué se gana/pierde si se convierte a aprobado/reprobado:
    Se gana simplificar el problema, convirtiendose en una clasificacion binaria, es decir, sería más facil comunicar.
    Se pierde presición y granularidad, se pierde la capacidad de distinguir un alumno sobresaliente y uno que apenas va a pasar (70 de calificacion), además de perder la capacidad de distinguir a un alumno con 59 a uno ue saca 20.

- Outliers / errores de captura:
    + **Outliers:** La mayoría de los alumnos estudia alrededor de 5 horas, pero hay unos pocos casos extremos (valores atípicos que reportan 20-25 horas) que "jalan" el promedio hacia arriba.
    + **Errores de captura:** : Limitar los valores. Transformar cualquier valor > 100 a exactamente 100 (asumiendo que fue un alumno perfecto al que le sumaron puntos extra erróneamente).

- Métricas (2):
necesitamos métricas que evalúen la distancia entre la predicción y el valor real:
    + **Error Absoluto Medio:** Mide el promedio de las diferencias absolutas entre lo predicho y lo real. Ejemplo: Un MAE de 5 significa que el modelo se equivoca, en promedio, por 5 puntos en la calificación final.

    + **Raíz del Error Cuadrático Medio:** Mide los errores, pero penaliza más fuertemente los errores grandes (al elevar las diferencias al cuadrado antes de promediarlas).

- Modelo propuesto:
    + Si la gráfica de ``examen_1`` contra ``calificacion_final`` es una línea recta: El modelo ideal sería una Regresión Lineal Simple (o Múltiple si sumamos más variables), ya que asume una relación proporcional directa.

    + **Si la gráfica tiene forma escalada:** La regresión lineal fallaría. El modelo simple ideal sería un Árbol de Decisión, el cual particiona los datos y hace predicciones por segmentos, creando visualmente ese efecto escalonado.

## Misión 4 — Tiempo de Estudio
1. **Pregunta de negocio en una frase:** ¿cuántas horas adicionales necesita un alumno para dominar el tema?

2. **Propón: ¿clasificar o predecir? Justifica con ``horas_adicionales``:**
Predecir, la escuela quiere obtener un apróximado de horas adicionales para ue un alumno domine un tema, además, la variable ``horas_adicionales`` es de tipo númerico, por lo que clasificar por clases no bastaría.

3. **Con la tabla por dificultad, formula una hipótesis EDA (“a mayor dificultad, …”):** A mayor dificultad del tema, el alumno ocupa más horas de estudio para alcanzar a dominar el tema, es decir, existe un crecimiento exponencial entre la dificultad del tema y las horas de estudio.

4. **¿Cómo inspeccionarías en EDA las categóricas ``tema_dificultad`` y ``dispositivo``?** Revisar cuántos alumnos hay en cada grupo (cuántos en dificultad alta, media, baja, cuántos usan PC, móvil o tablet). Esto explicará si algún grupo es demasiado pequeño o dominante. Además, Calcular cuántas horas adicionales en promedio necesita cada grupo.

5. **La cola > 40 h es solo 3%. ¿Borrar outliers o conservar casos reales? Argumenta antes de decidir.** Conservar los casos reales y comparar los casos específicos por los que se ocupan > 40, ajustar el tema para que sea menos 

6. **Si ``pretest_score`` y ``ejercicios_correctos_pct`` van juntos, ¿redundancia? ¿Cómo lo checarías?** Si, es casi seguro que si hay redundancia, de manera visual, crearía un gráfico de dispersión poniendo el pretest en un eje y los ejercicios en el otro. Si los puntos dibujan casi una línea recta inclinada hacia arriba, significa que dicen exactamente lo mismo y si se quiere numericamente, Calcularía la correlación. Si el resultado es un número muy cercano a 1, se confirma la redundancia.

7. **Alternativa: binarizar Y con umbral 15 h (“tutoría intensiva: sí/no”). ¿Cuándo tendría sentido y qué se pierde?** Tendría sentido solo si la escuela quisiera tomar una medida práctica, que se perdería?, Tratar exactamente a un alumno que necesita 16 horas a uno que necesita 35 horas, además de perder de vista a alumnos que aunque si necesiten de apoyo, reciban un "no".

8. **Propón métricas según tu tipo (si predices número: MAE/RMSE/…; si clasificas: otras). Justifica.** 
    + **MAE:** Es más fácil de interpretar para la escuela. Mide el promedio de equivocación. Si el MAE es de "3", significa que, en promedio, el modelo se equivoca por 3 horas al predecir el tiempo de estudio de un alumno.
    * **RMSE:** Esta métrica castiga los errores muy grandes. Es perfecta para este caso porque equivocarse por 2 horas no es tan grave, pero predecir que un alumno necesita 5 horas cuando en realidad ocupaba 25 es un error gigante que el RMSE ayudará a detectar y penalizar.

9. **Propuesta post-EDA: modelo + 2 chequeos EDA obligatorios antes de entrenar.** Modelo: Bosque aleatorio (Random forest regressor). <br>
Chequeos EDA obligatorios:
    + **Resolver la redundancia:** Confirmar que efectivamente se eliminó una de las columnas repetidas. Si se pasan al modelo, se generaría "ruido" matemático innecesario.
    + **Convertir textos a números:** Asegurar que variables como ``dispositivo`` y ``tema_dificultad`` ya fueron transformadas a un formato numérico. Sería algo obligatorio para que el algoritmo funcione.

## Síntesis (máx. 8 líneas)
1. **Tabla resumen de *mis* cuatro propuestas de tipo (M1–M4).**

| Misión | Problemas propuestos (Y) |
| --------- | --------- |
| **M1: Semáforo** | Clasificación multiclase |
| **M2: Alerta de Churn** | Clasificación binaria |
| **M3: Puntaje Final** | Predicción / Regresión (Magnitud númerica cotinua) |
| **M4: Tiempo de estudio** | Predicción / Regresión (Magnitud númerica cotinua) |

2. **Una pista que usé para decidir “clase vs número” en cualquier misión.**
Determinar si los datos de la variable objetivo representan una etiqueta finita (clase) o una escala medible (número).

3. **Frase final: “El tipo de problema se deduce de la pregunta y de Y porque…”**
El tipo de problema se deduce de la pregunta y de Y porque la naturaleza matemática del objetivo define si el algoritmo debe calcular una cantidad exacta o asignar una categoría estratégica.