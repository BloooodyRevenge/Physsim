import pygame
import sys
import os
import math
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Запуск воздушного шара")

# Цвета
SKY_TOP = (135, 206, 235)
SKY_BOTTOM = (200, 230, 255)
GREEN = (34, 139, 34)
YELLOW = (255, 255, 0)
PANEL_BG = (28, 28, 40)
TEXT_COLOR = (255, 255, 255)
HIGHLIGHT = (255, 215, 0)
WHITE = (255, 255, 255)
BROWN = (101, 67, 33)

# Шрифты
font_text = pygame.font.Font(None, 24)
font_small = pygame.font.Font(None, 18)
font_title = pygame.font.Font(None, 28)
font_button = pygame.font.Font(None, 28)

def load_image(filename, scale_factor=1.0):
    try:
        if not os.path.exists("assets"):
            os.makedirs("assets")
        image_path = os.path.join("assets", filename)
        if not os.path.exists(image_path):
            return None
        image = pygame.image.load(image_path)
        if filename.lower().endswith('.png'):
            image = image.convert_alpha()
        if scale_factor != 1.0:
            width = int(image.get_width() * scale_factor)
            height = int(image.get_height() * scale_factor)
            image = pygame.transform.scale(image, (width, height))
        return image
    except:
        return None

# Загрузка изображений
balloon_img = load_image("shar.png", 0.12)
balast_img = load_image("balast.png", 0.12)
klapan_img = load_image("klapan.png", 0.12)
tree_img = load_image("tree.png", 0.18)
sun_img = load_image("sun.png", 0.18)
kust_img = load_image("kust.png", 0.18)
sky_img = load_image("sky.png", 0.18)

bg_img = load_image("background.jpg", 1)
logo_img = load_image("logo.png", 1)

if balloon_img is None:
    balloon_img = pygame.Surface((36, 48), pygame.SRCALPHA)
    pygame.draw.circle(balloon_img, (255, 100, 100), (18, 16), 14)
    pygame.draw.rect(balloon_img, (139, 69, 19), (14, 30, 8, 18))

original_balloon = balloon_img.copy()

if tree_img is None:
    tree_img = pygame.Surface((22, 35), pygame.SRCALPHA)
    pygame.draw.rect(tree_img, BROWN, (8, 20, 6, 15))
    pygame.draw.circle(tree_img, (0, 120, 0), (11, 12), 8)

if balast_img is None:
    balast_img = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.circle(balast_img, (160, 82, 45), (10, 10), 8)

if klapan_img is None:
    klapan_img = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.circle(klapan_img, (100, 100, 100), (10, 10), 8)
    pygame.draw.line(klapan_img, (50, 50, 50), (3, 3), (17, 17), 3)
    pygame.draw.line(klapan_img, (50, 50, 50), (17, 3), (3, 17), 3)

# Размеры шара
balloon_width = balloon_img.get_width()
balloon_height = balloon_img.get_height()

# Мир
WORLD_WIDTH = 5000
WORLD_HEIGHT = 4000

# Начальная позиция шара в МИРЕ
GROUND_LEVEL = WORLD_HEIGHT - 300
balloon_x = 200
balloon_y = GROUND_LEVEL - balloon_height + 100
MAX_HEIGHT = 100
MIN_START_HEIGHT = 600

# ТРИ ПОЛОСЫ
ZONE_HEIGHT = 180
ZONE_SPACING = 20
zone_center_y = 0
show_zones = False

# Переменные для отслеживания положения
in_green_zone = False
wind_speed = 2.5
current_zone = 1

# ПЛАВНОЕ ПЕРЕМЕЩЕНИЕ
target_zone = 1
move_speed = 3.0

# Система смены цветов
color_change_counter = 0
max_color_changes = 10
game_completed = False
final_rise_speed = 1.5
final_rise_active = False

green_zone_distance = 0
distance_for_color_change = 500
last_color_change_x = balloon_x
color_config = 1

# Дебаг режим
debug_mode = False

