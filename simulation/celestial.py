import pygame
import math
import random
from simulation.config import CONFIG as cfg
from simulation.graphics import world_to_screen

class CelestialBody:
    def __init__(self, x, y, mass, radius, color, name, is_static=True, vx=0, vy=0):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.name = name
        self.is_static = is_static
        self.vx = vx
        self.vy = vy
        self.trail = []
        
    def update(self, bodies):
        if self.is_static:
            return
            
        total_ax = 0
        total_ay = 0
        
        for body in bodies:
            if body is self:
                continue
                
            dx = body.x - self.x
            dy = body.y - self.y
            distance = max(math.sqrt(dx**2 + dy**2), 1)
            
            force = cfg['G'] * body.mass / (distance**2)
            
            total_ax += force * dx / distance
            total_ay += force * dy / distance
        
        self.vx += total_ax
        self.vy += total_ay
        self.x += self.vx
        self.y += self.vy
        
        self.trail.append((self.x, self.y))
        if len(self.trail) > 300:
            self.trail.pop(0)
            
    def apply_impulse(self, direction):
        self.vx += cfg['IMPULSE_POWER'] * math.cos(direction)
        self.vy += cfg['IMPULSE_POWER'] * math.sin(direction)
        return direction + math.pi
    
    def draw(self, surface, camera_x=0, camera_y=0, scale=1.0):
        # Преобразование координат с учетом камеры и масштаба
        screen_x, screen_y = world_to_screen(
            self.x, self.y, camera_x, camera_y, scale, 
            surface.get_width(), surface.get_height()
        )
        
        # Рисование следа орбиты с антиалиасингом
        if len(self.trail) > 1 and not self.is_static:
            trail_points = []
            for tx, ty in self.trail:
                trail_x, trail_y = world_to_screen(
                    tx, ty, camera_x, camera_y, scale,
                    surface.get_width(), surface.get_height()
                )
                trail_points.append((trail_x, trail_y))
            
            if len(trail_points) > 1:
                pygame.draw.aalines(surface, cfg['TRAIL_COLOR'], False, trail_points)
        
        scaled_radius = max(1, int(self.radius * scale))
        pygame.draw.circle(surface, self.color, (int(screen_x), int(screen_y)), scaled_radius)
        
        if scaled_radius > 4:
            highlight = (
                min(self.color[0]+40, 255), 
                min(self.color[1]+40, 255), 
                min(self.color[2]+40, 255)
            )
            pygame.draw.circle(surface, highlight, (int(screen_x), int(screen_y)), 
                             max(1, int(scaled_radius * 0.5)))
        
        if self.is_static:
            font = pygame.font.SysFont(None, 20)
            text = font.render(self.name, True, (192, 192, 192))
            surface.blit(text, (int(screen_x) - text.get_width()//2, int(screen_y) + scaled_radius + 5))

def create_station(earth):
    orbit_radius = random.randint(150, 250)
    angle = random.uniform(0, 2 * math.pi)
    
    x = earth.x + orbit_radius * math.cos(angle)
    y = earth.y + orbit_radius * math.sin(angle)
    
    direction = random.uniform(0, 2 * math.pi)
    vx = cfg['INITIAL_SPEED'] * math.cos(direction)
    vy = cfg['INITIAL_SPEED'] * math.sin(direction)
    
    return CelestialBody(
        x, y, 1, cfg['STATION_RADIUS'], cfg['STATION_COLOR'],
        "Станция", is_static=False, vx=vx, vy=vy
    )

def create_bodies():
    earth = CelestialBody(
        0, 0, cfg['EARTH_MASS'], cfg['EARTH_RADIUS'], 
        cfg['EARTH_COLOR'], "Земля"
    )
    
    moon_angle = random.uniform(0, 2 * math.pi)
    moon_distance = 300
    moon = CelestialBody(
        earth.x + moon_distance * math.cos(moon_angle),
        earth.y + moon_distance * math.sin(moon_angle),
        cfg['MOON_MASS'], cfg['MOON_RADIUS'], 
        cfg['MOON_COLOR'], "Луна"
    )
    
    asteroid = CelestialBody(
        random.randint(-cfg['SCREEN_SIZE'][0]//2, cfg['SCREEN_SIZE'][0]//2),
        random.randint(-cfg['SCREEN_SIZE'][1]//2, cfg['SCREEN_SIZE'][1]//2),
        cfg['ASTEROID_MASS'], cfg['ASTEROID_RADIUS'], 
        cfg['ASTEROID_COLOR'], "Астероид"
    )
    
    station = create_station(earth)
    
    return earth, moon, asteroid, station
