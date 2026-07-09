import pygame


class Creditos:

    def desenhar(self, tela, fonte):

        tela.fill((15, 15, 15))

        titulo = pygame.font.SysFont(
            "Arial",
            60,
            bold=True
        )

        texto_titulo = titulo.render(
            "CRÉDITOS",
            True,
            (0, 255, 120)
        )

        tela.blit(
            texto_titulo,
            (470, 80)
        )

        linhas = [

            "Desenvolvedor: Ana Allyce, Lays Eduarda, Ana Elida",

            "Historia: Ana Allyce, lays eduarda, Ana Elida",

            "Programacao: Ana Allyce, Lays Eduarda, Ana Elida",

            "Agradecimentos especiais:",

            "Professor Hugo",

            "Rickson",

            "Anderson",

            "Alessandro",

            "Romerito"
        ]

        y = 220

        for linha in linhas:

            texto = fonte.render(
                linha,
                True,
                (255, 255, 255)
            )

            tela.blit(
                texto,
                (350, y)
            )

            y += 50