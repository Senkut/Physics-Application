import pygame
import math

# --- CONFIGURACIÓN DE ESTILO ---
pygame.init()
WIDTH, HEIGHT = 1200, 750
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("USTA Physics Lab - Cinematic Pro")

# Paleta de Colores "Deep Space"
BG_COLOR = (15, 23, 42)      # Azul muy oscuro
SIDEBAR_COLOR = (30, 41, 59)  # Azul grisáceo
ACCENT_COLOR = (45, 212, 191) # Turquesa neón
TEXT_COLOR = (241, 245, 249)  # Blanco grisáceo
ERROR_COLOR = (244, 63, 94)   # Carmesí
SUCCESS_COLOR = (34, 197, 94) # Verde esmeralda
TRAIL_COLOR = (94, 234, 212, 100) # Turquesa con transparencia

# Fuentes
FONT_MAIN = pygame.font.SysFont("Segoe UI", 22)
FONT_BOLD = pygame.font.SysFont("Segoe UI", 24, bold=True)
FONT_TITLE = pygame.font.SysFont("Segoe UI", 36, bold=True)
FONT_SMALL = pygame.font.SysFont("Segoe UI", 16)

# Constantes Físicas (Invariables)
G = 9.81
SCALE = 8  # Ajustado para mejor visibilidad en la nueva UI

