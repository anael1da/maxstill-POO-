"""
minigames/base.py — Classe base Minigame.

Define a interface comum (handle_event, update, draw) e os
métodos auxiliares de HUD usados pelos 4 minigames.
"""

import pygame
from config import SW, SH, font_lg, font_md, font_sm
from colors import C_ACCENT, C_GRAY, C_GREEN, C_RED, C_DGRAY, C_WHITE
from utils import draw_text_center, draw_text


class Minigame:
    """
    Classe base para os 4 minigames do jogo.

    Define a interface comum que todas as subclasses devem seguir:
        handle_event(event) → processa inputs do jogador
        update()            → atualiza a lógica do minigame
        draw()              → renderiza o minigame na tela

    Atributos de estado:
        done    → True quando o minigame acabou (vitória ou derrota)
        success → True = jogador venceu, False = perdeu
        timer   → contador auxiliar de frames (usado em transições)
        msg     → mensagem de resultado a exibir ("CHEGOU!", "GOL!", etc.)

    Métodos auxiliares de HUD:
        draw_hud()  → faixa semi-transparente no topo com título e subtítulo
        draw_bar()  → barra de progresso horizontal genérica

    Impacto no jogo:
        Quando Game detecta que self.minigame.done == True, chama
        finish_minigame() que concede (ou não) a pista ao player.
    """

    def __init__(self, screen):
        self.screen  = screen
        self.done    = False    # encerra o minigame quando True
        self.success = False    # True = vitória → pista liberada
        self.timer   = 0       # contador de frames auxiliar
        self.msg     = ""      # mensagem exibida ao final

    def handle_event(self, event): pass   # sobrescrito pelas subclasses
    def update(self):             pass   # sobrescrito pelas subclasses
    def draw(self):               pass   # sobrescrito pelas subclasses

    def draw_hud(self, title, subtitle=""):
        """
        Desenha a faixa de HUD no topo da tela do minigame.

        Parâmetros:
            title    → título grande do minigame (ex.: "CORRIDA NA PISCINA")
            subtitle → instrução breve para o jogador

        Também exibe self.msg centralizado na tela quando definido,
        em verde (vitória) ou vermelho (derrota).
        """
        s = pygame.Surface((SW, 80), pygame.SRCALPHA)
        s.fill((5, 3, 15, 200))   # fundo semi-transparente quase preto
        self.screen.blit(s, (0, 0))
        draw_text_center(self.screen, title,    font_lg, C_ACCENT, SW // 2, 22)
        if subtitle:
            draw_text_center(self.screen, subtitle, font_md, C_GRAY,   SW // 2, 54)
        if self.msg:
            draw_text_center(self.screen, self.msg, font_lg,
                             C_GREEN if self.success else C_RED,
                             SW // 2, SH // 2 + 100)

    def draw_bar(self, label, val, maxv, x, y, w=200, h=18, col=C_GREEN):
        """
        Desenha uma barra de progresso com rótulo.

        Parâmetros:
            label → texto acima da barra
            val   → valor atual
            maxv  → valor máximo (barra cheia)
            x, y  → posição do rótulo
            w, h  → largura e altura da barra em pixels
            col   → cor de preenchimento

        A barra tem fundo C_DGRAY e preenchimento proporcional a val/maxv.
        Usada para exibir progresso da corrida, vidas, etc.
        """
        draw_text(self.screen, label, font_sm, C_WHITE, x, y)
        pygame.draw.rect(self.screen, C_DGRAY, (x, y + 18, w, h),            border_radius=4)
        pygame.draw.rect(self.screen, col,     (x, y + 18, int(w * val / maxv), h), border_radius=4)

