# Informe de Análisis: ExamenFiltrado

 **Alumno:** Fernando Amilcar Rodriguez Ramirez  
 **Caso:** #ExamenFiltrado — «examen de IA está filtrado en un PDF por WhatsApp»

## Misión 0 — Aclaración del Problema
### 1. ¿Qué es el origen del rumor?
Es el origen de la noticia. No importa si es la cuenta más famosa o la que tuvo más likes, sino quién fue el primero en publicar las palabras clave antes de que existieran copias. En nuestro caso, el inicio fue `@luna_mx` en el minuto 12.

### 2. ¿Qué es la dispersión?
Es cómo viaja el mensaje por la red. Se da de tres formas: los bots que hacen copia exacta (cascada), las personas reales que reaccionan indignadas (amplificación) y la gente que desvía el tema hablando de otras cosas (ruido). Se mide viendo a cuánta gente llega y qué tan rápido se mueve.

### 3. ¿Por qué un coseno alto no basta para saber quién empezó?
Porque el coseno solo mide qué tan idéntico es un texto a otro. Los bots sacan casi 1.0 porque hacen "copy-paste", mientras que el autor original usa sus propias palabras (sacando 0.88). Si solo miras el coseno, terminarás culpando a un bot que llegó tarde en lugar del humano que inventó el rumor.

### 4. ¿Qué peligro hay si solo miras «quién tiene más seguidores»?
Que te vas a confundir de enemigo. `@rectoria_iti` tiene 5,000 seguidores pero los usa para desmentir, mientras que los bots tienen apenas 6 seguidores pero generan decenas de interacciones falsas. Para entender la red real, hay que cruzar seguidores con la velocidad y antigüedad de la cuenta.

## Misión 1 — ¿Cuándo explotó la conversación?
### Tabla de resultados (`eda_ventanas_10min.csv`)

| Ventana (min) | Tweets | Cuentas Nuevas |
|:---:|:---:|:---:|
| **30 – 40** | **6** | **67%** |

### Interpretación
El tema estuvo apagado los primeros 30 minutos (solo 3 tweets reales). Sin embargo, **entre el minuto 30 y 40 explotó**: hubo 6 tweets de 6 usuarios diferentes y el 67% de ellos eran cuentas recién creadas. Esto es un claro patrón de actividad de bots. Todo indica que las cuentas `@info_rapida_01` a `@viral_edu_05` (creadas hace menos de 4 días) se activaron de golpe para amplificar el rumor que inició `@luna_mx`.

## Misión 2 — Coseno: ¿mismo rumor o copia?
Usamos la similitud coseno para comparar cada tweet con las 4 semillas temáticas del CSV (`similitud_tweets_tf.csv`). La idea es simple: mientras más cercano a 1.0 sea el coseno, más se parece el tweet a esa semilla. Usamos umbral ≥ 0.90 para marcar pares "casi clon", porque arriba de ese punto dos textos comparten prácticamente el mismo vocabulario con las mismas frecuencias.

### Código utilizado

```python
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("datasets/similitud_tweets_tf.csv")
feats = [c for c in df.columns if c not in ("documento", "tipo")]

semillas = df[df["tipo"] == "semilla"].set_index("documento")[feats]
tweets = df[df["tipo"] == "tweet"].set_index("documento")[feats]

sim_sem = pd.DataFrame(
    cosine_similarity(tweets.values, semillas.values),
    index=tweets.index, columns=semillas.index,
)
sim_tw = pd.DataFrame(
    cosine_similarity(tweets.values),
    index=tweets.index, columns=tweets.index,
)

print(sim_sem.round(3))

# Pares casi-clon (sim_tw >= 0.90)
for i in range(len(sim_tw)):
    for j in range(i+1, len(sim_tw)):
        val = sim_tw.iloc[i, j]
        if val >= 0.90:
            print(f"{sim_tw.index[i]} <-> {sim_tw.columns[j]}: {val:.3f}")
```

### Tabla: ¿De qué tema habla cada tweet?

