import pygame
import sys
import math
import random

# === 1. Инициализация Pygame ===
pygame.init()

# === 2. Настройки экрана ===
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Черный мир - Дробаш и Катана")

# === 3. Цвета (RGB) ===
BLACK = (0, 0, 0)       # Фон
WHITE = (255, 255, 255) # Стены, игрок, оружие
YELLOW = (255, 255, 0)  # Пули
SPARK_COLOR = (255, 200, 100)  # Цвет искр
GRAY = (100, 100, 100)  # Серый для интерфейса
DARK_GRAY = (50, 50, 50) # Темно-серый для фона интерфейса
RED = (255, 50, 50)     # Красный для индикации перезарядки
LIGHT_GRAY = (150, 150, 150)  # Светло-серый для интерфейса

# === 4. Настройки стены (прямоугольник) ===
WALL_OFFSET = 50
wall_rect = pygame.Rect(
    WALL_OFFSET,
    WALL_OFFSET,
    SCREEN_WIDTH - 2 * WALL_OFFSET,
    SCREEN_HEIGHT - 2 * WALL_OFFSET
)

# === 5. Настройки игрока (круг) ===
PLAYER_RADIUS = 15
PLAYER_SPEED = 5
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2

# === 6. Типы оружия ===
WEAPON_SHOTGUN = 0
WEAPON_KATANA = 1
current_weapon = WEAPON_SHOTGUN  # По умолчанию дробаш

# === 7. Настройки дробаша (обрез) ===
SHOTGUN_LENGTH = 12
SHOTGUN_WIDTH = 3
BARREL_SPACING = 2
GUN_FORWARD_OFFSET = 5

# Переменные для дробаша
current_ammo = 2
MAX_AMMO = 2
RELOAD_TIME = 60
reload_timer = 0
is_reloading = False

# === 8. Настройки катаны ===
KATANA_LENGTH = 40       # Длина катаны
KATANA_WIDTH = 4         # Толщина катаны
KATANA_ANGLE = 45        # Угол наклона на спине (в градусах)

# Переменные для катаны
is_attacking = False
attack_timer = 0
ATTACK_DURATION = 15      # Длительность удара в кадрах
ATTACK_COOLDOWN = 30      # Перезарядка удара
attack_cooldown_timer = 0
attack_angle = 0          # Текущий угол удара
SWING_ANGLE = 120         # Угол размаха (чуть меньше 180)

# === 9. Класс для пули ===
class Bullet:
    def __init__(self, x, y, angle, speed=15, max_distance=300):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.max_distance = max_distance
        self.distance_traveled = 0
        self.active = True
        self.radius = 3

    def update(self):
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed

        self.x += dx
        self.y += dy
        self.distance_traveled += self.speed

        if self.distance_traveled >= self.max_distance:
            self.active = False

        bullet_rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                  self.radius * 2, self.radius * 2)
        if not wall_rect.contains(bullet_rect):
            self.active = False
            return True
        return False

    def draw(self, screen, camera):
        bullet_pos = camera.apply_point(self.x, self.y)
        pygame.draw.circle(screen, YELLOW, (int(bullet_pos[0]), int(bullet_pos[1])), self.radius)

# === 10. Класс для искры ===
class Spark:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle + random.uniform(-math.pi/2, math.pi/2)
        self.speed = random.uniform(2, 5)
        self.life = random.randint(15, 30)
        self.max_life = self.life
        self.size = random.randint(1, 3)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.life -= 1
        self.speed *= 0.95
        return self.life <= 0

    def draw(self, screen, camera):
        if self.life > 0:
            pos = camera.apply_point(self.x, self.y)
            alpha = int(255 * (self.life / self.max_life))
            spark_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(spark_surface, (*SPARK_COLOR, alpha),
                             (self.size, self.size), self.size)
            screen.blit(spark_surface, (int(pos[0] - self.size), int(pos[1] - self.size)))

