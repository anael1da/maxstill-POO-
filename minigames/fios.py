"""
minigames/fios.py — Minigame 4: conectar fios elétricos na sala de Hugo.
"""

import random
import math
import pygame
from config import SW, SH, font_lg, font_md, font_sm
from colors import C_WHITE, C_BLUE, C_DGRAY, C_GREEN, C_RED, C_YELLOW
from utils import draw_text, draw_text_center
from minigames.base import Minigame


class FiosGame(Minigame):
    """
    Minigame de lógica: arraste os fios do painel esquerdo para
    conectar cada um ao pino da mesma cor no painel direito.

    Mecânica:
        - 4 pinos à esquerda em ordem fixa (vermelho, azul, verde, amarelo)
        - 4 pinos à direita em ordem EMBARALHADA (right_order)
        - Jogador arrasta um fio do pino esquerdo até o pino direito correto
        - Ao conectar todos os 4: verifica se cada left_pin[i] → right_pin[j]
          corresponde à cor correta (right_order.index(i) == j)
        - Se errado: connections é limpo, mistakes += 1
        - Máximo de 3 erros (max_mistakes)

    Condição de vitória:  4 fios corretos conectados de uma vez
    Condição de derrota:  mistakes >= 3

    Impacto no jogo:
        Vencer → Diego revela que Romerito está na sala dos professores
                 → pista 4 adicionada; com todas as 4 pistas coletadas,
                   o jogo avança para a tela final (check_final())
    """

    COLORS = [C_RED, C_BLUE, C_GREEN, C_YELLOW]
    LABELS = ["VERMELHO", "AZUL", "VERDE", "AMARELO"]

    def __init__(self, screen):
        super().__init__(screen)
        self.left_order  = list(range(4))   # pinos esquerdos: 0,1,2,3 (fixos)
        self.right_order = list(range(4))   # pinos direitos: 0,1,2,3 embaralhados
        random.shuffle(self.right_order)
        self.connections  = {}    # dict {left_pin_idx: right_pin_idx} das conexões feitas
        self.dragging     = None  # índice do pino esquerdo sendo arrastado
        self.drag_pos     = (0, 0)  # posição atual do mouse durante drag
        self.mistakes     = 0     # número de tentativas erradas
        self.max_mistakes = 3

    def _left_pos(self, i):
        """Retorna (x, y) do centro do pino esquerdo i."""
        return (220, 160 + i * 100)

    def _right_pos(self, i):
        """Retorna (x, y) do centro do pino direito i."""
        return (740, 160 + i * 100)

    def handle_event(self, event):
        """
        Processa drag-and-drop de fios.

        MOUSEBUTTONDOWN:
            Verifica se o clique foi em um pino esquerdo não conectado
            (raio de 20px do centro). Se sim, inicia o drag.

        MOUSEMOTION:
            Atualiza drag_pos para o fio acompanhar o cursor.

        MOUSEBUTTONUP:
            Verifica se soltou sobre um pino direito disponível (raio 28px).
            Se sim, registra a conexão e chama _check().
            Cancela o drag em qualquer caso.
        """
        if self.done:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for i in range(4):
                lx, ly = self._left_pos(i)
                if math.hypot(mx - lx, my - ly) < 20 and i not in self.connections:
                    self.dragging = i
        if event.type == pygame.MOUSEMOTION:
            if self.dragging is not None:
                self.drag_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging is not None:
                mx, my = event.pos
                for j in range(4):
                    rx, ry = self._right_pos(j)
                    if math.hypot(mx - rx, my - ry) < 28:
                        # Só conecta se o pino direito ainda não foi usado
                        if j not in self.connections.values():
                            self.connections[self.dragging] = j
                            self._check()
                        break
                self.dragging = None

    def _check(self):
        """
        Verifica se todas as 4 conexões estão corretas após cada nova conexão.

        Lógica:
            Para cada pino esquerdo i, a cor correta no lado direito é
            right_order.index(i) — a posição onde a cor i aparece no
            embaralhamento.

        Se todas corretas → vitória.
        Se incorretas após 4 conexões → mistakes += 1, limpa conexões.
        Se mistakes >= max_mistakes → derrota.
        """
        if len(self.connections) == 4:
            correct = all(self.connections.get(i) == self.right_order.index(i)
                          for i in range(4))
            if correct:
                self.done    = True
                self.success = True
                self.msg     = "Fios conectados! Pista obtida!"
            else:
                self.mistakes += 1
                self.connections.clear()   # limpa para nova tentativa
                if self.mistakes >= self.max_mistakes:
                    self.done    = True
                    self.success = False
                    self.msg     = "Fios errados! (sem pista)"

    def draw(self):
        """
        Renderiza o minigame de fios.

        Elementos visuais:
            - Fundo azul-escuro
            - Painel esquerdo "SAÍDA" e painel direito "ENTRADA" (cinza)
            - Pinos circulares coloridos à esquerda (ordem fixa)
              e à direita (ordem embaralhada)
            - Labels de cor ao lado de cada pino
            - Linhas conectando pinos já ligados
            - Linha sendo arrastada (segue o mouse)
            - HUD com título, instrução e contador de erros
        """
        self.screen.fill((20, 20, 35))

        # Painéis laterais
        pygame.draw.rect(self.screen, C_DGRAY, (80,  100, 200, 420), border_radius=8)
        pygame.draw.rect(self.screen, C_DGRAY, (680, 100, 200, 420), border_radius=8)
        draw_text_center(self.screen, "SAÍDA",   font_md, C_WHITE, 180, 120)
        draw_text_center(self.screen, "ENTRADA", font_md, C_WHITE, 780, 120)

        for i in range(4):
            col = self.COLORS[i]
            lx, ly = self._left_pos(i)

            # Pino esquerdo (ordem fixa de cores)
            pygame.draw.circle(self.screen, col,     (lx, ly), 18)
            pygame.draw.circle(self.screen, C_WHITE, (lx, ly), 18, 2)
            draw_text(self.screen, self.LABELS[i], font_sm, col, lx - 100, ly - 9)

            # Pino direito (ordem embaralhada)
            ri   = self.right_order[i]     # índice de cor nesta posição
            rcol = self.COLORS[ri]
            rx, ry = self._right_pos(i)
            pygame.draw.circle(self.screen, rcol,    (rx, ry), 18)
            pygame.draw.circle(self.screen, C_WHITE, (rx, ry), 18, 2)
            draw_text(self.screen, self.LABELS[ri], font_sm, rcol, rx + 22, ry - 9)

        # Linhas das conexões já feitas
        for li, rj in self.connections.items():
            lx, ly = self._left_pos(li)
            rx, ry = self._right_pos(rj)
            pygame.draw.line(self.screen, self.COLORS[li], (lx + 18, ly), (rx - 18, ry), 5)

        # Fio em drag (segue o cursor)
        if self.dragging is not None:
            lx, ly = self._left_pos(self.dragging)
            pygame.draw.line(self.screen, self.COLORS[self.dragging],
                             (lx + 18, ly), self.drag_pos, 4)

        self.draw_hud("CONECTAR OS FIOS",
                      "Arraste cada fio da esquerda ao pino da mesma cor!")
        draw_text(self.screen, f"Erros: {self.mistakes}/{self.max_mistakes}",
                  font_md, C_RED, 20, 80)

        if self.msg:
            s = pygame.Surface((SW, 60), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            self.screen.blit(s, (0, SH // 2 + 80))
            draw_text_center(self.screen, self.msg, font_lg,
                             C_GREEN if self.success else C_RED, SW // 2, SH // 2 + 110)