| Tweet | Semilla más cercana | Coseno |
|-------|:-------------------:|:------:|
| `tw_origen_luna` | semilla_rumor_examen | **0.976** |
| `tw_bot_01` | semilla_rumor_examen | **0.967** |
| `tw_bot_02` | semilla_rumor_examen | **0.951** |
| `tw_bot_03` | semilla_rumor_examen | **0.925** |
| `tw_bot_05` | semilla_rumor_examen | **0.908** |
| `tw_bot_04` | semilla_rumor_examen | **0.891** |
| `tw_amplifica_diego` | semilla_rumor_examen | 0.814 |
| `tw_amplifica_vale` | semilla_rumor_examen | 0.644 |
| `tw_comedor_sofia` | semilla_rumor_comedor | 0.982 |
| `tw_comedor_eco` | semilla_rumor_comedor | 0.906 |
| `tw_ruido_becas` | semilla_ruido_becas | 0.993 |
| `tw_ruido_beca2` | semilla_ruido_becas | 0.869 |
| `tw_desmiente_omar` | semilla_desmentido | 0.982 |
| `tw_desmiente_rectoria` | semilla_desmentido | 0.913 |

### Pares casi-clon (coseno entre tweets ≥ 0.90)

| Par | Coseno |
|-----|:------:|
| bot_01 ↔ bot_02 | **0.984** |
| bot_02 ↔ bot_03 | 0.974 |
| bot_03 ↔ bot_04 | 0.973 |
| bot_02 ↔ bot_04 | 0.968 |
| bot_02 ↔ bot_05 | 0.963 |
| bot_04 ↔ bot_05 | 0.963 |
| bot_03 ↔ bot_05 | 0.962 |
| origen_luna ↔ bot_01 | 0.948 |
| bot_01 ↔ bot_03 | 0.944 |
| amplifica_diego ↔ amplifica_vale | 0.932 |
| bot_01 ↔ bot_05 | 0.930 |
| bot_01 ↔ bot_04 | 0.923 |
| origen_luna ↔ bot_02 | 0.901 |

### ¿Qué tweets hablan de otro tema?
- `tw_comedor_sofia` y `tw_comedor_eco` hablan del **rumor del comedor** (cos ≈ 0.98 y 0.91 con esa semilla). No tienen nada que ver con el examen.
- `tw_ruido_becas` y `tw_ruido_beca2` son **ruido sobre becas** (cos ≈ 0.99 y 0.87 con semilla_ruido_becas). Son irrelevantes para la investigación.

### Interpretación
Los 5 bots forman un bloque casi idéntico entre sí (cosenos entre 0.92 y 0.98), y todos están pegados a la semilla del examen. Eso confirma que están copiando el mismo texto con variaciones mínimas. Luna se parece mucho a la semilla (0.976) pero, como veremos en la Misión 3, publicó antes que todos: no es una copia, es el texto fuente. Diego y Vale se alejan de la semilla (0.81 y 0.64) porque reformulan el rumor con sus propias palabras.

## Misión 3 — Timeline + cascada: ¿quién primero y cómo se repartió?
El coseno nos dijo qué tan parecidos son los textos, pero no quién publicó primero. Para eso cruzamos `timeline_tweets.csv` (el minuto exacto de publicación) con `cascada_enlaces.csv` (quién copió de quién).

### Tabla de roles

| Rol | Usuario | Minuto | Evidencia |
|-----|---------|:------:|-----------|
| Origen del examen | `@luna_mx` | 12 | Primer tweet del rumor; cuenta de 1200 días (no es nueva) |
| Amplificador humano | `@diego_campus` | 28 | Cita a luna_mx agregando "injusto"; cuenta de 800 días |
| Amplificador humano | `@vale_ia` | 35 | Cita a diego; cuenta de 950 días, 1200 seguidores |
| Red de copias | `@info_rapida_01` | 31 | Copia texto de luna_mx; cuenta de 3 días |
| Red de copias | `@alertas_edu_02` | 32 | Copia texto de luna_mx; cuenta de 2 días |
| Red de copias | `@noticias_ya_03` | 33 | Copia a info_rapida_01; cuenta de 4 días |
| Red de copias | `@flash_campus_04` | 36 | Copia a alertas_edu_02; cuenta de 1 día |
| Red de copias | `@viral_edu_05` | 37 | Copia a noticias_ya_03; cuenta de 2 días |
| Desmentido | `@omar_verifica` | 45 | Desmiente directamente a luna_mx; 2100 seguidores |
| Refuerzo desmentido | `@rectoria_iti` | 52 | Refuerza el desmentido de omar; cuenta institucional |

### Cascada en ASCII

