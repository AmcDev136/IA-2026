import pygame
import sys
import heapq
import math

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
LIGHT_GRAY = (220, 220, 220)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
DARK_GREEN = (0, 100, 0)

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.parent = None
        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.is_visited = False
        self.is_path = False
        self.in_open = False
        self.id = x * 1000 + y
    
    def calculate_f(self):
        self.f = self.g + self.h
    
    def calculate_h(self, end_node):
        self.h = (abs(self.x - end_node.x) + abs(self.y - end_node.y)) * 10
        self.calculate_f()
    
    def __lt__(self, other):
        if self.f != other.f:
            return self.f < other.f
        return self.id < other.id
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)

class InputBox:
    def __init__(self, x, y, w, h, text='', max_length=2):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = LIGHT_GRAY
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, BLACK)
        self.active = False
        self.max_length = max_length
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = DARK_BLUE if self.active else LIGHT_GRAY
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = LIGHT_GRAY
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if event.unicode.isdigit() and len(self.text) < self.max_length:
                    self.text += event.unicode
            
            self.txt_surface = self.font.render(self.text, True, BLACK)
        return False
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        text_x = self.rect.x + 5
        text_y = self.rect.y + (self.rect.height - self.txt_surface.get_height()) // 2
        screen.blit(self.txt_surface, (text_x, text_y))
        
        if self.active:
            cursor_x = text_x + self.txt_surface.get_width() + 2
            cursor_y = self.rect.y + 5
            pygame.draw.line(screen, BLACK, (cursor_x, cursor_y), 
                           (cursor_x, cursor_y + self.rect.height - 10), 2)
    
    def get_value(self):
        return int(self.text) if self.text else 0

