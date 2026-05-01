import pygame

def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    
    width, height = surface.get_size()
    stack = [(x, y)]
    
    while stack:
        cx, cy = stack.pop()
        if 0 <= cx < width and 0 <= cy < height:
            if surface.get_at((cx, cy)) == target_color:
                surface.set_at((cx, cy), new_color)
                # Add neighbors
                stack.append((cx + 1, cy))
                stack.append((cx - 1, cy))
                stack.append((cx, cy + 1))
                stack.append((cx, cy - 1))

def draw_rhombus(surface, color, start_pos, end_pos, width):
    x1, y1 = start_pos
    x2, y2 = end_pos
    center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
    points = [
        (center_x, y1), # Top
        (x2, center_y), # Right
        (center_x, y2), # Bottom
        (x1, center_y)  # Left
    ]
    pygame.draw.polygon(surface, color, points, width)

def draw_equilateral_triangle(surface, color, start_pos, end_pos, width):
    x1, y1 = start_pos
    x2, y2 = end_pos
    side = abs(x2 - x1)
    height = int((3**0.5 / 2) * side)
    points = [
        (x1 + side // 2, y1),           # Top
        (x1, y1 + height),              # Bottom Left
        (x1 + side, y1 + height)         # Bottom Right
    ]
    pygame.draw.polygon(surface, color, points, width)