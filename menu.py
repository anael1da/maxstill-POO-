import pygame


class Menu:

    def __init__(self):

        self.fundo = pygame.image.load(
            "imagens/capa.png"
        )

        self.fundo = pygame.transform.scale(
            self.fundo,
            (1280, 720)
        )

        # BOTÃO JOGAR
        self.botao_jogar = pygame.Rect(
            400,
            360,
            500,
            95
        )

        # BOTÃO CRÉDITOS
        self.botao_creditos = pygame.Rect(
            400,
            485,
            500,
            80
        )

        # BOTÃO SAIR
        self.botao_sair = pygame.Rect(
            400,
            605,
            500,
            80
        )

    def desenhar(self, tela):

        tela.blit(
            self.fundo,
            (0, 0)
        )