# ДЕРЕВЬЯ (позиции в мире)
trees = []

# Первое дерево
trees.append({
    'image': tree_img,
    'x': 100,
    'y': GROUND_LEVEL - tree_img.get_height() + 100
})

# Второе дерево
trees.append({
    'image': tree_img,
    'x': 300,
    'y': GROUND_LEVEL - tree_img.get_height() + 100 + random.randint(-5, 5)
})

# Третье дерево
trees.append({
    'image': tree_img,
    'x': 500,
    'y': GROUND_LEVEL - tree_img.get_height() + 100 + random.randint(-5, 5)
})

# Четвёртое дерево
trees.append({
    'image': tree_img,
    'x': 700,
    'y': GROUND_LEVEL - tree_img.get_height() + 100 + random.randint(-5, 5)
})

# Пятое дерево
trees.append({
    'image': tree_img,
    'x': 900,
    'y': GROUND_LEVEL - tree_img.get_height() + 100 + random.randint(-5, 5)
})

# Шестое дерево
trees.append({
    'image': tree_img,
    'x': 1200,
    'y': GROUND_LEVEL - tree_img.get_height() + 100 + random.randint(-5, 5)
})

# Седьмое дерево
trees.append({
    'image': tree_img,
    'x': 1500,
    'y': GROUND_LEVEL - tree_img.get_height() + 100 + random.randint(-5, 5)
})

# Восьмое дерево
trees.append({
    'image': tree_img,
    'x': 1800,
    'y': GROUND_LEVEL - tree_img.get_height() + 100 + random.randint(-5, 5)
})

# Девятое дерево
trees.append({
    'image': tree_img,
    'x': 2100,
    'y': GROUND_LEVEL - tree_img.get_height() + 100 + random.randint(-5, 5)
})

# Десятое дерево
trees.append({
    'image': tree_img,
    'x': 2400,
    'y': GROUND_LEVEL - tree_img.get_height() + 100 + random.randint(-5, 5)
})

# Облака
clouds = []
for i in range(20):
    clouds.append({
        'x': random.randint(0, 5000),
        'y': random.randint(50, 400),
        'speed': random.uniform(0.2, 0.8),
        'size': random.randint(80, 250),
        'layer': random.randint(1, 3)
    })

# СЛАЙДЫ
slides = [
    {
        "title": "СТРОЕНИЕ",
        "text": "Воздушный шар состоит из трёх основных частей:\n\n• Оболочка - заполняется горячим воздухом\n• Корзина - для пассажиров и груза\n• Горелка - нагревает воздух",
        "color": (220, 120, 120)
    },
    {
        "title": "ФИЗИКА",
        "text": "Почему шар летит?\n\n• Горячий воздух легче холодного\n• Плотность горячего воздуха ниже\n• Архимедова сила выталкивает шар вверх",
        "color": (120, 180, 240)
    },
    {
        "title": "УПРАВЛЕНИЕ",
        "text": "БАЛАСТ (мешки с песком):\nСбрасывая балласт, шар становится легче\nи поднимается вверх.\n\nКЛАПАН (вверху оболочки):\nВыпуская горячий воздух, шар становится\nтяжелее и опускается вниз.",
        "color": (120, 220, 140)
    },
    {
        "title": "ФАКТЫ",
        "text": "Интересные факты:\n\n• Первый полёт - 1783 год\n• Рекорд высоты - 21 км",
        "color": (240, 200, 100)
    },
    {
        "title": "Выводы",
        "text": "Мы изучили и разобрали воздушный шар.\n\n Теперь перейдём к финальному тестированию и завершим данный урок",
        "color": (200, 150, 200)
    }
]

# ИГРОВЫЕ ПЕРЕМЕННЫЕ
current_slide = 0
button_hovered = False
game_started = False
auto_rising = False
rising_to_target = False
rising_to_start_height = False
balloon_speed = 0
balloon_acceleration = 0.02
max_speed = 2.0

color_shift = 0

# Зум камеры
camera_zoom = 1.0
target_zoom = 1.0
min_zoom = 0.35

