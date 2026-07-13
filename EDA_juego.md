# Reporte EDA — Juego tipo dinosaurio de google chrome
## Problema y dataset
- **Y**: ``salto`` (clase binaria ``1 = personaje en aire``, ``0 = personaje en el suelo``).
- **X (5 variables recomendadas):**
  1. `velocidad_bala`: Velocidad de aproximación del proyectil (float, valor negativo).
  2. `distancia`: Distancia absoluta en X entre el jugador y la bala (float).
  3. `tiempo_impacto` (Variable extra sugerida): Distancia dividida por el valor absoluto de la velocidad de la bala.
  4. `trigger_salto` (Variable extra sugerida): 1 solo en el frame exacto donde se presiona la tecla de salto, 0 el resto del tiempo.
  5. `altura_jugador` (Variable extra sugerida): Coordenada Y actual del personaje para dar contexto espacial de si está cayendo de un salto previo.
- **Granularidad:** Por frame (fotograma). Se registra una fila de datos nueva en cada ciclo del juego mientras exista una bala activa en pantalla.
- **Tamaño mínimo de dataset:** Mínimo técnico de 80 registros (establecido por las reglas del código), pero se recomiendan entre 1,000 y 3,000 frames de juego manual continuo para entrenar un modelo MLP estable.

## 2. Diccionario y muestra
- **Patrón:** Ecosistema de datos tabular dinámico. La información se genera en la memoria RAM como una lista de objetos (`Sample`) durante la ejecución del simulador y se exporta como un archivo plano (.csv) tradicional con columnas estrictamente numéricas.
- **¿Falta alguna columna?:** Sí. El dataset original tiene un sesgo de diseño. Es altamente recomendable agregar columnas de ingeniería de características, principalmente `tiempo_impacto` (crucial para que la red neuronal entienda el peligro real combinando velocidad y distancia) y `trigger_salto` (para eliminar el "ruido" de los datos en los frames donde el jugador ya está volando y no está tomando una decisión activa).