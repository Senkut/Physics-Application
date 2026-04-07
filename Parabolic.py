import pygame
import math

# --- CONFIGURACIÓN Y FÍSICA ---
WIDTH, HEIGHT = 1200, 750
GRAVITY = 9.8
PPM = 20 
DARK_GRAY = (15, 23, 42)
ACCENT_COLOR = (45, 212, 191)
TEXT_COLOR = (241, 245, 249)

def mru_pos(x0, v, t): return x0 + v * t
def mrua_pos(x0, v0, a, t): return x0 + v0 * t + 0.5 * a * (t**2)
def mrua_vel(v0, a, t): return v0 + a * t

def world_to_screen(x, y):
    return (int(280 + (x * PPM)), int(650 - (y * PPM)))

class InputField:
    def __init__(self, x, y, w, h, label, default=""):
        self.rect = pygame.Rect(x, y, w, h); self.label = label
        self.text = default; self.active = False
    def draw(self, surf, font_label, font_text):
        color = ACCENT_COLOR if self.active else (71, 85, 105)
        pygame.draw.rect(surf, (30, 41, 59), self.rect, border_radius=5)
        pygame.draw.rect(surf, color, self.rect, 2, border_radius=5)
        surf.blit(font_label.render(self.label, True, (148, 163, 184)), (self.rect.x, self.rect.y - 22))
        surf.blit(font_text.render(self.text, True, TEXT_COLOR), (self.rect.x + 10, self.rect.y + 8))
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
    
    inputs = [InputField(30, 150, 190, 45, "VELOCIDAD (m/s)", "40"), 
              InputField(30, 230, 190, 45, "ÁNGULO (°)", "45")]
    
    btn_rect = pygame.Rect(30, 600, 190, 50)
    simulating = False
    t, px, py, v_inst = 0, 0, 0, 0
    trail = []

    while True:
        dt = clock.tick(60) / 1000
        screen.fill(DARK_GRAY)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
            for inp in inputs: inp.handle(event)
            if event.type == pygame.MOUSEBUTTONDOWN and btn_rect.collidepoint(event.pos):
                simulating, t, trail = True, 0, []

        # Sidebar e Inputs
        pygame.draw.rect(screen, (30, 41, 59), (0, 0, 250, HEIGHT))
        for inp in inputs: inp.draw(screen, f_small, f_mid)
        pygame.draw.rect(screen, (34, 197, 94), btn_rect, border_radius=8)
        screen.blit(f_bold.render("LANZAR", True, TEXT_COLOR), (85, 610))

        if simulating or t > 0:
            if simulating:
                t += dt
                v0, ang = inputs[0].get_val(), math.radians(inputs[1].get_val())
                vx, vy0 = v0 * math.cos(ang), v0 * math.sin(ang)
                
                px = mru_pos(0, vx, t)
                py = mrua_pos(0, vy0, -GRAVITY, t)
                
                # Velocidad instantánea usando mrua_vel
                curr_vy = mrua_vel(vy0, -GRAVITY, t)
                v_inst = math.sqrt(vx**2 + curr_vy**2)

                if py <= 0 and t > 0.1: py, simulating = 0, False
                trail.append(world_to_screen(px, py))

            if len(trail) > 1: pygame.draw.lines(screen, ACCENT_COLOR, False, trail, 2)
            pygame.draw.circle(screen, TEXT_COLOR, world_to_screen(px, py), 12)

            # --- PANEL DE RESULTADOS (HUD) ---
            panel = pygame.Rect(WIDTH - 280, 20, 260, 180)
            pygame.draw.rect(screen, (30, 41, 59, 200), panel, border_radius=10)
            pygame.draw.rect(screen, ACCENT_COLOR, panel, 2, border_radius=10)
            
            headers = [("TIEMPO:", f"{t:.2f} s"), ("DISTANCIA X:", f"{px:.2f} m"), 
                       ("ALTURA Y:", f"{py:.2f} m"), ("VELOCIDAD:", f"{v_inst:.2f} m/s")]
            
            for i, (lab, val) in enumerate(headers):
                screen.blit(f_small.render(lab, True, (148, 163, 184)), (WIDTH - 265, 40 + i*35))
                screen.blit(f_bold.render(val, True, ACCENT_COLOR), (WIDTH - 140, 35 + i*35))

        pygame.display.flip()

if __name__ == "__main__": main()
