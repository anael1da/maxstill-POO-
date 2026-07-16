"""
player.py — Personagem controlável (MAX).
"""

import pygame
from config import TILE
from colors import C_PLAYER, C_BLACK
from utils import draw_rect_border


class Player:
    """
    Representa MAX, o personagem do jogador.

    Atributos principais:
        x, y      → posição em pixels no mundo (não na tela)
        score     → pontuação acumulada (100 pts por pista obtida)
        pistas    → lista de strings das pistas coletadas
        completed → conjunto de IDs de minigames concluídos (não usado diretamente,
                    mas preparado para extensão)

    Tamanho:  24×24 px (quadrado verde-jade)
    Velocidade: 3 px por frame
    """

    SIZE = 24   # lado do quadrado em pixels
    SPD  = 3    # velocidade de movimento em pixels por frame

    def __init__(self, tx, ty):
        """
        Inicializa o player na posição de tile (tx, ty).

        Converte coordenadas de tile para pixels, posicionando o player
        no centro do tile (offset de TILE//2 = 16 px).
        """
        self.x = tx * TILE + TILE // 2
        self.y = ty * TILE + TILE // 2
        self.score    = 0    # pontuação total (exibida no HUD)
        self.pistas   = []   # pistas coletadas (exibidas com TAB)
        self.completed = set()

    def rect(self):
        """
        Retorna o pygame.Rect de colisão do player no espaço do mundo.

        Centralizado em (self.x, self.y); usado para detecção de colisão
        com as paredes do mapa em Player.move().
        """
        h = self.SIZE
        return pygame.Rect(self.x - h // 2, self.y - h // 2, h, h)

    def move(self, dx, dy, walls):
        """
        Move o player aplicando colisão com paredes (AABB).

        Parâmetros:
            dx, dy → direção do movimento (-1, 0 ou 1) nos eixos X e Y
            walls  → lista de pygame.Rect das paredes do mapa

        Lógica de colisão em dois passos (separado por eixo):
            1. Testa o movimento horizontal (nx) com self.y atual.
               Se não colidir com nenhuma parede, aplica nx.
            2. Testa o movimento vertical (ny) com self.x atual (já atualizado).
               Se não colidir, aplica ny.
        Separar os eixos evita que o player "grude" em cantos de paredes.

        Impacto no jogo:
            Garante que MAX não atravesse paredes ('#') do RAW_MAP.
            A velocidade efetiva é SPD * direção = até 3 px/frame.
        """
        nx = self.x + dx * self.SPD
        ny = self.y + dy * self.SPD

        # Teste horizontal
        nr = pygame.Rect(nx - self.SIZE // 2, self.y - self.SIZE // 2, self.SIZE, self.SIZE)
        if not any(nr.colliderect(w) for w in walls):
            self.x = nx

        # Teste vertical (usa self.x que pode ter sido atualizado acima)
        nr = pygame.Rect(self.x - self.SIZE // 2, ny - self.SIZE // 2, self.SIZE, self.SIZE)
        if not any(nr.colliderect(w) for w in walls):
            self.y = ny

    def draw(self, surf, cam_x, cam_y):
        """
        Desenha MAX na tela ajustando pela posição da câmera.

        Parâmetros:
            surf          → surface principal da janela
            cam_x, cam_y  → deslocamento da câmera em pixels

        Visual:
            - Quadrado verde-jade com borda escura (draw_rect_border)
            - Dois retângulos 4×4 px pretos simulando "olhos"
            - Um retângulo 8×3 px preto simulando "boca"

        O offset da câmera é subtraído para converter coordenadas do
        mundo em coordenadas de tela.
        """
        r = self.rect().move(-cam_x, -cam_y)
        draw_rect_border(surf, C_PLAYER, r, radius=4)

        # Olhos: dois quadradinhos dentro do retângulo do player
        ex = r.x + 6
        ey = r.y + 7
        pygame.draw.rect(surf, C_BLACK, (ex,      ey, 4, 4))   # olho esquerdo
        pygame.draw.rect(surf, C_BLACK, (ex + 10, ey, 4, 4))   # olho direito

        # Boca: retângulo horizontal centralizado
        pygame.draw.rect(surf, C_BLACK, (ex + 2, ey + 9, 8, 3))

