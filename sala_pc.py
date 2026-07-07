import pygame

class SalaPC:

    def __init__(self):

        self.fundo = pygame.image.load(
            "imagens/sala_pc.png"
        )

        self.fundo = pygame.transform.scale(
            self.fundo,
            (1280, 720)
        )

        self.max = pygame.image.load(
            "imagens/max.png"
        )

        self.max = pygame.transform.scale(
            self.max,
            (280, 380)
        )

        self.hugo = pygame.image.load(
            "imagens/hugo.png"
        )

        self.hugo = pygame.transform.scale(
            self.hugo,
            (280, 380)
        )

    def desenhar(self, tela):

        tela.blit(
            self.fundo,
            (0, 0)
        )

        tela.blit(
            self.max,
            (150, 220)
        )

        tela.blit(
            self.hugo,
            (850, 220)
        )