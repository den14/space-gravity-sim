import pygame
import math
from simulation.config import CONFIG as cfg
from simulation.graphics import (  
    draw_gravity_grid,
    draw_dashed_line,
    draw_arrow,
    world_to_screen,
    draw_compass
)

def draw_ui(surface, station, earth, scale, show_vectors, show_grid, 
            show_info, camera_x, camera_y, current_width, current_height,
            bodies, thrust_particles, thrust_active, thrust_direction):
    
    # Рисование сетки
    if show_grid:
        draw_gravity_grid(surface, bodies, camera_x, camera_y, scale)
    
    # Рисование тел
    for body in bodies:
        body.draw(surface, camera_x, camera_y, scale)
    
    # Векторы сил
    if show_vectors:
        for body in bodies:
            if body is station or not body.is_static:
                continue
                
            dx = body.x - station.x
            dy = body.y - station.y
            distance = max(math.sqrt(dx**2 + dy**2), 1)
            force = cfg['G'] * body.mass / (distance**2)
            
            vector_scale = 50
            end_x = station.x + dx * force * vector_scale
            end_y = station.y + dy * force * vector_scale
            
            start_screen = world_to_screen(station.x, station.y, camera_x, camera_y, scale, 
                                         current_width, current_height)
            end_screen = world_to_screen(end_x, end_y, camera_x, camera_y, scale, 
                                       current_width, current_height)
            
            draw_dashed_line(surface, body.color, start_screen, end_screen, dash_length=8)
            direction_vector = (dx * force * vector_scale, dy * force * vector_scale)
            draw_arrow(surface, body.color, end_screen, direction_vector, size=12)
    
    # Частицы двигателя
    for p in thrust_particles:
        screen_x, screen_y = world_to_screen(p['x'], p['y'], camera_x, camera_y, scale, 
                                           current_width, current_height)
        alpha = min(255, p['life'] * 25)
        particle_surf = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surf, 
                         (*cfg['THRUST_PARTICLE_COLOR'], alpha), 
                         (p['size'], p['size']), 
                         p['size'])
        surface.blit(particle_surf, (screen_x - p['size'], screen_y - p['size']))
    
    # Пламя двигателя
    if thrust_active:
        flame_length = 15
        flame_width = 8
        
        base_x = station.x - cfg['STATION_RADIUS'] * math.cos(thrust_direction)
        base_y = station.y - cfg['STATION_RADIUS'] * math.sin(thrust_direction)
        tip_x = station.x - (cfg['STATION_RADIUS'] + flame_length) * math.cos(thrust_direction)
        tip_y = station.y - (cfg['STATION_RADIUS'] + flame_length) * math.sin(thrust_direction)
        
        perp_angle = thrust_direction + math.pi/2
        side1_x = base_x + flame_width * math.cos(perp_angle)
        side1_y = base_y + flame_width * math.sin(perp_angle)
        side2_x = base_x - flame_width * math.cos(perp_angle)
        side2_y = base_y - flame_width * math.sin(perp_angle)
        
        base_screen = world_to_screen(base_x, base_y, camera_x, camera_y, scale, 
                                    current_width, current_height)
        tip_screen = world_to_screen(tip_x, tip_y, camera_x, camera_y, scale, 
                                   current_width, current_height)
        side1_screen = world_to_screen(side1_x, side1_y, camera_x, camera_y, scale, 
                                     current_width, current_height)
        side2_screen = world_to_screen(side2_x, side2_y, camera_x, camera_y, scale, 
                                     current_width, current_height)
        
        flame_points = [
            (int(base_screen[0]), int(base_screen[1])),
            (int(side1_screen[0]), int(side1_screen[1])),
            (int(tip_screen[0]), int(tip_screen[1])),
            (int(side2_screen[0]), int(side2_screen[1]))
        ]
        
        pygame.draw.aalines(surface, cfg['THRUST_COLOR'], True, flame_points)
    
    # Информационная панель
    if show_info:
        earth_dist = math.sqrt((station.x - earth.x)**2 + (station.y - earth.y)**2)
        speed = math.sqrt(station.vx**2 + station.vy**2)
        
        small_font = pygame.font.SysFont(None, 20)
        medium_font = pygame.font.SysFont(None, 24)
        
        # Основные параметры
        texts_main = [
            f"Скорость: {speed:.2f}",
            f"Расст. до Земли: {earth_dist:.1f}",
            f"Масштаб: {scale:.2f}x"
        ]
        
        for i, text in enumerate(texts_main):
            text_surface = medium_font.render(text, True, cfg['TEXT_COLOR'])
            surface.blit(text_surface, (10, 10 + i * 25))
        
        # Управление
        texts_controls = [
            "Пробел: Пауза/Пуск",
            "R: Новая система",
            "C: Очистить след",
            f"V: Векторы сил: {'ВКЛ' if show_vectors else 'ВЫКЛ'}",
            f"G: Сетка: {'ВКЛ' if show_grid else 'ВЫКЛ'}",
            "F: Случайный импульс",
            "ЛКМ: Импульс к курсору",
            "ПКМ: Перемещение камеры",
            "Колесо: Масштаб",
            "0: Сброс камеры",
            "I: Скрыть/показать инфо",
            "F11: Полный экран"
        ]
        
        for i, text in enumerate(texts_controls):
            text_surface = small_font.render(text, True, (180, 200, 230))
            surface.blit(text_surface, 
                        (current_width - text_surface.get_width() - 10, 
                         current_height - (len(texts_controls) * 20) + i * 20))
        
        # Компас
        compass_x = current_width - 60
        compass_y = 60
        draw_compass(surface, station.vx, station.vy, compass_x, compass_y)
        compass_label = small_font.render("Направление", True, cfg['TEXT_COLOR'])
        surface.blit(compass_label, (compass_x - compass_label.get_width()//2, compass_y + 50))
    else:
        small_font = pygame.font.SysFont(None, 20)
        info_hint = small_font.render("Нажмите I для отображения информации", True, (150, 170, 200))
        surface.blit(info_hint, (current_width - info_hint.get_width() - 10, 10))
