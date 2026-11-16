"""
minigames/piscina.py — Minigame 1: corrida aquática contra Anderson.
"""

import random
import math
import pygame
from config import SW, SH, font_lg
from colors import C_WHITE, C_BLACK, C_PLAYER, C_NPC1, C_BLUE, C_GREEN, C_RED
from utils import draw_rect_border, draw_text_center
from minigames.base import Minigame


class PiscinaGame(Minigame):
    """
    Minigame de corrida aquática: desvie dos clones de Anderson
    e avance uma distância de 600 unidades sem perder as 3 vidas.

    Mecânica:
        - 5 raias verticais (LANES) de 80px de largura cada
        - Player se move lateralmente com A/D (muda de raia)
        - A cada ~40 frames, um "inimigo" (Anderson) aparece no topo
          de uma raia aleatória e desce em velocidade aleatória (2.5–4.5)
        - Colisão com inimigo: perde 1 vida; cooldown de 60 frames de invencibilidade
        - Progresso é acumulado em self.distance (3 unidades/frame)
        - Meta: atingir self.goal = 600 sem zerar as vidas

    Condição de vitória:  self.distance >= 600
    Condição de derrota:  self.lives <= 0

    Impacto no jogo:
        Vencer → Anderson revela que Romerito carregava uma peruca
                 → pista 1 adicionada ao caderno do player
    """

    LANES  = 5    # número de raias da piscina
    LANE_W = 80   # largura de cada raia em pixels

    def __init__(self, screen):
        super().__init__(screen)
        self.player_lane = 2        # raia inicial do player (centro)
        self.player_y    = SH - 80  # posição Y fixa do player (parte inferior)
        self.enemies     = []        # lista de [lane, y, speed] dos inimigos ativos
        self.spawn_timer = 0         # contador de frames até próximo spawn
        self.distance    = 0         # distância percorrida (progresso)
        self.goal        = 600       # distância necessária para vitória
        self.lives       = 3         # vidas do player
        self.cooldown    = 0         # frames de invencibilidade após colisão

    def _lane_x(self, lane):
        """
        Calcula o centro X em pixels de uma raia específica.

        As raias são centralizadas na tela. O offset inicial é calculado
        para que o conjunto de raias fique no meio horizontal da janela.
        """
        return (SW - self.LANES * self.LANE_W) // 2 + lane * self.LANE_W + self.LANE_W // 2

    def handle_event(self, event):
        """
        Processa entrada do teclado para troca de raia.

        A (ou ←): move para raia à esquerda (player_lane - 1)
        D (ou →): move para raia à direita (player_lane + 1)
        Limites: 0 (mais à esquerda) até LANES-1 (mais à direita)
        """
        if self.done:
            return
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_LEFT) and self.player_lane > 0:
                self.player_lane -= 1
            if event.key in (pygame.K_d, pygame.K_RIGHT) and self.player_lane < self.LANES - 1:
                self.player_lane += 1

    def update(self):
        """
        Lógica de atualização executada a cada frame.

        Sequência:
            1. Se done, encerra (noop após done).
            2. Incrementa self.distance (simula avanço do player).
            3. A cada 40 frames, spawna um inimigo em raia aleatória.
            4. Move todos os inimigos para baixo; remove os que saíram da tela.
            5. Se cooldown expirou, verifica colisão player × inimigos.
               Colisão: -1 vida → derrota se lives <= 0.
            6. Verifica vitória: distance >= goal.
        """
        if self.done:
            self.timer += 1
            return

        # Avança progresso da corrida (3 px por frame)
        self.distance += 3

        # Spawn de inimigos a cada 40 frames
        self.spawn_timer += 1
        if self.spawn_timer > 40:
            self.spawn_timer = 0
            lane = random.randint(0, self.LANES - 1)
            spd  = random.uniform(2.5, 4.5)   # velocidade variável aumenta dificuldade
            self.enemies.append([lane, -30, spd])  # spawn acima da tela (y=-30)

        # Move inimigos para baixo e remove os que saíram
        for e in self.enemies:
            e[1] += e[2]
        self.enemies = [e for e in self.enemies if e[1] < SH + 40]

        # Detecção de colisão (pulada durante cooldown)
        if self.cooldown > 0:
            self.cooldown -= 1
        else:
            px = self._lane_x(self.player_lane)
            py = self.player_y
            pr = pygame.Rect(px - 20, py - 28, 40, 56)   # hitbox do player
            for e in self.enemies:
                ex = self._lane_x(e[0])
                er = pygame.Rect(ex - 20, e[1] - 28, 40, 56)   # hitbox do inimigo
                if pr.colliderect(er):
                    self.lives   -= 1
                    self.cooldown = 60   # 1 segundo de invencibilidade (60 FPS)
                    if self.lives <= 0:
                        self.done    = True
                        self.success = False
                        self.msg     = "Você perdeu! (sem pista)"
                    break

        # Condição de vitória
        if self.distance >= self.goal:
            self.done    = True
            self.success = True
            self.msg     = "CHEGOU! Pista obtida!"

    def draw(self):
        """
        Renderiza o minigame da piscina.

        Elementos visuais:
            - Fundo azul escuro
            - Raias com cor azul animada por seno (mesma lógica de GameMap)
            - Linhas brancas separando raias
            - Faixa xadrez na parte superior representando a linha de chegada
            - Inimigos (vermelho) e player (verde, pisca durante cooldown)
            - HUD com título, barra de progresso e barra de vidas
        """
        self.screen.fill((20, 40, 80))

        # Calcula offset horizontal para centralizar as raias
        ox = (SW - self.LANES * self.LANE_W) // 2
        t  = pygame.time.get_ticks() / 1000

        # Desenha cada raia com animação de cor
        for i in range(self.LANES):
            x   = ox + i * self.LANE_W
            col = (30, 100, int(160 + 40 * math.sin(t + i)))
            pygame.draw.rect(self.screen, col, (x, 0, self.LANE_W, SH))
            # Linha divisória entre raias
            pygame.draw.rect(self.screen, (50, 150, 220), (x, 0, 2, SH))
        # Borda direita da última raia
        pygame.draw.rect(self.screen, (50, 150, 220), (ox + self.LANES * self.LANE_W, 0, 2, SH))

        # Linha de chegada xadrez no topo (posição fixa, decorativa)
        for i in range(0, self.LANES * self.LANE_W, 20):
            col = C_WHITE if (i // 20) % 2 == 0 else C_BLACK
            pygame.draw.rect(self.screen, col, (ox + i, 10, 20, 14))

        # Inimigos (clones de Anderson em vermelho)
        for e in self.enemies:
            ex = self._lane_x(e[0])
            er = pygame.Rect(ex - 22, int(e[1]) - 30, 44, 60)
            draw_rect_border(self.screen, C_NPC1, er, radius=4)
            # Rosto simplificado
            pygame.draw.rect(self.screen, C_BLACK, (er.x + 8,  er.y + 12, 6, 6))
            pygame.draw.rect(self.screen, C_BLACK, (er.x + 22, er.y + 12, 6, 6))
            pygame.draw.rect(self.screen, C_BLACK, (er.x + 8,  er.y + 25, 20, 4))

        # Player (pisca quando em cooldown: alterna entre verde e branco a cada 4 frames)
        px  = self._lane_x(self.player_lane)
        pr  = pygame.Rect(px - 22, self.player_y - 30, 44, 60)
        col = C_PLAYER if (self.cooldown % 8 < 4 or self.cooldown == 0) else C_WHITE
        draw_rect_border(self.screen, col, pr, radius=4)
        pygame.draw.rect(self.screen, C_BLACK, (pr.x + 8,  pr.y + 12, 6, 6))
        pygame.draw.rect(self.screen, C_BLACK, (pr.x + 22, pr.y + 12, 6, 6))
        pygame.draw.rect(self.screen, C_BLACK, (pr.x + 8,  pr.y + 25, 20, 4))

        # HUD do minigame
        self.draw_hud("CORRIDA NA PISCINA",
                      "A/D para mudar de raia – desvie de Anderson!")
        self.draw_bar("Progresso:", self.distance, self.goal,  20,  80, 300, 16, C_BLUE)
        self.draw_bar("Vidas:",     self.lives,    3,          20, 118, 100, 16, C_RED)

        # Mensagem de resultado (vitória/derrota)
        if self.msg:
            s = pygame.Surface((SW, 60), pygame.SRCALPHA)
            s.fill((0, 0, 0, 160))
            self.screen.blit(s, (0, SH // 2 + 70))
            draw_text_center(self.screen, self.msg, font_lg,
                             C_GREEN if self.success else C_RED, SW // 2, SH // 2 + 100)


