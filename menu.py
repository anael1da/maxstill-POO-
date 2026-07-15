import pygame
import os


class Menu:

    def __init__(self):

        pasta = os.path.dirname(__file__)

        caminho = os.path.join(
            pasta,
            "imagens",
            "capa.png"
        )

        self.fundo = pygame.image.load(caminho).convert()

        self.fundo = pygame.transform.scale(
            self.fundo,
            (1280, 720)
        )

       # JOGAR
        self.botao_jogar = pygame.Rect(
            400, 342,
            500, 95 #largura
        )

       # CRÉDITOS
        self.botao_creditos = pygame.Rect(
         400, 460,
         500, 65
        )

       # SAIR
        self.botao_sair = pygame.Rect(
         400, 536,
         500, 65
        )

    def desenhar(self, tela):

        tela.blit(self.fundo, (0, 0))
        # # Botões invisiveis
        # pygame.draw.rect(tela, (255, 0, 0), self.botao_jogar, 3)
        # pygame.draw.rect(tela, (0, 255, 0), self.botao_creditos, 3)
        # pygame.draw.rect(tela, (0, 0, 255), self.botao_sair, 3)