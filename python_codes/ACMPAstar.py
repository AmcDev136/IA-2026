import pygame
import sys
import heapq

# --- ALGORITMO A* (LÓGICA) ---
def resolver_acertijo():
    estado_inicial = (0, 0, 0, 0) # (Arriero, Coyote, Pollo, Maiz)
    estado_objetivo = (1, 1, 1, 1)

    def es_valido(estado):
        a, c, p, m = estado
        if c == p and a != c: return False
        if p == m and a != p: return False
        return True

    def obtener_sucesores(estado):
        a, c, p, m = estado
        proxima_orilla = 1 - a
        sucesores = []
        sucesores.append((proxima_orilla, c, p, m))
        if c == a: sucesores.append((proxima_orilla, proxima_orilla, p, m))
        if p == a: sucesores.append((proxima_orilla, c, proxima_orilla, m))
        if m == a: sucesores.append((proxima_orilla, c, p, proxima_orilla))
        return [s for s in sucesores if es_valido(s)]

    def heuristica(estado):
        return sum(1 for elemento in estado if elemento == 0)

    lista_abierta = []
    heapq.heappush(lista_abierta, (heuristica(estado_inicial), 0, estado_inicial, [estado_inicial]))
    costos_g = {estado_inicial: 0}

    while lista_abierta:
        f, g, actual, camino = heapq.heappop(lista_abierta)
        if actual == estado_objetivo: return camino
        if g > costos_g.get(actual, float('inf')): continue

        for sucesor in obtener_sucesores(actual):
            nuevo_g = g + 1  # Definido como 'nuevo_g'
            if nuevo_g < costos_g.get(sucesor, float('inf')):
                costos_g[sucesor] = nuevo_g  # <- CORREGIDO AQUÍ (Antes decía new_g)
                nuevo_f = nuevo_g + heuristica(sucesor)
                heapq.heappush(lista_abierta, (nuevo_f, nuevo_g, sucesor, camino + [sucesor]))
    return None

# --- CONFIGURACIÓN DE PYGAME ---
pygame.init()
pygame.font.init()

ANCHO, ALTO = 900, 550
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Acertijo del Arriero - Controles Manuales A*")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Arial", 18)
fuente_grande = pygame.font.SysFont("Arial", 26, bold=True)

VERDE = (34, 139, 34)
AZUL = (30, 144, 255)
MARRON = (139, 69, 19)
GRIS = (220, 220, 220)
GRIS_OSCURO = (100, 100, 100)
NEGRO = (0, 0, 0)

ELEMENTOS = [
    ("Arriero", (210, 105, 30)),
    ("Coyote", (255, 140, 0)),
    ("Pollo", (255, 215, 0)),
    ("Maíz", (154, 205, 50))
]

ruta_solucion = resolver_acertijo()
paso_actual = 0

def dibujar_escenario(estado, paso):
    pantalla.fill(NEGRO)
    
    pygame.draw.rect(pantalla, VERDE, (0, 100, 250, 380))
    pygame.draw.rect(pantalla, AZUL, (250, 100, 400, 380))
    pygame.draw.rect(pantalla, VERDE, (650, 100, 250, 380))

    pos_barca_x = 260 if estado[0] == 0 else 540  # Ajustado índice para leer la posición del Arriero
    pygame.draw.rect(pantalla, MARRON, (pos_barca_x, 260, 100, 50))
    texto_barca = fuente.render("Barca", True, GRIS)
    pantalla.blit(texto_barca, (pos_barca_x + 25, 275))

    elementos_en_a = 0
    elementos_en_b = 0

    for i, (nombre, color) in enumerate(ELEMENTOS):
        orilla = estado[i]
        if orilla == 0:
            x = 50
            y = 130 + (elementos_en_a * 55)
            elementos_en_a += 1
        else:
            x = 750
            y = 130 + (elementos_en_b * 55)
            elementos_en_b += 1

        pygame.draw.rect(pantalla, color, (x, y, 100, 40))
        txt = fuente.render(nombre, True, NEGRO)
        pantalla.blit(txt, (x + 10, y + 10))

    txt_paso = fuente_grande.render(f"Paso: {paso} / {len(ruta_solucion) - 1}", True, GRIS)
    pantalla.blit(txt_paso, (20, 20))
    
    txt_orilla_a = fuente_grande.render("Orilla A", True, VERDE)
    pantalla.blit(txt_orilla_a, (50, 65))
    
    txt_orilla_b = fuente_grande.render("Orilla B (Meta)", True, VERDE)
    pantalla.blit(txt_orilla_b, (680, 65))

    pygame.draw.rect(pantalla, GRIS_OSCURO, (0, 490, ANCHO, 60))
    txt_controles = fuente.render("Controles: [Derecha / Espacio] Avanzar  |  [Izquierda] Retroceder  |  [R] Reiniciar", True, GRIS)
    pantalla.blit(txt_controles, (30, 510))

    if paso == len(ruta_solucion) - 1:
        txt_fin = fuente_grande.render("¡Acertijo Resuelto!", True, (0, 255, 0))
        pantalla.blit(txt_fin, (330, 20))
    else:
        txt_estado = fuente.render(f"Estado binario (A, C, P, M): {estado}", True, GRIS)
        pantalla.blit(txt_estado, (320, 220))

# --- BUCLE PRINCIPAL ---
ejecutando = True
while ejecutando:
    reloj.tick(30)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RIGHT or evento.key == pygame.K_SPACE:
                if paso_actual < len(ruta_solucion) - 1:
                    paso_actual += 1
            elif evento.key == pygame.K_LEFT:
                if paso_actual > 0:
                    paso_actual -= 1
            elif evento.key == pygame.K_r:
                paso_actual = 0

    estado_animacion = ruta_solucion[paso_actual]
    dibujar_escenario(estado_animacion, paso_actual)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
