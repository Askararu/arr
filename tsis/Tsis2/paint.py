import pygame
import sys
from datetime import datetime
from tools import flood_fill, draw_rhombus, draw_equilateral_triangle

pygame.init()

WIDTH, HEIGHT = 1000, 800 
TOOLBAR_HEIGHT = 100
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Paint with UI")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)


canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

current_tool = 'pencil'
current_color = BLACK
brush_size = 5
is_drawing = False
start_pos = None
last_pos = None


typing = False
text_buffer = ""
text_pos = (0, 0)
font = pygame.font.SysFont("Arial", 18)


tools = [
    {'name': 'pencil', 'label': 'Pencil'},
    {'name': 'line', 'label': 'Line'},
    {'name': 'rect', 'label': 'Rect'},
    {'name': 'circle', 'label': 'Circle'},
    {'name': 'eraser', 'label': 'Eraser'},
    {'name': 'flood_fill', 'label': 'Fill'},
    {'name': 'text', 'label': 'Text'},
    {'name': 'rhombus', 'label': 'Rhombus'}
]

colors = [BLACK, RED, GREEN, BLUE, WHITE]

def draw_ui():
    
    pygame.draw.rect(screen, GRAY, (0, CANVAS_HEIGHT, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, CANVAS_HEIGHT), (WIDTH, CANVAS_HEIGHT), 2)
    
    #инструментики
    for i, tool in enumerate(tools):
        rect = pygame.Rect(10 + i * 85, CANVAS_HEIGHT + 10, 80, 35)
        color = DARK_GRAY if current_tool == tool['name'] else WHITE
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        
        text_surf = font.render(tool['label'], True, BLACK)
        screen.blit(text_surf, (rect.x + 5, rect.y + 10))
    
    # цвет
    for i, color in enumerate(colors):
        rect = pygame.Rect(10 + i * 40, CANVAS_HEIGHT + 55, 30, 30)
        pygame.draw.rect(screen, color, rect)
        border_color = WHITE if color == BLACK else BLACK
        pygame.draw.rect(screen, border_color, rect, 2)
        if current_color == color:
             pygame.draw.rect(screen, (255, 255, 0), rect, 3)


    size_label = font.render(f"Size: {brush_size}px", True, BLACK)
    screen.blit(size_label, (WIDTH - 150, CANVAS_HEIGHT + 20))
    
    save_hint = font.render("Ctrl+S to Save", True, BLACK)
    screen.blit(save_hint, (WIDTH - 150, CANVAS_HEIGHT + 50))

def save_canvas(surface):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"paint_{timestamp}.png"
    pygame.image.save(surface, filename)
    print(f"Saved: {filename}")

running = True
while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))
    
    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            
            if mouse_y > CANVAS_HEIGHT:
        
                for i, tool in enumerate(tools):
                    rect = pygame.Rect(10 + i * 85, CANVAS_HEIGHT + 10, 80, 35)
                    if rect.collidepoint(event.pos):
                        current_tool = tool['name']
                        if current_tool == 'eraser': current_color = WHITE
                
                
                for i, color in enumerate(colors):
                    rect = pygame.Rect(10 + i * 40, CANVAS_HEIGHT + 55, 30, 30)
                    if rect.collidepoint(event.pos):
                        current_color = color
            else:
        
                is_drawing = True
                start_pos = event.pos
                if current_tool == 'flood_fill':
                    flood_fill(canvas, *event.pos, current_color)
                elif current_tool == 'text':
                    typing = True
                    text_pos = event.pos
                    text_buffer = ""

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                save_canvas(canvas)
            
            
            if event.key == pygame.K_1: brush_size = 2
            if event.key == pygame.K_2: brush_size = 5
            if event.key == pygame.K_3: brush_size = 10

            if typing:
                if event.key == pygame.K_RETURN:
                    txt_surf = font.render(text_buffer, True, current_color)
                    canvas.blit(txt_surf, text_pos)
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                else:
                    text_buffer += event.unicode

        if event.type == pygame.MOUSEBUTTONUP:
            if is_drawing and start_pos:
                # Рисуем финальную фигуру на холсте
                if current_tool == 'line':
                    pygame.draw.line(canvas, current_color, start_pos, event.pos, brush_size)
                elif current_tool == 'rect':
                    rect_data = (min(start_pos[0], event.pos[0]), min(start_pos[1], event.pos[1]), 
                                 abs(event.pos[0]-start_pos[0]), abs(event.pos[1]-start_pos[1]))
                    pygame.draw.rect(canvas, current_color, rect_data, brush_size)
                elif current_tool == 'circle':
                    radius = int(((event.pos[0]-start_pos[0])**2 + (event.pos[1]-start_pos[1])**2)**0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)
                elif current_tool == 'rhombus':
                    draw_rhombus(canvas, current_color, start_pos, event.pos, brush_size)
                
            is_drawing = False
            last_pos = None

    
    if is_drawing and current_tool in ['pencil', 'eraser']:
        curr_pos = pygame.mouse.get_pos()
        if curr_pos[1] < CANVAS_HEIGHT: # Не рисуем на панели
            if last_pos:
                pygame.draw.line(canvas, current_color, last_pos, curr_pos, brush_size)
            last_pos = curr_pos

    
    if is_drawing and current_tool in ['line', 'rect', 'circle', 'rhombus']:
        curr_pos = pygame.mouse.get_pos()
        if curr_pos[1] < CANVAS_HEIGHT:
            if current_tool == 'line':
                pygame.draw.line(screen, current_color, start_pos, curr_pos, brush_size)
            elif current_tool == 'rect':
                rect_preview = (min(start_pos[0], curr_pos[0]), min(start_pos[1], curr_pos[1]), 
                                abs(curr_pos[0]-start_pos[0]), abs(curr_pos[1]-start_pos[1]))
                pygame.draw.rect(screen, current_color, rect_preview, brush_size)

    if typing:
        preview_txt = font.render(text_buffer + "|", True, current_color)
        screen.blit(preview_txt, text_pos)

    pygame.display.flip()

pygame.quit()