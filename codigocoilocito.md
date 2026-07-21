# Informe de Análisis: Código Coilocito — Caso Forense

**Alumno:** Fernando Amilcar Rodriguez Ramirez  
**Caso:** Desaparición del Dr. Arispe y robo del algoritmo de detección de coilocitos

## Tu rol
Como especialista en visión por computadora del laboratorio Arispe, seguridad te marcó como el principal sospechoso porque tenías acceso *root* y firmaste el último *commit* antes del apagón. Tu objetivo es limpiar tu nombre demostrando, con modelos y evidencia, quién robó realmente el algoritmo.

Si no encuentras al culpable, el código que podría democratizar y abaratar diagnósticos médicos terminará cerrado bajo una patente corporativa.

### Los Sospechosos

| Sospechoso | Motivo aparente | Huella técnica típica |
|------------|-----------------|-----------------------|
| **Dr. Valeriano** (rival) | Odia SIFT/SURF; quiere proteger su financiamiento | GPU, CNN, correos de queja |
| **Elena «La Full-Stack»** | Trabaja para un conglomerado que busca cerrar el código | Django, PostgreSQL, VPN, Docker |
| **Hacker interno anónimo** | Venganza o exalumno rencoroso | Emacs, SSH, borrados torpes |

---

## Acto 1 — Matching con similitud coseno

Para saber qué pista encaja mejor con qué sospechoso, calculamos la **similitud coseno** entre los vectores de términos de cada pista y cada perfil (dataset `similitud_tf_documentos.csv`).

### Código utilizado
```python
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("datasets/similitud_tf_documentos.csv")

# 1. Definimos las features numéricas
feats = [c for c in df.columns if c not in ("documento", "tipo")]

# 2. Filtramos y separamos perfiles y pistas
perfiles = df[df["tipo"] == "perfil"].set_index("documento")[feats]
pistas = df[df["tipo"] == "pista"].set_index("documento")[feats]

# 3. Calculamos la matriz de similitud
sim = pd.DataFrame(
    cosine_similarity(pistas.values, perfiles.values),
    index=pistas.index, columns=perfiles.index
)

print(sim.round(3))
print("\nMejor match por pista:")

# 4. Buscamos el perfil con mayor similitud para cada pista
for p in sim.index:
    mejor_perfil = sim.loc[p].idxmax()
    valor = sim.loc[p].max()
    print(f"{p}: {mejor_perfil} (cos={valor:.3f})")
```

### Resultados del Acto 1

| Pista | Perfil más similar | Coseno (aprox) |
| :--- | :--- | :--- |
| **A (bitácora red)** | Elena | **0.789** |
| **B (correo interno)** | Valeriano | **0.925** |
| **C (fragmento Emacs)** | Hacker interno | **0.935** |
| **D (commit GitLab)** | Elena | **0.970** |

**Hipótesis preliminar:**
Las pistas apuntan fuertemente hacia **Elena**. La Pista D (commit en GitLab) coincide de manera casi perfecta (0.970) con su perfil técnico, ya que ambos comparten términos clave como Docker, PostgreSQL y Django. Además, la Pista A (bitácora de red) también la señala por el uso de VPN. Aunque la Pista C apunta a un hacker interno (0.935), es probable que sea evidencia falsa plantada para desviar la atención, ya que en el laboratorio encontramos un directorio `.emacs.d` vacío en el usuario de Elena.

---

## Acto 2 — Tipo de ataque con k-NN

Ahora necesitamos saber cómo fue el sabotaje. Usaremos el algoritmo **k-NN** para comparar las métricas del servidor durante el robo contra 120 ataques históricos ya clasificados.

### Código utilizado
```python
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

train = pd.read_csv("datasets/knn_historial_ataques.csv")
caso = pd.read_csv("datasets/knn_caso_arispe.csv")

# 1. Seleccionamos las variables (features)
feats = [c for c in train.columns if c not in ("caso_id", "etiqueta_ataque")]

# 2. Escalamos los datos
scaler = StandardScaler()
X = scaler.fit_transform(train[feats])
y = train["etiqueta_ataque"]
X_new = scaler.transform(caso[feats])

# 3. Probamos distintos valores de k
for k in [3, 5, 7]:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X, y, cv=5, scoring="f1_macro")
    print(f"k={k} | f1_macro: {scores.mean():.3f} (±{scores.std():.3f})")

# 4. Entrenamos el modelo final y predecimos
modelo = KNeighborsClassifier(n_neighbors=5)
modelo.fit(X, y)
pred = modelo.predict(X_new)[0]

print(f"\nPredicción caso Arispe: {pred}")
```

### Resultados del Acto 2

- **k elegido:** 5
- **F1 macro (CV):** 0.992
- **Predicción caso Arispe:** `robo_sigiloso_cuello_blanco`

**¿Por qué escalar?**
Usamos `StandardScaler` porque las variables tienen magnitudes completamente distintas. Por ejemplo, los megabytes copiados pueden ser miles, pero el uso de VPN es 0 o 1. Si no escalamos, la distancia euclidiana de k-NN le daría toda la importancia a los megabytes ignorando el resto. (Ojo: si quitamos el scaler, la predicción del caso resulta igual porque las clases están muy separadas, pero validarlo con escala garantiza un modelo robusto).

