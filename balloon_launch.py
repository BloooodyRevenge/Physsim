import pygame
import sys
import os
import math
import random
from PIL import Image

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PhysSim - Воздушный шар")

# Цвета
SKY_TOP = (135, 206, 235)
SKY_BOTTOM = (200, 230, 255)
PANEL_BG = (28, 28, 40)
TEXT_COLOR = (255, 255, 255)
TEXT_SHADOW = (80, 80, 100)
HIGHLIGHT = (255, 215, 0)
WHITE = (255, 255, 255)
BROWN = (101, 67, 33)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 150, 200)
GREEN_OK = (0, 200, 0)
GRAY = (150, 150, 150)

# Шрифты
font_text = pygame.font.Font(None, 24)
font_small = pygame.font.Font(None, 20)
font_title = pygame.font.Font(None, 32)
font_button = pygame.font.Font(None, 28)
font_big = pygame.font.Font(None, 48)
font_game_title = pygame.font.Font(None, 72)
font_large = pygame.font.Font(None, 36)

def render_text_with_shadow(text, font, color, shadow_color, x, y):
    """Рисует текст с тенью"""
    shadow = font.render(text, True, shadow_color)
    text_surf = font.render(text, True, color)
    screen.blit(shadow, (x + 2, y + 2))
    screen.blit(text_surf, (x, y))

def render_centered_text(text, font, color, shadow_color, center_x, y):
    """Рисует центрированный текст с тенью"""
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(center_x, y))
    shadow_surf = font.render(text, True, shadow_color)
    shadow_rect = shadow_surf.get_rect(center=(center_x + 2, y + 2))
    screen.blit(shadow_surf, shadow_rect)
    screen.blit(text_surf, text_rect)

def wrap_text(text, font, max_width):
    """Переносит текст на несколько строк"""
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word + " "
    if current_line:
        lines.append(current_line)
    return lines

def wrap_title(title, font, max_width):
    """Переносит заголовок"""
    if font.size(title)[0] <= max_width:
        return [title]
    words = title.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word + " "
    if current_line:
        lines.append(current_line)
    return lines

def create_placeholder(name):
    """Создает заглушку для изображения"""
    surf = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.rect(surf, (100, 100, 100), (0, 0, 60, 60), 2)
    text = font_small.render("?", True, (150, 150, 150))
    surf.blit(text, (25, 20))
    return surf

def load_image(filename, scale_factor=1.0, name="unknown"):
    """Загружает изображение"""
    try:
        if not os.path.exists("assets"):
            os.makedirs("assets")
        image_path = os.path.join("assets", filename)
        if os.path.exists(image_path):
            image = pygame.image.load(image_path)
            if filename.lower().endswith('.png'):
                image = image.convert_alpha()
            if scale_factor != 1.0:
                width = int(image.get_width() * scale_factor)
                height = int(image.get_height() * scale_factor)
                image = pygame.transform.scale(image, (width, height))
            return image
        else:
            return create_placeholder(name)
    except Exception as e:
        return create_placeholder(name)

def load_gif_frames(filename, scale_factor=1.0):
    """Загружает анимированный GIF"""
    frames = []
    try:
        gif_path = os.path.join("assets", filename)
        if not os.path.exists(gif_path):
            for i in range(4):
                frame = pygame.Surface((50, 50), pygame.SRCALPHA)
                offset = math.sin(i * math.pi/2) * 5
                pygame.draw.polygon(frame, BLACK, [(25, 10 + offset), (10, 40), (40, 40)])
                frames.append(frame)
            return frames

        img = Image.open(gif_path)
        for frame in range(img.n_frames):
            img.seek(frame)
            frame_image = img.convert('RGBA')
            size = frame_image.size
            data = frame_image.tobytes()
            py_image = pygame.image.fromstring(data, size, 'RGBA').convert_alpha()
            if scale_factor != 1.0:
                width = int(py_image.get_width() * scale_factor)
                height = int(py_image.get_height() * scale_factor)
                py_image = pygame.transform.scale(py_image, (width, height))
            frames.append(py_image)
        return frames
    except Exception as e:
        for i in range(4):
            frame = pygame.Surface((50, 50), pygame.SRCALPHA)
            offset = math.sin(i * math.pi/2) * 5
            pygame.draw.polygon(frame, BLACK, [(25, 10 + offset), (10, 40), (40, 40)])
            frames.append(frame)
        return frames

# Загрузка изображений
balloon_img = load_image("shar.png", 0.12, "shar")
balast_img = load_image("balast.png", 0.12, "balast")
klapan_img = load_image("klapan.png", 0.12, "klapan")
tree_img = load_image("tree.png", 0.18, "tree")
sun_img = load_image("sun.png", 0.18, "sun")
sky_img = load_image("sky.png", 1.0, "sky")
terra_img = load_image("terra.png", 1.0, "terra")
gora_img = load_image("gora.png", 0.7, "gora")
verevka_img = load_image("verevka.png", 0.15, "verevka")
gorelka_img = load_image("gorelka.png", 0.15, "gorelka")
bird_frames = load_gif_frames("bird.gif", 0.8)

original_balloon = balloon_img.copy()
balloon_width = balloon_img.get_width()
balloon_height = balloon_img.get_height()

# Мир
WORLD_WIDTH = 5000
WORLD_HEIGHT = 4000
CAMERA_TRIGGER_HEIGHT = 300

# Зоны
ZONE_HEIGHT = 180
ZONE_SPACING = 20
zone_center_y = 0

# Переменные
in_green_zone = False
wind_speed = 2.5
current_zone = 1
target_zone = 1
move_speed = 3.0
total_progress = 0
TARGET_DISTANCE = 3000

# Таймер
GAME_TIME_LIMIT = 60
game_timer = GAME_TIME_LIMIT
game_time_started = False

