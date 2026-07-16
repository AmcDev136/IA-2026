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


- Qué se gana/pierde si se convierte a aprobado/reprobado:
- Outliers / errores de captura:
- Métricas (2):
- Modelo propuesto:

## Misión 4 — Tiempo de Estudio
- Pregunta de negocio:
- **Tipo propuesto:** [clasificar / predecir] — justificación:
- Hipótesis dificultad → horas:
- Cola larga: ¿borrar o conservar?
- Alternativa de binarizar Y:
- Métricas y modelo + 2 chequeos EDA:

## Síntesis (máx. 8 líneas)
1. Tabla resumen de *mis* cuatro propuestas de tipo (M1–M4).
2. Una pista que usé para decidir “clase vs número” en cualquier misión.
3. Frase final: “El tipo de problema se deduce de la pregunta y de Y porque…”