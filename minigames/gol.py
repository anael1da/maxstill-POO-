"""
minigames/gol.py — Minigame 2: timing de chute a gol contra Rickson.
"""

import random
import pygame
from config import SW, SH, font_lg, font_md
from colors import C_WHITE, C_BLACK, C_GREEN, C_RED, C_YELLOW
from utils import draw_text, draw_text_center
from minigames.base import Minigame


class GolGame(Minigame):
    """
    Minigame de timing: pressione ESPAÇO quando a bola estiver
    na zona verde da goleira para marcar gol.

    Mecânica:
        - Uma bola se move horizontalmente dentro da goleira (bar_pos 0→1→0)
        - Zona de acerto: 35%–65% do comprimento da goleira
        - Precisa de 2 gols (need) em até 3 erros (attempts)
        - A velocidade aumenta a cada tentativa (+0.002 por round)

    Condição de vitória:  self.wins >= 2
    Condição de derrota:  self.attempts <= 0

    Impacto no jogo:
        Vencer → Carlos revela que Romerito falava de fios elétricos
                 → pista 2 adicionada ao caderno do player
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.bar_pos   = 0.0     # posição relativa da bola (0.0 = esquerda, 1.0 = direita)
        self.bar_dir   = 1       # direção do movimento (+1 ou -1)
        self.bar_spd   = 0.012   # velocidade inicial da bola
        self.attempts  = 3       # tentativas restantes (erros permitidos)
        self.wins      = 0       # gols marcados
        self.need      = 2       # gols necessários para vencer
        self.phase     = "playing"   # "playing" ou "show_result"
        self.phase_t   = 0           # contador de frames na fase show_result
        self.last_ok   = None        # resultado da última tentativa (bool)
        self.rounds    = 0           # total de tentativas realizadas
        self.max_rounds = 5          # máximo de rodadas

    def handle_event(self, event):
        """
        Registra o pressionamento de ESPAÇO ou E durante a fase "playing".

        Verifica se bar_pos está na zona de acerto (0.35 a 0.65).
        Resultado:
            Acerto → wins += 1; verifica vitória
            Erro   → attempts -= 1; verifica derrota
        Muda para fase "show_result" para exibir "GOL!" ou "FORA!" brevemente.
        """
        if self.done or self.phase != "playing":
            return
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_e):
            ok = 0.35 < self.bar_pos < 0.65
            self.last_ok = ok
            if ok:
                self.wins += 1
            else:
                self.attempts -= 1
            self.rounds += 1
            self.phase   = "show_result"
            self.phase_t = 0

            if self.wins >= self.need:
                self.done    = True
                self.success = True
                self.msg     = "GOL! Pista obtida!"
            elif self.attempts <= 0:
                self.done    = True
                self.success = False
                self.msg     = "Errou! (sem pista)"

    def update(self):
        """
        Atualiza a posição da bola e a transição entre fases.

        Fase "playing":
            - bar_pos avança por bar_spd; inverte direção nas bordas
            - bar_spd aumenta gradualmente com o número de rounds,
              tornando o jogo mais difícil a cada chute

        Fase "show_result":
            - Aguarda 50 frames (~0.83s) antes de voltar ao "playing"
        """
        if self.phase == "playing":
            self.bar_pos += self.bar_spd * self.bar_dir
            if self.bar_pos >= 1: self.bar_dir = -1
            if self.bar_pos <= 0: self.bar_dir =  1
            # Dificuldade crescente: +0.002 por round completado
            self.bar_spd = 0.012 + self.rounds * 0.002
        elif self.phase == "show_result":
            self.phase_t += 1
            if self.phase_t > 50:
                self.phase = "playing"

    def draw(self):
        """
        Renderiza o minigame do gol.

        Elementos visuais:
            - Fundo verde com padrão de grama (quadrados alternados)
            - Goleira branca (300×120 px)
            - Zona de acerto verde translúcida (30% central)
            - Bola branca na posição bar_pos dentro da goleira
            - Jogador (bola amarela + retângulo) na parte inferior
            - Feedback "GOL!" ou "FORA!" entre tentativas
            - Contadores de gols e tentativas
        """
        self.screen.fill((30, 80, 30))

        # Padrão de grama com quadrados alternados
        for row in range(0, SH, 40):
            for col in range(0, SW, 40):
                if (row // 40 + col // 40) % 2 == 0:
                    pygame.draw.rect(self.screen, (35, 90, 35), (col, row, 40, 40))

        # Goleira
        gw, gh = 300, 120
        gx, gy = SW // 2 - gw // 2, 80
        pygame.draw.rect(self.screen, C_WHITE, (gx, gy, gw, gh), 4)  # apenas borda

        # Zona de acerto (30% central da goleira), transparente
        zw = int(gw * 0.3)
        zx = gx + gw // 2 - zw // 2
        s  = pygame.Surface((zw, gh), pygame.SRCALPHA)
        s.fill((0, 255, 0, 60))
        self.screen.blit(s, (zx, gy))

        # Bola em movimento dentro da goleira
        bx = int(gx + gw * self.bar_pos)
        by = gy + gh // 2
        pygame.draw.circle(self.screen, C_WHITE, (bx, by), 18)
        pygame.draw.circle(self.screen, C_BLACK, (bx, by), 18, 3)

        # "Jogador" (representação do chutador) abaixo da goleira
        pygame.draw.rect(self.screen, C_YELLOW, (SW // 2 - 8, gy + gh + 20, 16, 80))
        pygame.draw.circle(self.screen, C_YELLOW, (SW // 2, gy + gh + 100), 20)
        pygame.draw.circle(self.screen, (100, 60, 20), (SW // 2, gy + gh + 100), 20, 3)

        self.draw_hud("DESAFIO DO GOL",
                      "Pressione ESPAÇO quando a bola estiver na zona verde!")

        draw_text(self.screen, f"Gols: {self.wins}/{self.need}",           font_md, C_GREEN,  20,  80)
        draw_text(self.screen, f"Tentativas restantes: {self.attempts}", font_md, C_YELLOW, 20, 106)

        # Feedback entre tentativas
        if self.phase == "show_result" and not self.done:
            col = C_GREEN if self.last_ok else C_RED
            txt = "GOL!" if self.last_ok else "FORA!"
            draw_text_center(self.screen, txt, font_lg, col, SW // 2, SH // 2 + 80)

        # Mensagem de fim de minigame
        if self.msg:
            s2 = pygame.Surface((SW, 60), pygame.SRCALPHA)
            s2.fill((0, 0, 0, 160))
            self.screen.blit(s2, (0, SH // 2 + 70))
            draw_text_center(self.screen, self.msg, font_lg,
                             C_GREEN if self.success else C_RED, SW // 2, SH // 2 + 100)


