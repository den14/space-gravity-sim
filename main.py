import pygame
import random
import math
from simulation.config import load_config
from simulation.celestial import create_bodies, CelestialBody
from simulation.graphics import world_to_screen
from simulation.ui import draw_ui

# Загрузка конфигурации
cfg = load_config()

def main():
    pygame.init()
    pygame.display.set_caption("Гравитационная модель с импульсами корабля")
    
    # Инициализация экрана
    screen = pygame.display.set_mode(cfg['SCREEN_SIZE'], pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    # Создание небесных тел
    earth, moon, asteroid, station = create_bodies()
    bodies = [earth, moon, asteroid, station]
    
    # Переменные состояния
    max_speed = 0
    min_speed = float('inf')
    thrust_particles = []
    thrust_direction = 0
    thrust_active = False
    thrust_counter = 0
    camera_dragging = False
    camera_drag_start = (0, 0)
    camera_x, camera_y = 0, 0
    scale = 1.0
    min_scale, max_scale = 0.2, 3.0
    show_info = True
    show_vectors = False
    show_grid = True
    fullscreen = False
    screen_width, screen_height = cfg['SCREEN_SIZE']
    running = True
    paused = True
    
    while running:
        current_width, current_height = screen.get_size()
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.VIDEORESIZE:
                if not fullscreen:
                    screen_width, screen_height = event.w, event.h
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    earth, moon, asteroid, station = create_bodies()
                    bodies = [earth, moon, asteroid, station]
                    max_speed = 0
                    min_speed = float('inf')
                    thrust_active = False
                    thrust_particles = []
                    camera_x, camera_y = 0, 0
                    scale = 1.0
                elif event.key == pygame.K_c:
                    station.trail = []
                elif event.key == pygame.K_v:
                    show_vectors = not show_vectors
                elif event.key == pygame.K_f:
                    direction = random.uniform(0, 2 * math.pi)
                    thrust_direction = station.apply_impulse(direction)
                    thrust_active = True
                    thrust_counter = 10
                elif event.key == pygame.K_g:
                    show_grid = not show_grid
                elif event.key == pygame.K_0:
                    camera_x, camera_y = 0, 0
                    scale = 1.0
                elif event.key == pygame.K_i:
                    show_info = not show_info
                elif event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode(cfg['DESKTOP_SIZE'], pygame.FULLSCREEN)
                        screen_width, screen_height = cfg['DESKTOP_SIZE']
                    else:
                        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    station_screen_x, station_screen_y = world_to_screen(
                        station.x, station.y, camera_x, camera_y, scale, 
                        current_width, current_height
                    )
                    dx = mouse_x - station_screen_x
                    dy = mouse_y - station_screen_y
                    direction = math.atan2(dy, dx)
                    thrust_direction = station.apply_impulse(direction)
                    thrust_active = True
                    thrust_counter = 10
                elif event.button == 3:
                    camera_dragging = True
                    camera_drag_start = event.pos
                elif event.button == 4:
                    new_scale = scale * 1.1
                    if min_scale <= new_scale <= max_scale:
                        scale = new_scale
                elif event.button == 5:
                    new_scale = scale / 1.1
                    if min_scale <= new_scale <= max_scale:
                        scale = new_scale
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    camera_dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                if camera_dragging:
                    dx = event.pos[0] - camera_drag_start[0]
                    dy = event.pos[1] - camera_drag_start[1]
                    camera_x -= dx / scale
                    camera_y -= dy / scale
                    camera_drag_start = event.pos
        
        # Обновление частиц двигателя
        if thrust_active:
            thrust_counter -= 1
            if thrust_counter <= 0:
                thrust_active = False
                thrust_particles = []
            
            for _ in range(5):
                angle_offset = random.uniform(-0.3, 0.3)
                dist = cfg['STATION_RADIUS'] + random.randint(0, 5)
                px = station.x - dist * math.cos(thrust_direction + angle_offset)
                py = station.y - dist * math.sin(thrust_direction + angle_offset)
                speed = random.uniform(1.0, 3.0)
                vx = speed * math.cos(thrust_direction + angle_offset)
                vy = speed * math.sin(thrust_direction + angle_offset)
                
                thrust_particles.append({
                    'x': px, 'y': py, 'vx': vx, 'vy': vy,
                    'size': random.randint(2, 5), 'life': random.randint(10, 20)
                })
        
        for p in thrust_particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 1
            if p['life'] <= 0:
                thrust_particles.remove(p)
        
        # Обновление физики
        if not paused:
            station.update(bodies)
            current_speed = math.sqrt(station.vx**2 + station.vy**2)
            if current_speed > max_speed:
                max_speed = current_speed
            if current_speed < min_speed:
                min_speed = current_speed
        
        # Отрисовка
        screen.fill(cfg['BACKGROUND'])
        
        # Отрисовка UI
        draw_ui(
            screen, station, earth, scale, show_vectors, show_grid, show_info,
            camera_x, camera_y, current_width, current_height, bodies,
            thrust_particles, thrust_active, thrust_direction
        )
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