# Начальная позиция
GROUND_LEVEL = 3300
balloon_x = 300
balloon_y = GROUND_LEVEL - balloon_height + 50
MIN_START_HEIGHT = 800

# Деревья
trees = []
for x in [500, 700]:
    trees.append({
        'image': tree_img,
        'x': x,
        'y': GROUND_LEVEL - tree_img.get_height() + 50
    })

# Гора
gora_x = -200
gora_y = GROUND_LEVEL - gora_img.get_height() + 50

# Система смены цветов
color_change_counter = 0
game_completed = False
final_rise_active = False
distance_for_color_change = 500
color_config = 1

# Облака (летят справа налево)
clouds = []
if sky_img is not None:
    for i in range(15):
        cloud_img = sky_img.copy()
        clouds.append({
            'image': cloud_img,
            'x': random.randint(0, WORLD_WIDTH),
            'y': random.randint(500, 2500),
            'speed': random.uniform(0.8, 1.5),
        })

# Птицы
class Bird:
    def __init__(self, zone, zone_center_y, frames):
        self.zone = zone
        self.size = 50
        self.frames = frames
        self.current_frame = 0
        self.animation_speed = 0.15

        if zone == 0:
            self.zone_top = zone_center_y - ZONE_HEIGHT - ZONE_SPACING - ZONE_HEIGHT//2
            self.zone_bottom = zone_center_y - ZONE_HEIGHT - ZONE_SPACING + ZONE_HEIGHT//2
        elif zone == 1:
            self.zone_top = zone_center_y - ZONE_HEIGHT//2
            self.zone_bottom = zone_center_y + ZONE_HEIGHT//2
        else:
            self.zone_top = zone_center_y + ZONE_HEIGHT + ZONE_SPACING - ZONE_HEIGHT//2
            self.zone_bottom = zone_center_y + ZONE_HEIGHT + ZONE_SPACING + ZONE_HEIGHT//2

        self.y = random.randint(int(self.zone_top), int(self.zone_bottom))
        self.x = WORLD_WIDTH + random.randint(100, 500)
        self.speed = random.uniform(2.5, 4.5)
        self.rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x - self.size//2
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0

    def draw(self, screen, world_offset_x, world_offset_y):
        screen_x = self.x - world_offset_x
        screen_y = self.y - world_offset_y
        if -100 < screen_x < WIDTH + 100 and self.frames:
            frame = self.frames[int(self.current_frame)]
            scaled = pygame.transform.scale(frame, (self.size, self.size))
            screen.blit(scaled, (screen_x - self.size//2, screen_y - self.size//2))

    def is_offscreen(self):
        return self.x < -100

    def check_collision(self, balloon_rect):
        return self.rect.colliderect(balloon_rect)

# Система подсказок
class HintSystem:
    def __init__(self):
        self.hints = {
            "first_green_zone": {"text": "Зелёная зона! Ветер помогает двигаться вперёд", "shown": False},
            "balast": {"text": "Сброс балласта = подъём вверх", "shown": False},
            "klapan": {"text": "Выпуск воздуха = спуск вниз", "shown": False},
            "bird": {"text": "Осторожно! Облетай птиц", "shown": False}
        }
        self.active_hint = None
        self.hint_timer = 0
        self.hint_duration = 180

    def show_hint(self, hint_key):
        if hint_key in self.hints and not self.hints[hint_key]["shown"]:
            self.active_hint = hint_key
            self.hint_timer = self.hint_duration
            self.hints[hint_key]["shown"] = True

    def update(self):
        if self.hint_timer > 0:
            self.hint_timer -= 1
        else:
            self.active_hint = None

    def draw(self, screen):
        if self.active_hint and self.hint_timer > 0:
            hint_text = self.hints[self.active_hint]["text"]
            panel_width = 500
            panel_height = 80
            panel_x = WIDTH//2 - panel_width//2
            panel_y = 100

            pygame.draw.rect(screen, (28, 28, 40), (panel_x, panel_y, panel_width, panel_height), border_radius=20)
            pygame.draw.rect(screen, HIGHLIGHT, (panel_x, panel_y, panel_width, panel_height), 2, border_radius=20)

            lines = wrap_text(hint_text, font_text, panel_width - 40)
            y_offset = panel_y + 25
            for line in lines:
                text_surf = font_text.render(line, True, TEXT_COLOR)
                screen.blit(text_surf, (panel_x + 20, y_offset))
                y_offset += 28

# Мини-игра сопоставления
class MatchingGame:
    def __init__(self):
        self.items = [
            {"name": "Клапан", "image": klapan_img, "description": "Выпускает горячий воздух", "matched": False, "rect": pygame.Rect(0, 0, 120, 120)},
            {"name": "Веревка", "image": verevka_img, "description": "Соединяет корзину с оболочкой", "matched": False, "rect": pygame.Rect(0, 0, 120, 120)},
            {"name": "Горелка", "image": gorelka_img, "description": "Нагревает воздух", "matched": False, "rect": pygame.Rect(0, 0, 120, 120)}
        ]
        self.descriptions = [
            {"text": "Выпускает горячий воздух", "matched": False, "rect": pygame.Rect(0, 0, 240, 80)},
            {"text": "Соединяет корзину с оболочкой", "matched": False, "rect": pygame.Rect(0, 0, 240, 80)},
            {"text": "Нагревает воздух", "matched": False, "rect": pygame.Rect(0, 0, 240, 80)}
        ]

        self.selected_item = None
        self.message = ""
        self.message_timer = 0
        self.completed = False

        # Панель
        self.panel_w = 860
        self.panel_h = 520
        self.panel_x = WIDTH//2 - self.panel_w//2
        self.panel_y = HEIGHT//2 - self.panel_h//2

        self.update_positions()

    def update_positions(self):
        start_y = self.panel_y + 130
        for i in range(3):
            self.items[i]["rect"] = pygame.Rect(self.panel_x + 70, start_y + i * 130, 120, 120)
            self.descriptions[i]["rect"] = pygame.Rect(self.panel_x + self.panel_w - 300, start_y + i * 130, 240, 80)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.completed:
            mouse_pos = event.pos
            for i, item in enumerate(self.items):
                if not item["matched"] and item["rect"].collidepoint(mouse_pos):
                    self.selected_item = i
                    break
            if self.selected_item is not None:
                for j, desc in enumerate(self.descriptions):
                    if not desc["matched"] and desc["rect"].collidepoint(mouse_pos):
                        self.check_match(self.selected_item, j)
                        break

    def check_match(self, item_idx, desc_idx):
        if item_idx == desc_idx:
            self.items[item_idx]["matched"] = True
            self.descriptions[desc_idx]["matched"] = True
            self.message = "Правильно! ✓"
            self.message_timer = 120
            if all(item["matched"] for item in self.items):
                self.completed = True
        else:
            self.message = "Неправильно!"
            self.message_timer = 120
        self.selected_item = None

    def draw(self, screen):
        # Панель с круглыми углами
        panel_surface = pygame.Surface((self.panel_w, self.panel_h), pygame.SRCALPHA)
        panel_surface.fill((28, 28, 40, 235))
        pygame.draw.rect(panel_surface, (28, 28, 40, 235), (0, 0, self.panel_w, self.panel_h), border_radius=30)
        screen.blit(panel_surface, (self.panel_x, self.panel_y))
        pygame.draw.rect(screen, HIGHLIGHT, (self.panel_x, self.panel_y, self.panel_w, self.panel_h), 3, border_radius=30)

        # Заголовок
        render_centered_text("СОПОСТАВЬ ДЕТАЛИ", font_title, HIGHLIGHT, TEXT_SHADOW,
                            self.panel_x + self.panel_w//2, self.panel_y + 40)

        if self.completed:
            render_centered_text("ПРОЙДЕНО!", font_big, GREEN_OK, TEXT_SHADOW,
                                self.panel_x + self.panel_w//2, self.panel_y + self.panel_h//2)
        else:
            # Подписи колонок
            render_centered_text("ДЕТАЛИ", font_title, TEXT_COLOR, TEXT_SHADOW,
                                self.panel_x + 130, self.panel_y + 95)
            render_centered_text("ОПИСАНИЕ", font_title, TEXT_COLOR, TEXT_SHADOW,
                                self.panel_x + self.panel_w - 180, self.panel_y + 95)

            # Рисуем предметы
            for i, item in enumerate(self.items):
                rect = item["rect"]
                if not item["matched"]:
                    border_color = HIGHLIGHT if self.selected_item == i else (100, 100, 100)
                    pygame.draw.rect(screen, border_color, rect, 3, border_radius=20)
                    if item["image"]:
                        img = pygame.transform.scale(item["image"], (90, 90))
                        screen.blit(img, (rect.x + 15, rect.y + 15))
                    name_text = font_small.render(item["name"], True, TEXT_COLOR)
                    screen.blit(name_text, (rect.x + 35, rect.y + 100))
                else:
                    ok_text = font_big.render("✓", True, GREEN_OK)
                    screen.blit(ok_text, (rect.x + 48, rect.y + 45))
                    if item["image"]:
                        img = pygame.transform.scale(item["image"], (90, 90))
                        img.set_alpha(100)
                        screen.blit(img, (rect.x + 15, rect.y + 15))
                    name_text = font_small.render(item["name"], True, GRAY)
                    screen.blit(name_text, (rect.x + 35, rect.y + 100))

            # Рисуем описания
            for j, desc in enumerate(self.descriptions):
                rect = desc["rect"]
                if not desc["matched"]:
                    pygame.draw.rect(screen, (50, 50, 50), rect, border_radius=20)
                    pygame.draw.rect(screen, (100, 100, 100), rect, 2, border_radius=20)
                    lines = wrap_text(desc["text"], font_text, 220)
                    for k, line in enumerate(lines):
                        desc_text = font_text.render(line, True, TEXT_COLOR)
                        screen.blit(desc_text, (rect.x + 15, rect.y + 28 + k * 25))
                else:
                    ok_text = font_big.render("✓", True, GREEN_OK)
                    screen.blit(ok_text, (rect.x + 108, rect.y + 28))
                    lines = wrap_text(desc["text"], font_text, 220)
                    for k, line in enumerate(lines):
                        desc_text = font_text.render(line, True, GRAY)
                        screen.blit(desc_text, (rect.x + 15, rect.y + 28 + k * 25))

            if self.message_timer > 0:
                msg_color = GREEN_OK if "Правильно" in self.message else RED
                msg_text = font_text.render(self.message, True, msg_color)
                msg_rect = msg_text.get_rect(center=(self.panel_x + self.panel_w//2, self.panel_y + self.panel_h - 45))
                screen.blit(msg_text, msg_rect)
                self.message_timer -= 1

# Слайды
slides = [
    {"title": "ДОБРО ПОЖАЛОВАТЬ!", "text": "Твоя задача - долететь на воздушном шаре до города за 60 секунд.\n\nУправляй высотой, лови ветер в зелёных зонах и избегай птиц!", "color": HIGHLIGHT},
    {"title": "ЧТО ТАКОЕ ВОЗДУШНЫЙ ШАР?", "text": "Воздушный шар - это летательный аппарат, который использует нагретый воздух для подъёма.\n\nПринцип работы: тёплый воздух внутри шара легче холодного воздуха снаружи. Это создаёт подъёмную силу, и шар взлетает!", "color": (220, 120, 120)},
    {"title": "ИЗ ЧЕГО СОСТОИТ ШАР?", "text": "Оболочка - содержит горячий воздух и придаёт шару форму\nКорзина - место для пассажиров\nГорелка - нагревает воздух внутри оболочки\nБалласт - мешки с песком для регулировки массы\nКлапан - выпускает горячий воздух для снижения\nВеревки - соединяют корзину с оболочкой", "color": (120, 180, 240)},
    {"title": "ИСТОРИЯ ВОЗДУХОПЛАВАНИЯ", "text": "Первый полёт на воздушном шаре совершили братья Монгольфье в 1783 году.\n\nИнтересный факт: первыми пассажирами были баран, петух и утка! Они благополучно приземлились через 8 минут.", "color": (120, 220, 140)},
    {"title": "КАК ШАР ПОДНИМАЕТСЯ?", "text": "Горелка нагревает воздух внутри оболочки. Тёплый воздух расширяется и становится легче холодного.\n\nЭто похоже на дым от костра - он всегда поднимается вверх. Шар становится легче окружающего воздуха и взлетает!", "color": (240, 200, 100)},
    {"title": "СИЛА АРХИМЕДА", "text": "На любой предмет в жидкости или газе действует выталкивающая сила.\n\nФормула: F = ρ · g · V\n\nρ (ро) - плотность воздуха\ng - ускорение свободного падения\nV - объём шара\n\nТёплый воздух легче → выталкивающая сила больше веса шара → шар взлетает!", "color": (200, 150, 200)},
    {"title": "ПОЧЕМУ НЕ УЛЕТАЕТ В КОСМОС?", "text": "С высотой воздух становится разреженнее. Плотность воздуха уменьшается, а значит, уменьшается и выталкивающая сила.\n\nНаступает момент, когда выталкивающая сила сравнивается с весом шара. Это называется равновесием - шар зависает на определённой высоте.", "color": (100, 200, 255)},
    {"title": "УПРАВЛЕНИЕ: ВВЕРХ И ВНИЗ", "text": "ВВЕРХ:\n• Сбросить балласт (мешки с песком) - масса уменьшается\n• Включить горелку сильнее - воздух теплее, подъёмная сила больше\n\nВНИЗ:\n• Открыть клапан - выпустить горячий воздух\n• Выключить горелку - воздух остывает, шар становится тяжелее", "color": (220, 120, 120)},
    {"title": "УПРАВЛЕНИЕ: ВПРАВО И ВЛЕВО", "text": "Воздушный шар не имеет двигателя! Он движется туда, куда дует ветер.\n\nХитрость в том, что на разной высоте ветры дуют в разные стороны. Меняя высоту, можно поймать нужный ветер и лететь в нужном направлении!\n\nВ игре зелёные зоны показывают, где дует попутный ветер.", "color": (120, 180, 240)},
    {"title": "МИНИ-ИГРА", "text": "Сопоставь детали с их описанием!\n\nКликни на картинку детали, затем на её описание.", "color": (120, 220, 140)},
    {"title": "ТВОЯ ОЧЕРЕДЬ!", "text": "Теперь ты готов к полёту!\n\nУправляй шаром с помощью кнопок:\n🟤 Балласт - подъём вверх\n⚪ Клапан - спуск вниз\n\nПопадай в зелёные зоны - там ветер поможет двигаться вперёд.\nИзбегай птиц! У тебя есть 60 секунд.\n\nУдачи!", "color": (240, 200, 100)},
    {"title": "ПОЗДРАВЛЯЮ!", "text": "Ты успешно долетел до города!\n\nТеперь нужно безопасно приземлиться.", "color": HIGHLIGHT},
    {"title": "ПОСАДКА", "text": "Нажми кнопку СПУСК, чтобы выпустить воздух и плавно опустить шар на землю.", "color": (100, 200, 255), "type": "landing"},
    {"title": "ИНТЕРЕСНЫЙ ФАКТ", "text": "Первый полёт человека на воздушном шаре длился 25 минут! Пилоты пролетели около 9 километров над Парижем.", "color": (200, 150, 200)},
    {"title": "ИНТЕРЕСНЫЙ ФАКТ", "text": "Самый большой воздушный шар в мире мог поднять 8 человек и имел объём 15 000 кубических метров!", "color": (120, 220, 140)},
    {"title": "ИНТЕРЕСНЫЙ ФАКТ", "text": "Воздушные шары до сих пор используются для научных исследований стратосферы. Они могут подниматься на высоту до 40 км!", "color": (220, 120, 120)},
    {"title": "ФИНИШ", "text": "Уровень пройден!", "color": HIGHLIGHT, "type": "finish"}
]

# Игровые переменные
current_slide = 0
button_hovered = False
game_started = False
rising_to_start_height = False
balloon_speed = 0
balloon_acceleration = 0.02
max_speed = 2.0
color_shift = 0
total_progress = 0
game_timer = GAME_TIME_LIMIT
game_time_started = False
landing_mode = False
landing_speed = 1.5
finish_overlay = False
finish_timer = 0
slider_visible = True  # Видимость слайдера обучения

# Кнопки
BUTTON_SIZE = 60
BALAST_BUTTON = pygame.Rect(40, HEIGHT - 80, BUTTON_SIZE, BUTTON_SIZE)
KLAPAN_BUTTON = pygame.Rect(120, HEIGHT - 80, BUTTON_SIZE, BUTTON_SIZE)
LANDING_BUTTON = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50)

# Камера
world_offset_x = 0
world_offset_y = 0
target_offset_x = 0
target_offset_y = 0
camera_follow_speed = 0.05
camera_active = False

# Стартовое меню
START_BUTTON = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 40, 300, 60)
EXIT_BUTTON = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 40, 300, 60)
show_start_menu = True

game_mode = "tutorial"
current_game = None

birds = []
bird_spawn_timer = 0
bird_spawn_delay = 2500
max_birds = 3
game_over = False
restart_button = None

hint_system = HintSystem()

balloon_rising = False

def get_zone_info():
    zones = []
    top_top = zone_center_y - ZONE_HEIGHT - ZONE_SPACING - ZONE_HEIGHT//2
    top_bottom = zone_center_y - ZONE_HEIGHT - ZONE_SPACING + ZONE_HEIGHT//2
    zones.append({'center': zone_center_y - ZONE_HEIGHT - ZONE_SPACING, 'top': top_top, 'bottom': top_bottom})
    mid_top = zone_center_y - ZONE_HEIGHT//2
    mid_bottom = zone_center_y + ZONE_HEIGHT//2
    zones.append({'center': zone_center_y, 'top': mid_top, 'bottom': mid_bottom})
    bot_top = zone_center_y + ZONE_HEIGHT + ZONE_SPACING - ZONE_HEIGHT//2
    bot_bottom = zone_center_y + ZONE_HEIGHT + ZONE_SPACING + ZONE_HEIGHT//2
    zones.append({'center': zone_center_y + ZONE_HEIGHT + ZONE_SPACING, 'top': bot_top, 'bottom': bot_bottom})
    return zones

def get_zone_center_y(zone):
    return get_zone_info()[zone]['center']

def check_zone():
    global current_zone, in_green_zone
    balloon_center_y = balloon_y + balloon_height // 2
    zones = get_zone_info()
    for i, zone in enumerate(zones):
        if zone['top'] <= balloon_center_y <= zone['bottom']:
            current_zone = i
            break
    was_in_green = in_green_zone
    in_green_zone = (current_zone == color_config)
    if in_green_zone and not was_in_green and game_started:
        hint_system.show_hint("first_green_zone")
    return current_zone, in_green_zone

def set_target_zone(zone):
    global target_zone
    if game_completed or game_over:
        return
    target_zone = zone

def update_balloon_position():
    global balloon_y
    if game_completed or game_over:
        return
    target_y = get_zone_center_y(target_zone) - balloon_height // 2
    min_y = 100
    max_y = GROUND_LEVEL - balloon_height
    if abs(balloon_y - target_y) > move_speed:
        if balloon_y < target_y:
            balloon_y = min(balloon_y + move_speed, target_y)
        else:
            balloon_y = max(balloon_y - move_speed, target_y)
    else:
        balloon_y = target_y
    balloon_y = max(min_y, min(balloon_y, max_y))
    check_zone()

def change_colors():
    global color_config, color_change_counter
    if game_completed or game_over:
        return
    options = [0, 1, 2]
    options.remove(color_config)
    color_config = random.choice(options)
    color_change_counter += 1
    check_zone()

def complete_game():
    global game_completed, current_slide, game_started, landing_mode, final_rise_active
    game_completed = True
    final_rise_active = False
    game_started = False
    landing_mode = False
    current_slide = 11  # Поздравление

def start_landing():
    global landing_mode, current_slide, game_started
    landing_mode = True
    current_slide = 12  # Переходим к следующему слайду после посадки

def finish_level():
    global finish_overlay, finish_timer
    finish_overlay = True
    finish_timer = 180  # 3 секунды

def restart_game():
    global game_over, balloon_x, balloon_y, birds, bird_spawn_timer, color_change_counter
    global game_completed, final_rise_active, color_config
    global current_zone, target_zone, in_green_zone, world_offset_x, world_offset_y
    global rising_to_start_height, balloon_speed, current_slide
    global game_started, show_start_menu, game_mode, current_game, hint_system, balloon_rising
    global total_progress, game_timer, game_time_started, landing_mode, finish_overlay, finish_timer
    global slider_visible

    game_over = False
    balloon_x = 300
    balloon_y = GROUND_LEVEL - balloon_height + 50
    birds = []
    bird_spawn_timer = 0
    color_change_counter = 0
    game_completed = False
    final_rise_active = False
    color_config = 1
    total_progress = 0
    game_timer = GAME_TIME_LIMIT
    game_time_started = False
    current_zone = 1
    target_zone = 1
    in_green_zone = False
    rising_to_start_height = False
    balloon_speed = 0
    current_slide = 0
    game_started = False
    show_start_menu = True
    game_mode = "tutorial"
    current_game = None
    hint_system = HintSystem()
    balloon_rising = False
    landing_mode = False
    finish_overlay = False
    finish_timer = 0
    slider_visible = True
    target_offset_x = balloon_x - WIDTH//2 + balloon_width//2
    target_offset_y = (GROUND_LEVEL - 200) - HEIGHT//2
    world_offset_x = target_offset_x
    world_offset_y = target_offset_y

# Основной цикл
clock = pygame.time.Clock()
running = True
last_time = pygame.time.get_ticks()

while running:
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()

    # Обновление финального затемнения
    if finish_overlay:
        finish_timer -= 1
        if finish_timer <= 0:
            finish_overlay = False
            restart_game()

    # Спуск шара при посадке
    if landing_mode and not game_over:
        balloon_y += landing_speed
        if balloon_y >= GROUND_LEVEL - balloon_height:
            balloon_y = GROUND_LEVEL - balloon_height
            landing_mode = False
            finish_level()

    if balloon_rising and not game_started:
        balloon_y -= 3

    # Обновление таймера
    if game_started and not game_completed and not game_over and game_mode == "tutorial":
        if not game_time_started:
            game_time_started = True
            last_time = current_time
        else:
            if current_time - last_time >= 1000:
                game_timer -= 1
                last_time = current_time
                if game_timer <= 0:
                    game_over = True

    # Спавн птиц
    if game_started and not game_completed and not game_over and game_mode == "tutorial":
        bird_spawn_timer += dt
        if bird_spawn_timer >= bird_spawn_delay:
            bird_spawn_timer = 0
            occupied_zones = [bird.zone for bird in birds]
            free_zones = [z for z in range(3) if z not in occupied_zones]
            if free_zones and len(birds) < max_birds:
                if random.random() > 0.3:
                    zone_choice = random.choice(free_zones)
                    birds.append(Bird(zone_choice, zone_center_y, bird_frames))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                pass
            elif event.key == pygame.K_ESCAPE and game_mode != "tutorial":
                game_mode = "tutorial"
            elif event.key == pygame.K_SPACE and game_mode == "tutorial" and not game_started and not show_start_menu:
                slider_visible = not slider_visible
        elif event.type == pygame.MOUSEMOTION:
            if show_start_menu:
                button_hovered = START_BUTTON.collidepoint(event.pos) or EXIT_BUTTON.collidepoint(event.pos)
            elif (not game_started or game_completed) and not rising_to_start_height and game_mode == "tutorial":
                panel_x = WIDTH - 350
                button_x = panel_x + 200
                button_y = HEIGHT - 70
                button_hovered = pygame.Rect(button_x, button_y, 120, 40).collidepoint(event.pos)
            if game_over and restart_button:
                button_hovered = restart_button.collidepoint(event.pos)
            if landing_mode and LANDING_BUTTON.collidepoint(event.pos):
                button_hovered = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if show_start_menu:
                if START_BUTTON.collidepoint(event.pos):
                    show_start_menu = False
                    game_started = False
                    current_slide = 0
                elif EXIT_BUTTON.collidepoint(event.pos):
                    running = False
            elif game_mode != "tutorial" and current_game:
                current_game.handle_event(event)
            elif game_started and not game_completed and not game_over and game_mode == "tutorial":
                if BALAST_BUTTON.collidepoint(event.pos) and current_zone > 0:
                    set_target_zone(current_zone - 1)
                    hint_system.show_hint("balast")
                elif KLAPAN_BUTTON.collidepoint(event.pos) and current_zone < 2:
                    set_target_zone(current_zone + 1)
                    hint_system.show_hint("klapan")
            if game_over and restart_button and restart_button.collidepoint(event.pos):
                restart_game()

            # Навигация по слайдам
            if (not game_started or game_completed) and not rising_to_start_height and not show_start_menu and game_mode == "tutorial":
                panel_x = WIDTH - 350
                button_x = panel_x + 200
                button_y = HEIGHT - 70
                if pygame.Rect(button_x, button_y, 120, 40).collidepoint(event.pos):
                    if current_slide == 0:
                        current_slide = 1
                        balloon_rising = True
                    elif current_slide == 1:
                        current_slide = 2
                    elif current_slide == 2:
                        current_slide = 3
                    elif current_slide == 3:
                        current_slide = 4
                    elif current_slide == 4:
                        current_slide = 5
                    elif current_slide == 5:
                        current_slide = 6
                    elif current_slide == 6:
                        current_slide = 7
                    elif current_slide == 7:
                        current_slide = 8
                        game_mode = "game3"
                        current_game = MatchingGame()
                    elif current_slide == 8:
                        current_slide = 9
                    elif current_slide == 9 and not game_started:
                        game_started = True
                        rising_to_start_height = True
                        balloon_speed = 0
                        game_timer = GAME_TIME_LIMIT
                        game_time_started = False
                    elif current_slide == 10:
                        complete_game()
                    elif current_slide == 11:
                        current_slide = 12
                    elif current_slide == 12:
                        current_slide = 13
                    elif current_slide == 13:
                        current_slide = 14
                    elif current_slide == 14:
                        current_slide = 15
                    elif current_slide == 15:
                        show_start_menu = True
                        restart_game()

            # Кнопка спуска
            if landing_mode and LANDING_BUTTON.collidepoint(event.pos):
                start_landing()

    if game_mode == "game3" and current_game and current_game.completed:
        game_mode = "tutorial"
        current_slide = 9

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
            zone_center_y = balloon_y + balloon_height // 2
            color_config = 1
            target_zone = 1

    if game_started and not game_over and game_mode == "tutorial" and not game_completed:
        update_balloon_position()
        check_zone()
        for bird in birds[:]:
            bird.update()
            if bird.is_offscreen():
                birds.remove(bird)

        hitbox_reduction = 0.8
        hitbox_width = int(balloon_width * hitbox_reduction)
        hitbox_height = int(balloon_height * hitbox_reduction)
        balloon_rect = pygame.Rect(
            balloon_x - hitbox_width//2,
            balloon_y - hitbox_height//2,
            hitbox_width,
            hitbox_height
        )

        for bird in birds[:]:
            if bird.check_collision(balloon_rect):
                game_over = True
                hint_system.show_hint("bird")
                break

        if in_green_zone and not game_over and not game_completed:
            balloon_x += wind_speed
            total_progress += wind_speed
            if total_progress >= TARGET_DISTANCE:
                complete_game()
            if int(total_progress / distance_for_color_change) > color_change_counter:
                change_colors()

    hint_system.update()

    # Обновление облаков
    for cloud in clouds:
        cloud['x'] -= cloud['speed']
        if cloud['x'] < -300:
            cloud['x'] = WORLD_WIDTH + random.randint(100, 500)

    current_height = GROUND_LEVEL - balloon_y - balloon_height
    if current_height >= CAMERA_TRIGGER_HEIGHT:
        camera_active = True
    else:
        camera_active = False
        target_offset_x = balloon_x - WIDTH//2 + balloon_width//2
        target_offset_y = (GROUND_LEVEL - 200) - HEIGHT//2
    if camera_active:
        target_offset_x = balloon_x - WIDTH//2 + balloon_width//2
        target_offset_y = balloon_y - HEIGHT//2 + balloon_height//2
    world_offset_x += (target_offset_x - world_offset_x) * camera_follow_speed
    world_offset_y += (target_offset_y - world_offset_y) * camera_follow_speed

    # Отрисовка фона
    for i in range(HEIGHT):
        ratio = i / HEIGHT
        r = int(135 * (1-ratio) + 200 * ratio)
        g = int(206 * (1-ratio) + 230 * ratio)
        b = int(235 * (1-ratio) + 255 * ratio)
        pygame.draw.line(screen, (r, g, b), (0, i), (WIDTH, i))

    if sun_img:
        screen.blit(sun_img, (800 - world_offset_x * 0.1, 50 - world_offset_y * 0.1))

    for cloud in clouds:
        cx = cloud['x'] - world_offset_x
        cy = cloud['y'] - world_offset_y
        if -300 < cx < WIDTH + 300:
            screen.blit(cloud['image'], (cx, cy))

    if gora_img:
        screen.blit(gora_img, (gora_x - world_offset_x, gora_y - world_offset_y))

    ground_y = GROUND_LEVEL - world_offset_y
    if ground_y < HEIGHT and terra_img:
        terra_stretched = pygame.transform.scale(terra_img, (WIDTH, terra_img.get_height()))
        screen.blit(terra_stretched, (0, ground_y))

    for tree in trees:
        tx = tree['x'] - world_offset_x
        ty = tree['y'] - world_offset_y
        if -100 < tx < WIDTH + 100:
            screen.blit(tree['image'], (tx, ty))

    if game_started and not game_completed and not game_over:
        for bird in birds:
            bird.draw(screen, world_offset_x, world_offset_y)

    # Визуализация ветра
    if game_started and not game_over and in_green_zone and not game_completed:
        time_offset = pygame.time.get_ticks() * 0.15
        zones = get_zone_info()
        center_y = zones[color_config]['center'] - world_offset_y

        for row in range(3):
            row_offset = (row - 1) * 12
            y_pos = center_y + row_offset
            for i in range(15):
                x_pos = (time_offset + i * 55 + row * 25) % (WIDTH + 300) - 150
                length = 70 + (i % 3) * 20
                for j in range(3):
                    line_x = x_pos + j * 4
                    pygame.draw.line(screen, (255, 255, 255),
                                   (line_x, y_pos),
                                   (line_x + length, y_pos), 2)

    if original_balloon:
        balloon_screen_x = balloon_x - world_offset_x
        balloon_screen_y = balloon_y - world_offset_y
        screen.blit(original_balloon, (balloon_screen_x, balloon_screen_y))

    # Прогресс-бар и таймер
    if game_started and not game_completed and not game_over:
        bar_width = 300
        bar_height = 20
        bar_x = WIDTH - bar_width - 30
        bar_y = 30
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=10)
        fill_width = int((total_progress / TARGET_DISTANCE) * bar_width)
        if fill_width > 0:
            pygame.draw.rect(screen, (100, 255, 100), (bar_x, bar_y, fill_width, bar_height), border_radius=10)
        pygame.draw.rect(screen, HIGHLIGHT, (bar_x, bar_y, bar_width, bar_height), 2, border_radius=10)

        timer_size = 70
        timer_x = 30
        timer_y = 25
        timer_angle = (game_timer / GAME_TIME_LIMIT) * 360

        pygame.draw.circle(screen, (50, 50, 50), (timer_x + timer_size//2, timer_y + timer_size//2), timer_size//2)
        pygame.draw.circle(screen, (80, 80, 80), (timer_x + timer_size//2, timer_y + timer_size//2), timer_size//2 - 2)

        if game_timer > 0:
            for i in range(int(timer_angle)):
                angle_rad = math.radians(i)
                x = timer_x + timer_size//2 + int((timer_size//2 - 5) * math.cos(angle_rad))
                y = timer_y + timer_size//2 + int((timer_size//2 - 5) * math.sin(angle_rad))
                pygame.draw.circle(screen, (100, 255, 100), (x, y), 2)

        pygame.draw.circle(screen, (28, 28, 40), (timer_x + timer_size//2, timer_y + timer_size//2), timer_size//2 - 8)
        timer_text = font_big.render(f"{game_timer}", True, HIGHLIGHT)
        timer_text_rect = timer_text.get_rect(center=(timer_x + timer_size//2, timer_y + timer_size//2))
        screen.blit(timer_text, timer_text_rect)

    hint_system.draw(screen)

    # Отрисовка меню
    if show_start_menu:
        for i in range(HEIGHT):
            ratio = i / HEIGHT
            r = int(135 * (1-ratio) + 200 * ratio)
            g = int(206 * (1-ratio) + 230 * ratio)
            b = int(235 * (1-ratio) + 255 * ratio)
            pygame.draw.line(screen, (r, g, b), (0, i), (WIDTH, i))

        title_text = font_game_title.render("PhysSim", True, (50, 50, 80))
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 80))
        screen.blit(title_text, title_rect)

        start_color = BUTTON_HOVER if START_BUTTON.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(screen, start_color, START_BUTTON, border_radius=15)
        pygame.draw.rect(screen, WHITE, START_BUTTON, 3, border_radius=15)
        start_text = font_button.render("НАЧАТЬ", True, WHITE)
        screen.blit(start_text, start_text.get_rect(center=START_BUTTON.center))

        exit_color = BUTTON_HOVER if EXIT_BUTTON.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(screen, exit_color, EXIT_BUTTON, border_radius=15)
        pygame.draw.rect(screen, WHITE, EXIT_BUTTON, 3, border_radius=15)
        exit_text = font_button.render("ВЫЙТИ", True, WHITE)
        screen.blit(exit_text, exit_text.get_rect(center=EXIT_BUTTON.center))

    elif game_mode != "tutorial" and current_game:
        current_game.draw(screen)
        esc_text = font_small.render("ESC - выйти", True, WHITE)
        screen.blit(esc_text, (WIDTH - 100, HEIGHT - 30))

    else:
        # Слайдер обучения
        if (not game_started or game_completed) and not rising_to_start_height and not show_start_menu and game_mode == "tutorial" and slider_visible:
            panel_x = WIDTH - 350
            panel_y = 20
            panel_w = 330
            panel_h = HEIGHT - 40
            pulse = math.sin(color_shift) * 15

            color = slides[current_slide]["color"]
            animated_color = (max(0, min(255, color[0] + int(pulse))),
                             max(0, min(255, color[1] + int(pulse * 0.5))),
                             max(0, min(255, color[2] + int(pulse * 0.8))))

            pygame.draw.rect(screen, PANEL_BG, (panel_x, panel_y, panel_w, panel_h), border_radius=20)
            pygame.draw.rect(screen, animated_color, (panel_x, panel_y, panel_w, panel_h), 3, border_radius=20)

            title_lines = wrap_title(slides[current_slide]["title"], font_title, panel_w - 40)
            y_offset = panel_y + 30
            for line in title_lines:
                render_text_with_shadow(line, font_title, animated_color, TEXT_SHADOW, panel_x + 20, y_offset)
                y_offset += 38

            text_lines = slides[current_slide]["text"].split('\n')
            for paragraph in text_lines:
                if paragraph.strip():
                    wrapped = wrap_text(paragraph, font_text, panel_w - 40)
                    for line in wrapped:
                        text_surf = font_text.render(line, True, TEXT_COLOR)
                        screen.blit(text_surf, (panel_x + 20, y_offset))
                        y_offset += 28
                else:
                    y_offset += 15

            # Кнопка для слайда посадки
            if current_slide == 12:  # Слайд с кнопкой спуска
                landing_btn_x = panel_x + panel_w//2 - 100
                landing_btn_y = panel_y + panel_h - 80
                landing_btn_rect = pygame.Rect(landing_btn_x, landing_btn_y, 200, 50)
                btn_color = BUTTON_HOVER if landing_btn_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
                pygame.draw.rect(screen, btn_color, landing_btn_rect, border_radius=15)
                landing_text = font_button.render("СПУСК", True, WHITE)
                screen.blit(landing_text, landing_text.get_rect(center=landing_btn_rect.center))
                button_hovered = landing_btn_rect.collidepoint(pygame.mouse.get_pos())
                # Обработка клика на кнопку спуска
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if landing_btn_rect.collidepoint(event.pos):
                        start_landing()
            else:
                button_x = panel_x + panel_w - 130
                button_y = panel_y + panel_h - 50
                btn_color = BUTTON_HOVER if button_hovered else BUTTON_COLOR
                pygame.draw.rect(screen, btn_color, (button_x, button_y, 120, 40), border_radius=10)

                if current_slide == 8:
                    btn_text = "ИГРАТЬ"
                elif current_slide == 9 and not game_started:
                    btn_text = "СТАРТ"
                elif current_slide == 10:
                    btn_text = "ДАЛЕЕ"
                elif current_slide == 11:
                    btn_text = "ДАЛЕЕ"
                elif current_slide == 12:
                    btn_text = "СПУСК"
                else:
                    btn_text = "ДАЛЕЕ"
                text = font_button.render(btn_text, True, TEXT_COLOR)
                screen.blit(text, text.get_rect(center=(button_x + 60, button_y + 20)))

        # Подсказка о скрытии/показе слайдера
        if (not game_started or game_completed) and not rising_to_start_height and not show_start_menu and game_mode == "tutorial":
            hint_text = font_small.render("Пробел - скрыть/показать панель", True, (200, 200, 200))
            screen.blit(hint_text, (10, HEIGHT - 30))

        # Кнопки управления
        if game_started and not game_completed and not game_over and game_mode == "tutorial":
            pygame.draw.rect(screen, (139, 69, 19), BALAST_BUTTON, border_radius=10)
            if balast_img:
                scaled = pygame.transform.scale(balast_img, (45, 45))
                screen.blit(scaled, (BALAST_BUTTON.x + 8, BALAST_BUTTON.y + 8))
            pygame.draw.rect(screen, HIGHLIGHT, BALAST_BUTTON, 2, border_radius=10)

            pygame.draw.rect(screen, (100, 100, 100), KLAPAN_BUTTON, border_radius=10)
            if klapan_img:
                scaled = pygame.transform.scale(klapan_img, (45, 45))
                screen.blit(scaled, (KLAPAN_BUTTON.x + 8, KLAPAN_BUTTON.y + 8))
            pygame.draw.rect(screen, HIGHLIGHT, KLAPAN_BUTTON, 2, border_radius=10)

        # GAME OVER
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            game_over_text = font_big.render("GAME OVER", True, RED)
            screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
            restart_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50)
            btn_color = BUTTON_HOVER if button_hovered else BUTTON_COLOR
            pygame.draw.rect(screen, btn_color, restart_button, border_radius=10)
            pygame.draw.rect(screen, WHITE, restart_button, 2, border_radius=10)
            restart_text = font_button.render("В МЕНЮ", True, WHITE)
            screen.blit(restart_text, restart_text.get_rect(center=restart_button.center))

        # Финальное затемнение
        if finish_overlay:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            alpha = int(255 * (1 - finish_timer / 180))
            overlay.set_alpha(alpha)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            if finish_timer < 120:
                complete_text = font_big.render("УРОВЕНЬ ПРОЙДЕН!", True, HIGHLIGHT)
                complete_rect = complete_text.get_rect(center=(WIDTH//2, HEIGHT//2))
                screen.blit(complete_text, complete_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()