class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        c = self.hover_color if self.is_hovered else self.color
        # Dibujar sombra
        pygame.draw.rect(surface, (10, 15, 25), (self.rect.x+2, self.rect.y+2, self.rect.w, self.rect.h), border_radius=8)
        # Botón principal
        pygame.draw.rect(surface, c, self.rect, border_radius=8)
        txt = FONT_BOLD.render(self.text, True, TEXT_COLOR)
        surface.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))

    def update(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

class InputField:
    def __init__(self, x, y, w, h, label, default=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.text = default
        self.active = False

    def draw(self, surface):
        color = ACCENT_COLOR if self.active else (71, 85, 105)
        # Etiqueta
        lbl = FONT_SMALL.render(self.label.upper(), True, (148, 163, 184))
        surface.blit(lbl, (self.rect.x, self.rect.y - 22))
        # Caja
        pygame.draw.rect(surface, (15, 23, 42), self.rect, border_radius=5)
        pygame.draw.rect(surface, color, self.rect, 2, border_radius=5)
        # Texto
        txt = FONT_MAIN.render(self.text, True, TEXT_COLOR)
        surface.blit(txt, (self.rect.x + 12, self.rect.y + 8))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE: self.text = self.text[:-1]
            elif event.unicode in "0123456789.": self.text += event.unicode

    def get_val(self):
        try: return float(self.text)
        except: return 0.0

def draw_grid(surface):
    # Dibujar una cuadrícula de fondo profesional
    for x in range(250, WIDTH, 50):
        pygame.draw.line(surface, (30, 41, 59), (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 50):
        pygame.draw.line(surface, (30, 41, 59), (250, y), (WIDTH, y), 1)

def main():
    state = "MENU"
    running = True
    clock = pygame.time.Clock()
    
    # Botones del Menú Principal (Solo Parabólico y Semiparabólico, centrados)
    menu_btns = [
        Button(450, 300, 300, 55, "Parabólico", SIDEBAR_COLOR, ACCENT_COLOR),
        Button(450, 380, 300, 55, "Semiparabólico", SIDEBAR_COLOR, ACCENT_COLOR)
    ]
    
    back_btn = Button(20, 680, 210, 45, "VOLVER AL MENÚ", ERROR_COLOR, (190, 18, 60))
    run_btn = Button(20, 610, 210, 55, "INICIAR", SUCCESS_COLOR, (21, 128, 61))
    
    # Inputs especializados (Solo para los modelos requeridos)
    inputs = {
        "Parabólico": [InputField(30, 150, 190, 45, "Velocidad (m/s)", "55"), InputField(30, 230, 190, 45, "Ángulo (°)", "45")],
        "Semiparabólico": [InputField(30, 150, 190, 45, "V. Horizontal", "30"), InputField(30, 230, 190, 45, "Altura (m)", "50")]
    }

    simulating = False
    has_results = False
    start_ticks = 0
    trail = []
    res_t, res_x, res_y, res_v = 0, 0, 0, 0

    while running:
        SCREEN.fill(BG_COLOR)
        m_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            
            if state == "MENU":
                for b in menu_btns:
                    b.update(m_pos)
                    if event.type == pygame.MOUSEBUTTONDOWN and b.rect.collidepoint(m_pos):
                        state = b.text
                        simulating = False
                        has_results = False
                        trail = []
            else:
                for inp in inputs[state]: inp.handle_event(event)
                back_btn.update(m_pos)
                run_btn.update(m_pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_btn.rect.collidepoint(m_pos): state = "MENU"
                    if run_btn.rect.collidepoint(m_pos):
                        simulating, has_results = True, True
                        start_ticks = pygame.time.get_ticks()
                        trail = []

        if state == "MENU":
            # Pantalla de Inicio
            title_surf = FONT_TITLE.render("PHYSICS ENGINE PRO", True, ACCENT_COLOR)
            subtitle = FONT_MAIN.render("Seleccione un modelo cinemático para iniciar la simulación", True, (148, 163, 184))
            SCREEN.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 80))
            SCREEN.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 130))
            for b in menu_btns: b.draw(SCREEN)
        else:
            # INTERFAZ DE SIMULACIÓN PROFESIONAL
            # Sidebar
            pygame.draw.rect(SCREEN, SIDEBAR_COLOR, (0, 0, 250, HEIGHT))
            pygame.draw.line(SCREEN, ACCENT_COLOR, (250, 0), (250, HEIGHT), 2)
            
            # Area de dibujo
            draw_grid(SCREEN)
            pygame.draw.line(SCREEN, (71, 85, 105), (250, 650), (WIDTH, 650), 4) # Suelo
            
            mode_title = FONT_BOLD.render(state.upper(), True, ACCENT_COLOR)
            SCREEN.blit(mode_title, (30, 40))
            
            for inp in inputs[state]: inp.draw(SCREEN)
            back_btn.draw(SCREEN)
            run_btn.draw(SCREEN)
            
            if simulating or has_results:
                t = (pygame.time.get_ticks() - start_ticks) / 1000.0 if simulating else res_t

                # Lógica Matemática Exacta
                if state == "Parabólico":
                    v0, ang = inputs[state][0].get_val(), math.radians(inputs[state][1].get_val())
                    m_x, m_y = (v0 * math.cos(ang) * t), (v0 * math.sin(ang) * t) - (0.5 * G * t**2)
                    v_inst = math.sqrt((v0 * math.cos(ang))**2 + (v0 * math.sin(ang) - G * t)**2)
                    if m_y < 0 and t > 0.1: m_y, simulating = 0, False
                elif state == "Semiparabólico":
                    vx_k, h0 = inputs[state][0].get_val(), inputs[state][1].get_val()
                    m_x, m_y = vx_k * t, h0 - (0.5 * G * t**2)
                    v_inst = math.sqrt(vx_k**2 + (G * t)**2)
                    if m_y < 0: m_y, simulating = 0, False

                if simulating:
                    res_t, res_x, res_y, res_v = t, m_x, m_y, v_inst
                    # Desplazamiento visual para que no choque con la sidebar
                    draw_x, draw_y = 300 + (m_x * SCALE), 650 - (m_y * SCALE)
                    trail.append((int(draw_x), int(draw_y)))

                # Dibujar Rastro con estilo
                if len(trail) > 1:
                    pygame.draw.lines(SCREEN, ACCENT_COLOR, False, trail, 3)

                # Dibujar Objeto (Partícula con brillo)
                obj_pos = (int(300 + (res_x * SCALE)), int(650 - (res_y * SCALE)))
                pygame.draw.circle(SCREEN, ACCENT_COLOR, obj_pos, 15, 3) # Borde
                pygame.draw.circle(SCREEN, TEXT_COLOR, obj_pos, 10)     # Centro
                
                # PANEL DE RESULTADOS ESTILO "HUD"
                res_panel = pygame.Rect(WIDTH - 320, 30, 290, 200)
                pygame.draw.rect(SCREEN, (15, 23, 42, 200), res_panel, border_radius=15)
                pygame.draw.rect(SCREEN, ACCENT_COLOR, res_panel, 2, border_radius=15)
                
                status_txt = "EN PROGRESO..." if simulating else "SISTEMA EN REPOSO"
                status_clr = ACCENT_COLOR if simulating else SUCCESS_COLOR
                SCREEN.blit(FONT_SMALL.render(status_txt, True, status_clr), (WIDTH - 305, 45))

                stats = [
                    ("TIEMPO", f"{res_t:.3f} s"),
                    ("POSICIÓN X", f"{res_x:.2f} m"),
                    ("ALTURA Y", f"{res_y:.2f} m"),
                    ("VELOCIDAD", f"{res_v:.2f} m/s")
                ]
                for i, (label, val) in enumerate(stats):
                    l_surf = FONT_SMALL.render(label, True, (148, 163, 184))
                    v_surf = FONT_BOLD.render(val, True, TEXT_COLOR)
                    SCREEN.blit(l_surf, (WIDTH - 305, 80 + i*35))
                    SCREEN.blit(v_surf, (WIDTH - 150, 75 + i*35))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()