# Кнопки
BUTTON_SIZE = 60
BALAST_BUTTON = pygame.Rect(40, HEIGHT - 80, BUTTON_SIZE, BUTTON_SIZE)
KLAPAN_BUTTON = pygame.Rect(120, HEIGHT - 80, BUTTON_SIZE, BUTTON_SIZE)

# Смещение мира (для эффекта движения) - с плавным следованием
world_offset_x = 0
world_offset_y = 0
target_offset_x = 0
target_offset_y = 0
camera_follow_speed = 0.05  # Скорость следования камеры (чем меньше, тем медленнее)

def apply_zoom(surface, zoom):
    if zoom == 1.0:
        return surface
    new_width = int(surface.get_width() * zoom)
    new_height = int(surface.get_height() * zoom)
    return pygame.transform.scale(surface, (new_width, new_height))

def get_zone_center_y(zone):
    if zone == 0:
        return zone_center_y - ZONE_HEIGHT - ZONE_SPACING
    elif zone == 1:
        return zone_center_y
    else:
        return zone_center_y + ZONE_HEIGHT + ZONE_SPACING

def check_zone():
    global current_zone, in_green_zone
    balloon_center_y = balloon_y + balloon_height // 2

    if balloon_center_y < zone_center_y - ZONE_HEIGHT//2 - ZONE_SPACING//2:
        current_zone = 0
    elif balloon_center_y > zone_center_y + ZONE_HEIGHT//2 + ZONE_SPACING//2:
        current_zone = 2
    else:
        current_zone = 1

    in_green_zone = (current_zone == color_config)
    return current_zone, in_green_zone

def set_target_zone(zone):
    global target_zone
    if game_completed:
        return
    target_zone = zone

def update_balloon_position():
    global balloon_y
    if game_completed:
        return

    target_y = get_zone_center_y(target_zone) - balloon_height // 2

    if abs(balloon_y - target_y) > move_speed:
        if balloon_y < target_y:
            balloon_y += move_speed
        else:
            balloon_y -= move_speed
    else:
        balloon_y = target_y

    check_zone()

def change_colors():
    global color_config, color_change_counter, last_color_change_x, green_zone_distance
    if game_completed:
        return

    options = [0, 1, 2]
    options.remove(color_config)
    color_config = random.choice(options)

    color_change_counter += 1
    last_color_change_x = balloon_x
    green_zone_distance = 0
    check_zone()

    if color_change_counter >= max_color_changes:
        complete_game()

def complete_game():
    global game_completed, final_rise_active, in_green_zone, current_slide
    game_completed = True
    final_rise_active = True
    in_green_zone = False
    current_slide = 3

