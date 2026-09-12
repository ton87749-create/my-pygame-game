import pygame
import random
import sys
import math
import time

pygame.init()

# Включаем полный экран
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

clock = pygame.time.Clock()

# --- ЦВЕТА ---
SKY_BLUE = (100, 150, 200)
WOOD_BROWN = (120, 70, 40)
WOOD_DARK = (70, 35, 20)
BRICK_RED = (140, 45, 35)
PAVEMENT_GRAY = (90, 85, 85)
PAVEMENT_DARK = (55, 50, 50)

ROLLTON_RED = (210, 20, 25)
ROLLTON_YELLOW = (255, 210, 0)
ROLLTON_ORANGE = (255, 100, 0)
DARK_RED = (120, 10, 15)

BIGBON_BLACK = (25, 25, 30)
BIGBON_RED = (200, 30, 30)
BIGBON_GREEN = (30, 160, 70)
BRIGHT_RED = (255, 10, 10)
BRIGHT_GREEN = (30, 230, 70)

GROUND_Y = int(HEIGHT * 0.78)

# --- ШРИФТЫ ---
font_hud = pygame.font.SysFont("impact", int(WIDTH * 0.042))
font_fps = pygame.font.SysFont("arial", int(WIDTH * 0.025), bold=True)
font_big = pygame.font.SysFont("impact", int(WIDTH * 0.08))
font_btn = pygame.font.SysFont("impact", int(WIDTH * 0.05))
font_hit_text = pygame.font.SysFont("impact", int(WIDTH * 0.085), bold=True)
font_logo = pygame.font.SysFont("arial", 26, bold=True)
font_sub = pygame.font.SysFont("impact", 26)
font_wok = pygame.font.SysFont("impact", 38)
font_bb = pygame.font.SysFont("arial", 20, bold=True)
font_hp_num = pygame.font.SysFont("impact", 20)
font_poster = pygame.font.SysFont("impact", int(WIDTH * 0.055), bold=True)

# Предварительный рендер частых текстов
txt_poster = font_poster.render("BIGBON VS ROLLTON 🔥", True, ROLLTON_YELLOW)
txt_rollton_logo = font_logo.render("Роллтон", True, ROLLTON_RED)
txt_rollton_fire = font_sub.render("С ОГОНЬКОМ", True, ROLLTON_YELLOW)
txt_wok_title = font_wok.render("WOK", True, (255, 255, 255))
txt_bb_title = font_bb.render("BigBon", True, (255, 255, 255))

txt_title_menu = font_big.render("ВЫБОР СЛОЖНОСТИ", True, ROLLTON_YELLOW)
txt_title_pause = font_big.render("ПАУЗА", True, ROLLTON_YELLOW)
txt_title_gameover = font_big.render("ПЕРЕВАРИЛ!", True, ROLLTON_RED)

sign_w, sign_h = int(WIDTH * 0.7), int(HEIGHT * 0.16)