```text
@luna_mx (min 12) ──copia_texto──→ @info_rapida_01 (min 31)
                  ──copia_texto──→ @alertas_edu_02 (min 32)
                  ──cita_comenta─→ @diego_campus (min 28)
                  ──desmiente───→  @omar_verifica (min 45)

@info_rapida_01   ──copia_texto──→ @noticias_ya_03 (min 33)
@alertas_edu_02   ──copia_texto──→ @flash_campus_04 (min 36)
@noticias_ya_03   ──copia_texto──→ @viral_edu_05 (min 37)
@diego_campus     ──cita_comenta─→ @vale_ia (min 35)
@omar_verifica    ──refuerza────→  @rectoria_iti (min 52)
```

### ¿Por qué «más likes» o «más seguidores» no define al originador?
El bot `@flash_campus_04` acumula 60 likes y 20 respuestas a pesar de tener solo 6 seguidores, lo que sugiere interacción inflada artificialmente. Mientras tanto, `@luna_mx` (el verdadero origen) solo logró 1 like y 2 respuestas. Si eligiéramos al originador por engagement, caeríamos en la trampa de señalar a un bot que llegó 24 minutos después. Lo mismo con seguidores: `@rectoria_iti` tiene 5,000, pero su rol es desmentir, no originar. Para identificar al responsable hay que cruzar el timestamp (quién primero), la antigüedad de la cuenta (quién es real) y la cascada de enlaces (quién copia a quién).

## Misión 4 — k-NN: ¿bot o humano?
Ahora formalizamos la clasificación con **k-NN**. El algoritmo compara cada cuenta nueva contra un historial de 120 cuentas ya etiquetadas (`knn_cuentas_historial.csv`) y le asigna la etiqueta de sus vecinos más cercanos.

### Código utilizado

```python
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

train = pd.read_csv("datasets/knn_cuentas_historial.csv")
caso = pd.read_csv("datasets/knn_cuentas_caso.csv")
feats = [c for c in train.columns if c not in ("cuenta_id", "etiqueta")]

scaler = StandardScaler()
X = scaler.fit_transform(train[feats])
y = train["etiqueta"]
X_new = scaler.transform(caso[feats])

for k in (3, 5, 7):
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X, y, cv=5, scoring="f1_macro")
    print(k, scores.mean(), scores.std())

# Entrenar con k=5 y predecir
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X, y)
preds = knn.predict(X_new)
for cuenta, pred in zip(caso["cuenta_id"], preds):
    print(f"{cuenta}: {pred}")
```

### ¿Por qué escalar?
Usamos `StandardScaler` porque las features tienen rangos muy distintos: seguidores va de 0 a 5000, mientras que pct_retweet va de 0 a 1. Sin escalar, la distancia euclidiana estaría dominada por seguidores y el resto de features no contaría.

### Validación cruzada (f1_macro, 5-fold)

| k | f1_macro |
|:-:|:--------:|
| 3 | 1.000 ± 0.000 |
| 5 | 1.000 ± 0.000 |
| 7 | 1.000 ± 0.000 |

Los tres valores de k dan f1 perfecto. Elegimos **k = 5** para tener más estabilidad en la votación sin perder precisión.

### Predicciones (k = 5)

| Cuenta | Predicción | ¿Cuadra con M2/M3? |
|--------|:----------:|:-------------------:|
| `@info_rapida_01` | **bot** | Sí: clon del rumor (cos=0.967), cuenta de 3 días |
| `@alertas_edu_02` | **bot** | Sí: clon (cos=0.951), cuenta de 2 días |
| `@noticias_ya_03` | **bot** | Sí: clon (cos=0.925), cuenta de 4 días |
| `@flash_campus_04` | **bot** | Sí: clon (cos=0.891), cuenta de 1 día |
| `@viral_edu_05` | **bot** | Sí: clon (cos=0.908), cuenta de 2 días |
| `@luna_mx` | **humano** | Sí: origen real (min 12), cuenta de 1200 días |
| `@diego_campus` | **humano** | Sí: amplificador con sus palabras (cos=0.814) |
| `@vale_ia` | **humano** | Sí: amplificador (cos=0.644), cuenta antigua |
| `@omar_verifica` | **humano** | Sí: desmentidor (cos=0.982 con semilla_desmentido) |
| `@sofia_comedor` | **humano** | Sí: otro rumor, no involucrada |
| `@rectoria_iti` | **humano** | Sí: cuenta institucional que desmiente |

