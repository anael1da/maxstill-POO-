
"""
player.py — Personagem controlável (ALUNO).
"""

import math
import pygame
from pathlib import Path
from config import TILE


class Player:

    SIZE = 24
    SPD = 3
    SPRITE_WIDTH = 48
    SPRITE_HEIGHT = 64

    def __init__(self, tx, ty):
        self.x = tx * TILE + TILE // 2
        self.y = ty * TILE + TILE // 2

        self.score = 0
        self.pistas = []
        self.completed = set()

        # Direção inicial: frente
        self.direction = 2
        self.frame = 0
        self.anim_tick = 0

        self.frames = self.load_sprites()

    def load_sprites(self):

        caminho = Path(__file__).parent / "imagens" / "aluno.png"
        sheet = pygame.image.load(str(caminho)).convert_alpha()

        # Centros dos quatro personagens em cada linha
        centros_x = [321, 524, 724, 925]

        # Limites verticais das quatro linhas
        linhas_y = [
            (80, 330),
            (370, 620),
            (650, 890),
            (920, 1170)
        ]

        frames = []

        for y0, y1 in linhas_y:

            direction_frames = []

            for centro_x in centros_x:

                # Região individual de cada quadro
                x0 = max(0, centro_x - 95)
                x1 = min(sheet.get_width(), centro_x + 95)

                cell = sheet.subsurface(
                    (x0, y0, x1 - x0, y1 - y0)
                ).copy()

                # Recorta somente a parte visível do personagem
                bounds = cell.get_bounding_rect()

                if bounds.width == 0 or bounds.height == 0:
                    raise ValueError(
                        "Quadro vazio na imagem aluno.png"
                    )

                cell = cell.subsurface(bounds).copy()

                # Mantém a proporção dentro de um espaço fixo
                largura = cell.get_width()
                altura = cell.get_height()

                fator = min(
                    34 / largura,
                    46 / altura
                )

                novo_tamanho = (
                    max(1, round(largura * fator)),
                    max(1, round(altura * fator))
                )

                cell = pygame.transform.scale(
                    cell, novo_tamanho
                )

                # Quadro fixo para evitar tremedeira
                quadro = pygame.Surface(
                    (self.SPRITE_WIDTH, self.SPRITE_HEIGHT),
                    pygame.SRCALPHA
                )

                pos_x = (
                    self.SPRITE_WIDTH - cell.get_width()
                ) // 2

                pos_y = (
                    self.SPRITE_HEIGHT - cell.get_height()
                )

                quadro.blit(cell, (pos_x, pos_y))

                direction_frames.append(quadro)

            frames.append(direction_frames)

        return frames

    def rect(self):

        h = self.SIZE

        return pygame.Rect(
            self.x - h // 2,
            self.y - h // 2,
            h,
            h
        )

    def move(self, dx, dy, walls):

        if dx > 0:
            self.direction = 1

        elif dx < 0:
            self.direction = 3

        elif dy < 0:
            self.direction = 0

        elif dy > 0:
            self.direction = 2

        self.anim_tick += 1

        if self.anim_tick >= 8:
            self.frame = (self.frame + 1) % 4
            self.anim_tick = 0

        direction = pygame.Vector2(dx, dy)

        if direction.length_squared() > 1:
            direction.normalize_ip()

        delta = direction * self.SPD

        steps = max(
            1,
            math.ceil(max(abs(delta.x), abs(delta.y)))
        )

        for _ in range(steps):

            for axis, amount in (
                ("x", delta.x / steps),
                ("y", delta.y / steps)
            ):

                previous = getattr(self, axis)

                setattr(self, axis, previous + amount)

                if any(
                    self.rect().colliderect(wall)
                    for wall in walls
                ):
                    setattr(self, axis, previous)

    def stop(self):

        self.frame = 0
        self.anim_tick = 0

    def draw(self, surf, cam_x, cam_y):

        sprite = self.frames[self.direction][self.frame]

        draw_x = round(
            self.x - cam_x - self.SPRITE_WIDTH // 2
        )

        draw_y = round(
            self.y - cam_y + self.SIZE // 2 - self.SPRITE_HEIGHT
        )

        surf.blit(sprite, (draw_x, draw_y))

