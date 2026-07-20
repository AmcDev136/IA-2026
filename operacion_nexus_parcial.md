
# Table of Contents

1.  [Operación Nexus — Acertijos de Inteligencia Artificial](#orgeb47126)
    1.  [De qué va esto (léelo antes de empezar)](#orgf616cc0)
    2.  [Reglas del juego (acertijos)](#org21a355d)
    3.  [Qué NO es este examen](#org943b306)
    4.  [Qué SÍ es](#org9d5e171)
2.  [BLOQUE A — Datos (la IA empieza por la pregunta, no por el modelo)](#org57d56b2)
    1.  [N1 — Sobres sin etiqueta (~20 min)](#orge2c6884)
    2.  [N2 — La columna impostora (~15 min)](#org8eaa852)
    3.  [N3 — El informe que miente (~20 min)](#orgf170a83)
3.  [BLOQUE B — Modelos (IA clásica: más allá del chat)](#orgdca9149)
    1.  [N4 — Cinco cajas negras (~15 min)](#orge020324)
    2.  [N5 — El perceptrón no es omnipotente (~15 min)](#org1a6b6a4)
    3.  [N6 — Gemelos P y Q (~15 min)](#org1dd4057)
    4.  [N7 — Imagen vs tabla (~10 min)](#org5a7442b)
4.  [Autochequeo antes de entregar](#org8c54205)
5.  [Plantilla `informe_nexus.md`](#org9fbbd99)



<a id="orgeb47126"></a>

# Operación Nexus — Acertijos de Inteligencia Artificial


<a id="orgf616cc0"></a>

## De qué va esto (léelo antes de empezar)

La IA **no** es solo ChatGPT, copilotos de código ni “pedirle cosas a un bot”.
También es: **mirar datos**, **formular preguntas**, **elegir cómo representar un problema**,
**detectar trampas** (leakage, métricas engañosas) y **decidir qué tipo de modelo tiene sentido**
— regresión lineal, logística, perceptrón, MLP, CNN, etc.

Este parcial son **acertijos**: fragmentos de información incompleta o contradictoria.
Ustedes deben **deducir** la respuesta encadenando pistas. No es memorizar definiciones;
es **pensar** como analistas de IA.


<a id="org21a355d"></a>

## Reglas del juego (acertijos)

1.  **Individual.** Sin copiar respuestas literales de un compañero o de un LLM.
2.  **Conclusión + justificación.** Si aciertan pero no explican el razonamiento, la pregunta vale 0.
3.  **Una solución coherente con todas las pistas.** Si una pieza no encaja con el resto, revisen.
4.  **No entrenar modelos.** Calculadora y cuentas a mano sí. Python solo para aritmética si quieren.
5.  **No asuman lo que no está escrito.** Si falta un dato, digan qué hipótesis harían y por qué.
6.  **La IA no es magia:** si algo suena “demasiado perfecto” (accuracy 0.86, correlación 0.95 en 8 filas),
    sospechen y demuestren con números o lógica.
7.  Entregable: `informe_nexus.md` (o este Org rellenado).
8.  **Tiempo:** 120 minutos.


<a id="org943b306"></a>

## Qué NO es este examen

-   No es escribir prompts a un chatbot.
-   No es recitar “la IA es el futuro”.
-   No es implementar una red desde cero en GPU.


<a id="org9d5e171"></a>

## Qué SÍ es

-   Elegir el **dataset** correcto para una pregunta.
-   Detectar columnas que **engañan** (leakage, ruido).
-   Leer una matriz de confusión y contradecir un informe falso.
-   Emparejar un **problema** con un **modelo** visto en clase (y decir por qué no otro).
-   Entender **límites** (perceptrón lineal, overfitting, CNN solo cuando hay imágenes).

**Distribución sugerida**

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-right" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Bloque</th>
<th scope="col" class="org-left">Misiones</th>
<th scope="col" class="org-right">Min aprox.</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-left">A — Datos y EDA</td>
<td class="org-left">N1 N2 N3</td>
<td class="org-right">55</td>
</tr>

<tr>
<td class="org-left">B — Modelos clásicos de ML</td>
<td class="org-left">N4 N5 N6 N7</td>
<td class="org-right">55</td>
</tr>

<tr>
<td class="org-left">Repaso</td>
<td class="org-left">autochequeo</td>
<td class="org-right">10</td>
</tr>
</tbody>
</table>

---


<a id="org57d56b2"></a>

# BLOQUE A — Datos (la IA empieza por la pregunta, no por el modelo)


<a id="orge2c6884"></a>

## N1 — Sobres sin etiqueta (~20 min)


### Contexto

Tres equipos pidieron “un modelo de IA” pero nadie acordó **qué preguntar**.
Hay tres sobres (CSV) y tres órdenes. Emparejen orden ↔ sobre.


### Órdenes

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Código</th>
<th scope="col" class="org-left">Orden</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-left">O1</td>
<td class="org-left">¿Este alumno <b>abandonará</b> el curso?</td>
</tr>

<tr>
<td class="org-left">O2</td>
<td class="org-left">¿*Cuántos puntos* (0–100) sacará en el final?</td>
</tr>

<tr>
<td class="org-left">O3</td>
<td class="org-left">Riesgo <b>verde / amarillo / rojo</b></td>
</tr>
</tbody>
</table>


### Sobres (muestra)

**Sobre A**

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-right">id</th>
<th scope="col" class="org-right">dias<sub>sin</sub><sub>login</sub></th>
<th scope="col" class="org-right">avance<sub>pct</sub></th>
<th scope="col" class="org-right">beca</th>
<th scope="col" class="org-right">marca</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-right">11</td>
<td class="org-right">2</td>
<td class="org-right">78</td>
<td class="org-right">1</td>
<td class="org-right">0</td>
</tr>

<tr>
<td class="org-right">12</td>
<td class="org-right">19</td>
<td class="org-right">12</td>
<td class="org-right">0</td>
<td class="org-right">1</td>
</tr>

<tr>
<td class="org-right">13</td>
<td class="org-right">4</td>
<td class="org-right">61</td>
<td class="org-right">1</td>
<td class="org-right">0</td>
</tr>
</tbody>
</table>

**Sobre B**

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-right">id</th>
<th scope="col" class="org-right">asistencia</th>
<th scope="col" class="org-right">tareas</th>
<th scope="col" class="org-right">parcial1</th>
<th scope="col" class="org-left">etiqueta</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-right">21</td>
<td class="org-right">92</td>
<td class="org-right">8</td>
<td class="org-right">8.5</td>
<td class="org-left">verde</td>
</tr>

<tr>
<td class="org-right">22</td>
<td class="org-right">71</td>
<td class="org-right">5</td>
<td class="org-right">6.8</td>
<td class="org-left">amarillo</td>
</tr>

<tr>
<td class="org-right">23</td>
<td class="org-right">48</td>
<td class="org-right">2</td>
<td class="org-right">4.9</td>
<td class="org-left">rojo</td>
</tr>
</tbody>
</table>

**Sobre C**

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-right">id</th>
<th scope="col" class="org-right">promedio<sub>tareas</sub></th>
<th scope="col" class="org-right">examen1</th>
<th scope="col" class="org-right">examen2</th>
<th scope="col" class="org-right">score</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-right">31</td>
<td class="org-right">88</td>
<td class="org-right">85</td>
<td class="org-right">90</td>
<td class="org-right">89</td>
</tr>

<tr>
<td class="org-right">32</td>
<td class="org-right">60</td>
<td class="org-right">55</td>
<td class="org-right">62</td>
<td class="org-right">61</td>
</tr>

<tr>
<td class="org-right">33</td>
<td class="org-right">75</td>
<td class="org-right">70</td>
<td class="org-right">78</td>
<td class="org-right">76</td>
</tr>
</tbody>
</table>


### Pistas

-   Una orden pide un **número continuo**; otra **sí/no** (0/1); otra **tres niveles**.
-   `marca` solo vale 0 o 1 en todo el archivo.
-   `etiqueta` no es numérica.


### Tareas

1.  Empareja O1/O2/O3 → A/B/C.
2.  Por cada par: columna Y + ¿propones **clasificar** o **predecir**? Justifica mirando Y.
3.  **Trampa:** usar Sobre C para O3 convirtiendo `score` en semáforo con umbrales. ¿Válido? ¿Qué se pierde?

---


<a id="org8eaa852"></a>

## N2 — La columna impostora (~15 min)

Objetivo: predecir `aprueba` (0/1).

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-right">id</th>
<th scope="col" class="org-right">asistencia</th>
<th scope="col" class="org-right">promedio</th>
<th scope="col" class="org-right">horas<sub>plataforma</sub></th>
<th scope="col" class="org-right">nota<sub>final</sub></th>
<th scope="col" class="org-right">mes<sub>nacimiento</sub></th>
<th scope="col" class="org-right">aprueba</th>
<th scope="col" class="org-right">fecha<sub>acta</sub></th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-right">90</td>
<td class="org-right">8.2</td>
<td class="org-right">12</td>
<td class="org-right">8.5</td>
<td class="org-right">3</td>
<td class="org-right">1</td>
<td class="org-right">2026-06-10</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">55</td>
<td class="org-right">5.0</td>
<td class="org-right">2</td>
<td class="org-right">4.8</td>
<td class="org-right">11</td>
<td class="org-right">0</td>
<td class="org-right">2026-06-10</td>
</tr>

<tr>
<td class="org-right">3</td>
<td class="org-right">80</td>
<td class="org-right">7.1</td>
<td class="org-right">9</td>
<td class="org-right">7.0</td>
<td class="org-right">7</td>
<td class="org-right">1</td>
<td class="org-right">2026-06-11</td>
</tr>

<tr>
<td class="org-right">4</td>
<td class="org-right">40</td>
<td class="org-right">4.2</td>
<td class="org-right">1</td>
<td class="org-right">3.9</td>
<td class="org-right">1</td>
<td class="org-right">0</td>
<td class="org-right">2026-06-11</td>
</tr>

<tr>
<td class="org-right">5</td>
<td class="org-right">95</td>
<td class="org-right">9.0</td>
<td class="org-right">15</td>
<td class="org-right">9.2</td>
<td class="org-right">5</td>
<td class="org-right">1</td>
<td class="org-right">2026-06-12</td>
</tr>

<tr>
<td class="org-right">6</td>
<td class="org-right">60</td>
<td class="org-right">5.5</td>
<td class="org-right">3</td>
<td class="org-right">5.4</td>
<td class="org-right">9</td>
<td class="org-right">0</td>
<td class="org-right">2026-06-12</td>
</tr>

<tr>
<td class="org-right">7</td>
<td class="org-right">70</td>
<td class="org-right">6.0</td>
<td class="org-right">4</td>
<td class="org-right">6.1</td>
<td class="org-right">2</td>
<td class="org-right">1</td>
<td class="org-right">2026-06-13</td>
</tr>

<tr>
<td class="org-right">8</td>
<td class="org-right">88</td>
<td class="org-right">7.8</td>
<td class="org-right">10</td>
<td class="org-right">7.9</td>
<td class="org-right">12</td>
<td class="org-right">1</td>
<td class="org-right">2026-06-13</td>
</tr>
</tbody>
</table>

Pistas (**una es falsa**):

-   α: Con `nota_final` casi no hace falta modelo para `aprueba`.
-   β: `mes_nacimiento` correlaciona 0.95 con `aprueba` en estas 8 filas.
-   γ: `fecha_acta` se llena **después** de cerrar el curso.
-   δ: `asistencia` y `promedio` se conocen **antes** del acta.


### Tareas

1.  ¿Cuál pista es falsa? ¿Por qué?
2.  Clasifica cada columna: **X usable** / **leakage** / **ruido** / **Y**.
3.  Lista el **dataset mínimo limpio** para un modelo honesto.

---


<a id="orgf170a83"></a>

## N3 — El informe que miente (~20 min)

Un consultor vendió “IA de abandono” con este resumen:

> N=500. Clase positiva (abandona=1) = 70 (14%).
> Accuracy test = 0.86 → modelo excelente, desplegar ya.

Matriz real del mismo test:

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Pred \ Real</th>
<th scope="col" class="org-right">0</th>
<th scope="col" class="org-right">1</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-left">predice 0</td>
<td class="org-right">420</td>
<td class="org-right">65</td>
</tr>

<tr>
<td class="org-left">predice 1</td>
<td class="org-right">10</td>
<td class="org-right">5</td>
</tr>
</tbody>
</table>


### Tareas

1.  Verifica accuracy con la matriz (muestra la cuenta).
2.  ¿Qué hace **casi siempre** el modelo?
3.  Recall y precisión de clase 1 (aprox.).
4.  Contra-informe ≤5 líneas: métrica que priorizarías si **no detectar** un abandono es muy costoso.
5.  **Acertijo:** accuracy de un modelo tonto que **siempre** predice 0. ¿Qué relación tiene con 0.86?

---


<a id="orgdca9149"></a>

# BLOQUE B — Modelos (IA clásica: más allá del chat)


<a id="orge020324"></a>

## N4 — Cinco cajas negras (~15 min)

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Caja</th>
<th scope="col" class="org-left">Modelo</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-left">C1</td>
<td class="org-left">Regresión lineal</td>
</tr>

<tr>
<td class="org-left">C2</td>
<td class="org-left">Regresión logística</td>
</tr>

<tr>
<td class="org-left">C3</td>
<td class="org-left">Perceptrón simple</td>
</tr>

<tr>
<td class="org-left">C4</td>
<td class="org-left">MLP (red multicapa)</td>
</tr>

<tr>
<td class="org-left">C5</td>
<td class="org-left">CNN</td>
</tr>
</tbody>
</table>

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Caso</th>
<th scope="col" class="org-left">Situación</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-left">K1</td>
<td class="org-left">Precio de casa (número) con metros y habitaciones</td>
</tr>

<tr>
<td class="org-left">K2</td>
<td class="org-left">Spam sí/no con datos <b>tabulares</b></td>
</tr>

<tr>
<td class="org-left">K3</td>
<td class="org-left">Dígitos manuscritos en <b>imágenes</b> 28×28</td>
</tr>

<tr>
<td class="org-left">K4</td>
<td class="org-left">Dos clases <b>linealmente separables</b> en 2D (el más simple posible)</td>
</tr>

<tr>
<td class="org-left">K5</td>
<td class="org-left">Tres clases con relaciones <b>no lineales</b> en datos tabulares</td>
</tr>
</tbody>
</table>


### Tareas

1.  Empareja K1..K5 → C1..C5 (cada caja una sola vez) + una frase de por qué.
2.  **Trampa:** regresión lineal cruda + umbral 0.5 para spam. ¿Qué caja encaja mejor y por qué?

---


<a id="org1a6b6a4"></a>

## N5 — El perceptrón no es omnipotente (~15 min)

Alguien dice: “Con más epochs el perceptrón simple aprende **cualquier** cosa.”

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">ID</th>
<th scope="col" class="org-left">Situación</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-left">D1</td>
<td class="org-left">Dos clases separables con una recta</td>
</tr>

<tr>
<td class="org-left">D2</td>
<td class="org-left">XOR (clases en diagonal)</td>
</tr>

<tr>
<td class="org-left">D3</td>
<td class="org-left">Clase A dentro de un anillo de clase B</td>
</tr>

<tr>
<td class="org-left">D4</td>
<td class="org-left">Spam tabular casi separable con un plano</td>
</tr>
</tbody>
</table>


### Tareas

1.  ¿En cuáles puede el perceptrón simple? ¿En cuáles no?
2.  Corrige la afirmación en ≤2 frases.
3.  ¿Por qué un MLP con activación no lineal ayuda en D2 o D3? (idea, no fórmula larga)
4.  Cuenta: `w=(1,1)`, `b`-1.5=, `x=(1,0)`. `w·x+b`? Clase 1 si ≥0, si no 0.

---


<a id="org1dd4057"></a>

## N6 — Gemelos P y Q (~15 min)

    Modelo P:  ŷ = w·x + b
    
    Modelo Q:  p = 1 / (1 + e^{-(w·x+b)})
               clase = 1 si p ≥ 0.5

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Código</th>
<th scope="col" class="org-left">Pregunta</th>
<th scope="col" class="org-left">Salida deseada</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-left">E1</td>
<td class="org-left">¿Cuántos puntos? (0–100)</td>
<td class="org-left">Número</td>
</tr>

<tr>
<td class="org-left">E2</td>
<td class="org-left">¿Abandona? (sí/no)</td>
<td class="org-left">Clase / probabilidad</td>
</tr>

<tr>
<td class="org-left">E3</td>
<td class="org-left">¿Probabilidad de aprobar?</td>
<td class="org-left">Entre 0 y 1</td>
</tr>
</tbody>
</table>


### Tareas

1.  ¿Cuál es lineal y cuál logística?
2.  Empareja E1/E2/E3 → P o Q.
3.  Si P en E2 da ŷ=2.7 o ŷ=−1.3, ¿qué problema hay?
4.  Si `w·x+b` es muy positivo, ¿p→0 o p→1? Razona con la fórmula.

---


<a id="org5a7442b"></a>

## N7 — Imagen vs tabla (~10 min)

Clasificar fotos 64×64 “soldado / no soldado”.

-   **Alfa:** vector de 4096 píxeles → MLP denso enorme.
-   **Beta:** filtros locales + pooling + capas densas al final.
-   **Gamma:** regresión lineal sobre 4096 píxeles “como probabilidad”.


### Tareas

1.  ¿Cuál se parece a una CNN? Dos razones por las que Alfa suele ser peor.
2.  ¿Por qué Gamma es rara para sí/no?
3.  Datos **solo tabulares** (asistencia, promedio), sin imágenes: ¿CNN? Sí/No + por qué.
4.  Una frase: ventaja de un filtro 3×3 vs conectar todos los píxeles con todos.

---


<a id="org8c54205"></a>

# Autochequeo antes de entregar

1.  ¿Respondí **por qué**, no solo la letra?
2.  ¿Mis emparejamientos encajan con **todas** las pistas?
3.  ¿Distinguí datos tabulares vs imágenes?
4.  ¿Evité confundir “número” con “clase/probabilidad”?
5.  ¿Cuestioné resultados demasiado bonitos?

---


<a id="org9fbbd99"></a>

# Plantilla `informe_nexus.md`

    # Operación Nexus — Informe
    **Nombre / Matrícula:**
    
    ## N1 …
    ## N2 …
    ## N3 …
    ## N4 …
    ## N5 …
    ## N6 …
    ## N7 …
    
    ## Reflexión final (3 líneas)
    ¿En qué se parece resolver estos acertijos a hacer IA “de verdad”
    y en qué se diferencia de solo usar un chatbot?