### ¿Qué haría si coseno y k-NN se contradijeran?
Si una cuenta tuviera coseno alto con el rumor (pareciera clon) pero k-NN la clasificara como humano, revisaría dos cosas: primero, la **antigüedad** de la cuenta (los bots suelen tener menos de 10 días); segundo, la **diversidad léxica** (un humano que de casualidad usó palabras parecidas tendrá diversidad alta, un bot tendrá diversidad menor a 0.15). Si ambos indicadores apuntan a humano, confiaría en k-NN y asumiría que el coseno alto fue coincidencia de vocabulario. Si la diversidad es baja y la cuenta es nueva, el coseno tiene razón y revisaría los hiperparámetros de k-NN.

## Misión 5 — Árbol: ¿amplifica o contrarresta?
Entrenamos un `DecisionTreeClassifier(max_depth=4)` sobre 160 casos históricos para predecir qué hará cada actor frente al rumor.

### Código utilizado

```python
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text

arbol_hist = pd.read_csv("datasets/arbol_amplificacion_historial.csv")
arbol_caso = pd.read_csv("datasets/arbol_escenarios_caso.csv")
arbol_feats = [c for c in arbol_hist.columns if c not in ("caso_id", "accion")]

X_arbol = arbol_hist[arbol_feats].values
y_arbol = arbol_hist["accion"].values

tree = DecisionTreeClassifier(max_depth=4, random_state=42)
tree.fit(X_arbol, y_arbol)

print(export_text(tree, feature_names=arbol_feats))

X_caso = arbol_caso[arbol_feats].values
preds_arbol = tree.predict(X_caso)
for caso_id, pred in zip(arbol_caso["caso_id"], preds_arbol):
    print(f"{caso_id}: {pred}")
```

### Reglas del árbol

```text
¿Ya desmintió antes?
├── SÍ → contrarresta
└── NO
    ├── ¿Similitud alta con el rumor (sim > 0.5)?
    │   ├── NO → ignora
    │   └── SÍ
    │       ├── ¿Es bot según k-NN?
    │       │   ├── SÍ → amplifica_en_masa
    │       │   └── NO
    │       │       ├── ¿Tiene muchos seguidores?
    │       │       │   ├── SÍ → amplifica_influencer
    │       │       │   └── NO → amplifica_leve
```

### Predicción por escenario

| Escenario | Acción predicha |
|-----------|:---------------:|
| **red_bots** (sim=1, bot=1, seg=0) | **amplifica_en_masa** |
| **diego** (sim=1, bot=0, seg=1) | **amplifica_influencer** |
| **vale** (sim=1, bot=0, seg=1) | **amplifica_influencer** |
| **omar** (sim=0, bot=0, desmintió=1) | **contrarresta** |
| **sofia_comedor** (sim=0, bot=0, desmintió=0) | **ignora** |

### Acción prioritaria para el campus
La primera prioridad es **mutear la red de bots**. El árbol muestra que cuando sim=1 y es_bot=1, el resultado es siempre "amplifica_en_masa", que es la acción más dañina porque genera volumen artificial masivo. Eliminar estos 5 nodos corta de raíz la cascada principal. Como segunda línea, conviene **impulsar el desmentido** de Omar y Rectoría, porque el árbol muestra que las cuentas con historial de desmentido siempre contrarrestan. Y como tercer paso, hablar con Diego y Vale (los amplificadores influencer): el árbol predice que seguirán amplificando mientras no exista un desmentido visible; si ven el comunicado oficial, es probable que cambien de postura.

## Misión 6 — Regresión: ¿qué mueve el alcance?
Ajustamos una regresión lineal sobre `regresion_alcance_rumor.csv` para cuantificar el peso de cada variable en el alcance del rumor.

### Código utilizado

```python
import pandas as pd
from sklearn.linear_model import LinearRegression

reg_df = pd.read_csv("datasets/regresion_alcance_rumor.csv")
X_reg = reg_df[["minutos_desde_origen", "bots_activos", "desmentidos_activos"]].values
y_reg = reg_df["alcance_cuentas"].values

lr = LinearRegression()
lr.fit(X_reg, y_reg)

print(f"B0 (intercepto) = {lr.intercept_:.2f}")
for name, coef in zip(["B_minutos", "B_bots", "B_desmentidos"], lr.coef_):
    print(f"{name} = {coef:.2f}")
print(f"R2 = {lr.score(X_reg, y_reg):.4f}")

# Escenarios
for name, mins, bots, desm in [("A",60,10,0),("B",60,10,2),("C",60,0,2)]:
    pred = lr.predict([[mins, bots, desm]])[0]
    print(f"{name}: min={mins}, bots={bots}, desm={desm} -> alcance={pred:.1f}")
```

