
"""
corrida.py — Competição entre Max e Romerito.
"""

from pathlib import Path
import pygame
from config import SW, SH


class Corrida:

    def __init__(self):

        # CARREGAR CENÁRIO
        caminho = Path(__file__).parent / "assets" / "pista_corrida.png"

        imagem = pygame.image.load(str(caminho)).convert()

        escala = min(
            SW / imagem.get_width(),
            SH / imagem.get_height()
        )

        largura = round(imagem.get_width() * escala)
        altura = round(imagem.get_height() * escala)

        imagem = pygame.transform.smoothscale(
            imagem,
            (largura, altura)
        )

        self.background = pygame.Surface((SW, SH))
        self.background.fill((20, 18, 27))

        self.offset_x = (SW - largura) // 2
        self.offset_y = (SH - altura) // 2

        self.background.blit(
            imagem,
            (self.offset_x, self.offset_y)
        )

        # LIMITES DA PISTA
        topo_pista = self.offset_y + round(347 * escala)
        fim_pista = self.offset_y + round(620 * escala)

        self.walls = [
            pygame.Rect(0, 0, SW, topo_pista),
            pygame.Rect(0, fim_pista, SW, SH - fim_pista),
            pygame.Rect(0, 0, 4, SH),
            pygame.Rect(SW - 4, 0, 4, SH),
        ]

        self.player_y = (topo_pista + fim_pista) // 2

        # ROMERITO
        self.rival_x = 80
        self.rival_y = self.player_y - 55
        self.rival_speed = 2.5

        sprite_path = (
            Path(__file__).parent
            / "assets"
            / "romerito.png"
        )

        sprite_sheet = pygame.image.load(
            str(sprite_path)
        ).convert_alpha()

        # RECORTAR ROMERITO CORRENDO
        self.rival_sprite = sprite_sheet.subsurface(
            pygame.Rect(961, 595, 217, 314)
        ).copy()

        self.rival_sprite = pygame.transform.scale(
            self.rival_sprite,
            (55, 80)
        )

        # CHEGADA
        self.finish_x = SW - 60

        self.done = False
        self.winner = None

    # ATUALIZAR CORRIDA
    def update(self, player, keys):

        if self.done:
            return

        # MAX
        if keys[pygame.K_SPACE] or keys[pygame.K_d]:
            player.move(1, 0, self.walls)
        else:
            player.stop()

        # ROMERITO
        self.rival_x += self.rival_speed

        # VERIFICAR VENCEDOR
        if player.x >= self.finish_x:

            self.winner = "max"
            self.done = True

        elif self.rival_x >= self.finish_x:

            self.winner = "romerito"
            self.done = True

    # DESENHAR CORRIDA
    def draw(self, screen):

        screen.blit(self.background, (0, 0))

        # LINHA DE CHEGADA
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (self.finish_x, 0),
            (self.finish_x, SH),
            4
        )

        # DESENHAR ROMERITO
        screen.blit(
            self.rival_sprite,
            (
                int(self.rival_x),
                int(self.rival_y - 40)
            )
        )
