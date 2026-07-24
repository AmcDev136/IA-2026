import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from pathlib import Path

# Configuración de URLs y encabezados
USER_AGENT = "ScraperPartidosLlama/1.0 (contacto@ejemplo.com)"
HEADERS = {"User-Agent": USER_AGENT}

TORNEOS = [
    {"nombre": "Mundial 2022", "url": "https://es.wikipedia.org/wiki/Copa_Mundial_de_F%C3%BAtbol_de_2022"},
    {"nombre": "Copa América 2024", "url": "https://es.wikipedia.org/wiki/Copa_Am%C3%A9rica_2024"},
    {"nombre": "Eurocopa 2024", "url": "https://es.wikipedia.org/wiki/Eurocopa_2024"},
    {"nombre": "Mundial 2026", "url": "https://es.wikipedia.org/wiki/Copa_Mundial_de_F%C3%BAtbol_de_2026"}
]

RUTA_CSV = Path("partidos_historicos.csv")

def limpiar_texto(texto: str) -> str:
    texto = re.sub(r'\[\w+\]', '', texto) 
    return texto.strip()

# Analiza el string del resultado para decidir quién ganó o si fue empate.
def determinar_ganador(eq1: str, res: str, eq2: str) -> str:
    # Estandarizar el separador de goles para que siempre sea ':'
    res = res.replace('-', ':')
    
    # Extraer el marcador principal (ej: "2:1" o "0:0")
    main_match = re.search(r'^(\d+)\s*:\s*(\d+)', res)
    
    if not main_match:
        return "Desconocido"
        
    goles_eq1 = int(main_match.group(1))
    goles_eq2 = int(main_match.group(2))
    
    # 1. Ganador en tiempo regular o extra
    if goles_eq1 > goles_eq2:
        return eq1
    elif goles_eq2 > goles_eq1:
        return eq2
    else:
        # 2. Si hay empate, buscar si hubo penales (ej: "(4:2 p.)")
        penales_match = re.search(r'\((\d+)\s*:\s*(\d+)\s*p', res, re.IGNORECASE)
        if penales_match:
            pen_eq1 = int(penales_match.group(1))
            pen_eq2 = int(penales_match.group(2))
            if pen_eq1 > pen_eq2:
                return eq1
            elif pen_eq2 > pen_eq1:
                return eq2
                
        # Si no hubo penales, se queda en empate (fase de grupos)
        return "Empate"

def extraer_partidos_de_html(html: str, nombre_torneo: str):
    partidos_encontrados = []
    soup = BeautifulSoup(html, "html.parser")
    filas = soup.find_all("tr")
    
    for fila in filas:
        celdas = fila.find_all(["td", "th"])
        if len(celdas) >= 3:
            for i in range(len(celdas) - 2):
                eq1 = limpiar_texto(celdas[i].get_text(separator=" "))
                res = limpiar_texto(celdas[i+1].get_text(separator=" "))
                eq2 = limpiar_texto(celdas[i+2].get_text(separator=" "))
                
                if re.search(r'^\d+\s*[:\-]\s*\d+', res):
                    if re.search(r'[a-zA-ZáéíóúÁÉÍÓÚ]', eq1) and re.search(r'[a-zA-ZáéíóúÁÉÍÓÚ]', eq2):
                        
                        # Llamamos a la función para determinar el ganador
                        ganador = determinar_ganador(eq1, res, eq2)
                        
                        partidos_encontrados.append({
                            "Torneo": nombre_torneo,
                            "Equipo_Local": eq1,
                            "Resultado": res,
                            "Equipo_Visitante": eq2,
                            "Ganador": ganador  # Nueva columna agregada
                        })
                        break 
                        
    return partidos_encontrados

def generar_csv_partidos():
    todos_los_partidos = []
    print("=== Iniciando extracción de Partidos ===")
    
    for torneo in TORNEOS:
        print(f"Rastreando marcadores de: {torneo['nombre']}...")
        try:
            respuesta = requests.get(torneo["url"], headers=HEADERS)
            respuesta.raise_for_status() 
            
            partidos_extraidos = extraer_partidos_de_html(respuesta.text, torneo["nombre"])
            todos_los_partidos.extend(partidos_extraidos)
            print(f"  -> Se encontraron {len(partidos_extraidos)} partidos.")
            
        except Exception as e:
            print(f"[ERROR] No se pudo acceder a {torneo['nombre']}: {e}")

    if todos_los_partidos:
        df = pd.DataFrame(todos_los_partidos)
        df.to_csv(RUTA_CSV, index=False, encoding="utf-8-sig")
        print(f"\n¡Extracción exitosa! Se guardaron {len(df)} partidos en '{RUTA_CSV.resolve()}'.")
    else:
        print("\nNo se encontraron partidos.")

if __name__ == "__main__":
    generar_csv_partidos()