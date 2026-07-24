import json
import re
import wikipediaapi
from pathlib import Path

# Configuración de la API de Wikipedia
USER_AGENT = "CorpusMundialLlama/1.0 (contacto@ejemplo.com)"

wiki = wikipediaapi.Wikipedia(
    user_agent=USER_AGENT,
    language='es',
    extract_format=wikipediaapi.ExtractFormat.WIKI
)

# Lista de artículos a extraer
ARTICULOS = [
    {
        "titulo_wiki": "Copa_Mundial_de_Fútbol_de_2022",
        "nombre_bonito": "Copa Mundial de Fútbol Catar 2022"
    },
    {
        "titulo_wiki": "Copa_América_2024",
        "nombre_bonito": "Copa América 2024"
    },
    {
        "titulo_wiki": "Eurocopa_2024",
        "nombre_bonito": "Eurocopa 2024"
    },
    {
        "titulo_wiki": "Copa_Mundial_de_Fútbol_de_2026",
        "nombre_bonito": "Copa Mundial de Fútbol Norteamérica 2026"
    }
]

# Ruta del archivo final
RUTA_JSONL = Path("corpus_mundial.jsonl")

# Limpia saltos de línea excesivos.
def limpiar_texto(texto: str) -> str:
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    return texto.strip()

# Extrae el contenido de cada sección recursivamente.
def extraer_secciones_recursivo(sections):
    datos_secciones = []
    
    for sec in sections:
        # Evitar secciones irrelevantes para el modelo
        if sec.title.lower() in ["véase también", "referencias", "enlaces externos", "bibliografía"]:
            continue
            
        contenido = sec.text.strip()
        
        if contenido:
            datos_secciones.append({
                "subtema": sec.title,
                "texto": contenido
            })
            
        # Llamada recursiva para subsecciones
        if sec.sections:
            datos_secciones.extend(extraer_secciones_recursivo(sec.sections))
            
    return datos_secciones

def procesar_corpus():
    jsonl_records = []
    
    print("=== Iniciando extracción para JSONL ===")
    
    for item in ARTICULOS:
        titulo_page = item["titulo_wiki"]
        nombre_torneo = item["nombre_bonito"]
        
        print(f"Procesando: {nombre_torneo}...")
        page = wiki.page(titulo_page)
        
        if not page.exists():
            print(f"[ERROR] La página '{titulo_page}' no existe en Wikipedia.")
            continue
            
        # Resumen inicial
        resumen = limpiar_texto(page.summary)
        jsonl_records.append({
            "instruction": f"Proporciona un resumen general de {nombre_torneo}.",
            "context": f"Información sobre {nombre_torneo}.",
            "response": resumen
        })
        
        # Secciones individuales
        secciones = extraer_secciones_recursivo(page.sections)
        for sec in secciones:
            jsonl_records.append({
                "instruction": f"Información sobre {sec['subtema']} en {nombre_torneo}.",
                "context": f"Torneo: {nombre_torneo} | Sección: {sec['subtema']}",
                "response": sec['texto']
            })

    # Exporta directamente el archivo JSONL
    print(f"\nGuardando archivo en: {RUTA_JSONL.resolve()}")
    with open(RUTA_JSONL, "w", encoding="utf-8") as f:
        for record in jsonl_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            
    print(f"¡Proceso completado! Se guardó 'corpus_llama.jsonl' con {len(jsonl_records)} registros.")

if __name__ == "__main__":
    procesar_corpus()