
"""
minigames/peruca.py — Minigame 3: encontrar a peruca de Rolim.
"""

import random
from pathlib import Path

import pygame

from config import SW, SH, font_lg, font_md, font_sm
from colors import C_BLACK, C_BLUE, C_DGRAY, C_GRAY, C_GREEN, C_RED, C_YELLOW
from utils import draw_text, draw_text_center
from minigames.base import Minigame


class PerucaGame(Minigame):

    GRID = 6

    def __init__(self, screen):
        super().__init__(screen)

        self.hidden = (
            random.randint(0, self.GRID - 1),
            random.randint(0, self.GRID - 1)
        )

        self.revealed = [[False] * self.GRID for _ in range(self.GRID)]

        self.tries = 18
        self.hovered = (-1, -1)

        # Caminho da pasta das fotografias
        pasta = Path(__file__).resolve().parent.parent / "assets" / "perucas"

        # Carrega e organiza as 36 fotografias
        fotos = []

        for numero in range(1, 37):
            caminho = pasta / f"{numero}.jpg"

            if not caminho.exists():
                raise FileNotFoundError(
                    f"Não encontrei a fotografia: {caminho}"
                )

            imagem = pygame.image.load(str(caminho)).convert()

            # Ajusta a fotografia para caber no quadradinho
            tamanho = (68, 68)
            imagem = pygame.transform.smoothscale(imagem, tamanho)

            fotos.append(imagem)

        # As primeiras 35 são pessoas carecas.
        # A última (36.jpg) é Rolim com a peruca.
        rolim = fotos[35]
        carecas = fotos[:35]

        random.shuffle(carecas)

        # Distribui uma fotografia para cada posição
        self.cards = {}

        posicoes = [
            (c, r)
            for r in range(self.GRID)
            for c in range(self.GRID)
        ]

        random.shuffle(posicoes)

        self.cards[self.hidden] = rolim

        for posicao, foto in zip(
            [p for p in posicoes if p != self.hidden],
            carecas
        ):
            self.cards[posicao] = foto

    def _cell_rect(self, col, row):
        cw = ch = 80

        ox = SW // 2 - self.GRID * cw // 2
        oy = 130

        return pygame.Rect(
            ox + col * cw + 2,
            oy + row * ch + 2,
            cw - 4,
            ch - 4
        )

    def handle_event(self, event):

        if self.done:
            return

        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            self.hovered = (-1, -1)

            for r in range(self.GRID):
                for c in range(self.GRID):
                    if self._cell_rect(c, r).collidepoint(mx, my):
                        self.hovered = (c, r)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            mx, my = event.pos

            for r in range(self.GRID):
                for c in range(self.GRID):

                    if (
                        self._cell_rect(c, r).collidepoint(mx, my)
                        and not self.revealed[r][c]
                    ):

                        self.revealed[r][c] = True
                        self.tries -= 1

                        if (c, r) == self.hidden:
                            self.done = True
                            self.success = True
                            self.msg = "Rolim! Voce encontrou a peruca!"

                        elif self.tries <= 0:
                            self.done = True
                            self.success = False
                            self.msg = "As tentativas acabaram!"

    def draw(self):

        self.screen.fill((40, 30, 50))

        for r in range(self.GRID):
            for c in range(self.GRID):

                rect = self._cell_rect(c, r)

                if self.revealed[r][c]:

                    # Calcula a proximidade da peruca
                    hx, hy = self.hidden
                    dist = abs(c - hx) + abs(r - hy)

                    if (c, r) == self.hidden:
                        cor = C_YELLOW

                    elif dist <= 1:
                        cor = C_RED

                    elif dist <= 3:
                        cor = C_YELLOW

                    else:
                        cor = C_BLUE

                    # Fundo da carta
                    pygame.draw.rect(
                        self.screen,
                        C_DGRAY,
                        rect,
                        border_radius=6
                    )

                    # Fotografia da pessoa
                    foto = self.cards[(c, r)]

                    area_foto = pygame.Rect(
                        rect.x + 4,
                        rect.y + 4,
                        68,
                        68
                    )

                    self.screen.blit(foto, area_foto)

                    # Borda indicando a temperatura
                    pygame.draw.rect(
                        self.screen,
                        cor,
                        rect,
                        4,
                        border_radius=6
                    )

                else:

                    # Carta ainda fechada
                    cor = (
                        (80, 70, 100)
                        if (c, r) == self.hovered
                        else (60, 55, 75)
                    )

                    pygame.draw.rect(
                        self.screen,
                        cor,
                        rect,
                        border_radius=6
                    )

                    pygame.draw.rect(
                        self.screen,
                        (100, 90, 120),
                        rect,
                        2,
                        border_radius=6
                    )

                    draw_text_center(
                        self.screen,
                        "?",
                        font_md,
                        C_GRAY,
                        rect.centerx,
                        rect.centery
                    )

        self.draw_hud(
            "ACHANDO A PERUCA",
            "Encontre Rolim! Vermelho = muito perto"
        )

        draw_text(
            self.screen,
            f"Tentativas: {self.tries}",
            font_md,
            C_YELLOW,
            20,
            80
        )

        if self.msg:

            s = pygame.Surface((SW, 60), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))

            self.screen.blit(
                s,
                (0, SH // 2 + 80)
            )

            draw_text_center(
                self.screen,
                self.msg,
                font_lg,
                C_GREEN if self.success else C_RED,
                SW // 2,
                SH // 2 + 110
            )
