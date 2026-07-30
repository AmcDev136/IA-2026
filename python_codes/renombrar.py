"""
Renombra ÚNICAMENTE los archivos que empiezan con un prefijo específico
(por defecto "FacFer") dentro de una carpeta, dividiéndolos en sesiones
reales según los rangos de número que tú definas. El resto de archivos en
la carpeta (con otros prefijos) NO se tocan.

Ejemplo de lo que hace (con PREFIJO_A_BUSCAR = "FacFer"):
    FacFer1.jpg  ... FacFer85.jpg   -> ManuelSesion1_1.jpg ... ManuelSesion1_85.jpg
    FacFer86.jpg ... FacFer200.jpg  -> ManuelEntrevistaTV_1.jpg ... ManuelEntrevistaTV_115.jpg

El nombre nuevo (tercer valor de cada tupla en RANGOS) es TOTALMENTE LIBRE:
puede ser cualquier texto que quieras, no tiene que parecerse al prefijo
original ni entre sí. Solo evita espacios, comillas o caracteres especiales.

Uso:
    1. Cambia CARPETA a la ruta de la persona que quieras procesar
       (ej. "D:/Caras/Ryan/").
    2. Cambia PREFIJO_A_BUSCAR si el prefijo ambiguo no es "FacFer".
    3. Define RANGOS con los números reales y el nombre que tú quieras darle
       a cada sesión.
    4. Corre primero con DRY_RUN = True para ver una vista previa SIN
       renombrar nada todavía.
    5. Si la vista previa se ve bien, cambia DRY_RUN = False y vuelve a correr.
"""

import os
import re
import shutil

# ============================================================
# CONFIGURACIÓN — AJUSTA ESTO PARA CADA CARPETA QUE PROCESES
# ============================================================
CARPETA = "D:/Caras/Will_smith/"   # <-- cambia esta ruta según la persona

PREFIJO_A_BUSCAR = "FacFer"  # <-- el prefijo ambiguo que quieres dividir en sesiones

# Rangos reales de número que corresponden a cada sesión distinta.
# Formato: (numero_inicial, numero_final, "nombre_que_tu_quieras")
# El nombre puede ser lo que sea: "RyanEntrevistaGQ", "sesion_lluvia", etc.
RANGOS = [
    (1, 266, "Will_smith"),
    # Agrega más tuplas aquí si hay más sesiones mezcladas bajo el mismo prefijo
]

DRY_RUN = True   # True = solo muestra la vista previa, no renombra nada todavía

# PROCESO
def construir_patron(prefijo):
    return re.compile(rf'^{re.escape(prefijo)}(\d+)(\.\w+)$', re.IGNORECASE)

def encontrar_rango(numero, rangos):
    for (inicio, fin, nombre_sesion) in rangos:
        if inicio <= numero <= fin:
            return nombre_sesion
    return None

def main():
    patron = construir_patron(PREFIJO_A_BUSCAR)
    archivos = os.listdir(CARPETA)
    archivos_encontrados = []

    for archivo in archivos:
        match = patron.match(archivo)
        if match:
            numero = int(match.group(1))
            extension = match.group(2)
            archivos_encontrados.append((archivo, numero, extension))

    if not archivos_encontrados:
        print(f"No se encontraron archivos con prefijo '{PREFIJO_A_BUSCAR}' en {CARPETA}")
        return

    # Ordenamos por número para que la renumeración quede en orden
    archivos_encontrados.sort(key=lambda t: t[1])

    print(f"Encontrados {len(archivos_encontrados)} archivos con prefijo '{PREFIJO_A_BUSCAR}' en {CARPETA}\n")

    # Contador independiente por cada sesión nueva, para renumerar 1, 2, 3...
    contador_por_sesion = {}
    sin_rango = []
    operaciones = []  # (nombre_original, nombre_nuevo)

    for nombre_original, numero, extension in archivos_encontrados:
        nombre_sesion = encontrar_rango(numero, RANGOS)

        if nombre_sesion is None:
            sin_rango.append(nombre_original)
            continue

        contador_por_sesion[nombre_sesion] = contador_por_sesion.get(nombre_sesion, 0) + 1
        nuevo_numero = contador_por_sesion[nombre_sesion]
        nombre_nuevo = f"{nombre_sesion}_{nuevo_numero}{extension}"
        operaciones.append((nombre_original, nombre_nuevo))

    # ============================================================
    # VISTA PREVIA / EJECUCIÓN
    # ============================================================
    for nombre_original, nombre_nuevo in operaciones:
        print(f"  {nombre_original}  ->  {nombre_nuevo}")

    if sin_rango:
        print(f"\n⚠ {len(sin_rango)} archivos NO cayeron en ningún rango definido y NO se van a tocar:")
        for nombre in sin_rango:
            print(f"    - {nombre}")
        print("  Ajusta RANGOS si crees que deberían incluirse.")

    if DRY_RUN:
        print("\n[DRY_RUN=True] Esto fue solo una vista previa. No se renombró nada.")
        print("Si se ve correcto, cambia DRY_RUN = False y vuelve a correr el script.")
        return

    # Renombrado real
    renombrados = 0
    for nombre_original, nombre_nuevo in operaciones:
        ruta_original = os.path.join(CARPETA, nombre_original)
        ruta_nueva = os.path.join(CARPETA, nombre_nuevo)

        if os.path.exists(ruta_nueva):
            print(f"  ⚠ Se omitió '{nombre_original}': ya existe un archivo llamado '{nombre_nuevo}'")
            continue

        shutil.move(ruta_original, ruta_nueva)
        renombrados += 1

    print(f"\nListo. {renombrados} archivos renombrados en {CARPETA}")

if __name__ == "__main__":
    main()