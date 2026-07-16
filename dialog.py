"""
dialog.py — Caixa de diálogo (DialogBox).

Gerencia a exibição sequencial de falas de personagens.
"""

import pygame
from config import SW, SH, font_md, font_sm
from colors import C_ACCENT, C_WHITE, C_GRAY
from utils import draw_text


class DialogBox:

    def __init__(self):
        self.lines    = []      # lista de strings a exibir em sequência
        self.index    = 0       # índice da linha atualmente visível
        self.active   = False   # True enquanto a caixa está na tela
        self.callback = None    # função chamada ao terminar todas as linhas

    def start(self, lines, callback=None):
        """
        Inicia a caixa com novas linhas e um callback opcional.

        Parâmetros:
            lines    → lista de strings (cada item = uma "tela" de diálogo)
            callback → função a chamar quando o diálogo terminar
                       (ex.: lambda que chama start_minigame(npc))
        """
        self.lines    = lines
        self.index    = 0
        self.active   = True
        self.callback = callback

    def advance(self):
        """
        Avança para a próxima linha de diálogo.

        Chamado quando o jogador pressiona E ou ESPAÇO.
        """
        self.index += 1
        if self.index >= len(self.lines):
            self.active = False
            if self.callback:
                self.callback()

    def draw(self, surf):
        """
        Desenha o painel de diálogo na parte inferior da tela.

        """
        if not self.active:
            return

        bx, by, bw, bh = 40, SH - 180, SW - 80, 150

        # Cria surface com canal alpha para o fundo semi-transparente
        s = pygame.Surface((bw, bh), pygame.SRCALPHA)
        s.fill((10, 8, 20, 210))   # RGBA: quase preto com 82% de opacidade
        surf.blit(s, (bx, by))

        # Borda colorida que destaca o painel
        pygame.draw.rect(surf, C_ACCENT, (bx, by, bw, bh), 2, border_radius=6)

        # Exibe a linha atual, tratando \n para quebras manuais
        line = self.lines[self.index]
        for i, ln in enumerate(line.split("\n")):
            draw_text(surf, ln, font_md, C_WHITE, bx + 14, by + 14 + i * 22)

        # Dica de avançar no canto inferior direito do painel
        hint = font_sm.render("[ ESPAÇO / E para avançar ]", True, C_GRAY)
        surf.blit(hint, (bx + bw - hint.get_width() - 10, by + bh - 22))