class AStarGame:
    def __init__(self):
        pygame.init()
        
        # Configuración inicial
        self.rows = 8
        self.cols = 8
        self.cell_size = 55
        self.margin = 40
        self.top_offset = 60
        
        # Costos de movimiento
        self.COST_STRAIGHT = 10
        self.COST_DIAGONAL = 14
        
        self.calculate_dimensions()
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("A* Pathfinding - Con cálculos de f(n)=g(n)+h(n)")
        self.clock = pygame.time.Clock()
        
        # Fuentes
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 14)
        self.big_font = pygame.font.Font(None, 28)
        self.info_font = pygame.font.Font(None, 20)
        self.cell_font = pygame.font.Font(None, 12)
        
        self.reset()
        self.size_selector_active = False
        self.input_rows = InputBox(0, 0, 60, 35, str(self.rows), 2)
        self.input_cols = InputBox(0, 0, 60, 35, str(self.cols), 2)
        self.btn_accept = None
        self.btn_cancel = None
        
        self.selected_node = None
        self.show_info_panel = False
    
    def calculate_dimensions(self):
        min_width = self.cols * self.cell_size + self.margin * 2 + 250
        min_height = self.rows * self.cell_size + self.margin * 2 + 180
        
        self.screen_width = max(800, min_width)
        self.screen_height = max(500, min_height)
    
    def reset(self):
        self.grid = [[Node(x, y) for y in range(self.rows)] for x in range(self.cols)]
        self.start = None
        self.end = None
        self.running = False
        self.finished = False
        self.open_set = []
        self.closed_set = set()
        self.current_node = None
        self.step_counter = 0
        self.path = []
        self.message = "Click izquierdo: INICIO | Click derecho: MURO"
        self.search_complete = False
        self.auto_mode = False
        self.dragging = False
        self.drag_type = None
        self.selected_node = None
        self.show_info_panel = False
    
    def set_start(self, x, y):
        if self.grid[x][y].is_wall:
            return False
        if self.start:
            self.start.is_start = False
        self.start = self.grid[x][y]
        self.start.is_start = True
        self.start.g = 0
        self.start.h = 0
        self.start.f = 0
        return True
    
    def set_end(self, x, y):
        if self.grid[x][y].is_wall:
            return False
        if self.end:
            self.end.is_end = False
        self.end = self.grid[x][y]
        self.end.is_end = True
        return True
    
    def toggle_wall(self, x, y):
        node = self.grid[x][y]
        if node.is_start or node.is_end:
            return False
        node.is_wall = not node.is_wall
        return True
    
    def get_neighbors(self, node):
        neighbors = []
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            nx, ny = node.x + dx, node.y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows:
                if not self.grid[nx][ny].is_wall:
                    neighbors.append(self.grid[nx][ny])
        return neighbors
    
    def get_movement_cost(self, from_node, to_node):
        dx = abs(from_node.x - to_node.x)
        dy = abs(from_node.y - to_node.y)
        
        if dx == 1 and dy == 1:
            return self.COST_DIAGONAL
        elif (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
            return self.COST_STRAIGHT
        return 0
    
    def step_astar(self):
        if not self.open_set or self.finished:
            return False
        
        self.current_node = heapq.heappop(self.open_set)[1]
        
        if self.current_node == self.end:
            self.finished = True
            self.search_complete = True
            self.reconstruct_path()
            self.message = f"¡Camino encontrado! Costo total: {self.end.g}"
            self.auto_mode = False
            return True
        
        self.closed_set.add(self.current_node)
        self.current_node.is_visited = True
        self.step_counter += 1
        
        for neighbor in self.get_neighbors(self.current_node):
            if neighbor in self.closed_set or neighbor.is_wall:
                continue
            
            move_cost = self.get_movement_cost(self.current_node, neighbor)
            temp_g = self.current_node.g + move_cost
            
            if temp_g < neighbor.g:
                neighbor.parent = self.current_node
                neighbor.g = temp_g
                neighbor.calculate_h(self.end)
                neighbor.calculate_f()
                
                in_open = False
                for item in self.open_set:
                    if item[1] == neighbor:
                        in_open = True
                        break
                
                if not in_open:
                    heapq.heappush(self.open_set, (neighbor.f, neighbor))
                    neighbor.in_open = True
        
        return True
    
    def reconstruct_path(self):
        if not self.end.parent:
            return
        
        current = self.end
        while current:
            self.path.append(current)
            if current == self.start:
                break
            current = current.parent
        
        self.path.reverse()
        for node in self.path:
            node.is_path = True
    
    def run_astar(self):
        if not self.start or not self.end:
            self.message = "¡Coloca INICIO y META primero!"
            return
        
        for row in self.grid:
            for node in row:
                if not node.is_start and not node.is_end and not node.is_wall:
                    node.is_visited = False
                    node.is_path = False
                    node.in_open = False
                    node.g = float('inf')
                    node.f = float('inf')
                    node.parent = None
        
        self.start.g = 0
        self.start.calculate_h(self.end)
        self.start.calculate_f()
        self.open_set = [(self.start.f, self.start)]
        self.closed_set = set()
        self.finished = False
        self.search_complete = False
        self.path = []
        self.step_counter = 0
        
        self.message = "Ejecutando A* con movimiento diagonal (costo: 10/14)..."
        self.running = True
    
    def get_grid_pos(self, pos):
        x = (pos[0] - self.margin) // self.cell_size
        y = (pos[1] - self.margin - self.top_offset) // self.cell_size
        return x, y
    
    def is_in_grid(self, pos):
        x, y = self.get_grid_pos(pos)
        return 0 <= x < self.cols and 0 <= y < self.rows
    
    def get_grid_rect(self, x, y):
        return pygame.Rect(
            self.margin + x * self.cell_size,
            self.margin + self.top_offset + y * self.cell_size,
            self.cell_size,
            self.cell_size
        )
    
    def handle_click(self, pos, button):
        if self.running:
            return
        
        x, y = self.get_grid_pos(pos)
        if not (0 <= x < self.cols and 0 <= y < self.rows):
            return
        
        node = self.grid[x][y]
        
        if button == 1:
            if not self.start:
                if self.set_start(x, y):
                    self.message = "Ahora coloca la META"
                    self.selected_node = node
                    self.show_info_panel = True
            elif not self.end:
                if self.set_end(x, y):
                    self.message = "¡Listo! Usa clic derecho para muros"
                    self.selected_node = node
                    self.show_info_panel = True
            elif node == self.start:
                self.dragging = True
                self.drag_type = 'start'
                self.start.is_start = False
                self.start = None
                self.message = "Moviendo INICIO..."
            elif node == self.end:
                self.dragging = True
                self.drag_type = 'end'
                self.end.is_end = False
                self.end = None
                self.message = "Moviendo META..."
            else:
                self.selected_node = node
                self.show_info_panel = True
                self.message = f"Info: Celda ({x}, {y})"
        
        elif button == 3:
            if not node.is_start and not node.is_end:
                self.toggle_wall(x, y)
                self.message = f"Muro {'añadido' if node.is_wall else 'eliminado'}"
                if node.is_wall:
                    self.selected_node = None
                    self.show_info_panel = False
    
    def handle_drag(self, pos):
        if not self.dragging:
            return
        
        x, y = self.get_grid_pos(pos)
        if not (0 <= x < self.cols and 0 <= y < self.rows):
            return
        
        if self.drag_type == 'start':
            if not self.grid[x][y].is_wall and self.grid[x][y] != self.end:
                if self.start:
                    self.start.is_start = False
                self.start = self.grid[x][y]
                self.start.is_start = True
                self.start.g = 0
                self.start.h = 0
                self.start.f = 0
                self.message = f"Inicio movido a ({x}, {y})"
                self.selected_node = self.start
        elif self.drag_type == 'end':
            if not self.grid[x][y].is_wall and self.grid[x][y] != self.start:
                if self.end:
                    self.end.is_end = False
                self.end = self.grid[x][y]
                self.end.is_end = True
                self.message = f"Meta movida a ({x}, {y})"
                self.selected_node = self.end
    
    def draw_cell_values(self, rect, node):
        """Dibujar los valores G, H, F en la celda"""
        if node.is_wall or node.is_start or node.is_end:
            return
        
        if node.f == float('inf'):
            return
        
        cell_size = rect.width
        
        # Solo mostrar si la celda es lo suficientemente grande
        if cell_size < 40:
            return
        
        # Colores para los textos
        color_g = (0, 0, 200)  # Azul oscuro
        color_h = (200, 0, 0)  # Rojo
        color_f = (0, 150, 0)  # Verde oscuro
        
        # Tamaño de fuente según el tamaño de celda
        font_size = max(8, min(12, cell_size // 4))
        cell_font = pygame.font.Font(None, font_size)
        
        # Posiciones
        spacing = cell_size // 4
        
        # G
        if node.g != float('inf'):
            g_text = cell_font.render(f"G={int(node.g)}", True, color_g)
            self.screen.blit(g_text, (rect.x + 2, rect.y + 2))
        
        # H
        if node.h != float('inf'):
            h_text = cell_font.render(f"H={int(node.h)}", True, color_h)
            self.screen.blit(h_text, (rect.x + 2, rect.y + spacing))
        
        # F
        if node.f != float('inf'):
            f_text = cell_font.render(f"F={int(node.f)}", True, color_f)
            self.screen.blit(f_text, (rect.x + 2, rect.y + spacing * 2))
    
    def draw_info_panel(self):
        if not self.show_info_panel or not self.selected_node:
            return
        
        node = self.selected_node
        
        panel_x = self.margin + self.cols * self.cell_size + 20
        panel_y = self.margin + self.top_offset
        panel_width = 220
        panel_height = 320
        
        pygame.draw.rect(self.screen, LIGHT_GRAY, (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, DARK_GRAY, (panel_x, panel_y, panel_width, panel_height), 2)
        
        title = self.font.render("Información de Celda", True, DARK_BLUE)
        self.screen.blit(title, (panel_x + 10, panel_y + 10))
        pygame.draw.line(self.screen, DARK_GRAY, (panel_x + 10, panel_y + 35), 
                        (panel_x + panel_width - 10, panel_y + 35), 2)
        
        y_pos = panel_y + 50
        info_lines = [
            f"Posición: ({node.x}, {node.y})",
            f"Tipo: {'Inicio' if node.is_start else 'Meta' if node.is_end else 'Normal'}",
            f"Es muro: {'Sí' if node.is_wall else 'No'}",
            "",
            "--- VALORES ---",
            f"G(n) = {node.g if node.g != float('inf') else '∞'}",
            f"H(n) = {node.h}",
            f"F(n) = {node.f if node.f != float('inf') else '∞'}",
            "",
            f"Fórmula: F(n) = G(n) + H(n)",
            f"F(n) = {node.g if node.g != float('inf') else '∞'} + {node.h}",
            f"F(n) = {node.f if node.f != float('inf') else '∞'}"
        ]
        
        for line in info_lines:
            if line.startswith("---"):
                text = self.info_font.render(line, True, DARK_BLUE)
                self.screen.blit(text, (panel_x + 10, y_pos))
            elif line.startswith("F(n) =") and node.f != float('inf'):
                text = self.info_font.render(line, True, RED)
                self.screen.blit(text, (panel_x + 10, y_pos))
            else:
                text = self.info_font.render(line, True, BLACK)
                self.screen.blit(text, (panel_x + 10, y_pos))
            y_pos += 22
        
        # Estado
        status_y = y_pos + 10
        if node.is_visited:
            status = "Estado: Visitado (Closed)"
            color = LIGHT_BLUE
        elif node.in_open:
            status = "Estado: En Open Set"
            color = ORANGE
        elif node.is_path:
            status = "Estado: En el Camino"
            color = GREEN
        else:
            status = "Estado: No explorado"
            color = GRAY
        
        status_text = self.info_font.render(status, True, color)
        self.screen.blit(status_text, (panel_x + 10, status_y))
    
    def draw_legend(self):
        panel_x = self.margin + self.cols * self.cell_size + 20
        panel_y = self.margin + self.top_offset + 340
        panel_width = 220
        panel_height = 180
        
        pygame.draw.rect(self.screen, LIGHT_GRAY, (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, DARK_GRAY, (panel_x, panel_y, panel_width, panel_height), 2)
        
        title = self.small_font.render("Leyenda", True, DARK_BLUE)
        self.screen.blit(title, (panel_x + 10, panel_y + 5))
        
        legend_items = [
            (BLUE, "Inicio (S)"),
            (RED, "Meta (E)"),
            (BLACK, "Muro"),
            (LIGHT_BLUE, "Visitado"),
            (ORANGE, "En Open Set"),
            (GREEN, "Camino"),
            (WHITE, "No explorado")
        ]
        
        y_pos = panel_y + 30
        for color, label in legend_items:
            pygame.draw.rect(self.screen, color, (panel_x + 10, y_pos, 15, 15))
            pygame.draw.rect(self.screen, DARK_GRAY, (panel_x + 10, y_pos, 15, 15), 1)
            text = self.small_font.render(label, True, BLACK)
            self.screen.blit(text, (panel_x + 30, y_pos - 2))
            y_pos += 20
        
        # Mostrar también los colores de los valores
        y_pos += 5
        pygame.draw.line(self.screen, DARK_GRAY, (panel_x + 10, y_pos), 
                        (panel_x + panel_width - 10, y_pos), 1)
        y_pos += 5
        text = self.small_font.render("G=Azul  H=Rojo  F=Verde", True, DARK_GRAY)
        self.screen.blit(text, (panel_x + 10, y_pos))
    
    def draw_size_selector(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(WHITE)
        self.screen.blit(overlay, (0, 0))
        
        panel_width = 400
        panel_height = 350
        panel_x = (self.screen_width - panel_width) // 2
        panel_y = (self.screen_height - panel_height) // 2
        
        pygame.draw.rect(self.screen, WHITE, (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, BLACK, (panel_x, panel_y, panel_width, panel_height), 3)
        
        title = self.big_font.render("Cambiar Tamaño del Laberinto", True, DARK_BLUE)
        title_rect = title.get_rect(center=(self.screen_width//2, panel_y + 40))
        self.screen.blit(title, title_rect)
        
        instruction = self.small_font.render("Ingresa el número de FILAS y COLUMNAS (3-20):", True, BLACK)
        instr_rect = instruction.get_rect(center=(self.screen_width//2, panel_y + 80))
        self.screen.blit(instruction, instr_rect)
        
        label_x = panel_x + 50
        label_y = panel_y + 130
        
        rows_label = self.font.render("Filas:", True, BLACK)
        self.screen.blit(rows_label, (label_x, label_y))
        self.input_rows.rect.x = label_x + 80
        self.input_rows.rect.y = label_y - 5
        self.input_rows.draw(self.screen)
        
        cols_label = self.font.render("Columnas:", True, BLACK)
        self.screen.blit(cols_label, (label_x, label_y + 60))
        self.input_cols.rect.x = label_x + 80
        self.input_cols.rect.y = label_y + 55
        self.input_cols.draw(self.screen)
        
        btn_width = 100
        btn_height = 40
        
        self.btn_accept = pygame.Rect(panel_x + 80, panel_y + 260, btn_width, btn_height)
        pygame.draw.rect(self.screen, GREEN, self.btn_accept)
        pygame.draw.rect(self.screen, BLACK, self.btn_accept, 2)
        accept_text = self.font.render("Aceptar", True, BLACK)
        accept_rect = accept_text.get_rect(center=self.btn_accept.center)
        self.screen.blit(accept_text, accept_rect)
        
        self.btn_cancel = pygame.Rect(panel_x + 220, panel_y + 260, btn_width, btn_height)
        pygame.draw.rect(self.screen, RED, self.btn_cancel)
        pygame.draw.rect(self.screen, BLACK, self.btn_cancel, 2)
        cancel_text = self.font.render("Cancelar", True, WHITE)
        cancel_rect = cancel_text.get_rect(center=self.btn_cancel.center)
        self.screen.blit(cancel_text, cancel_rect)
        
        range_text = self.small_font.render("Rango permitido: 3 - 20", True, GRAY)
        range_rect = range_text.get_rect(center=(self.screen_width//2, panel_y + 320))
        self.screen.blit(range_text, range_rect)
    
    def handle_size_selector_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_accept and self.btn_accept.collidepoint(event.pos):
                rows = self.input_rows.get_value()
                cols = self.input_cols.get_value()
                
                if 3 <= rows <= 20 and 3 <= cols <= 20:
                    self.rows = rows
                    self.cols = cols
                    self.calculate_dimensions()
                    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
                    self.reset()
                    self.size_selector_active = False
                    self.message = f"Tamaño cambiado a {cols}x{rows}"
                else:
                    self.message = "Error: El tamaño debe estar entre 3 y 20"
            
            elif self.btn_cancel and self.btn_cancel.collidepoint(event.pos):
                self.size_selector_active = False
                self.message = "Cambio de tamaño cancelado"
        
        self.input_rows.handle_event(event)
        self.input_cols.handle_event(event)
    
    def draw_grid(self):
        self.screen.fill(WHITE)
        
        # Título
        title = self.big_font.render("A* Pathfinding - Con movimiento diagonal (costo: 10/14)", True, DARK_BLUE)
        self.screen.blit(title, (self.margin, 5))
        
        # Calcular tamaño de celda
        available_width = self.screen_width - self.margin * 2 - 250
        available_height = self.screen_height - self.margin * 2 - self.top_offset - 160
        
        if available_width > 0 and available_height > 0:
            max_cell_width = available_width // self.cols
            max_cell_height = available_height // self.rows
            self.cell_size = min(55, max_cell_width, max_cell_height)
            self.cell_size = max(25, self.cell_size)
        
        # Dibujar grid
        for x in range(self.cols):
            for y in range(self.rows):
                rect = self.get_grid_rect(x, y)
                node = self.grid[x][y]
                
                # Color según tipo
                if node.is_wall:
                    color = BLACK
                elif node.is_path:
                    color = GREEN
                elif node.is_visited:
                    color = LIGHT_BLUE
                elif node.is_start:
                    color = BLUE
                elif node.is_end:
                    color = RED
                elif node.in_open:
                    color = ORANGE
                else:
                    color = WHITE
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, GRAY, rect, 1)
                
                # Dibujar S o E
                if node.is_start:
                    text = self.big_font.render("S", True, WHITE)
                    self.screen.blit(text, (rect.x + rect.width//2 - 10, rect.y + rect.height//2 - 12))
                elif node.is_end:
                    text = self.big_font.render("E", True, WHITE)
                    self.screen.blit(text, (rect.x + rect.width//2 - 10, rect.y + rect.height//2 - 12))
                else:
                    # Dibujar valores G, H, F
                    self.draw_cell_values(rect, node)
        
        # Dibujar panel de información y leyenda
        self.draw_info_panel()
        self.draw_legend()
        
        # Información
        info_y = self.margin + self.top_offset + self.rows * self.cell_size + 10
        info_text = f"Pasos: {self.step_counter} | Tamaño: {self.cols}x{self.rows}"
        if self.start and self.end:
            dist = (abs(self.start.x - self.end.x) + abs(self.start.y - self.end.y)) * 10
            info_text += f" | Dist. Manhattan: {dist}"
        
        text_surface = self.font.render(info_text, True, BLACK)
        self.screen.blit(text_surface, (self.margin, info_y))
        
        # Mensaje
        msg_surface = self.font.render(self.message, True, RED)
        self.screen.blit(msg_surface, (self.margin, info_y + 30))
        
        # Controles
        controls_y = info_y + 60
        controls = [
            "Click IZQUIERDO: Colocar/Mover INICIO (azul) y META (rojo)",
            "Click DERECHO: Poner/Quitar MURO (negro)",
            "Click en celda: Ver cálculos de F(n)=G(n)+H(n)",
            "ESPACIO: Paso a paso | A: Automático | R: Reiniciar | T: Tamaño | C: Limpiar"
        ]
        
        for i, ctrl in enumerate(controls):
            ctrl_surface = self.small_font.render(ctrl, True, DARK_BLUE)
            self.screen.blit(ctrl_surface, (self.margin, controls_y + i * 20))
    
    def clear_all(self):
        self.start = None
        self.end = None
        self.running = False
        self.finished = False
        self.path = []
        self.step_counter = 0
        self.open_set = []
        self.closed_set = set()
        
        for row in self.grid:
            for node in row:
                if not node.is_wall:
                    node.is_start = False
                    node.is_end = False
                    node.is_visited = False
                    node.is_path = False
                    node.in_open = False
                    node.g = float('inf')
                    node.f = float('inf')
                    node.parent = None
        
        self.selected_node = None
        self.show_info_panel = False
        self.message = "Todo limpiado. Coloca INICIO y META"
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.VIDEORESIZE:
                    self.screen_width, self.screen_height = event.w, event.h
                    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
                
                if self.size_selector_active:
                    self.handle_size_selector_events(event)
                    continue
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 or event.button == 3:
                        if self.is_in_grid(event.pos):
                            self.handle_click(event.pos, event.button)
                
                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[0] or event.buttons[2]:
                        if self.is_in_grid(event.pos):
                            self.handle_drag(event.pos)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.dragging:
                        self.dragging = False
                        self.drag_type = None
                        self.message = "Listo para continuar"
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.running:
                            self.run_astar()
                        else:
                            if not self.finished:
                                self.step_astar()
                    
                    elif event.key == pygame.K_a:
                        if not self.running:
                            self.run_astar()
                            self.auto_mode = True
                        elif not self.finished:
                            self.auto_mode = True
                    
                    elif event.key == pygame.K_r:
                        self.reset()
                        self.auto_mode = False
                    
                    elif event.key == pygame.K_t:
                        self.input_rows.text = str(self.rows)
                        self.input_cols.text = str(self.cols)
                        self.input_rows.txt_surface = self.input_rows.font.render(self.input_rows.text, True, BLACK)
                        self.input_cols.txt_surface = self.input_cols.font.render(self.input_cols.text, True, BLACK)
                        self.size_selector_active = True
                        self.auto_mode = False
                    
                    elif event.key == pygame.K_c:
                        self.clear_all()
                        self.auto_mode = False
                    
                    elif event.key == pygame.K_ESCAPE:
                        self.selected_node = None
                        self.show_info_panel = False
                        self.message = "Panel de información cerrado"
            
            if self.auto_mode and self.running and not self.finished:
                self.step_astar()
                self.clock.tick(5)
            
            if self.size_selector_active:
                self.draw_grid()
                self.draw_size_selector()
            else:
                self.draw_grid()
            
            pygame.display.flip()
            self.clock.tick(30)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = AStarGame()
    game.run()