# === 11. Класс для камеры ===
class SmoothCamera:
    def __init__(self, width, height, smoothness=0.1):
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.smoothness = smoothness

        self.current_x = 0
        self.current_y = 0
        self.target_x = 0
        self.target_y = 0

    def apply(self, entity_rect):
        return entity_rect.move(self.current_x, self.current_y)

    def apply_point(self, x, y):
        return (x + self.current_x, y + self.current_y)

    def update(self, target_x, target_y):
        self.target_x = -target_x + self.width // 2
        self.target_y = -target_y + self.height // 2

        self.current_x += (self.target_x - self.current_x) * self.smoothness
        self.current_y += (self.target_y - self.current_y) * self.smoothness

        self.camera_rect.x = self.current_x
        self.camera_rect.y = self.current_y

camera = SmoothCamera(SCREEN_WIDTH, SCREEN_HEIGHT, smoothness=0.08)

# === 12. Функция для проверки столкновений ===
def can_move_to(new_x, new_y):
    new_player_rect = pygame.Rect(
        new_x - PLAYER_RADIUS,
        new_y - PLAYER_RADIUS,
        PLAYER_RADIUS * 2,
        PLAYER_RADIUS * 2
    )
    return wall_rect.contains(new_player_rect)

# === 13. Функция для стрельбы из дробаша ===
def shoot_shotgun():
    global current_ammo, reload_timer, is_reloading

    if current_ammo > 0 and reload_timer <= 0 and not is_reloading:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_mouse_x = mouse_x - camera.current_x
        world_mouse_y = mouse_y - camera.current_y

        dx = world_mouse_x - player_x
        dy = world_mouse_y - player_y
        angle = math.atan2(dy, dx)

        right_angle = angle + math.pi / 2

        gun_base_x = player_x + math.cos(angle) * GUN_FORWARD_OFFSET + math.cos(right_angle) * PLAYER_RADIUS
        gun_base_y = player_y + math.sin(angle) * GUN_FORWARD_OFFSET + math.sin(right_angle) * PLAYER_RADIUS

        for i in [-1, 1]:
            offset_x = math.cos(right_angle) * (BARREL_SPACING + SHOTGUN_WIDTH) / 2 * i
            offset_y = math.sin(right_angle) * (BARREL_SPACING + SHOTGUN_WIDTH) / 2 * i

            bullet_x = gun_base_x + offset_x + math.cos(angle) * SHOTGUN_LENGTH
            bullet_y = gun_base_y + offset_y + math.sin(angle) * SHOTGUN_LENGTH

            bullets.append(Bullet(bullet_x, bullet_y, angle))

        current_ammo -= 1

        if current_ammo == 0:
            reload_timer = RELOAD_TIME
            is_reloading = True

# === 14. Функция для удара катаной ===
def katana_attack():
    global is_attacking, attack_timer, attack_cooldown_timer, attack_angle

    if not is_attacking and attack_cooldown_timer <= 0:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_mouse_x = mouse_x - camera.current_x
        world_mouse_y = mouse_y - camera.current_y

        dx = world_mouse_x - player_x
        dy = world_mouse_y - player_y
        target_angle = math.atan2(dy, dx)

        # Начинаем удар
        is_attacking = True
        attack_timer = ATTACK_DURATION
        attack_cooldown_timer = ATTACK_COOLDOWN

        # Начальный угол удара (смещаем влево от цели)
        attack_angle = target_angle - math.radians(SWING_ANGLE / 2)

        # Здесь можно добавить проверку попаданий по врагам
        # (пока просто эффект)

# === 15. Функция для перезарядки дробаша ===
def reload_shotgun():
    global reload_timer, is_reloading
    if current_ammo < MAX_AMMO and reload_timer <= 0 and not is_reloading:
        reload_timer = RELOAD_TIME
        is_reloading = True

# === 16. Функция для отрисовки пиксельного текста ===
def draw_pixel_text(screen, text, x, y, color, size=2):
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, color)
    scaled_surface = pygame.transform.scale(text_surface,
                                          (text_surface.get_width() * size,
                                           text_surface.get_height() * size))
    screen.blit(scaled_surface, (x, y))

