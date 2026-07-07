import pygame

class Escola:

    def __init__(self):

        self.fundo = pygame.image.load(
            "imagens/escola.png"
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

        # TEMPORÁRIO
        # enquanto aluno.png não funciona

        self.aluno = pygame.image.load(
            "imagens/aluno.png"
        )

        self.aluno = pygame.transform.scale(
            self.aluno,
            (280, 380)
        )

    def desenhar(self, tela):

        tela.blit(self.fundo, (0, 0))

        tela.blit(self.max, (150, 220))

        tela.blit(self.aluno, (850, 220))