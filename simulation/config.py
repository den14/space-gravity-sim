import configparser
import pygame

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Получаем информацию об экране
    pygame.display.init()
    screen_info = pygame.display.Info()
    DESKTOP_WIDTH, DESKTOP_HEIGHT = screen_info.current_w, screen_info.current_h
    
    # Загрузка графических настроек
    graphics = config['GRAPHICS']
    
    def parse_color(color_str):
        return tuple(map(int, color_str.split(',')))
    
    settings = {
        'DESKTOP_SIZE': (DESKTOP_WIDTH, DESKTOP_HEIGHT),
        'SCREEN_SIZE': (
            int(graphics.get('width', 1024)),
            int(graphics.get('height', 768))
        ),
        'BACKGROUND': parse_color(graphics['background']),
        'GRID_COLOR': parse_color(graphics['grid_color']),
        'EARTH_COLOR': parse_color(graphics['earth_color']),
        'MOON_COLOR': parse_color(graphics['moon_color']),
        'ASTEROID_COLOR': parse_color(graphics['asteroid_color']),
        'STATION_COLOR': parse_color(graphics['station_color']),
        'TRAIL_COLOR': parse_color(graphics['trail_color']),
        'TEXT_COLOR': parse_color(graphics['text_color']),
        'COMPASS_COLOR': parse_color(graphics['compass_color']),
        'ARROW_COLOR': parse_color(graphics['arrow_color']),
        'THRUST_COLOR': parse_color(graphics['thrust_color']),
        'THRUST_PARTICLE_COLOR': parse_color(graphics['thrust_particle_color']),
        'GRID_SIZE': int(graphics['grid_size']),
        'MAX_GRID_DIST': int(graphics['max_grid_dist']),
        
        'G': float(config['PHYSICS']['g']),
        'INITIAL_SPEED': float(config['PHYSICS']['initial_speed']),
        'EARTH_MASS': float(config['PHYSICS']['earth_mass']),
        'MOON_MASS': float(config['PHYSICS']['moon_mass']),  # Исправлено moon_mass
        'ASTEROID_MASS': float(config['PHYSICS']['asteroid_mass']),
        'EARTH_RADIUS': float(config['PHYSICS']['earth_radius']),
        'MOON_RADIUS': float(config['PHYSICS']['moon_radius']),
        'ASTEROID_RADIUS': float(config['PHYSICS']['asteroid_radius']),
        'STATION_RADIUS': float(config['PHYSICS']['station_radius']),
        'IMPULSE_POWER': float(config['PHYSICS']['impulse_power']),
    }
    return settings

# Создаем глобальную переменную CONFIG
CONFIG = load_config()