**Relación con el Acto 1:**
La predicción confirma el estilo de Elena. El "robo sigiloso de cuello blanco" se caracteriza por conexiones limpias de madrugada, uso de VPN y copias de datos sin fuerza bruta. Esto encaja perfectamente con su perfil de contratista que entra al sistema, extrae los datos y se va sin dejar rastro aparente.


## Acto 3 — Fuga con árbol de decisión

Sabiendo que Elena es la responsable, necesitamos predecir su ruta de escape. Para esto, entrenamos un árbol de decisión con datos históricos de fugas.

### Código utilizado
```python
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text

hist = pd.read_csv("datasets/arbol_fugas_historial.csv")
esc = pd.read_csv("datasets/arbol_escenario_culpable.csv")
esc_val = pd.read_csv("datasets/arbol_escenario_valeriano.csv")

# 1. Definimos las features
feats = [c for c in hist.columns if c not in ("fuga_id", "ruta_elegida")]

# 2. Entrenamos el árbol
clf = DecisionTreeClassifier(max_depth=4, random_state=42)
clf.fit(hist[feats].values, hist["ruta_elegida"].values)

print(export_text(clf, feature_names=feats))

# 3. Predecimos los escenarios
ruta_elena = clf.predict(esc[feats].values)[0]
ruta_valeriano = clf.predict(esc_val[feats].values)[0]

print(f"Ruta Elena: {ruta_elena}")
print(f"Ruta Valeriano: {ruta_valeriano}")
```

### Resultados del Acto 3

1. **Culpable acusada:** Elena «La Full-Stack»
2. **Ruta predicha:** `vuelo_internacional`
3. **Contrafactual Valeriano → ruta:** `escondite_instituto`
4. **Orden de interceptación:** Emitir alerta inmediata a migración en aeropuertos internacionales. Elena cuenta con fondos corporativos y no tiene alertas activas previas, por lo que su ruta prioritaria es salir del país en vuelo comercial. Se solicita retenerla antes del abordaje.

---

## Acto Extra — Regresión lineal: SIFT/SURF vs CNN

¿Por qué robaron el algoritmo? Para entender su valor comercial, comparamos cómo escala el tiempo de inferencia entre SIFT/SURF (el algoritmo del Dr. Arispe) y una red neuronal CNN profunda, proyectando a 10,000 células.

### Código utilizado
```python
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("datasets/regresion_benchmark_coilocitos.csv")

for metodo, g in df.groupby("metodo"):
    X = g[["n_celulas"]].values
    y = g["tiempo_inferencia_s"].values
    
    lr = LinearRegression()
    lr.fit(X, y)
    pred_10k = lr.predict([[10000]])[0]
    
    print(f"{metodo} -> B0: {lr.intercept_:.3f} | B1: {lr.coef_[0]:.6f} | t@10k: {pred_10k:.1f}s")
```

### Resultados Extra

| Método | β₀ (Intersección) | β₁ (Pendiente) | t@10k (s) |
| :--- | :--- | :--- | :--- |
| **SIFT/SURF clásico** | 1.767 | 0.011993 | 121.7 |
| **CNN profunda** | 11.977 | 0.085058 | 862.6 |

**Interpretación:**
El algoritmo SIFT/SURF del Dr. Arispe es **siete veces más rápido** por célula (0.011 s frente a los 0.085 s de la CNN). Al procesar 10,000 células, el código robado tarda apenas 2 minutos, mientras que la CNN requiere más de 14. *(Nota: asumiendo que la memoria RAM no sea un cuello de botella al extrapolar el modelo lineal)*.
Este rendimiento le da un móvil corporativo enorme a Elena: quien controle este algoritmo puede vender equipos de diagnóstico en tiempo real muy económicos, destruyendo el mercado de equipos costosos con GPU.

---

## Veredicto Final

Con base en la evidencia matemática y los modelos predictivos, el caso queda resuelto de la siguiente forma:

**1. ¿A quién acusas y por qué?**
Acuso formalmente a **Elena «La Full-Stack»**. Todas las piezas encajan sin contradicciones. La **similitud coseno** demostró que su vocabulario coincide perfectamente (0.970) con el commit de GitLab borrado, y el algoritmo **k-NN** confirmó que el modus operandi del sabotaje corresponde exactamente a su perfil técnico: un robo limpio, usando VPN, propio de alguien con accesos corporativos. Finalmente, la regresión lineal revela el inmenso valor financiero del algoritmo que robó para su corporación.

**2. ¿Qué pista o resultado podría estar engañándote?**
La **Pista C** (fragmento de Emacs) sugería fuertemente a un hacker interno (coseno 0.935). Sin embargo, al cruzar esto con la evidencia del laboratorio (donde encontramos un directorio `.emacs.d` vacío en el usuario de Elena), se vuelve obvio que intentó plantar pistas falsas para incriminar a un estudiante o exalumno.

**3. ¿Qué harías si tu k-NN y tu coseno no coincidieran?**
Si ambos modelos me dieran sospechosos diferentes, no acusaría a ciegas. Revisaría qué variables están pesando más en el k-NN (quizás la hora o los megabytes) y evaluaría si el coseno alto proviene de coincidencia en palabras clave muy específicas o es general. Le daría mayor peso al k-NN validado con un alto `f1_macro` por medir el comportamiento de ataque, pero siempre usaría pruebas forenses físicas (como las bitácoras o el USB) para desempatar y confirmar la historia.