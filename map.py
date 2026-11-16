"""Mapa ajustado à janela original, com salas e portas transitáveis.
Todas as estruturas são definidas em pixels da imagem original e passam
pela mesma transformação uniforme usada pelo desenho.
"""
from pathlib import Path
import pygame
from config import TILE, SW, SH

# Retângulos (x, y, largura, altura) medidos na imagem 1402 x 1122.
MAP_COLLIDERS = [
    # Muro externo, incluindo os portões fechados e pilares laterais.
    (0, 0, 1402, 91), (0, 1030, 1402, 92),
    (0, 91, 68, 939), (1335, 91, 67, 939),
    # Bancos.
    (83, 321, 78, 58), (83, 696, 78, 58),
    (1243, 321, 78, 58), (1243, 802, 78, 59),
    # Bases dos postes (a parte alta não bloqueia o chão).
    (204, 502, 29, 29), (204, 856, 29, 29), (1268, 523, 29, 30),
    # Troncos; as copas ficam acima do personagem.
    (107, 182, 31, 39), (107, 516, 31, 41), (107, 880, 31, 43),
    (1263, 183, 31, 38), (1263, 670, 31, 40), (1263, 976, 31, 42),
    # Arbustos: retângulo central + base estreita para acompanhar o contorno.
]
for x, y in [(94, 238), (94, 612), (94, 945), (1253, 238), (1253, 724)]:
    MAP_COLLIDERS.extend([(x, y + 12, 57, 39), (x + 9, y + 4, 39, 58)])

# Paredes das salas, deixando vão de 56px em cada entrada.
ROOMS = [(308, 175, 501, 435), (780, 175, 501, 913),
         (308, 630, 961, 435), (780, 630, 961, 913)]
for left, top, bottom, door_x in ROOMS:
    right = left + 315
    MAP_COLLIDERS.extend([
        (left, top, 315, 46),
        (left, top + 46, 28, bottom - top - 46),
        (right - 28, top + 46, 28, bottom - top - 46),
        (left + 28, bottom - 61, door_x - left - 28, 61),
        (door_x + 56, bottom - 61, right - 28 - door_x - 56, 61),
    ])
# Mobília dentro das salas: estantes, mesas, planta e armários.
MAP_COLLIDERS.extend([
    (339, 229, 107, 85), (450, 257, 82, 56), (550, 267, 41, 41),
    (812, 229, 88, 85), (944, 256, 79, 57), (1025, 251, 36, 61),
    (365, 723, 110, 60), (530, 713, 40, 77),
    (944, 697, 118, 89),
])
PLAYER_SPAWN = (701, 985)
NPC_POSITIONS = {1: (465, 376), 4: (939, 376),
                 2: (465, 843), 3: (939, 843)}


def tile_position(point):
    """Adapta pixels aos construtores existentes, sem arredondamento."""
    return tuple((value - TILE // 2) / TILE for value in point)


class GameMap:
    def __init__(self):
        source = pygame.image.load(str(Path(__file__).parent / 'assets' / 'cenario.jpeg')).convert()
        if source.get_size() != (1402, 1122):
            raise ValueError('Asset original esperado: 1402 x 1122.')
        # Substitui visualmente as folhas fechadas por piso da própria sala.
        # O asset original permanece intacto; o vão visual coincide com a colisão.
        for left, top, bottom, door_x in ROOMS:
            floor = source.subsurface((door_x, bottom - 125, 56, 61)).copy()
            source.blit(floor, (door_x, bottom - 61))
        self.width, self.height = SW, SH
        self.scale = min(SW / source.get_width(), SH / source.get_height())
        size = (round(source.get_width() * self.scale), round(source.get_height() * self.scale))
        self.offset = ((SW - size[0]) // 2, (SH - size[1]) // 2)
        self.image = pygame.Surface((SW, SH)).convert()
        self.image.fill((20, 18, 27))
        self.image.blit(pygame.transform.smoothscale(source, size), self.offset)
        self.walls = [self.transform_rect(r) for r in MAP_COLLIDERS]
        ox, oy = self.offset
        self.walls.extend([pygame.Rect(0, 0, ox, SH), pygame.Rect(ox + size[0], 0, SW - ox - size[0], SH)])
        self.minimap = pygame.transform.smoothscale(self.image, (180, 120))

    def world_position(self, point):
        return tuple(round(v * self.scale) + o for v, o in zip(point, self.offset))

    def transform_rect(self, rect):
        x, y, w, h = rect
        left, top = self.world_position((x, y))
        right, bottom = self.world_position((x + w, y + h))
        return pygame.Rect(left, top, right - left, bottom - top)

    def player_start(self):
        return tile_position(self.world_position(PLAYER_SPAWN))

    def npc_pos(self, nid):
        return tile_position(self.world_position(NPC_POSITIONS[nid]))

    def draw(self, surf, cam_x, cam_y):
        surf.fill((0, 0, 0))
        surf.blit(self.image, (-cam_x, -cam_y))
