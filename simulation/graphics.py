import math
import pygame
from simulation.config import CONFIG as cfg

def draw_compass(surface, vx, vy, x, y, size=40):
    pygame.draw.circle(surface, cfg['COMPASS_COLOR'], (x, y), size, 2)
    pygame.draw.line(surface, cfg['COMPASS_COLOR'], (x - size, y), (x + size, y), 1)
    pygame.draw.line(surface, cfg['COMPASS_COLOR'], (x, y - size), (x, y + size), 1)
    
    if vx == 0 and vy == 0:
        return
    
    angle = math.atan2(vy, vx)
    arrow_length = size * 0.8
    end_x = x + arrow_length * math.cos(angle)
    end_y = y + arrow_length * math.sin(angle)
    
    pygame.draw.aaline(surface, cfg['ARROW_COLOR'], (x, y), (end_x, end_y))
    
    arrow_size = size * 0.2
    pygame.draw.aaline(surface, cfg['ARROW_COLOR'], (end_x, end_y), 
                   (end_x + arrow_size * math.cos(angle + math.pi * 0.8), 
                    end_y + arrow_size * math.sin(angle + math.pi * 0.8)))
    
    pygame.draw.aaline(surface, cfg['ARROW_COLOR'], (end_x, end_y), 
                   (end_x + arrow_size * math.cos(angle - math.pi * 0.8), 
                    end_y + arrow_size * math.sin(angle - math.pi * 0.8)))

def draw_gravity_grid(surface, bodies, camera_x, camera_y, scale):
    grid_size = cfg['GRID_SIZE']
    num_horizontal = int(surface.get_height() // grid_size) + 2
    num_vertical = int(surface.get_width() // grid_size) + 2
    
    points = []
    for i in range(num_horizontal):
        row = []
        for j in range(num_vertical):
            world_x = (j - num_vertical//2) * grid_size
            world_y = (i - num_horizontal//2) * grid_size
            
            dx, dy = 0, 0
            for body in bodies:
                if body.is_static:
                    dist_x = world_x - body.x
                    dist_y = world_y - body.y
                    distance = max(math.sqrt(dist_x**2 + dist_y**2), 1)
                    force = body.mass / (distance**1.7) * 40
                    dx += -force * dist_x / distance
                    dy += -force * dist_y / distance
            
            screen_x = (world_x + dx - camera_x) * scale + surface.get_width()/2
            screen_y = (world_y + dy - camera_y) * scale + surface.get_height()/2
            row.append((screen_x, screen_y))
        points.append(row)
    
    # Горизонтальные линии
    for i in range(num_horizontal):
        for j in range(num_vertical - 1):
            x1, y1 = points[i][j]
            x2, y2 = points[i][j+1]
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            if distance < cfg['MAX_GRID_DIST'] * scale:
                pygame.draw.aaline(surface, cfg['GRID_COLOR'], (x1, y1), (x2, y2))
    
    # Вертикальные линии
    for j in range(num_vertical):
        for i in range(num_horizontal - 1):
            x1, y1 = points[i][j]
            x2, y2 = points[i+1][j]
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            if distance < cfg['MAX_GRID_DIST'] * scale:
                pygame.draw.aaline(surface, cfg['GRID_COLOR'], (x1, y1), (x2, y2))

def draw_dashed_line(surface, color, start_pos, end_pos, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    distance = max(1, math.hypot(dx, dy))
    dx, dy = dx / distance, dy / distance
    
    for i in range(0, int(distance), dash_length * 2):
        start = i
        end = min(i + dash_length, distance)
        pygame.draw.aaline(surface, color, 
                          (x1 + dx * start, y1 + dy * start),
                          (x1 + dx * end, y1 + dy * end))

def draw_arrow(surface, color, pos, direction, size=10):
    x, y = pos
    angle = math.atan2(direction[1], direction[0])
    
    arrow_points = [
        (x + size * math.cos(angle), y + size * math.sin(angle)),
        (x + size * 0.5 * math.cos(angle + 2.5), y + size * 0.5 * math.sin(angle + 2.5)),
        (x + size * 0.5 * math.cos(angle - 2.5), y + size * 0.5 * math.sin(angle - 2.5))
    ]
    
    pygame.draw.aalines(surface, color, True, arrow_points)

def world_to_screen(x, y, camera_x, camera_y, scale, screen_width, screen_height):
    """Преобразует мировые координаты в экранные"""
    return (
        (x - camera_x) * scale + screen_width/2,
        (y - camera_y) * scale + screen_height/2
    )
