
import sys
import math
import random
import pygame
from config import SW, SH, TILE, FPS, font_lg, font_md, font_sm
from colors import (
    C_BLACK, C_WHITE, C_GRAY, C_DGRAY, C_ACCENT,
    C_GREEN, C_RED, C_YELLOW,
)
from utils import draw_text, draw_text_center


# ─────────────────────────────────────────────────────
#  FONTES E CORES EXCLUSIVAS DESTAS TELAS
# ─────────────────────────────────────────────────────
# Criadas uma única vez (fora do loop) por eficiência — o código original
# recriava a fonte do título a cada frame dentro do while.
font_title  = pygame.font.SysFont("monospace", 32, bold=True)  # títulos grandes (vitória)
font_title2 = pygame.font.SysFont("monospace", 23, bold=True)  # títulos de 2 linhas (derrota)
font_stamp  = pygame.font.SysFont("monospace", 18, bold=True)  # carimbo do cartaz
font_btn    = pygame.font.SysFont("monospace", 19, bold=True)  # itens de menu

CORK      = (58, 43, 33)     # cortiça (fundo do quadro)
CORK_DOT  = (74, 57, 44)     # textura pontilhada da cortiça
BANNER_BG = (28, 20, 16)     # faixa escura de cabeçalho
PAPER     = (223, 212, 184)  # papel do cartaz/ficha
PAPER_DK  = (196, 182, 150)  # sombra/borda do papel


