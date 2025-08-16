# Space Gravity Simulation

![Simulation Screenshot](screenshot.png)

A physics-based gravity simulation with interactive spacecraft control. Simulates gravitational interactions between celestial bodies and allows applying impulses to a space station.

## Features
- Realistic gravitational physics
- Interactive spacecraft control
- Dynamic gravity grid visualization
- Velocity vectors display
- Camera controls (pan/zoom)
- Particle effects for thrusters
- Trail rendering for orbits

## Controls
| Key          | Action                      |
|--------------|----------------------------|
| Space        | Pause/resume simulation    |
| R            | Reset simulation           |
| C            | Clear station trail        |
| V            | Toggle vectors display     |
| G            | Toggle grid                |
| F            | Apply random impulse       |
| Left Click   | Apply impulse to cursor    |
| Right Click  | Pan camera                 |
| Mouse Wheel  | Zoom in/out                |
| 0            | Reset camera               |
| F11          | Toggle fullscreen          |

## Installation
```bash
git clone https://github.com/den14/space-gravity-sim.git
cd space-gravity-sim
pip install -r requirements.txt
python main.py
```

## Planned Improvements
- Collision detection and visualization
- Automated spacecraft controls
- Time warp (speed up simulation)
- Multiple spacecraft types
- Save/load simulation states
- Improved trajectory prediction


### README.md (Русский)

# Гравитационная модель космической станции

![Скриншот симуляции](screenshot.png)

Физическая симуляция гравитации с интерактивным управлением космическим кораблем. Моделирует гравитационное взаимодействие небесных тел и позволяет применять импульсы к космической станции.

## Возможности
- Реалистичная гравитационная физика
- Интерактивное управление кораблем
- Динамическая визуализация гравитационной сетки
- Отображение векторов скорости
- Управление камерой (перемещение/масштаб)
- Эффекты частиц для двигателей
- Визуализация траектории орбит

## Управление
| Клавиша      | Действие                     |
|--------------|------------------------------|
| Пробел       | Пауза/продолжение симуляции |
| R            | Сброс симуляции             |
| C            | Очистка следа станции       |
| V            | Переключение векторов       |
| G            | Переключение сетки          |
| F            | Случайный импульс           |
| ЛКМ          | Импульс к курсору           |
| ПКМ          | Перемещение камеры          |
| Колесо мыши  | Масштабирование             |
| 0            | Сброс камеры                |
| F11          | Полноэкранный режим         |

## Установка
```bash
git clone https://github.com/den14/space-gravity-sim.git
cd space-gravity-sim
pip install -r requirements.txt
python main.py
```

## Планируемые улучшения
- Обнаружение и визуализация столкновений
- Автоматическое управление кораблем
- Ускорение времени (time warp)
- Несколько типов космических кораблей
- Сохранение/загрузка состояний
- Улучшенный прогноз траектории
