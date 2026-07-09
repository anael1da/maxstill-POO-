import pygame
import sys

from menu import Menu
from escola import Escola
from sala_pc import SalaPC
from desafio_fios import DesafioFios
from creditos import Creditos
from dialogos import falas_escola, falas_hugo

pygame.init()

# ======================
# TELA
# ======================

LARGURA = 1280
ALTURA = 720

tela = pygame.display.set_mode(
    (LARGURA, ALTURA)
)

pygame.display.set_caption(
    "Eu Sei O Que Voces Fizeram Na Corrida Passada"
)

clock = pygame.time.Clock()

# ======================
# CORES
# ======================

BRANCO = (255, 255, 255)
VERDE = (0, 255, 120)
PRETO = (20, 20, 20)

# ======================
# FONTE
# ======================

fonte = pygame.font.SysFont(
    "Arial",
    30
)

# ======================
# OBJETOS
# ======================

menu = Menu()
escola = Escola()
sala_pc = SalaPC()
desafio_fios = DesafioFios()
creditos = Creditos()

# ======================
# CONTROLE
# ======================

fase = "menu"

fala_escola_atual = 0
fala_hugo_atual = 0

rodando = True

# ======================
# LOOP PRINCIPAL
# ======================

while rodando:

    clock.tick(60)

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:

            # MENU
            if fase == "menu":

                if menu.botao_jogar.collidepoint(evento.pos):

                    fase = "escola"

                elif menu.botao_creditos.collidepoint(evento.pos):

                    fase = "creditos"

                elif menu.botao_sair.collidepoint(evento.pos):
                    print("CLICOU EM SAIR")

                    rodando = False

            # CRÉDITOS
            elif fase == "creditos":

                fase = "menu"

            # ESCOLA
            elif fase == "escola":

                if fala_escola_atual < len(falas_escola) - 1:

                    fala_escola_atual += 1

                else:

                    fase = "sala_pc"

            # SALA PC
            elif fase == "sala_pc":

                if fala_hugo_atual < len(falas_hugo) - 1:

                    fala_hugo_atual += 1

                else:

                    fase = "desafio_fios"

            # DESAFIO DOS FIOS
            elif fase == "desafio_fios":

                desafio_fios.clique(evento.pos)

                if desafio_fios.concluido():

                    fase = "pista_hugo"

        elif evento.type == pygame.MOUSEMOTION:

            if fase == "desafio_fios":

                desafio_fios.mover_mouse(evento.pos)

        elif evento.type == pygame.MOUSEBUTTONUP:

            if fase == "desafio_fios":

                desafio_fios.soltar(evento.pos)

                if desafio_fios.concluido():

                    fase = "pista_hugo"

    # ======================
    # MENU
    # ======================

    if fase == "menu":

        menu.desenhar(tela)

    # ======================
    # CRÉDITOS
    # ======================

    elif fase == "creditos":

        creditos.desenhar(
            tela,
            fonte
        )

    # ======================
    # ESCOLA
    # ======================

    elif fase == "escola":

        escola.desenhar(tela)

        pygame.draw.rect(
            tela,
            PRETO,
            (40, 520, 1200, 150),
            border_radius=20
        )

        pygame.draw.rect(
            tela,
            VERDE,
            (40, 520, 1200, 150),
            3,
            border_radius=20
        )

        texto = fonte.render(
            falas_escola[fala_escola_atual],
            True,
            BRANCO
        )

        tela.blit(
            texto,
            (70, 580)
        )

    # ======================
    # SALA PC
    # ======================

    elif fase == "sala_pc":

        sala_pc.desenhar(tela)

        pygame.draw.rect(
            tela,
            PRETO,
            (40, 520, 1200, 150),
            border_radius=20
        )

        pygame.draw.rect(
            tela,
            VERDE,
            (40, 520, 1200, 150),
            3,
            border_radius=20
        )

        texto = fonte.render(
            falas_hugo[fala_hugo_atual],
            True,
            BRANCO
        )

        tela.blit(
            texto,
            (70, 580)
        )

    # ======================
    # DESAFIO DOS FIOS
    # ======================

    elif fase == "desafio_fios":

        desafio_fios.desenhar(
            tela,
            fonte
        )

    pygame.display.flip()

pygame.quit()
sys.exit()