# === 17. Функция для отрисовки интерфейса оружия ===
def draw_weapon_ui(screen):
    # Позиция интерфейса (правый верхний угол)
    margin = 20
    ui_width = 160
    ui_height = 60
    ui_x = SCREEN_WIDTH - ui_width - margin
    ui_y = margin

    # Фон интерфейса (полупрозрачный черный)
    ui_surface = pygame.Surface((ui_width, ui_height), pygame.SRCALPHA)
    ui_surface.fill((0, 0, 0, 200))
    screen.blit(ui_surface, (ui_x, ui_y))

    # Рамка интерфейса
    pygame.draw.rect(screen, GRAY, (ui_x, ui_y, ui_width, ui_height), 2)

    # Пиксельная надпись "ОРУЖИЕ"
    draw_pixel_text(screen, "ОРУЖИЕ", ui_x + 15, ui_y + 5, WHITE, 1)

    # Индикаторы оружия (два квадрата)
    weapon_size = 30
    weapon_spacing = 15
    total_width = weapon_size * 2 + weapon_spacing
    start_x = ui_x + (ui_width - total_width) // 2
    start_y = ui_y + 22

    # Дробаш (первый)
    x1 = start_x
    if current_weapon == WEAPON_SHOTGUN:
        color = WHITE
    else:
        color = DARK_GRAY

    # Рисуем иконку дробаша (два маленьких квадратика)
    pygame.draw.rect(screen, color, (x1, start_y, weapon_size, weapon_size))
    pygame.draw.rect(screen, WHITE, (x1, start_y, weapon_size, weapon_size), 1)

    # Рисуем внутри два маленьких ствола
    inner_size = 8
    inner_spacing = 4
    inner_x = x1 + (weapon_size - inner_size * 2 - inner_spacing) // 2
    inner_y = start_y + (weapon_size - inner_size) // 2

    pygame.draw.rect(screen, color if current_weapon == WEAPON_SHOTGUN else DARK_GRAY,
                    (inner_x, inner_y, inner_size, inner_size))
    pygame.draw.rect(screen, color if current_weapon == WEAPON_SHOTGUN else DARK_GRAY,
                    (inner_x + inner_size + inner_spacing, inner_y, inner_size, inner_size))

    # Катана (второй)
    x2 = start_x + weapon_size + weapon_spacing
    if current_weapon == WEAPON_KATANA:
        color = WHITE
    else:
        color = DARK_GRAY

    pygame.draw.rect(screen, color, (x2, start_y, weapon_size, weapon_size))
    pygame.draw.rect(screen, WHITE, (x2, start_y, weapon_size, weapon_size), 1)

    # Рисуем внутри диагональную линию (катана)
    line_start = (x2 + 5, start_y + 5)
    line_end = (x2 + weapon_size - 5, start_y + weapon_size - 5)
    pygame.draw.line(screen, color if current_weapon == WEAPON_KATANA else DARK_GRAY,
                    line_start, line_end, 3)

# === 18. Функция для отрисовки интерфейса патронов ===
def draw_ammo_ui(screen):
    # Позиция интерфейса (правый нижний угол)
    margin = 20
    ui_width = 160
    ui_height = 95
    ui_x = SCREEN_WIDTH - ui_width - margin
    ui_y = SCREEN_HEIGHT - ui_height - margin

    # Фон интерфейса (полупрозрачный черный)
    ui_surface = pygame.Surface((ui_width, ui_height), pygame.SRCALPHA)
    ui_surface.fill((0, 0, 0, 200))
    screen.blit(ui_surface, (ui_x, ui_y))

    # Рамка интерфейса
    pygame.draw.rect(screen, GRAY, (ui_x, ui_y, ui_width, ui_height), 2)

    # Пиксельная надпись "ПАТРОНЫ"
    draw_pixel_text(screen, "ПАТРОНЫ", ui_x + 15, ui_y + 8, WHITE, 1)

    # Индикаторы патронов (два квадратика)
    ammo_size = 30
    ammo_spacing = 15
    total_ammo_width = ammo_size * 2 + ammo_spacing
    start_x = ui_x + (ui_width - total_ammo_width) // 2
    start_y = ui_y + 35

    for i in range(MAX_AMMO):
        x = start_x + i * (ammo_size + ammo_spacing)
        y = start_y

        if is_reloading:
            if i < current_ammo:
                color = YELLOW
            else:
                pulse = abs(math.sin(pygame.time.get_ticks() * 0.005))
                pulse_value = int(100 + 155 * pulse)
                color = (pulse_value, 0, 0)
        else:
            if i < current_ammo:
                color = YELLOW
            else:
                color = DARK_GRAY

        pygame.draw.rect(screen, color, (x, y, ammo_size, ammo_size))
        pygame.draw.rect(screen, WHITE, (x, y, ammo_size, ammo_size), 1)

    # Прогресс-бар перезарядки (только если идет перезарядка)
    if is_reloading:
        bar_width = ui_width - 30
        bar_height = 6
        bar_x = ui_x + 15
        bar_y = ui_y + ui_height - 22

        pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))

        progress = 1 - (reload_timer / RELOAD_TIME)
        fill_width = int(bar_width * progress)
        if fill_width > 0:
            pygame.draw.rect(screen, YELLOW, (bar_x, bar_y, fill_width, bar_height))

