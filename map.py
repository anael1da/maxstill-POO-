"""
map.py — Mapa da escola e renderização de cenário (GameMap).
"""

import math
import pygame
from config import RAW_MAP, TILE, MAP_COLS, MAP_ROWS, SW, SH
from colors import C_WALL, C_WATER, C_GRASS, C_FLOOR, C_FLOOR2, C_DOOR, C_LOCKED


class GameMap:

    def __init__(self):
        self.tiles  = RAW_MAP    # referência à lista de strings do mapa
        self.walls  = []
        self.water  = []
        self.grass  = []
        self.doors  = []
        self.locked = []
        self._parse()

    def _parse(self):
       
        for row, line in enumerate(self.tiles):
            for col, ch in enumerate(line):
                r = pygame.Rect(col * TILE, row * TILE, TILE, TILE)
                if   ch == '#': self.walls.append(r)
                elif ch == 'W': self.water.append(r)
                elif ch == 'G': self.grass.append(r)
                elif ch == 'D': self.doors.append(r)
                elif ch == 'L': self.locked.append(r)

    def player_start(self):
        """
        Localiza o tile 'P' no mapa e retorna suas coordenadas (col, row).

        Impacto no jogo:
            Define onde MAX começa ao iniciar ou reiniciar o jogo.
            Se 'P' não existir, retorna (1,1) como fallback seguro.
        """
        for row, line in enumerate(self.tiles):
            for col, ch in enumerate(line):
                if ch == 'P':
                    return col, row
        return 1, 1  # fallback

    def npc_pos(self, nid):
        
        ch = str(nid)
        for row, line in enumerate(self.tiles):
            for col, c in enumerate(line):
                if c == ch:
                    return col, row
        return 2, 2  # fallback

    def draw(self, surf, cam_x, cam_y):
        """
        Renderiza todos os tiles do mapa ajustados pela câmera.

        """
        surf.fill(C_FLOOR)  # preenche o fundo antes de desenhar os tiles

        for row in range(MAP_ROWS):
            for col in range(MAP_COLS):
                # Converte coordenadas de mundo para coordenadas de tela
                rx = col * TILE - cam_x
                ry = row * TILE - cam_y

                # Culling: pula tiles fora da área visível
                if rx < -TILE or ry < -TILE or rx > SW or ry > SH:
                    continue

                ch = self.tiles[row][col]

                # ── Chão comum (tiles passáveis) ──
                if ch in ('.', 'P', '1', '2', '3', '4', 'R', 'D', 'L', ' '):
                    # Alternância de cor cria efeito de grade discreta
                    col_tile = C_FLOOR if (row + col) % 2 == 0 else C_FLOOR2
                    pygame.draw.rect(surf, col_tile, (rx, ry, TILE, TILE))

                # ── Água animada (piscina) ──
                elif ch == 'W':
                    t = pygame.time.get_ticks() / 1000   # tempo em segundos
                    # Ondulação: componente azul varia entre 100 e 180
                    blue = int(140 + 40 * math.sin(t + col * 0.3 + row * 0.2))
                    pygame.draw.rect(surf, (30, 80, blue), (rx, ry, TILE, TILE))

                # ── Grama / quadra ──
                elif ch == 'G':
                    pygame.draw.rect(surf, C_GRASS, (rx, ry, TILE, TILE))

                # ── Parede ──
                elif ch == '#':
                    pygame.draw.rect(surf, C_WALL, (rx, ry, TILE, TILE))
                    # Borda interna 1px para dar sensação de bloco
                    pygame.draw.rect(surf, (40, 35, 50), (rx, ry, TILE, TILE), 1)

                # ── Porta normal ──
                elif ch == 'D':
                    pygame.draw.rect(surf, C_FLOOR, (rx, ry, TILE, TILE))
                    pygame.draw.rect(surf, C_DOOR, (rx + 4, ry, TILE - 8, TILE), border_radius=3)

                # ── Porta trancada ──
                elif ch == 'L':
                    pygame.draw.rect(surf, C_FLOOR, (rx, ry, TILE, TILE))
                    pygame.draw.rect(surf, C_LOCKED, (rx + 4, ry, TILE - 8, TILE), border_radius=3)