# ==========================================
# ЗАПЕКАНИЕ ФОНА (GPU READY)
# ==========================================
def create_static_background(with_poster=True):
    bg_surface = pygame.Surface((WIDTH, HEIGHT)).convert()
    bg_surface.fill(SKY_BLUE)
    
    building_height = int(HEIGHT * 0.48)
    pygame.draw.rect(bg_surface, BRICK_RED, (0, 0, WIDTH, building_height))
    for y in range(0, building_height, 40):
        pygame.draw.line(bg_surface, (85, 25, 18), (0, y), (WIDTH, y), 2)
        
    if with_poster:
        poster_x = (WIDTH - sign_w) // 2
        poster_y = int(HEIGHT * 0.14)
        pygame.draw.rect(bg_surface, (20, 20, 25), (poster_x, poster_y, sign_w, sign_h), border_radius=18)
        pygame.draw.rect(bg_surface, BRIGHT_RED, (poster_x, poster_y, sign_w, sign_h), width=6, border_radius=18)
        pygame.draw.rect(bg_surface, ROLLTON_ORANGE, (poster_x + 4, poster_y + 4, sign_w - 8, sign_h - 8), width=3, border_radius=14)
        bg_surface.blit(txt_poster, (poster_x + (sign_w - txt_poster.get_width()) // 2, poster_y + (sign_h - txt_poster.get_height()) // 2))

    fence_y = building_height
    fence_h = int(HEIGHT * 0.10)
    for x in range(0, WIDTH, 65):
        pygame.draw.rect(bg_surface, WOOD_BROWN, (x, fence_y, 52, fence_h))
        pygame.draw.polygon(bg_surface, WOOD_DARK, [(x, fence_y), (x + 26, fence_y - 22), (x + 52, fence_y)])
    
    pygame.draw.rect(bg_surface, PAVEMENT_GRAY, (0, fence_y + fence_h, WIDTH, HEIGHT - (fence_y + fence_h)))
    pygame.draw.line(bg_surface, (30, 30, 30), (0, fence_y + fence_h), (WIDTH, fence_y + fence_h), 6)
    
    for y in range(fence_y + fence_h + 40, HEIGHT, 70):
        pygame.draw.line(bg_surface, PAVEMENT_DARK, (0, y), (WIDTH, y), 3)

    return bg_surface

# Генерируем два готовых фона один раз в памяти
BG_GAME = create_static_background(with_poster=True)
BG_MENU = create_static_background(with_poster=False)

def draw_rollton_pack(x, y, facing, shoot_timer, idle_frame, hp, max_hp):
    bounce = math.sin(idle_frame * 0.12) * 6 if shoot_timer == 0 else 0
    cur_y = y + bounce
    dir_m = 1 if facing == "right" else -1

    pygame.draw.rect(screen, DARK_RED, (x - 38, cur_y - 20, 26, 30), border_radius=6)
    pygame.draw.rect(screen, DARK_RED, (x + 12, cur_y - 20, 26, 30), border_radius=6)

    pack_w, pack_h = 160, 210
    pack_x = x - pack_w // 2
    pack_y = cur_y - 220

    pygame.draw.rect(screen, ROLLTON_RED, (pack_x, pack_y, pack_w, pack_h), border_radius=24)
    pygame.draw.rect(screen, (255, 80, 80), (pack_x + 6, pack_y + 6, pack_w - 12, pack_h - 12), width=5, border_radius=20)

    for f_x in range(pack_x + 12, pack_x + pack_w - 12, 22):
        pygame.draw.polygon(screen, ROLLTON_ORANGE, [(f_x - 11, pack_y + pack_h - 8), (f_x + 11, pack_y + pack_h - 8), (f_x, pack_y + pack_h - 38)])
        pygame.draw.polygon(screen, ROLLTON_YELLOW, [(f_x - 5, pack_y + pack_h - 8), (f_x + 5, pack_y + pack_h - 8), (f_x, pack_y + pack_h - 22)])

    pygame.draw.ellipse(screen, ROLLTON_YELLOW, (x - 58, pack_y + 28, 116, 50))
    screen.blit(txt_rollton_logo, (x - txt_rollton_logo.get_width() // 2, pack_y + 38))
    screen.blit(txt_rollton_fire, (x - txt_rollton_fire.get_width() // 2, pack_y + 92))

    gun_x = x + (82 * dir_m)
    gun_y = pack_y + 125
    pygame.draw.rect(screen, (220, 160, 20), (gun_x - 22, gun_y - 12, 44, 24), border_radius=5)
    pygame.draw.rect(screen, (220, 160, 20), (gun_x + (10 * dir_m) - 7, gun_y - 5, 16, 32), border_radius=5)

    if shoot_timer > 0:
        flash_x = gun_x + (40 * dir_m)
        pygame.draw.circle(screen, ROLLTON_ORANGE, (flash_x, gun_y), 35)
        pygame.draw.circle(screen, ROLLTON_YELLOW, (flash_x, gun_y), 18)

    hp_w = 140
    hp_x = x - hp_w // 2
    hp_y = pack_y - 38
    pygame.draw.rect(screen, (30, 30, 30), (hp_x - 4, hp_y - 4, hp_w + 8, 22), border_radius=8)
    pygame.draw.rect(screen, (80, 10, 10), (hp_x, hp_y, hp_w, 14), border_radius=6)
    if hp > 0:
        pygame.draw.rect(screen, (0, 230, 70), (hp_x, hp_y, int(hp_w * (hp / max_hp)), 14), border_radius=6)
    
    txt_hp = font_hp_num.render(f"HP {hp}/{max_hp}", True, (255, 255, 255))
    screen.blit(txt_hp, (x - txt_hp.get_width() // 2, hp_y - 20))

def draw_bigbon_wok(x, y, variant, anim_frame, hp, max_hp):
    bounce = math.cos(anim_frame * 0.15) * 4
    cur_y = y + bounce
    accent_color = BIGBON_RED if variant == "red" else BIGBON_GREEN

    pygame.draw.rect(screen, (15, 15, 15), (x - 32, cur_y - 18, 22, 28), border_radius=6)
    pygame.draw.rect(screen, (15, 15, 15), (x + 10, cur_y - 18, 22, 28), border_radius=6)

    top_w, bot_w, h = 146, 102, 170
    top_y = cur_y - 185
    bot_y = top_y + h

    points = [
        (x - top_w // 2, top_y),
        (x + top_w // 2, top_y),
        (x + bot_w // 2, bot_y),
        (x - bot_w // 2, bot_y)
    ]
    pygame.draw.polygon(screen, BIGBON_BLACK, points)
    pygame.draw.polygon(screen, (60, 60, 65), points, width=5)

    pygame.draw.ellipse(screen, (40, 40, 45), (x - top_w // 2, top_y - 18, top_w, 36))
    pygame.draw.ellipse(screen, accent_color, (x - top_w // 2 + 10, top_y - 13, top_w - 20, 26), width=5)

    pygame.draw.rect(screen, accent_color, (x - 50, top_y + 90, 100, 38), border_radius=10)

    screen.blit(txt_wok_title, (x - txt_wok_title.get_width() // 2, top_y + 40))
    screen.blit(txt_bb_title, (x - txt_bb_title.get_width() // 2, top_y + 15))

    bar_w = 110
    bar_x = x - bar_w // 2
    bar_y = top_y - 32
    pygame.draw.rect(screen, (40, 0, 0), (bar_x, bar_y, bar_w, 12), border_radius=5)
    if hp > 0:
        pygame.draw.rect(screen, (50, 220, 50), (bar_x, bar_y, int(bar_w * (hp / max_hp)), 12), border_radius=5)
    pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_w, 12), width=2, border_radius=5)

# --- ЧАСТИЦА С ДИНАМИЧЕСКИМ ЦВЕТОМ ---
class HitTextParticle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y - 30
        self.vy = -120
        self.text_str = random.choice(["КОЧ!", "ГАЛДА!"])
        self.life = 1.0
        self.color = color

    def update(self, dt):
        self.y += self.vy * dt
        self.life -= dt

    def draw(self):
        if self.life > 0:
            txt_shadow = font_hit_text.render(self.text_str, True, (0, 0, 0))
            txt = font_hit_text.render(self.text_str, True, self.color)
            tx = self.x - txt.get_width() // 2
            ty = self.y - txt.get_height() // 2
            screen.blit(txt_shadow, (tx + 3, ty + 3))
            screen.blit(txt, (tx, ty))

class ChiliBullet:
    def __init__(self, x, y, direction, is_mega=False):
        self.x = x
        self.y = y
        self.dir = direction
        self.is_mega = is_mega
        self.speed = WIDTH * (4.2 if is_mega else 3.5)
        self.damage = 100 if is_mega else 35

    def update(self, dt):
        self.x += self.dir * self.speed * dt

    def draw(self):
        scale = 2.0 if self.is_mega else 1.3
        w, h = int(36 * scale), int(18 * scale)
        color = (255, 20, 20) if self.is_mega else ROLLTON_RED
        
        pygame.draw.ellipse(screen, color, (self.x - w//2, self.y - h//2, w, h))
        tail_x = self.x - (int(20 * scale) * self.dir)
        pygame.draw.circle(screen, ROLLTON_ORANGE, (tail_x, self.y), int(8 * scale))

class BigBonEnemy:
    def __init__(self, side, speed_mult, hp_val):
        self.side = side
        self.x = -100 if side == "left" else WIDTH + 100
        self.y = GROUND_Y
        self.speed = random.uniform(WIDTH * 0.18, WIDTH * 0.28) * speed_mult
        self.variant = random.choice(["red", "green"])
        self.anim_frame = random.randint(0, 100)
        self.max_hp = hp_val
        self.hp = hp_val

    def update(self, dt):
        self.anim_frame += 1
        if self.side == "left":
            self.x += self.speed * dt
        else:
            self.x -= self.speed * dt

# Увеличено здоровье врагов (enemy_hp)
DIFFICULTIES = {
    "EASY": {"speed": 0.65, "hp": 100, "spawn": 1.8, "enemy_hp": 160, "name": "ЛЕГКО"},    # ~5 пулей
    "NORMAL": {"speed": 0.90, "hp": 100, "spawn": 1.4, "enemy_hp": 240, "name": "СРЕДНЕ"},   # ~7 пулей
    "HARD": {"speed": 1.15, "hp": 100, "spawn": 1.0, "enemy_hp": 320, "name": "СЛОЖНО"}    # ~10 пулей
}

current_diff = "NORMAL"
state = "MENU"

enemies = []
bullets = []
particles = []
spawn_timer = -1.0

player_x = WIDTH // 2
player_y = GROUND_Y
max_player_hp = 100
player_hp = 100
facing = "right"
shoot_timer = 0
score = 0
combo = 0
idle_frame = 0

last_time = time.time()

def start_game(diff_key):
    global current_diff, state, enemies, bullets, particles, spawn_timer, player_hp, max_player_hp, score, combo
    current_diff = diff_key
    cfg = DIFFICULTIES[diff_key]
    max_player_hp = 100
    player_hp = max_player_hp
    score = 0
    combo = 0
    spawn_timer = -1.0
    enemies.clear()
    bullets.clear()
    particles.clear()
    state = "GAME"

running = True
while running:
    current_time = time.time()
    dt = min(current_time - last_time, 0.05)
    last_time = current_time
    
    clock.tick(120)
    fps_val = int(clock.get_fps())

    idle_frame += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if state == "MENU":
                btn_w, btn_h = int(WIDTH * 0.7), int(HEIGHT * 0.1)
                cx = (WIDTH - btn_w) // 2
                
                if cx <= mx <= cx + btn_w:
                    if int(HEIGHT * 0.4) <= my <= int(HEIGHT * 0.4) + btn_h:
                        start_game("EASY")
                    elif int(HEIGHT * 0.53) <= my <= int(HEIGHT * 0.53) + btn_h:
                        start_game("NORMAL")
                    elif int(HEIGHT * 0.66) <= my <= int(HEIGHT * 0.66) + btn_h:
                        start_game("HARD")

            elif state == "GAME":
                if mx > WIDTH - 90 and my < 90:
                    state = "PAUSE"
                else:
                    shoot_timer = 0.08
                    is_mega = (combo > 0 and combo % 5 == 0)
                    
                    if mx < WIDTH // 2:
                        facing = "left"
                        bullets.append(ChiliBullet(player_x - 70, player_y - 100, -1, is_mega))
                    else:
                        facing = "right"
                        bullets.append(ChiliBullet(player_x + 70, player_y - 100, 1, is_mega))

            elif state == "PAUSE":
                btn_w, btn_h = int(WIDTH * 0.6), int(HEIGHT * 0.08)
                cx = (WIDTH - btn_w) // 2
                
                if cx <= mx <= cx + btn_w:
                    if int(HEIGHT * 0.42) <= my <= int(HEIGHT * 0.42) + btn_h:
                        current_diff = "EASY"
                        state = "GAME"
                    elif int(HEIGHT * 0.52) <= my <= int(HEIGHT * 0.52) + btn_h:
                        current_diff = "NORMAL"
                        state = "GAME"
                    elif int(HEIGHT * 0.62) <= my <= int(HEIGHT * 0.62) + btn_h:
                        current_diff = "HARD"
                        state = "GAME"

            elif state == "GAMEOVER":
                state = "MENU"

    if state == "GAME":
        screen.blit(BG_GAME, (0, 0))
        cfg = DIFFICULTIES[current_diff]
        
        spawn_timer += dt
        spawn_interval = max(0.65, cfg["spawn"] - (score / 5000.0))
        if spawn_timer >= spawn_interval:
            enemies.append(BigBonEnemy(random.choice(["left", "right"]), cfg["speed"], cfg["enemy_hp"]))
            spawn_timer = 0

        for bullet in bullets[:]:
            bullet.update(dt)
            bullet.draw()
            
            if bullet.x < -80 or bullet.x > WIDTH + 80:
                bullets.remove(bullet)
                continue

            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(enemy.x - 75, enemy.y - 185, 150, 185)
                if enemy_rect.collidepoint(bullet.x, bullet.y):
                    enemy.hp -= bullet.damage
                    
                    # Цвет надписи зависит от типа врага
                    hit_color = BRIGHT_GREEN if enemy.variant == "green" else BRIGHT_RED
                    particles.append(HitTextParticle(enemy.x, enemy.y - 100, hit_color))

                    if bullet in bullets and not bullet.is_mega:
                        bullets.remove(bullet)
                    
                    if enemy.hp <= 0:
                        if enemy in enemies:
                            enemies.remove(enemy)
                        score += 100
                        combo += 1
                    break

        for p in particles[:]:
            p.update(dt)
            p.draw()
            if p.life <= 0:
                particles.remove(p)

        for enemy in enemies[:]:
            enemy.update(dt)
            draw_bigbon_wok(enemy.x, enemy.y, enemy.variant, enemy.anim_frame, enemy.hp, enemy.max_hp)
            
            if abs(enemy.x - player_x) < 95:
                player_hp -= 25
                enemies.remove(enemy)
                combo = 0
                if player_hp <= 0:
                    state = "GAMEOVER"

        if shoot_timer > 0:
            shoot_timer -= dt

        draw_rollton_pack(player_x, player_y, facing, 1 if shoot_timer > 0 else 0, idle_frame, player_hp, max_player_hp)

        # HUD
        txt_score = font_hud.render(f"SCORE: {score}", True, ROLLTON_YELLOW)
        score_bg_w = txt_score.get_width() + 30
        pygame.draw.rect(screen, (20, 20, 25), (20, 20, score_bg_w, 55), border_radius=12)
        pygame.draw.rect(screen, BRIGHT_RED, (20, 20, score_bg_w, 55), width=3, border_radius=12)
        screen.blit(txt_score, (35, 22))

        txt_fps_disp = font_fps.render(f"FPS: {fps_val} | СЛОЖНОСТЬ: {cfg['name']}", True, (0, 255, 120))
        fps_bg_w = txt_fps_disp.get_width() + 20
        pygame.draw.rect(screen, (15, 15, 20), (20, HEIGHT - 50, fps_bg_w, 35), border_radius=8)
        screen.blit(txt_fps_disp, (30, HEIGHT - 45))

        if combo > 1:
            txt_combo = font_hud.render(f"COMBO x{combo}!", True, ROLLTON_ORANGE)
            screen.blit(txt_combo, (20, 85))

        pygame.draw.rect(screen, (40, 40, 40), (WIDTH - 80, 20, 60, 60), border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), (WIDTH - 65, 34, 11, 32))
        pygame.draw.rect(screen, (255, 255, 255), (WIDTH - 45, 34, 11, 32))

    elif state == "MENU":
        screen.blit(BG_MENU, (0, 0))
        screen.blit(txt_title_menu, ((WIDTH - txt_title_menu.get_width()) // 2, int(HEIGHT * 0.2)))

        btn_w, btn_h = int(WIDTH * 0.7), int(HEIGHT * 0.1)
        cx = (WIDTH - btn_w) // 2

        for i, (key, diff) in enumerate(DIFFICULTIES.items()):
            btn_y = int(HEIGHT * (0.4 + i * 0.13))
            color = (50, 180, 50) if key == "EASY" else ((220, 150, 0) if key == "NORMAL" else (200, 40, 40))
            
            pygame.draw.rect(screen, color, (cx, btn_y, btn_w, btn_h), border_radius=15)
            pygame.draw.rect(screen, (255, 255, 255), (cx, btn_y, btn_w, btn_h), width=3, border_radius=15)
            
            t = font_btn.render(diff["name"], True, (255, 255, 255))
            screen.blit(t, (cx + (btn_w - t.get_width()) // 2, btn_y + (btn_h - t.get_height()) // 2))

    elif state == "PAUSE":
        screen.blit(BG_MENU, (0, 0))
        screen.blit(txt_title_pause, ((WIDTH - txt_title_pause.get_width()) // 2, int(HEIGHT * 0.2)))

        btn_w, btn_h = int(WIDTH * 0.6), int(HEIGHT * 0.08)
        cx = (WIDTH - btn_w) // 2

        for i, (key, diff) in enumerate(DIFFICULTIES.items()):
            btn_y = int(HEIGHT * (0.42 + i * 0.10))
            is_active = (current_diff == key)
            color = (50, 180, 50) if key == "EASY" else ((220, 150, 0) if key == "NORMAL" else (200, 40, 40))
            
            pygame.draw.rect(screen, color, (cx, btn_y, btn_w, btn_h), border_radius=12)
            border_c = ROLLTON_YELLOW if is_active else (255, 255, 255)
            pygame.draw.rect(screen, border_c, (cx, btn_y, btn_w, btn_h), width=(5 if is_active else 2), border_radius=12)
            
            t = font_btn.render(diff["name"] + ("  ✓" if is_active else ""), True, (255, 255, 255))
            screen.blit(t, (cx + (btn_w - t.get_width()) // 2, btn_y + (btn_h - t.get_height()) // 2))

    elif state == "GAMEOVER":
        screen.blit(BG_MENU, (0, 0))
        txt_res = font_hud.render(f"Счёт: {score}", True, ROLLTON_YELLOW)
        txt_sub = font_hud.render("Тапни для выхода в меню", True, (255, 255, 255))
        
        screen.blit(txt_title_gameover, ((WIDTH - txt_title_gameover.get_width()) // 2, HEIGHT // 2 - 100))
        screen.blit(txt_res, ((WIDTH - txt_res.get_width()) // 2, HEIGHT // 2))
        screen.blit(txt_sub, ((WIDTH - txt_sub.get_width()) // 2, HEIGHT // 2 + 70))

    pygame.display.flip()

pygame.quit()
sys.exit()
