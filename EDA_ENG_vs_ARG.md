# Analisis explicatorio de Datos (EDA) 
## Inglaterra vs Argentina

Al explorar los datos históricos y el rendimiento de ambas selecciones hasta llegar a esta instancia de la Copa Mundial 2026, los hallazgos principales son:

+ **Distribución de Probabilidades:** Inglaterra llega con una ligera ventaja matemática (39.1% de probabilidad de victoria en los 90 minutos) frente a Argentina (31.6%). El modelo asigna un 29.3% de probabilidad a un empate que forzaría el tiempo extra.

+ **Desgaste Físico:** Una variable clave que el EDA resaltaría es el tiempo en cancha. Ambos equipos llegan tras extenuantes partidos de Cuartos de Final que se definieron en la prórroga (Inglaterra superó a Noruega 2-1 y Argentina a Suiza 3-1).

+ **Poderío Ofensivo Sesgado:** La dupla inglesa de Jude Bellingham y Harry Kane representa casi la totalidad de la producción ofensiva de su equipo en el torneo, un sesgo de dependencia vital a considerar en el modelo.

+ **Historial Directo:** En 14 enfrentamientos competitivos y amistosos previos, Inglaterra tiene una tendencia favorable con 6 victorias contra 3 de Argentina (y 5 empates).

## Estructura del dataset.
Un buen dataset requiere características que capturen el contexto y el momentum relativo de cada selección.
### Variables de Identificación y Contexto:
+ **Fecha_partido (Datetime):** Para ordenar cronológicamente y calcular rachas.

+ **Tipo_torneo (Categórica):** Amistoso, Eliminatoria, o Mundial (al codificar, los partidos de Mundial tendrían un peso estadístico mucho mayor).

+ **Cancha_neutral (Booleana):** True en este caso, ya que juegan en un país tercero (EE. UU.).

### Variables de fuerza relativa
+ **Elo de rating a y b**: El puntaje Elo actualizado a la fecha del partido es el predictor histórico más fuerte en el fútbol, superior al Ranking FIFA tradicional.

+ ``diferencia_elo``: La resta matemática entre ambos ratings.

### Variables de forma reciente
+ **Porcentajes de victorias:**

+ **Goles a favor en promedio y promedio de goles en contra:** Refleja el momento ofensivo actual y la solidez de la línea defensiva.

+ **Minutos jugados en el mundial:** Para medir el nivel de desgaste fisico acumulado.

### Variables objetivo (target)
+ **Resultado:** La etiqueta a predecir. Generalmente se define como 1 (Victoria Inglaterra), 0 (Empate), o -1 (Victoria Argentina). Para predicciones estándar, se utiliza el resultado pitado en los 90 minutos reglamentarios, ignorando las tandas de penales.