# === 19. Списки для объектов ===
bullets = []
sparks = []

# === 20. Настройки рывка ===
DASH_DISTANCE = 150
DASH_DURATION = 10
DASH_COOLDOWN = 60

is_dashing = False
dash_timer = 0
dash_cooldown_timer = 0
dash_target_x = 0
dash_target_y = 0
dash_start_x = 0
dash_start_y = 0

# === 21. Главный игровой цикл ===
clock = pygame.time.Clock()
running = True
keys_pressed = {}

while running:
    # --- Обработка событий ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keys_pressed[event.key] = True

            # Перезарядка на R (только для дробаша)
            if event.key == pygame.K_r and current_weapon == WEAPON_SHOTGUN:
                reload_shotgun()

            # Рывок на Shift
            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                if not is_dashing and dash_cooldown_timer <= 0:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    world_mouse_x = mouse_x - camera.current_x
                    world_mouse_y = mouse_y - camera.current_y

                    dx = world_mouse_x - player_x
                    dy = world_mouse_y - player_y

                    if dx != 0 or dy != 0:
                        distance = math.sqrt(dx * dx + dy * dy)
                        dx /= distance
                        dy /= distance

                        dash_target_x = player_x + dx * DASH_DISTANCE
                        dash_target_y = player_y + dy * DASH_DISTANCE

                        if not can_move_to(dash_target_x, dash_target_y):
                            steps = 10
                            for i in range(1, steps + 1):
                                check_x = player_x + dx * DASH_DISTANCE * i / steps
                                check_y = player_y + dy * DASH_DISTANCE * i / steps
                                if not can_move_to(check_x, check_y):
                                    dash_target_x = player_x + dx * DASH_DISTANCE * (i - 1) / steps
                                    dash_target_y = player_y + dy * DASH_DISTANCE * (i - 1) / steps
                                    break

                        is_dashing = True
                        dash_timer = DASH_DURATION
                        dash_cooldown_timer = DASH_COOLDOWN
                        dash_start_x, dash_start_y = player_x, player_y

        elif event.type == pygame.KEYUP:
            keys_pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                if current_weapon == WEAPON_SHOTGUN:
                    shoot_shotgun()
                elif current_weapon == WEAPON_KATANA:
                    katana_attack()

        elif event.type == pygame.MOUSEWHEEL:
            # Переключение оружия колесиком мыши
            if event.y > 0:  # Скролл вверх
                current_weapon = WEAPON_KATANA
            elif event.y < 0:  # Скролл вниз
                current_weapon = WEAPON_SHOTGUN

    # --- Обновление таймеров ---
    if dash_cooldown_timer > 0:
        dash_cooldown_timer -= 1

    if reload_timer > 0:
        reload_timer -= 1
        if reload_timer <= 0:
            current_ammo = MAX_AMMO
            is_reloading = False

    if attack_cooldown_timer > 0:
        attack_cooldown_timer -= 1

    # --- Обновление атаки катаной ---
    if is_attacking:
        attack_timer -= 1

        # Обновляем угол удара (двигаемся к цели)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_mouse_x = mouse_x - camera.current_x
        world_mouse_y = mouse_y - camera.current_y

        dx = world_mouse_x - player_x
        dy = world_mouse_y - player_y
        target_angle = math.atan2(dy, dx)

        # Плавно двигаем угол удара к цели
        progress = 1 - (attack_timer / ATTACK_DURATION)
        start_angle = target_angle - math.radians(SWING_ANGLE / 2)
        end_angle = target_angle + math.radians(SWING_ANGLE / 2)
        attack_angle = start_angle + (end_angle - start_angle) * progress

        if attack_timer <= 0:
            is_attacking = False

    # --- Рывок ---
    if is_dashing:
        progress = 1 - (dash_timer / DASH_DURATION)
        player_x = dash_start_x + (dash_target_x - dash_start_x) * progress
        player_y = dash_start_y + (dash_target_y - dash_start_y) * progress

        dash_timer -= 1
        if dash_timer <= 0:
            is_dashing = False
            player_x, player_y = dash_target_x, dash_target_y

    # --- Обычное управление ---
    if not is_dashing:
        if keys_pressed.get(pygame.K_a, False):
            new_x = player_x - PLAYER_SPEED
            if can_move_to(new_x, player_y):
                player_x = new_x
        if keys_pressed.get(pygame.K_d, False):
            new_x = player_x + PLAYER_SPEED
            if can_move_to(new_x, player_y):
                player_x = new_x
        if keys_pressed.get(pygame.K_w, False):
            new_y = player_y - PLAYER_SPEED
            if can_move_to(player_x, new_y):
                player_y = new_y
        if keys_pressed.get(pygame.K_s, False):
            new_y = player_y + PLAYER_SPEED
            if can_move_to(player_x, new_y):
                player_y = new_y

    # --- Обновление пуль ---
    for bullet in bullets[:]:
        hit_wall = bullet.update()
        if hit_wall:
            for _ in range(8):
                sparks.append(Spark(bullet.x, bullet.y, bullet.angle))
        if not bullet.active:
            bullets.remove(bullet)

    # --- Обновление искр ---
    for spark in sparks[:]:
        if spark.update():
            sparks.remove(spark)

    # --- Обновление камеры ---
    camera.update(player_x, player_y)

    # --- Отрисовка ---
    screen.fill(BLACK)

    # Рисуем стену
    wall_rect_camera = camera.apply(wall_rect)
    pygame.draw.rect(screen, WHITE, wall_rect_camera, width=3)

    # Рисуем искры
    for spark in sparks:
        spark.draw(screen, camera)

    # Рисуем пули
    for bullet in bullets:
        bullet.draw(screen, camera)

    # Рисуем игрока
    player_pos_camera = camera.apply_point(player_x, player_y)
    pygame.draw.circle(screen, WHITE, player_pos_camera, PLAYER_RADIUS, width=3)

    # Рисуем оружие (только текущее)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    world_mouse_x = mouse_x - camera.current_x
    world_mouse_y = mouse_y - camera.current_y

    dx = world_mouse_x - player_x
    dy = world_mouse_y - player_y
    angle = math.atan2(dy, dx)

    if current_weapon == WEAPON_SHOTGUN:
        # Рисуем дробаш
        right_angle = angle + math.pi / 2

        gun_base_x = player_x + math.cos(angle) * GUN_FORWARD_OFFSET + math.cos(right_angle) * PLAYER_RADIUS
        gun_base_y = player_y + math.sin(angle) * GUN_FORWARD_OFFSET + math.sin(right_angle) * PLAYER_RADIUS

        for i in [-1, 1]:
            offset = i * (SHOTGUN_WIDTH + BARREL_SPACING) / 2

            barrel_dir_x = math.cos(angle)
            barrel_dir_y = math.sin(angle)
            perp_x = math.cos(right_angle)
            perp_y = math.sin(right_angle)

            start_x = gun_base_x + perp_x * offset
            start_y = gun_base_y + perp_y * offset
            end_x = start_x + barrel_dir_x * SHOTGUN_LENGTH
            end_y = start_y + barrel_dir_y * SHOTGUN_LENGTH

            half_width = SHOTGUN_WIDTH / 2
            p1 = (start_x + perp_x * half_width, start_y + perp_y * half_width)
            p2 = (start_x - perp_x * half_width, start_y - perp_y * half_width)
            p3 = (end_x - perp_x * half_width, end_y - perp_y * half_width)
            p4 = (end_x + perp_x * half_width, end_y + perp_y * half_width)

            points = [
                camera.apply_point(p1[0], p1[1]),
                camera.apply_point(p2[0], p2[1]),
                camera.apply_point(p3[0], p3[1]),
                camera.apply_point(p4[0], p4[1])
            ]

            pygame.draw.polygon(screen, WHITE, points, 2)

    elif current_weapon == WEAPON_KATANA:
        if is_attacking:
            # Во время атаки - рисуем меч в движении
            sword_angle = attack_angle
            sword_length = KATANA_LENGTH * 1.2  # Чуть длиннее во время атаки

            # Начало меча (у руки)
            start_x = player_x + math.cos(angle) * PLAYER_RADIUS
            start_y = player_y + math.sin(angle) * PLAYER_RADIUS

            # Конец меча
            end_x = start_x + math.cos(sword_angle) * sword_length
            end_y = start_y + math.sin(sword_angle) * sword_length

            # Толщина меча
            perp_angle = sword_angle + math.pi / 2
            half_width = KATANA_WIDTH / 2

            p1 = (start_x + math.cos(perp_angle) * half_width,
                  start_y + math.sin(perp_angle) * half_width)
            p2 = (start_x - math.cos(perp_angle) * half_width,
                  start_y - math.sin(perp_angle) * half_width)
            p3 = (end_x - math.cos(perp_angle) * half_width,
                  end_y - math.sin(perp_angle) * half_width)
            p4 = (end_x + math.cos(perp_angle) * half_width,
                  end_y + math.sin(perp_angle) * half_width)

            points = [
                camera.apply_point(p1[0], p1[1]),
                camera.apply_point(p2[0], p2[1]),
                camera.apply_point(p3[0], p3[1]),
                camera.apply_point(p4[0], p4[1])
            ]

            # Добавляем эффект свинга (немного размытия)
            for i in range(3):
                alpha = 100 - i * 30
                points_offset = []
                offset_amount = i * 2
                for px, py in points:
                    points_offset.append((px + math.cos(perp_angle) * offset_amount,
                                         py + math.sin(perp_angle) * offset_amount))

                if alpha > 0:
                    color = (255, 255, 255, alpha)
                    # Создаем поверхность с прозрачностью
                    sword_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                    pygame.draw.polygon(sword_surface, color, points_offset, 2)
                    screen.blit(sword_surface, (0, 0))

            # Основной меч
            pygame.draw.polygon(screen, WHITE, points, 2)

        else:
            # Катана на спине (сбоку)
            # Угол наклона на спине (45 градусов)
            back_angle = math.radians(135)  # Направление на спине

            # Позиция меча на спине (смещение вправо и вверх)
            offset_x = math.cos(back_angle) * PLAYER_RADIUS * 1.5
            offset_y = math.sin(back_angle) * PLAYER_RADIUS * 1.5

            start_x = player_x + offset_x
            start_y = player_y + offset_y

            # Конец меча
            end_x = start_x + math.cos(back_angle) * KATANA_LENGTH
            end_y = start_y + math.sin(back_angle) * KATANA_LENGTH

            # Толщина меча
            perp_angle = back_angle + math.pi / 2
            half_width = KATANA_WIDTH / 2

            p1 = (start_x + math.cos(perp_angle) * half_width,
                  start_y + math.sin(perp_angle) * half_width)
            p2 = (start_x - math.cos(perp_angle) * half_width,
                  start_y - math.sin(perp_angle) * half_width)
            p3 = (end_x - math.cos(perp_angle) * half_width,
                  end_y - math.sin(perp_angle) * half_width)
            p4 = (end_x + math.cos(perp_angle) * half_width,
                  end_y + math.sin(perp_angle) * half_width)

            points = [
                camera.apply_point(p1[0], p1[1]),
                camera.apply_point(p2[0], p2[1]),
                camera.apply_point(p3[0], p3[1]),
                camera.apply_point(p4[0], p4[1])
            ]

            # Рисуем меч на спине (чуть темнее)
            pygame.draw.polygon(screen, GRAY, points, 2)

    # --- Рисуем интерфейсы ---
    draw_weapon_ui(screen)
    if current_weapon == WEAPON_SHOTGUN:
        draw_ammo_ui(screen)

    pygame.display.flip()
    clock.tick(60)
