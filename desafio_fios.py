import pygame


class DesafioFios:

    def __init__(self):

        # pontos da esquerda
        self.esquerda = [
            (200, 180),
            (200, 320),
            (200, 460)
        ]

        # pontos da direita embaralhados
        self.direita = [
            (1000, 320),
            (1000, 460),
            (1000, 180)
        ]

        self.cores = [
            (255, 0, 0),
            (0, 100, 255),
            (0, 255, 0)
        ]

        self.arrastando = None

        self.pos_mouse = (0, 0)

        self.conectados = [False, False, False]

    def clique(self, pos):

        for i, ponto in enumerate(self.esquerda):

            if not self.conectados[i]:

                x, y = ponto

                if (pos[0]-x)**2 + (pos[1]-y)**2 < 25**2:

                    self.arrastando = i

    def mover_mouse(self, pos):

        self.pos_mouse = pos

    def soltar(self, pos):

        if self.arrastando is None:
            return

        i = self.arrastando

        x, y = self.direita[i]

        if (pos[0]-x)**2 + (pos[1]-y)**2 < 40**2:

            self.conectados[i] = True

        self.arrastando = None

    def concluido(self):

        return all(self.conectados)

    def desenhar(self, tela):

        tela.fill((35, 35, 35))

        fonte = pygame.font.SysFont("Arial", 40)

        titulo = fonte.render(
            "Conserte os fios dos computadores",
            True,
            (255, 255, 255)
        )

        tela.blit(titulo, (330, 50))

        # fios conectados
        for i in range(3):

            if self.conectados[i]:

                pygame.draw.line(
                    tela,
                    self.cores[i],
                    self.esquerda[i],
                    self.direita[i],
                    10
                )

        # fio sendo arrastado
        if self.arrastando is not None:

            pygame.draw.line(
                tela,
                self.cores[self.arrastando],
                self.esquerda[self.arrastando],
                self.pos_mouse,
                10
            )

        # conectores
        for i in range(3):

            pygame.draw.circle(
                tela,
                self.cores[i],
                self.esquerda[i],
                25
            )

            pygame.draw.circle(
                tela,
                self.cores[i],
                self.direita[i],
                25
            )