"""
minigames/peruca.py — Minigame 3: achar a peruca escondida de Rolim.
"""

import random
import pygame
from config import SW, SH, font_lg, font_md, font_sm
from colors import C_BLACK, C_BLUE, C_DGRAY, C_GRAY, C_GREEN, C_RED, C_YELLOW
from utils import draw_text, draw_text_center
from minigames.base import Minigame


class PerucaGame(Minigame):
    """
    Minigame de busca: clique nas caixas de uma grade 6×6 para
    encontrar a peruca escondida em posição aleatória.

    Mecânica:
        - Grade 6×6 de células 80×80 px centralizadas na tela
        - A peruca está oculta em uma célula aleatória (hidden)
        - Ao clicar em uma célula, ela é revelada mostrando:
            * A cor indica a distância Manhattan até a peruca:
                vermelho → ≤ 1 (muito perto)
                amarelo  → ≤ 3 (perto)
                azul     → > 3 (longe)
            * O número exato da distância Manhattan
        - Jogador tem 8 tentativas (tries)

    Condição de vitória:  clicar na célula da peruca
    Condição de derrota:  tries <= 0 sem encontrar

    Impacto no jogo:
        Vencer → Bianca revela que Romerito pediu um livro de eletricidade
                 → pista 3 adicionada ao caderno do player
    """

    GRID = 6   # dimensão da grade (6 linhas × 6 colunas)

    def __init__(self, screen):
        super().__init__(screen)
        # Posição aleatória da peruca (coluna, linha)
        self.hidden   = (random.randint(0, self.GRID - 1),
                         random.randint(0, self.GRID - 1))
        # Matriz de revelação: True = célula já clicada
        self.revealed = [[False] * self.GRID for _ in range(self.GRID)]
        self.tries    = 8       # tentativas restantes
        self.hovered  = (-1, -1)  # célula sobre a qual o mouse está

    def _cell_rect(self, col, row):
        """
        Calcula o pygame.Rect de uma célula da grade na tela.

        As células têm 80×80 px com 2px de margem interna (78×78 úteis).
        A grade é centralizada horizontalmente; começa em y=130.
        """
        cw = ch = 80
        ox = SW // 2 - self.GRID * cw // 2
        oy = 130
        return pygame.Rect(ox + col * cw + 2, oy + row * ch + 2, cw - 4, ch - 4)

    def handle_event(self, event):
        """
        Processa movimento do mouse (hover) e cliques nas células.

        MOUSEMOTION: atualiza self.hovered para realce visual.
        MOUSEBUTTONDOWN (botão esquerdo):
            - Encontra a célula clicada
            - Marca como revelada e decrementa tries
            - Se for a célula da peruca → vitória
            - Se tries chegou a 0 sem encontrar → derrota
        """
        if self.done:
            return
        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            found = False
            for r in range(self.GRID):
                for c in range(self.GRID):
                    if self._cell_rect(c, r).collidepoint(mx, my):
                        self.hovered = (c, r)
                        found = True
            if not found:
                self.hovered = (-1, -1)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for r in range(self.GRID):
                for c in range(self.GRID):
                    if self._cell_rect(c, r).collidepoint(mx, my) and not self.revealed[r][c]:
                        self.revealed[r][c] = True
                        self.tries -= 1
                        if (c, r) == self.hidden:
                            self.done    = True
                            self.success = True
                            self.msg     = "Achou a peruca! Pista obtida!"
                        elif self.tries <= 0:
                            self.done    = True
                            self.success = False
                            self.msg     = "Não achou... (sem pista)"

    def draw(self):
        """
        Renderiza o minigame da peruca.

        Células:
            Não revelada → cinza escuro com "?" (realce ao hover)
            Revelada (errada) → fundo cinza + borda colorida conforme distância
                                + número da distância Manhattan no centro
            Revelada (peruca) → fundo amarelo + texto "PERUCA"
        """
        self.screen.fill((40, 30, 50))

        for r in range(self.GRID):
            for c in range(self.GRID):
                rect = self._cell_rect(c, r)

                if self.revealed[r][c]:
                    if (c, r) == self.hidden:
                        # Célula da peruca encontrada
                        pygame.draw.rect(self.screen, C_YELLOW, rect, border_radius=6)
                        draw_text_center(self.screen, "PERUCA", font_sm, C_BLACK,
                                         rect.centerx, rect.centery)
                    else:
                        # Célula errada: mostra distância com cor indicativa
                        pygame.draw.rect(self.screen, C_DGRAY, rect, border_radius=6)
                        hx, hy = self.hidden
                        dist = abs(c - hx) + abs(r - hy)  # distância Manhattan
                        if   dist <= 1: hint_col = C_RED     # muito perto
                        elif dist <= 3: hint_col = C_YELLOW  # perto
                        else:           hint_col = C_BLUE    # longe
                        pygame.draw.rect(self.screen, hint_col, rect, 3, border_radius=6)
                        draw_text_center(self.screen, str(dist), font_md, hint_col,
                                         rect.centerx, rect.centery)
                else:
                    # Célula não revelada
                    col = (80, 70, 100) if (c, r) == self.hovered else (60, 55, 75)
                    pygame.draw.rect(self.screen, col, rect, border_radius=6)
                    pygame.draw.rect(self.screen, (100, 90, 120), rect, 2, border_radius=6)
                    draw_text_center(self.screen, "?", font_md, C_GRAY,
                                     rect.centerx, rect.centery)

        self.draw_hud("ACHANDO A PERUCA",
                      "Clique nas caixas! A cor indica a distância (vermelho=perto)")
        draw_text(self.screen, f"Tentativas: {self.tries}", font_md, C_YELLOW, 20, 80)

        if self.msg:
            s = pygame.Surface((SW, 60), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            self.screen.blit(s, (0, SH // 2 + 80))
            draw_text_center(self.screen, self.msg, font_lg,
                             C_GREEN if self.success else C_RED, SW // 2, SH // 2 + 110)


