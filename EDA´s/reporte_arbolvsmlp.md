# Reporte comparativo: MLP vs Árbol de decisión en juego tipo Dino_Crash

## 1. Contexto
Se desarrolla un juego endless runner (Como el dinosaurio de Google Chrome), donde primero se juega de modo manual, con la finalidad de crear un dataset y entrena un modelo de clasificación binaria para predecir si el jugador debe saltar en modo **Auto**. Originalmente el modelo era un `MLPClassifier` (red neuronal) de scikit-learn; se migró a un `DecisionTreeClassifier` (árbol de decisión). Este documento compara ambas versiones a nivel de backend (ML) y de experiencia de juego.

## 2. ¿Qué cambia en el backend?
1. **Los imports:** antes importaba ``MLPClassifier`` y ``StandardScaler``, ahora importo ``DecisionTreeClassifier``.

2. **No necesita escalar los datos:** con la red neuronal tenía que usar ``StandardScaler`` para "normalizar" los números antes de metérselos al modelo (si no, la red no aprende bien). Con el árbol esto ya no hace falta, así que borré esa parte.

3. **Cómo se entrena el modelo:** en vez de crear una ``MLPClassifier`` con capas ocultas, ahora creo un ``DecisionTreeClassifier`` con dos parámetros para que no se sobreajuste: ``max_depth=5`` (que no crezca demasiado) y ``min_samples_leaf=5`` (que cada "rama final" tenga al menos 5 ejemplos).

4. **Cuando el bot decide si saltar:** antes tenía que transformar los datos con el scaler antes de preguntarle al modelo. Ahora simplemente le paso los datos tal cual al árbol.

5. **Textos del juego:** cambié las partes del menú y de las gráficas que decían "MLP" para que digan "Árbol de Decisión".

## 3. ¿Qué cambia en el frontend (la ventana de juego)?
| Cosa que noté | Con la red neuronal (MLP) | Con el árbol de decisión |
|---|---|---|
| Cómo salta el bot | Pareciera que va "probando" un poco antes, la transición es más suave | Es más brusco: no salta, no salta... y de repente sí salta, como si tuviera un límite fijo |
| El número de probabilidad en pantalla | Va cambiando poco a poco (0.2, 0.35, 0.5, 0.8...) | Se repite mucho en los mismos valores (0.0, 0.33, 1.0...) |
| Qué tan rápido entrena al presionar "T" | Se tardaba un poco más | Es prácticamente instantáneo |
| Si vuelvo a entrenar con los mismos datos | Podía salir un modelo un poquito distinto cada vez | Sale exactamente el mismo árbol siempre |
| Qué tan "misterioso" es el modelo | No puedo saber por qué decide saltar, es una caja negra | Puedo ver las reglas exactas que usa para decidir (tipo "si la distancia es menor a X, salta") |

## 4. Ventajas y desventajas de cada uno
### Red Neuronal (MLP)
#### Ventajas
- El bot salta de forma más natural, no se "siente" ni se ve robótico.

#### Desventajas
- Necesita el paso extra del ``StandardScaler``, si no se aplica bien, el modelo puede fallar.
- No puedo ver "por qué" decide algo, es una caja negra.
- Tarda más en entrenar.

### Árbol de decision
#### Ventajas
- No necesita escalar los datos, es más simple de programar.
- Entrena muy rápido, casi al instante.
- Puedo ver las reglas que aprendió (es más fácil de entender/explicar).

#### Desventajas
- El bot se siente un poco más "robótico" al saltar, como si tuviera un botón de encendido/apagado en vez de una transición suave.
- Si no le pongo límites (`max_depth`, `min_samples_leaf`), se puede memorizar mis datos en vez de aprender un patrón general.

## 5. ¿Cual parece mejor para el juego?
En mi opinión, el **Árbol de decisión** es mejor para el juego, ya que:
- Los datos son pocos (se generan jugando).
- Solo se usan 2 variables (súper simple).
- Se entrena al instante, sin esperar tiempo a que se entrene.
- Más fácil de entender.