# Основной цикл
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60)
    color_shift += 0.01

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                debug_mode = not debug_mode
                show_zones = debug_mode

        elif event.type == pygame.MOUSEMOTION:
            if (not game_started or game_completed) and not rising_to_start_height:
                panel_width = 300
                panel_x = WIDTH - panel_width - 20
                panel_y = 20
                button_x = panel_x + panel_width - 130
                button_y = panel_y + HEIGHT - 40 - 50
                next_button = pygame.Rect(button_x, button_y, 120, 40)
                button_hovered = next_button.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_started and not game_completed:
                if BALAST_BUTTON.collidepoint(event.pos):
                    if current_zone > 0:
                        set_target_zone(current_zone - 1)
                elif KLAPAN_BUTTON.collidepoint(event.pos):
                    if current_zone < 2:
                        set_target_zone(current_zone + 1)

            if (not game_started or game_completed) and not rising_to_start_height:
                panel_width = 300
                panel_x = WIDTH - panel_width - 20
                panel_y = 20
                button_x = panel_x + panel_width - 130
                button_y = panel_y + HEIGHT - 40 - 50
                next_button = pygame.Rect(button_x, button_y, 120, 40)

                if next_button.collidepoint(event.pos):
                    if current_slide == 2 and not game_started:
                        current_height = GROUND_LEVEL - balloon_y - balloon_height
                        if current_height >= MIN_START_HEIGHT:
                            game_started = True
                            target_zoom = min_zoom
                            zone_center_y = balloon_y + balloon_height // 2
                            balloon_speed = 0
                            last_color_change_x = balloon_x
                            color_config = 1
                            target_zone = 1
                        else:
                            rising_to_start_height = True
                            current_slide += 1

                    elif current_slide < len(slides) - 1:
                        current_slide += 1
                        if current_slide == 1:
                            auto_rising = True
                        elif current_slide == 2:
                            current_height = GROUND_LEVEL - balloon_y - balloon_height
                            if current_height < MIN_START_HEIGHT:
                                rising_to_start_height = True
                    elif game_completed and current_slide == 3:
                        if current_slide < len(slides) - 1:
                            current_slide += 1

    # ФИЗИКА ДО ИГРЫ
    if not game_started:
        if rising_to_start_height:
            current_height = GROUND_LEVEL - balloon_y - balloon_height
            if current_height < MIN_START_HEIGHT:
                balloon_speed += balloon_acceleration
                if balloon_speed > max_speed:
                    balloon_speed = max_speed
                balloon_y -= balloon_speed
            else:
                rising_to_start_height = False
                balloon_speed = 0
                game_started = True
                target_zoom = min_zoom
                zone_center_y = balloon_y + balloon_height // 2
                last_color_change_x = balloon_x
                color_config = 1
                target_zone = 1

        if auto_rising and balloon_y > MAX_HEIGHT and not rising_to_start_height:
            balloon_speed += balloon_acceleration
            if balloon_speed > max_speed:
                balloon_speed = max_speed
            balloon_y -= balloon_speed

    # ФИЗИКА ВО ВРЕМЯ ИГРЫ
    if game_started:
        if not game_completed:
            update_balloon_position()
            check_zone()

            if in_green_zone:
                # Шар движется вправо по миру (без ограничений)
                balloon_x += wind_speed
                green_zone_distance = balloon_x - last_color_change_x

                if green_zone_distance >= distance_for_color_change:
                    change_colors()

            balloon_y = max(MAX_HEIGHT, min(balloon_y, GROUND_LEVEL - balloon_height))

        else:
            if final_rise_active:
                balloon_y -= final_rise_speed
                balloon_x += math.sin(pygame.time.get_ticks() * 0.005) * 0.5
                balloon_y = max(MAX_HEIGHT, balloon_y)

    # Вычисляем целевую позицию камеры (где должен быть центр экрана относительно мира)
    # Цель - держать шар в центре экрана
    target_offset_x = balloon_x - WIDTH//2 + balloon_width//2
    target_offset_y = balloon_y - HEIGHT//2 + balloon_height//2

    # НИКАКИХ ОГРАНИЧЕНИЙ! Камера следует за шаром куда угодно

    # Плавно двигаем камеру к целевой позиции (неуспевающее движение)
    world_offset_x += (target_offset_x - world_offset_x) * camera_follow_speed
    world_offset_y += (target_offset_y - world_offset_y) * camera_follow_speed

    # ОТРИСОВКА
    # Небо (фон всегда на месте, не двигается с миром)
    for i in range(HEIGHT):
        ratio = i / HEIGHT
        r = int(135 * (1-ratio) + 200 * ratio)
        g = int(206 * (1-ratio) + 230 * ratio)
        b = int(235 * (1-ratio) + 255 * ratio)
        pygame.draw.line(screen, (r, g, b), (0, i), (WIDTH, i))

    # Солнце (не двигается с миром)
    pygame.draw.circle(screen, YELLOW, (850, 70), 40)

    # Облака (двигаются с миром)
    for cloud in clouds:
        cloud['x'] += cloud['speed']
        if cloud['x'] > WORLD_WIDTH + 300:
            cloud['x'] = -300

        # Позиция облака на экране с учетом смещения мира
        cx = cloud['x'] - world_offset_x
        cy = cloud['y'] - world_offset_y

        if -300 < cx < WIDTH + 300:
            size = int(cloud['size'] * camera_zoom)
            alpha = 180 - cloud['layer'] * 30

            cloud_surf = pygame.Surface((size, size//2), pygame.SRCALPHA)
            for j in range(3):
                circle_x = j * size//3
                circle_y = 0
                circle_radius = size//4
                pygame.draw.circle(cloud_surf, (255, 255, 255, alpha),
                                 (circle_x, circle_y), circle_radius)
            screen.blit(cloud_surf, (cx, cy))

    # ЗЕМЛЯ (с учетом смещения мира)
    ground_y = GROUND_LEVEL - world_offset_y
    if ground_y < HEIGHT:
        pygame.draw.rect(screen, GREEN, (0, ground_y, WIDTH, HEIGHT - ground_y + 20))

    # ДЕРЕВЬЯ (с учетом смещения мира)
    for tree in trees:
        tree_x = tree['x'] - world_offset_x
        tree_y = tree['y'] - world_offset_y
        if -100 < tree_x < WIDTH + 100:
            scaled_tree = apply_zoom(tree['image'], camera_zoom)
            screen.blit(scaled_tree, (tree_x, tree_y))

    # ПОЛОСЫ - только в F3, с правильными цветами (с учетом смещения мира)
    if game_started and show_zones:
        zone_screen_y = zone_center_y - world_offset_y

        # Верхняя зона (индекс 0)
        top_zone_y = zone_screen_y - ZONE_HEIGHT - ZONE_SPACING - ZONE_HEIGHT//2
        if color_config == 0:
            zone_color = (100, 255, 100, 60)  # Зеленая
        else:
            zone_color = (255, 100, 100, 60)  # Красная
        pygame.draw.rect(screen, zone_color, (0, top_zone_y, WIDTH, ZONE_HEIGHT))

        # Средняя зона (индекс 1)
        middle_zone_y = zone_screen_y - ZONE_HEIGHT//2
        if color_config == 1:
            zone_color = (100, 255, 100, 60)  # Зеленая
        else:
            zone_color = (255, 100, 100, 60)  # Красная
        pygame.draw.rect(screen, zone_color, (0, middle_zone_y, WIDTH, ZONE_HEIGHT))

        # Нижняя зона (индекс 2)
        bottom_zone_y = zone_screen_y + ZONE_HEIGHT + ZONE_SPACING - ZONE_HEIGHT//2
        if color_config == 2:
            zone_color = (100, 255, 100, 60)  # Зеленая
        else:
            zone_color = (255, 100, 100, 60)  # Красная
        pygame.draw.rect(screen, zone_color, (0, bottom_zone_y, WIDTH, ZONE_HEIGHT))

    # ВЕТЕР - ТОЛЬКО ПО ЦЕНТРУ АКТИВНОЙ ЗОНЫ (с учетом смещения мира)
    if game_started:
        time_offset = pygame.time.get_ticks() * 0.15
        zone_screen_y = zone_center_y - world_offset_y

        # Правильные центры каждой зоны
        zone_centers = [
            zone_screen_y - ZONE_HEIGHT - ZONE_SPACING,  # Центр верхней зоны
            zone_screen_y,                                # Центр средней зоны
            zone_screen_y + ZONE_HEIGHT + ZONE_SPACING   # Центр нижней зоны
        ]

        # Только для активной зоны (color_config) отрисовываем ветер
        active_zone_idx = color_config
        center_y = zone_centers[active_zone_idx]

        # Узкая полоса ветра (толщиной 30 пикселей)
        wind_strip_top = center_y - 15
        wind_strip_bottom = center_y + 15

        # Создаём несколько рядов линий внутри узкой полосы
        for row in range(3):  # 3 ряда линий
            row_offset = (row - 1) * 8  # Небольшое смещение по вертикали
            y_pos = center_y + row_offset

            # Проверяем, находится ли ряд в пределах узкой полосы
            if wind_strip_top <= y_pos <= wind_strip_bottom:
                for i in range(12):  # 12 линий в ряду
                    # Линии движутся справа налево
                    x_pos = (time_offset + i * 70 + row * 25) % (WIDTH + 300) - 150

                    # Разная длина линий для разнообразия
                    length = 60 + (i % 3) * 25

                    # Основная линия
                    alpha = 255 - row * 30
                    pygame.draw.line(screen, (255, 255, 255, alpha),
                                   (x_pos, y_pos), (x_pos + length, y_pos), 3)

                    # Дополнительная линия для эффекта скорости
                    if i % 2 == 0:
                        pygame.draw.line(screen, (255, 255, 255, alpha//2),
                                       (x_pos - 10, y_pos - 1), (x_pos + length - 10, y_pos - 1), 2)

    # ШАР - теперь всегда следует за камерой
    # Позиция шара на экране зависит от смещения камеры
    balloon_screen_x = balloon_x - world_offset_x
    balloon_screen_y = balloon_y - world_offset_y
    scaled_balloon = apply_zoom(original_balloon, camera_zoom)
    screen.blit(scaled_balloon, (balloon_screen_x, balloon_screen_y))

    # Дебаг информация
    if debug_mode:
        debug_text1 = font_small.render(f"Zone: {current_zone}", True, WHITE)
        debug_text2 = font_small.render(f"Green: {color_config}", True, WHITE)
        debug_text3 = font_small.render(f"Count: {color_change_counter}", True, WHITE)
        debug_text4 = font_small.render(f"World X: {int(balloon_x)}", True, WHITE)
        debug_text5 = font_small.render(f"Cam Speed: {camera_follow_speed}", True, WHITE)
        debug_text6 = font_small.render(f"Cam Offset: {int(world_offset_x)}", True, WHITE)
        screen.blit(debug_text1, (10, 10))
        screen.blit(debug_text2, (10, 30))
        screen.blit(debug_text3, (10, 50))
        screen.blit(debug_text4, (10, 70))
        screen.blit(debug_text5, (10, 90))
        screen.blit(debug_text6, (10, 110))

    # СЧЁТЧИК
    if game_started and not game_completed and in_green_zone:
        counter_text = font_small.render(f"Смена: {color_change_counter}/{max_color_changes}", True, HIGHLIGHT)
        screen.blit(counter_text, (WIDTH - 150, 20))

        bar_width = 100
        bar_height = 10
        bar_x = WIDTH - 150
        bar_y = 45
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        progress = (green_zone_distance / distance_for_color_change) * bar_width
        if progress > 0:
            pygame.draw.rect(screen, (100, 255, 100), (bar_x, bar_y, min(progress, bar_width), bar_height))

    # Высота при подъёме
    if not game_started and rising_to_start_height:
        current_height = GROUND_LEVEL - balloon_y - balloon_height
        height_text = font_small.render(f"Подъём: {int(current_height)}/{MIN_START_HEIGHT}", True, (255, 255, 255))
        screen.blit(height_text, (WIDTH//2 - 50, 50))

    # СЛАЙДЕР
    if (not game_started and not rising_to_start_height) or (game_completed):
        panel_width = 300
        panel_x = WIDTH - panel_width - 20
        panel_y = 20
        panel_height = HEIGHT - 40

        pulse = math.sin(color_shift) * 15
        color = slides[current_slide]["color"]
        animated_color = (
            max(0, min(255, color[0] + int(pulse))),
            max(0, min(255, color[1] + int(pulse * 0.5))),
            max(0, min(255, color[2] + int(pulse * 0.8)))
        )

        pygame.draw.rect(screen, PANEL_BG, (panel_x, panel_y, panel_width, panel_height), border_radius=15)
        pygame.draw.rect(screen, animated_color, (panel_x, panel_y, panel_width, panel_height), 3, border_radius=15)

        # Заголовок
        title = font_title.render(slides[current_slide]["title"], True, animated_color)
        screen.blit(title, (panel_x + 15, panel_y + 15))

        # Линия
        pygame.draw.line(screen, animated_color,
                        (panel_x + 15, panel_y + 45),
                        (panel_x + panel_width - 15, panel_y + 45), 2)

        # Индикаторы
        dot_spacing = 25
        total_width = len(slides) * dot_spacing
        start_x = panel_x + (panel_width - total_width) // 2
        dot_y = panel_y + 70

        for i in range(len(slides)):
            if i == current_slide:
                pygame.draw.circle(screen, animated_color, (start_x + i * dot_spacing, dot_y), 6)
            elif i < current_slide:
                pygame.draw.circle(screen, (180, 180, 180), (start_x + i * dot_spacing, dot_y), 5)
            else:
                pygame.draw.circle(screen, (100, 100, 100), (start_x + i * dot_spacing, dot_y), 4)

        # Текст
        y = dot_y + 30
        text_lines = slides[current_slide]["text"].split('\n')
        for line in text_lines:
            if line.strip():
                words = line.split()
                current_line = ""
                for word in words:
                    test_line = current_line + word + " "
                    if font_text.size(test_line)[0] < panel_width - 30:
                        current_line = test_line
                    else:
                        if current_line:
                            screen.blit(font_text.render(current_line, True, TEXT_COLOR), (panel_x + 15, y))
                            y += 25
                        current_line = word + " "
                if current_line:
                    screen.blit(font_text.render(current_line, True, TEXT_COLOR), (panel_x + 15, y))
                    y += 25
            else:
                y += 15

        # Кнопка
        if current_slide < len(slides) - 1:
            button_x = panel_x + panel_width - 130
            button_y = panel_y + panel_height - 50
            button_rect = pygame.Rect(button_x, button_y, 120, 40)

            if button_hovered:
                btn_color = tuple(max(30, min(255, c - 40)) for c in animated_color)
            else:
                btn_color = animated_color

            pygame.draw.rect(screen, btn_color, button_rect, border_radius=8)
            pygame.draw.rect(screen, animated_color, button_rect, 2, border_radius=8)

            if current_slide == 2 and not game_started:
                btn_text = "НАЧАТЬ"
            else:
                btn_text = "ДАЛЕЕ"

            text = font_button.render(btn_text, True, TEXT_COLOR)
            screen.blit(text, text.get_rect(center=button_rect.center))

    # Кнопки управления
    if game_started and not game_completed:
        # Баласт
        pygame.draw.rect(screen, (160, 82, 45), BALAST_BUTTON, border_radius=10)
        if balast_img:
            scaled_balast = pygame.transform.scale(balast_img, (40, 40))
            img_rect = scaled_balast.get_rect(center=BALAST_BUTTON.center)
            screen.blit(scaled_balast, img_rect)
        pygame.draw.rect(screen, HIGHLIGHT, BALAST_BUTTON, 2, border_radius=10)

        # Клапан
        pygame.draw.rect(screen, (100, 100, 100), KLAPAN_BUTTON, border_radius=10)
        if klapan_img:
            scaled_klapan = pygame.transform.scale(klapan_img, (40, 40))
            img_rect = scaled_klapan.get_rect(center=KLAPAN_BUTTON.center)
            screen.blit(scaled_klapan, img_rect)
        pygame.draw.rect(screen, HIGHLIGHT, KLAPAN_BUTTON, 2, border_radius=10)

        # Индикатор зоны
        if in_green_zone:
            zone_text = font_small.render("ЗЕЛЁНАЯ ЗОНА", True, (100, 255, 100))
        else:
            if current_zone == 0:
                zone_text = font_small.render("ВЕРХНЯЯ ЗОНА", True, (255, 100, 100))
            elif current_zone == 2:
                zone_text = font_small.render("НИЖНЯЯ ЗОНА", True, (255, 100, 100))
            else:
                zone_text = font_small.render("СРЕДНЯЯ ЗОНА", True, (255, 100, 100))
        screen.blit(zone_text, (40, HEIGHT - 120))

    pygame.display.flip()

pygame.quit()
sys.exit()