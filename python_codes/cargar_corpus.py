import pandas as pd
import re
import nltk
from nltk import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from pathlib import Path

# Definir rutas de entrada y salida
ruta_entrada = Path(r"D:\IA Verano 2026\reddit_voto.csv")
ruta_salida = Path(r"D:\IA Verano 2026\reddit_voto_limpio.csv")

print(f"Cargando archivo: {ruta_entrada}")
df = pd.read_csv(ruta_entrada)
print(f"Total de filas cargadas: {len(df)}")

# Identificar y combinar columnas fragmentadas generadas por el scraper
columnas_texto = [col for col in df.columns if 'py-0' in col]

print("Combinando columnas fragmentadas...")
df['comentario_completo'] = df[columnas_texto].apply(
    lambda row: ' '.join([str(x) for x in row if pd.notna(x)]), axis=1
)

# Función de limpieza (minúsculas y quitar símbolos/puntuación)
def limpiar_texto(texto):
    texto = str(texto).lower()
    # Mantener solo palabras y espacios (elimina puntuación y símbolos)
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

print("Aplicando limpieza básica...")
df['texto_limpio'] = df['comentario_completo'].apply(limpiar_texto)

# Tokenización (partir en palabras)
print("Tokenizando el texto...")
df['tokens'] = df['texto_limpio'].apply(word_tokenize)

# Eliminar stopwords
print("Eliminando stopwords (palabras comunes)...")
stop_words = set(stopwords.words('spanish'))

def quitar_stopwords(tokens):
    return [palabra for palabra in tokens if palabra not in stop_words]

df['tokens_limpios'] = df['tokens'].apply(quitar_stopwords)

# Unir tokens limpios de nuevo en texto para el clasificador
df['texto_final'] = df['tokens_limpios'].apply(lambda x: ' '.join(x))

# Analisis de frecuencia del corpus
todos_los_tokens = [] #juntar todos los tokens en una lista grande
#iteramos sobre la columna sin stopwords
for lista_de_tokens in df['tokens_limpios']:
    todos_los_tokens.extend(lista_de_tokens)

#Calcular la distribucion de frec
fd = FreqDist(todos_los_tokens)
print(f"Tokens totales (con repetición): {len(todos_los_tokens)}")
print(f"Vocabulario (palabras únicas): {len(fd)}")
print("\nTop 20 palabras más frecuentes del tema:")
for w, n in fd.most_common(20):
    print(f"  {w:20s}  {n}")
print("-----------------------------------------\n")

# Prueba de Vectorización (Matriz de frecuencias / Features)
print("Generando matriz de frecuencias (BoW)...")
vectorizer = CountVectorizer()
X_features = vectorizer.fit_transform(df['texto_final'])
print(f"Matriz de características (X_features) generada con dimensiones: {X_features.shape}")

# Guardar CSV limpio
print("Guardando el nuevo archivo CSV...")
df_limpio = df[['comentario_completo', 'texto_final']].copy()
df_limpio.to_csv(ruta_salida, index=False, encoding='utf-8')

print(f"¡Proceso finalizado! El archivo limpio está en: {ruta_salida}")