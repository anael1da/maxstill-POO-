import pygame
import sys

from menu import Menu
from creditos import Creditos

pygame.init()

# TELA
LARGURA = 1280
ALTURA = 720

tela = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption(
    "Eu Sei O Que Vocês Fizeram Na Corrida Passada"
)

clock = pygame.time.Clock()

# FONTE
fonte = pygame.font.SysFont("Arial", 30)

# OBJETOS
menu = Menu()
creditos = Creditos()

# CONTROLE DO JOGO
fase = "menu"
rodando = True

while rodando:

    clock.tick(60)

    # EVENTOS
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:

            # MENU
            if fase == "menu":

                if menu.botao_jogar.collidepoint(evento.pos):
                    print("BOTÃO JOGAR FUNCIONOU")
                    fase = "jogo"

                elif menu.botao_creditos.collidepoint(evento.pos):
                    fase = "creditos"

                elif menu.botao_sair.collidepoint(evento.pos):
                    rodando = False

            # VOLTAR DOS CRÉDITOS
            elif fase == "creditos":

                if creditos.botao_voltar.collidepoint(evento.pos):
                    fase = "menu"

            # VOLTAR DA TELA DE TESTE
            elif fase == "jogo":
                fase = "menu"

    # DESENHAR MENU
    if fase == "menu":

        menu.desenhar(tela)

    # DESENHAR CRÉDITOS
    elif fase == "creditos":

        creditos.desenhar(tela, fonte)

    # TESTE DO BOTÃO JOGAR
    elif fase == "jogo":

        tela.fill((10, 15, 20))

        titulo = pygame.font.SysFont(
            "Arial",
            60,
            bold=True
        )

        texto = titulo.render(
            "JOGO INICIADO!",
            True,
            (0, 255, 120)
        )

        tela.blit(
            texto,
            texto.get_rect(center=(640, 320))
        )

        aviso = fonte.render(
            "Clique para voltar ao menu",
            True,
            (255, 255, 255)
        )

        tela.blit(
            aviso,
            aviso.get_rect(center=(640, 400))
        )

    pygame.display.flip()

pygame.quit()
sys.exit()