# ─────────────────────────────────────────────────────
#  ELEMENTOS DECORATIVOS REUTILIZÁVEIS
# ─────────────────────────────────────────────────────
def draw_corkboard(surf):
    """
    Preenche o fundo com uma textura de quadro de cortiça (estática).

    Substitui a antiga grade de linhas pulsantes em arco-íris do menu
    original — mantém uma textura sutil sem depender de cores piscando,
    e reforça o tema de "quadro de investigação" usado em toda a UI.
    """
    surf.fill(CORK)
    for y in range(10, SH, 20):
        for x in range(10, SW, 20):
            shade = CORK_DOT if (x // 20 + y // 20) % 2 == 0 else CORK
            pygame.draw.circle(surf, shade, (x, y), 1)


def draw_pin(surf, x, y, color=C_RED):
    """Desenha um pequeno alfinete/percevejo (sombra + cabeça colorida + brilho)."""
    pygame.draw.circle(surf, (20, 15, 12), (x + 1, y + 2), 5)
    pygame.draw.circle(surf, color, (x, y), 5)
    pygame.draw.circle(surf, C_WHITE, (x - 1, y - 1), 1)


def draw_missing_poster(surf, cx, cy):
    """
    Desenha um pequeno cartaz "DESAPARECIDO" com a silhueta do professor
    Romerito, levemente rotacionado e preso por um alfinete — como se
    estivesse pregado no quadro de investigação.
    """
    w, h = 168, 196
    # SRCALPHA + fill transparente: sem isso, pygame.transform.rotate()
    # preencheria os cantos "sobrando" da rotação com preto sólido em vez
    # de transparente, aparecendo como um quadrado preto atrás do cartaz.
    poster = pygame.Surface((w, h), pygame.SRCALPHA)
    poster.fill((0, 0, 0, 0))
    pygame.draw.rect(poster, PAPER, (0, 0, w, h))
    pygame.draw.rect(poster, PAPER_DK, (0, 0, w, h), 4)

    draw_text_center(poster, "DESAPARECIDO", font_stamp, C_RED, w // 2, 20)
    pygame.draw.line(poster, C_RED, (14, 32), (w - 14, 32), 2)

    # silhueta simples (cabeça + tronco) representando o professor
    pygame.draw.circle(poster, C_DGRAY, (w // 2, 78), 28)
    pygame.draw.rect(poster, C_DGRAY, (w // 2 - 38, 106, 76, 66), border_radius=10)

    draw_text_center(poster, "PROF. ROMERITO", font_sm, C_BLACK, w // 2, h - 38)
    draw_text_center(poster, "Visto pela última vez", font_sm, C_GRAY, w // 2, h - 22)
    draw_text_center(poster, "na escola.", font_sm, C_GRAY, w // 2, h - 8)

    rotated = pygame.transform.rotate(poster, -3)
    rect = rotated.get_rect(center=(cx, cy))
    surf.blit(rotated, rect)
    draw_pin(surf, cx, rect.top + 6)


CREDITS_TEAM = "TURMA: INFOWEB 2M"
CREDITS_DEVS = [
    "Ana Elida N. de Souza",
    "Ana Allyce da Silva",
    "Lays Eduarda A. Silva",
]


def draw_credits_block(surf, cx, top_y, shake=False):
    """
    Desenha o bloco "CRÉDITOS" (turma + desenvolvedoras) centralizado
    horizontalmente em cx, começando em top_y.

    Parâmetro:
        shake → se True, aplica um pequeno tremor (poucos pixels,
                recalculado a cada frame) em cada linha. Usado nas telas
                de vitória/derrota para dar um toque de "selo final".

    Retorna a altura total ocupada pelo bloco (para permitir empilhar
    outros elementos depois dele).
    """
    rows = [("CRÉDITOS", font_title2, C_ACCENT)]
    rows.append((CREDITS_TEAM, font_md, C_WHITE))
    rows.append(("Desenvolvedoras:", font_md, C_YELLOW))
    for dev in CREDITS_DEVS:
        rows.append((dev, font_md, C_WHITE))

    line_h = 28
    y = top_y
    for i, (text, font, color) in enumerate(rows):
        if shake:
            t = pygame.time.get_ticks() / 1000  # tempo em segundos
    
            ox = math.sin(t * 2.2 + i * 0.7) * 0.5
            oy = math.cos(t * 1.8 + i * 0.7) * 0.3
        else:
            ox = oy = 0
    
        draw_text_center(surf, text, font, color, cx + ox, y + oy)
        y += line_h



# ─────────────────────────────────────────────────────
#  TELA DE TÍTULO / MENU PRINCIPAL
# ─────────────────────────────────────────────────────
MENU_OPTIONS = ["INICIAR INVESTIGAÇÃO", "CRÉDITOS", "SAIR"]


def screen_title(surf, clock):
    """
    Exibe o menu principal e aguarda a escolha do jogador.

    Layout ("ficha de caso" pregada em um quadro de cortiça):
        - Faixa superior com o título do jogo
        - Cartaz "DESAPARECIDO" do prof. Romerito à esquerda
        - Briefing do caso + tabela de controles à direita
        - Menu navegável: INICIAR INVESTIGAÇÃO / CRÉDITOS / SAIR

    Controles:
        W/S ou ↑/↓ → navega entre as opções
        ENTER / ESPAÇO → confirma a opção selecionada
        ESC → encerra o programa

    Impacto no jogo:
        Primeira coisa que o jogador vê. "CRÉDITOS" abre screen_credits()
        e retorna para este mesmo menu; "SAIR" encerra o programa;
        "INICIAR INVESTIGAÇÃO" retorna da função para começar o jogo.
    """
    selected = 0
    t = 0
    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_w, pygame.K_UP):
                    selected = (selected - 1) % len(MENU_OPTIONS)
                elif ev.key in (pygame.K_s, pygame.K_DOWN):
                    selected = (selected + 1) % len(MENU_OPTIONS)
                elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if selected == 0:
                        return                              # inicia o jogo
                    elif selected == 1:
                        screen_credits(surf, clock)          # abre créditos, depois volta pro menu
                    elif selected == 2:
                        pygame.quit(); sys.exit()
                elif ev.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        t += 1
        draw_corkboard(surf)

        # Faixa de cabeçalho com o título do jogo
        pygame.draw.rect(surf, BANNER_BG, (0, 0, SW, 92))
        pygame.draw.line(surf, C_ACCENT, (0, 92), (SW, 92), 2)
        draw_text_center(surf, "EU SEI O QUE VOCÊS FIZERAM", font_title, C_ACCENT, SW // 2, 32)
        draw_text_center(surf, "NA CORRIDA PASSADA",          font_title, C_ACCENT, SW // 2, 62)

        # Cartaz "desaparecido" à esquerda
        draw_missing_poster(surf, 150, 260)

        # Briefing do caso à direita do cartaz
        bx = 262
        draw_text(surf, "Você é MAX, um aluno curioso.",           font_md, C_WHITE, bx, 148)
        draw_text(surf, "O prof. Romerito desapareceu na",         font_md, C_WHITE, bx, 174)
        draw_text(surf, "véspera da festa de encerramento.",       font_md, C_WHITE, bx, 200)
        draw_text(surf, "Investigue os 4 suspeitos e descubra",    font_md, C_WHITE, bx, 226)
        draw_text(surf, "o que aconteceu com ele!",                font_md, C_WHITE, bx, 252)

        controls = [("W A S D", "Mover"), ("E / ESPAÇO", "Interagir"), ("ESC", "Pausar/Sair")]
        for i, (k, v) in enumerate(controls):
            cy = 292 + i * 32
            pygame.draw.rect(surf, C_DGRAY, (bx, cy, 330, 26), border_radius=4)
            draw_text(surf, k, font_sm, C_ACCENT, bx + 8,   cy + 6)
            draw_text(surf, v, font_sm, C_WHITE,  bx + 168, cy + 6)

        # Menu de opções
        my = 428
        pulse = int(20 * (0.5 + 0.5 * math.sin(t / 12)))   # leve respiração só no item selecionado
        for i, opt in enumerate(MENU_OPTIONS):
            is_sel = (i == selected)
            bw, bh = 330, 42
            rx, ry = SW // 2 - bw // 2, my + i * 52

            bg = (90 + pulse, 58, 20) if is_sel else C_DGRAY
            pygame.draw.rect(surf, bg, (rx, ry, bw, bh), border_radius=6)
            pygame.draw.rect(surf, C_ACCENT if is_sel else C_GRAY, (rx, ry, bw, bh), 2, border_radius=6)

            col = C_YELLOW if is_sel else C_WHITE
            draw_text_center(surf, opt, font_btn, col, SW // 2, ry + bh // 2)
            if is_sel:
                draw_text(surf, ">", font_btn, C_ACCENT, rx - 20, ry + bh // 2 - 9)

        draw_text_center(surf, "W/S ou ↑/↓ para navegar   •   ENTER para confirmar",
                         font_sm, C_GRAY, SW // 2, SH - 18)

        pygame.display.flip()



# ─────────────────────────────────────────────────────
#  TELA DE CRÉDITOS (a partir do menu)
# ─────────────────────────────────────────────────────
def screen_credits(surf, clock):
    """
    Exibe a ficha de créditos (turma e desenvolvedoras) em um cartão
    de papel pregado no quadro, acessível pela opção "CRÉDITOS" do menu.

    Controles:
        ENTER / ESPAÇO / ESC → volta para o menu principal (retorna da função)
    """
    t = 0
    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                    return

        t += 1
        draw_corkboard(surf)
        pygame.draw.rect(surf, BANNER_BG, (0, 0, SW, 70))
        pygame.draw.line(surf, C_ACCENT, (0, 70), (SW, 70), 2)
        draw_text_center(surf, "CRÉDITOS", font_title, C_ACCENT, SW // 2, 35)

        card_w, card_h = 420, 260
        card = pygame.Surface((card_w, card_h))
        card.fill(PAPER)
        pygame.draw.rect(card, PAPER_DK, (0, 0, card_w, card_h), 4)
        draw_text_center(card, CREDITS_TEAM,        font_md, C_BLACK, card_w // 2, 42)
        draw_text_center(card, "DESENVOLVEDORAS",   font_md, C_RED,   card_w // 2, 92)
        for i, dev in enumerate(CREDITS_DEVS):
            draw_text_center(card, dev, font_md, C_DGRAY, card_w // 2, 134 + i * 34)

        rect = card.get_rect(center=(SW // 2, SH // 2 + 14))
        surf.blit(card, rect)
        draw_pin(surf, SW // 2, rect.top + 6)

        blink = int(t / 20) % 2 == 0
        if blink:
            draw_text_center(surf, "[ ENTER / ESC para voltar ]", font_sm, C_GRAY, SW // 2, SH - 26)

        pygame.display.flip()



# ─────────────────────────────────────────────────────
#  TELA DE PAUSA
# ─────────────────────────────────────────────────────
def screen_pause(surf, clock):
    """
    Sobreposição de pausa semi-transparente sobre o jogo.

    Controles:
        ESC → retoma o jogo (retorna "resume")
        Q   → encerra o programa

    Impacto no jogo:
        Permite ao jogador pausar sem perder o estado atual.
        O fundo do jogo continua visível sob a sobreposição (SRCALPHA).
        É acionada pelo ESC durante a fase "explore".
    """
    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE: return "resume"
                if ev.key == pygame.K_q:
                    pygame.quit(); sys.exit()

        # Overlay escuro semi-transparente (preserva o quadro anterior do jogo)
        s = pygame.Surface((SW, SH), pygame.SRCALPHA)
        s.fill((0, 0, 0, 160))
        surf.blit(s, (0, 0))

        draw_text_center(surf, "PAUSADO",         font_lg, C_ACCENT, SW // 2, SH // 2 - 60)
        draw_text_center(surf, "ESC  – Continuar", font_md, C_WHITE,  SW // 2, SH // 2)
        draw_text_center(surf, "Q    – Sair",      font_md, C_RED,    SW // 2, SH // 2 + 40)
        pygame.display.flip()



# ─────────────────────────────────────────────────────
#  TELA DE PISTAS (TAB)
# ─────────────────────────────────────────────────────
def screen_pistas(surf, clock, player):
    """
    Exibe o caderno de pistas coletadas pelo jogador.

    Acessada pressionando TAB durante a exploração.
    Qualquer tecla fecha a tela e retorna ao jogo.

    Layout:
        - Fundo escuro sólido
        - Título "CADERNO DE PISTAS"
        - Cada pista em painel individual com borda dourada
          (máximo de 4 pistas, uma por NPC vencido)
        - Mensagem se nenhuma pista foi coletada ainda

    Impacto no jogo:
        Permite ao jogador rever as pistas coletadas para
        entender a narrativa sem precisar memorizar tudo.
        Cada pista revela um detalhe do paradeiro de Romerito.
    """
    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                return   # qualquer tecla fecha

        surf.fill((10, 8, 20))
        draw_text_center(surf, "CADERNO DE PISTAS", font_lg, C_ACCENT, SW // 2, 50)

        if not player.pistas:
            draw_text_center(surf, "Nenhuma pista ainda. Fale com os suspeitos!",
                             font_md, C_GRAY, SW // 2, SH // 2)

        for i, p in enumerate(player.pistas):
            bx, by = 60, 100 + i * 90
            pygame.draw.rect(surf, C_DGRAY,  (bx, by, SW - 120, 80), border_radius=6)
            pygame.draw.rect(surf, C_ACCENT, (bx, by, SW - 120, 80), 2, border_radius=6)
            for j, ln in enumerate(p.split("\n")):
                draw_text(surf, ln, font_md, C_WHITE, bx + 14, by + 12 + j * 22)

        draw_text_center(surf, "[ qualquer tecla para voltar ]",
                         font_sm, C_GRAY, SW // 2, SH - 30)
        pygame.display.flip()



# ─────────────────────────────────────────────────────
#  TELA FINAL (vitória ou derrota)
# ─────────────────────────────────────────────────────
def screen_final(surf, clock, player):
    """
    Exibe o desfecho da investigação, os créditos (com pequeno tremor) e
    as opções de reinício/saída.

    Dois desfechos possíveis:
        VITÓRIA (4/4 pistas coletadas):
            "VOCÊ ENCONTROU ROMERITO!" — ele estava preparando uma surpresa.
        DERROTA (todos os suspeitos abordados, mas pistas incompletas):
            "ROMERITO CONTINUA PERDIDO CORRENDO POR AÍ..."

    Em ambos os casos, logo abaixo do texto de desfecho é exibido o bloco
    de créditos com uma pequena animação de tremor (shake).

    Controles:
        ENTER → reinicia o jogo (a função retorna; Game.reset() é chamado
                pelo chamador, sem passar pelo menu novamente)
        ESC / Q → encerra o programa

    Impacto no jogo:
        É a tela de conclusão de cada partida — sempre oferece ao jogador
        a chance de jogar de novo ou sair, sem forçar volta ao menu.
    """
    t    = 0
    full = len(player.pistas) >= 4

    while True:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    return                       # reinicia (reset() é chamado por quem chamou)
                if ev.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit(); sys.exit()

        t += 1
        draw_corkboard(surf)

        pygame.draw.rect(surf, BANNER_BG, (0, 0, SW, 70))
        pygame.draw.line(surf, C_ACCENT, (0, 70), (SW, 70), 2)

        if full:
            draw_text_center(surf, "VOCÊ ENCONTROU ROMERITO!", font_title, C_GREEN, SW // 2, 35)
        else:
            draw_text_center(surf, "ROMERITO CONTINUA PERDIDO", font_title2, C_RED, SW // 2, 22)
            draw_text_center(surf, "CORRENDO POR AÍ...",        font_title2, C_RED, SW // 2, 50)

        # Narrativa curta do desfecho
        if full:
            lines = [
                "Com as informações dos 4 suspeitos, MAX foi",
                "direto à sala dos professores — lá estava Romerito,",
                "preparando uma surpresa para a festa da escola!",
            ]
        else:
            n = len(player.pistas)
            lines = [
                f"Você coletou apenas {n}/4 pistas.",
                "MAX até encontrou o professor, mas não entendeu",
                "completamente o que havia acontecido...",
            ]
        for i, ln in enumerate(lines):
            draw_text_center(surf, ln, font_sm, C_WHITE, SW // 2, 96 + i * 20)

        draw_text_center(surf, f"Pontuação final: {player.score}", font_md, C_YELLOW, SW // 2, 172)
        pygame.draw.line(surf, C_GRAY, (SW // 2 - 210, 194), (SW // 2 + 210, 194), 1)

        # Bloco de créditos com pequena animação de tremor
        draw_credits_block(surf, SW // 2, 210, shake=True)

        blink = int(t / 20) % 2 == 0
        if blink:
            draw_text_center(surf, "ENTER – Jogar novamente     ESC – Sair",
                             font_sm, C_GRAY, SW // 2, SH - 24)

        pygame.display.flip()