### Coeficientes del modelo (R² = 0.991)

| Coeficiente | Valor | Significado |
|-------------|:-----:|-------------|
| β₀ | **19.86** | Alcance base: aún sin bots ni tiempo, unas 20 cuentas ya ven el rumor |
| β_minutos | **+1.82** | Cada minuto que pasa, el rumor llega a casi 2 cuentas más |
| β_bots | **+14.36** | Cada bot activo suma ~14 cuentas de alcance |
| β_desmentidos | **−17.37** | Cada desmentido activo resta ~17 cuentas de alcance |

### Escenarios a 60 minutos

| Escenario | Minutos | Bots | Desmentidos | Alcance predicho |
|:---------:|:-------:|:----:|:-----------:|:----------------:|
| A (sin intervención) | 60 | 10 | 0 | **272.8** |
| B (solo desmentir) | 60 | 10 | 2 | **238.1** |
| C (bloquear bots + desmentir) | 60 | 0 | 2 | **94.5** |

### ¿Qué escenario conviene más?
El **escenario C** es el que más conviene al campus. Mientras que solo desmentir (escenario B) apenas baja el alcance 35 cuentas, eliminar los bots y desmentir al mismo tiempo (escenario C) lo reduce de 273 a 95 cuentas, una caída del 65%. Esto tiene sentido: β_bots (+14.36) multiplicado por 10 bots pesa muchísimo más que lo que pueden compensar 2 desmentidos. La estrategia óptima es cortar la fuente del ruido artificial primero.

## Misión 7 — Informe final de dispersión

### 1. ¿Quién originó el rumor del examen?
El rumor comenzó con **`@luna_mx`** en el minuto 12. Es una cuenta humana de más de 3 años de antigüedad que publicó el texto semilla con sus propias palabras: «examen IA con filtro en pdf por whatsapp». Su coseno con la semilla del rumor es 0.976, y k-NN (k=5) la clasifica como humana.

### 2. ¿Cómo se dispersó (copias / amplificadores)?
A los 28 minutos, **`@diego_campus`** citó el tweet agregando indignación propia (cos=0.814 con la semilla). Poco después, **`@vale_ia`** se sumó amplificando con sus palabras. Ambos son humanos con cuentas antiguas y muchos seguidores; el árbol de decisión predice que actuarán como "amplificadores influencer". En paralelo, la verdadera explosión llegó entre el minuto 31 y 37, cuando 5 cuentas falsas se activaron en ráfaga copiando el texto casi idéntico (cosenos entre sí de 0.92 a 0.98).

### 3. ¿Qué cuentas son bots según k-NN?
k-NN (k=5, f1=1.0) clasifica como bots a: `@info_rapida_01`, `@alertas_edu_02`, `@noticias_ya_03`, `@flash_campus_04` y `@viral_edu_05`. Sus métricas son contundentes: menos de 5 días de antigüedad, entre 35 y 60 tweets por hora, más del 88% de su actividad es retweet, y diversidad léxica menor a 0.15.

### 4. ¿Qué intervención priorizas (usa árbol + regresión)?
Según la regresión lineal (R²=0.991), cada bot activo agrega 14.36 cuentas de alcance, mientras que cada desmentido resta 17.37. Pero como hay 10 bots potenciales contra solo 2 desmentidores, **la intervención prioritaria es bloquear a los bots**: el escenario C (bots eliminados + 2 desmentidos) baja el alcance de 273 a 95 cuentas a los 60 minutos. El árbol de decisión respalda esto: sim=1 + bot=1 siempre produce "amplifica_en_masa".

### 5. Una limitación del análisis
Nuestro análisis asume que la cascada de enlaces es completa, pero en la realidad podrían existir interacciones fuera de la plataforma (WhatsApp, grupos privados) que no aparecen en los CSV. Además, la regresión es lineal y el alcance real podría tener efectos no lineales cuando se combinan muchos bots con amplificadores humanos de alta audiencia.