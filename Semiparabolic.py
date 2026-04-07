import pygame
import math

# --- TUS CONSTANTES INTEGRADAS ---
WIDTH, HEIGHT = 1200, 800
GRAVITY = 9.8
PPM = 10  # Reducido para que alturas grandes (como 50m) quepan en pantalla
DARK_GRAY = (15, 23, 42)
ACCENT_COLOR = (251, 146, 60) 
TEXT_COLOR = (241, 245, 249)

# --- TUS FÓRMULAS ---
def mru_pos(x0, v, t): return x0 + v * t
def mrua_pos(x0, v0, a, t): return x0 + v0 * t + 0.5 * a * (t**2)
def mrua_vel(v0, a, t): return v0 + a * t

def world_to_screen(x, y):
    # Ajustamos el 'suelo' a la posición 700 para dar más espacio arriba
    return (int(280 + (x * PPM)), int(700 - (y * PPM)))

class InputField:
    def __init__(self, x, y, w, h, label, default=""):
        self.rect = pygame.Rect(x, y, w, h); self.label = label
        self.text = default; self.active = False
    def draw(self, surf, f_s, f_m):
        color = ACCENT_COLOR if self.active else (71, 85, 105)
        pygame.draw.rect(surf, (30, 41, 59), self.rect, border_radius=5)
        pygame.draw.rect(surf, color, self.rect, 2, border_radius=5)
        surf.blit(f_s.render(self.label, True, (148, 163, 184)), (self.rect.x, self.rect.y - 22))
        surf.blit(f_m.render(self.text, True, TEXT_COLOR), (self.rect.x + 10, self.rect.y + 8))
    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN: self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE: self.text = self.text[:-1]
            elif event.unicode in "0123456789.": self.text += event.unicode
    def get_val(self):
        try: return float(self.text)
        except: return 0.0

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    f_small = pygame.font.SysFont("Segoe UI", 16)
    f_mid = pygame.font.SysFont("Segoe UI", 20)
    f_bold = pygame.font.SysFont("Segoe UI", 22, bold=True)
    
    # Inputs específicos para SEMIPARABÓLICO (Velocidad horizontal y Altura inicial)
    inputs = [InputField(30, 150, 190, 45, "V. HORIZONTAL (m/s)", "20"), 
              InputField(30, 230, 190, 45, "ALTURA INICIAL (m)", "40")]
    
    btn_rect = pygame.Rect(30, 600, 190, 50)
    simulating = False
    t, res_x, res_y, res_v = 0, 0, 0, 0
    trail = []

    while True:
        dt = clock.tick(60) / 1000
        screen.fill(DARK_GRAY)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
            for inp in inputs: inp.handle(event)
            if event.type == pygame.MOUSEBUTTONDOWN and btn_rect.collidepoint(event.pos):
                simulating, t, trail = True, 0, []

        # Dibujar Interfaz Lateral
        pygame.draw.rect(screen, (30, 41, 59), (0, 0, 250, HEIGHT))
        for inp in inputs: inp.draw(screen, f_small, f_mid)
        pygame.draw.rect(screen, (34, 197, 94), btn_rect, border_radius=8)
        screen.blit(f_bold.render("LANZAR", True, TEXT_COLOR), (85, 610))

        # Suelo de referencia
        pygame.draw.line(screen, (71, 85, 105), (250, 700), (WIDTH, 700), 2)

        if simulating or t > 0:
            if simulating:
                t += dt
                v_horiz = inputs[0].get_val()
                h_inicial = inputs[1].get_val()
                
                # --- LÓGICA FÍSICA ---
                res_x = mru_pos(0, v_horiz, t)
                # En semiparabólico, v0y es 0. Empezamos en h_inicial.
                res_y = mrua_pos(h_inicial, 0, -GRAVITY, t) 
                
                # Velocidad: vx es constante, vy aumenta por gravedad
                vy_actual = mrua_vel(0, -GRAVITY, t)
                res_v = math.sqrt(v_horiz**2 + vy_actual**2)

                if res_y <= 0: 
                    res_y = 0
                    simulating = False
                
                trail.append(world_to_screen(res_x, res_y))

            # Dibujo de trayectoria y partícula
            if len(trail) > 1: pygame.draw.lines(screen, ACCENT_COLOR, False, trail, 3)
            pos_pantalla = world_to_screen(res_x, res_y)
            pygame.draw.circle(screen, (255, 255, 255), pos_pantalla, 12)

            # --- PANEL DE RESULTADOS (Basado en tu imagen de VS Code) ---
            panel = pygame.Rect(WIDTH - 300, 30, 270, 200)
            pygame.draw.rect(screen, (30, 41, 59, 220), panel, border_radius=12)
            pygame.draw.rect(screen, ACCENT_COLOR, panel, 2, border_radius=12)
            
            stats = [
                ("TIEMPO", f"{t:.3f} s"),
                ("POSICIÓN X", f"{res_x:.2f} m"),
                ("ALTURA Y", f"{res_y:.2f} m"),
                ("VELOCIDAD", f"{res_v:.2f} m/s")
            ]
            
            for i, (label, val) in enumerate(stats):
                l_surf = f_small.render(label, True, (148, 163, 184))
                v_surf = f_bold.render(val, True, ACCENT_COLOR)
                screen.blit(l_surf, (WIDTH - 280, 55 + i * 40))
                screen.blit(v_surf, (WIDTH - 160, 50 + i * 40))

        pygame.display.flip()

if __name__ == "__main__":
    main()