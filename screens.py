
"""
screens.py — Telas de estado do jogo: título, pausa, pistas, créditos e final.

Estética "quadro de investigação" (cortiça + papel + fita + alfinete).
"""

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
# FONTES E CORES
# ─────────────────────────────────────────────────────

font_title = pygame.font.SysFont("monospace", 32, bold=True)
font_title2 = pygame.font.SysFont("monospace", 23, bold=True)
font_stamp = pygame.font.SysFont("monospace", 18, bold=True)
font_btn = pygame.font.SysFont("monospace", 19, bold=True)

CORK = (58, 43, 33)
CORK_DOT = (74, 57, 44)
BANNER_BG = (28, 20, 16)
PAPER = (223, 212, 184)
PAPER_DK = (196, 182, 150)


# ─────────────────────────────────────────────────────
# ELEMENTOS DECORATIVOS
# ─────────────────────────────────────────────────────

def draw_corkboard(surf):

    surf.fill(CORK)

    for y in range(10, SH, 20):
        for x in range(10, SW, 20):
            shade = CORK_DOT if (x // 20 + y // 20) % 2 == 0 else CORK
            pygame.draw.circle(surf, shade, (x, y), 1)


def draw_pin(surf, x, y, color=C_RED):

    pygame.draw.circle(surf, (20, 15, 12), (x + 1, y + 2), 5)
    pygame.draw.circle(surf, color, (x, y), 5)
    pygame.draw.circle(surf, C_WHITE, (x - 1, y - 1), 1)


def draw_missing_poster(surf, cx, cy):

    w, h = 168, 196

    poster = pygame.Surface((w, h), pygame.SRCALPHA)
    poster.fill((0, 0, 0, 0))

    pygame.draw.rect(poster, PAPER, (0, 0, w, h))
    pygame.draw.rect(poster, PAPER_DK, (0, 0, w, h), 4)

    draw_text_center(poster, "DESAPARECIDO", font_stamp, C_RED, w // 2, 20)

    pygame.draw.line(poster, C_RED, (14, 32), (w - 14, 32), 2)

    pygame.draw.circle(poster, C_DGRAY, (w // 2, 78), 28)
    pygame.draw.rect(
        poster,
        C_DGRAY,
        (w // 2 - 38, 106, 76, 66),
        border_radius=10
    )

    draw_text_center(poster, "PROF. ROMERITO", font_sm, C_BLACK, w // 2, h - 38)
    draw_text_center(poster, "Visto pela última vez", font_sm, C_GRAY, w // 2, h - 22)
    draw_text_center(poster, "na escola.", font_sm, C_GRAY, w // 2, h - 8)

    rotated = pygame.transform.rotate(poster, -3)
    rect = rotated.get_rect(center=(cx, cy))

    surf.blit(rotated, rect)
    draw_pin(surf, cx, rect.top + 6)


# ─────────────────────────────────────────────────────
# CRÉDITOS
# ─────────────────────────────────────────────────────

CREDITS_TEAM = "TURMA: INFOWEB 2M"

CREDITS_DEVS = [
    "Ana Elida N. de Souza",
    "Ana Allyce da Silva",
    "Lays Eduarda A. Silva",
]


def draw_credits_block(surf, cx, top_y, shake=False):

    rows = [("CRÉDITOS", font_title2, C_ACCENT)]
    rows.append((CREDITS_TEAM, font_md, C_WHITE))
    rows.append(("Desenvolvedoras:", font_md, C_YELLOW))

    for dev in CREDITS_DEVS:
        rows.append((dev, font_md, C_WHITE))

    line_h = 28
    y = top_y

    for i, (text, font, color) in enumerate(rows):

        if shake:
            t = pygame.time.get_ticks() / 1000

            ox = math.sin(t * 2.2 + i * 0.7) * 0.5
            oy = math.cos(t * 1.8 + i * 0.7) * 0.3
        else:
            ox = oy = 0

        draw_text_center(surf, text, font, color, cx + ox, y + oy)
        y += line_h


# ─────────────────────────────────────────────────────
# TELA DE TÍTULO / MENU PRINCIPAL
# ─────────────────────────────────────────────────────

MENU_OPTIONS = ["INICIAR INVESTIGAÇÃO", "CRÉDITOS", "SAIR"]


def screen_title(surf, clock):

    selected = 0
    t = 0

    while True:

        clock.tick(FPS)

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.KEYDOWN:

                print("TECLA PRESSIONADA:", pygame.key.name(ev.key))

                if ev.key in (pygame.K_w, pygame.K_UP):
                    selected = (selected - 1) % len(MENU_OPTIONS)

                elif ev.key in (pygame.K_s, pygame.K_DOWN):
                    selected = (selected + 1) % len(MENU_OPTIONS)

                elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):

                    if selected == 0:
                        return

                    elif selected == 1:
                        screen_credits(surf, clock)

                    elif selected == 2:
                        pygame.quit()
                        sys.exit()

                elif ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        t += 1

        draw_corkboard(surf)

        pygame.draw.rect(surf, BANNER_BG, (0, 0, SW, 92))
        pygame.draw.line(surf, C_ACCENT, (0, 92), (SW, 92), 2)

        draw_text_center(
            surf,
            "EU SEI O QUE VOCÊS FIZERAM",
            font_title,
            C_ACCENT,
            SW // 2,
            32
        )

        draw_text_center(
            surf,
            "NA CORRIDA PASSADA",
            font_title,
            C_ACCENT,
            SW // 2,
            62
        )

        draw_missing_poster(surf, 150, 260)

        bx = 262

        draw_text(surf, "Você é MAX, um aluno curioso.", font_md, C_WHITE, bx, 148)
        draw_text(surf, "O prof. Romerito desapareceu na", font_md, C_WHITE, bx, 174)
        draw_text(surf, "véspera da festa de encerramento.", font_md, C_WHITE, bx, 200)
        draw_text(surf, "Investigue os 4 suspeitos e descubra", font_md, C_WHITE, bx, 226)
        draw_text(surf, "o que aconteceu com ele!", font_md, C_WHITE, bx, 252)

        controls = [
            ("W A S D", "Mover"),
            ("E / ESPAÇO", "Interagir"),
            ("ESC", "Pausar/Sair")
        ]

        for i, (k, v) in enumerate(controls):

            cy = 292 + i * 32

            pygame.draw.rect(
                surf,
                C_DGRAY,
                (bx, cy, 330, 26),
                border_radius=4
            )

            draw_text(surf, k, font_sm, C_ACCENT, bx + 8, cy + 6)
            draw_text(surf, v, font_sm, C_WHITE, bx + 168, cy + 6)

        my = 428
        pulse = int(20 * (0.5 + 0.5 * math.sin(t / 12)))

        for i, opt in enumerate(MENU_OPTIONS):

            is_sel = (i == selected)

            bw, bh = 330, 42
            rx = SW // 2 - bw // 2
            ry = my + i * 52

            bg = (90 + pulse, 58, 20) if is_sel else C_DGRAY

            pygame.draw.rect(
                surf,
                bg,
                (rx, ry, bw, bh),
                border_radius=6
            )

            pygame.draw.rect(
                surf,
                C_ACCENT if is_sel else C_GRAY,
                (rx, ry, bw, bh),
                2,
                border_radius=6
            )

            col = C_YELLOW if is_sel else C_WHITE

            draw_text_center(
                surf,
                opt,
                font_btn,
                col,
                SW // 2,
                ry + bh // 2
            )

            if is_sel:
                draw_text(surf, ">", font_btn, C_ACCENT, rx - 20, ry + bh // 2 - 9)

        draw_text_center(
            surf,
            "W/S ou ↑/↓ para navegar   •   ENTER para confirmar",
            font_sm,
            C_GRAY,
            SW // 2,
            SH - 18
        )

        pygame.display.flip()


# ─────────────────────────────────────────────────────
# TELA DE CRÉDITOS
# ─────────────────────────────────────────────────────

def screen_credits(surf, clock):

    t = 0

    while True:

        clock.tick(FPS)

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.KEYDOWN:

                if ev.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE,
                    pygame.K_ESCAPE
                ):
                    return

        t += 1

        draw_corkboard(surf)

        pygame.draw.rect(surf, BANNER_BG, (0, 0, SW, 70))
        pygame.draw.line(surf, C_ACCENT, (0, 70), (SW, 70), 2)

        draw_text_center(
            surf,
            "CRÉDITOS",
            font_title,
            C_ACCENT,
            SW // 2,
            35
        )

        card_w, card_h = 420, 260

        card = pygame.Surface((card_w, card_h))
        card.fill(PAPER)

        pygame.draw.rect(card, PAPER_DK, (0, 0, card_w, card_h), 4)

        draw_text_center(card, CREDITS_TEAM, font_md, C_BLACK, card_w // 2, 42)
        draw_text_center(card, "DESENVOLVEDORAS", font_md, C_RED, card_w // 2, 92)

        for i, dev in enumerate(CREDITS_DEVS):
            draw_text_center(card, dev, font_md, C_DGRAY, card_w // 2, 134 + i * 34)

        rect = card.get_rect(center=(SW // 2, SH // 2 + 14))

        surf.blit(card, rect)
        draw_pin(surf, SW // 2, rect.top + 6)

        blink = int(t / 20) % 2 == 0

        if blink:
            draw_text_center(
                surf,
                "[ ENTER / ESC para voltar ]",
                font_sm,
                C_GRAY,
                SW // 2,
                SH - 26
            )

        pygame.display.flip()


# ─────────────────────────────────────────────────────
# TELA DE PAUSA
# ─────────────────────────────────────────────────────

def screen_pause(surf, clock):

    while True:

        clock.tick(FPS)

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.KEYDOWN:

                if ev.key == pygame.K_ESCAPE:
                    return "resume"

                if ev.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        s = pygame.Surface((SW, SH), pygame.SRCALPHA)
        s.fill((0, 0, 0, 160))

        surf.blit(s, (0, 0))

        draw_text_center(
            surf,
            "PAUSADO",
            font_lg,
            C_ACCENT,
            SW // 2,
            SH // 2 - 60
        )

        draw_text_center(
            surf,
            "ESC  – Continuar",
            font_md,
            C_WHITE,
            SW // 2,
            SH // 2
        )

        draw_text_center(
            surf,
            "Q    – Sair",
            font_md,
            C_RED,
            SW // 2,
            SH // 2 + 40
        )

        pygame.display.flip()


# ─────────────────────────────────────────────────────
# TELA DE PISTAS
# ─────────────────────────────────────────────────────

def screen_pistas(surf, clock, player):

    while True:

        clock.tick(FPS)

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.KEYDOWN:
                return

        surf.fill((10, 8, 20))

        draw_text_center(
            surf,
            "CADERNO DE PISTAS",
            font_lg,
            C_ACCENT,
            SW // 2,
            50
        )

        if not player.pistas:

            draw_text_center(
                surf,
                "Nenhuma pista ainda. Fale com os suspeitos!",
                font_md,
                C_GRAY,
                SW // 2,
                SH // 2
            )

        for i, p in enumerate(player.pistas):

            bx, by = 60, 100 + i * 90

            pygame.draw.rect(
                surf,
                C_DGRAY,
                (bx, by, SW - 120, 80),
                border_radius=6
            )

            pygame.draw.rect(
                surf,
                C_ACCENT,
                (bx, by, SW - 120, 80),
                2,
                border_radius=6
            )

            for j, ln in enumerate(p.split("\n")):
                draw_text(
                    surf,
                    ln,
                    font_md,
                    C_WHITE,
                    bx + 14,
                    by + 12 + j * 22
                )

        draw_text_center(
            surf,
            "[ qualquer tecla para voltar ]",
            font_sm,
            C_GRAY,
            SW // 2,
            SH - 30
        )

        pygame.display.flip()


# ─────────────────────────────────────────────────────
# TELA FINAL
# ─────────────────────────────────────────────────────

def screen_final(surf, clock, player):

    t = 0
    full = len(player.pistas) >= 4

    while True:

        clock.tick(FPS)

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.KEYDOWN:

                if ev.key == pygame.K_RETURN:
                    return

                if ev.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()

        t += 1

        draw_corkboard(surf)

        pygame.draw.rect(surf, BANNER_BG, (0, 0, SW, 70))
        pygame.draw.line(surf, C_ACCENT, (0, 70), (SW, 70), 2)

        if full:

            draw_text_center(
                surf,
                "VOCÊ ENCONTROU ROMERITO!",
                font_title,
                C_GREEN,
                SW // 2,
                35
            )

        else:

            draw_text_center(
                surf,
                "ROMERITO CONTINUA PERDIDO",
                font_title2,
                C_RED,
                SW // 2,
                22
            )

            draw_text_center(
                surf,
                "CORRENDO POR AÍ...",
                font_title2,
                C_RED,
                SW // 2,
                50
            )

        # MENSAGEM DO DESFECHO
        if full:

            lines = [
                "Depois de enfrentar os quatro desafios,",
                "MAX entrou na corrida e finalmente encontrou",
                "Romerito! O mistério foi resolvido e a surpresa",
                "para a festa da escola estava garantida!"
            ]

        else:

            n = len(player.pistas)

            lines = [
                f"Você coletou apenas {n}/4 pistas.",
                "MAX ainda não conseguiu descobrir",
                "completamente o que aconteceu com Romerito..."
            ]

        for i, ln in enumerate(lines):

            draw_text_center(
                surf,
                ln,
                font_sm,
                C_WHITE,
                SW // 2,
                96 + i * 20
            )

        draw_text_center(
            surf,
            f"Pontuação final: {player.score}",
            font_md,
            C_YELLOW,
            SW // 2,
            192
        )

        pygame.draw.line(
            surf,
            C_GRAY,
            (SW // 2 - 210, 214),
            (SW // 2 + 210, 214),
            1
        )

        draw_credits_block(
            surf,
            SW // 2,
            230,
            shake=True
        )

        blink = int(t / 20) % 2 == 0

        if blink:

            draw_text_center(
                surf,
                "ENTER – Jogar novamente     ESC – Sair",
                font_sm,
                C_GRAY,
                SW // 2,
                SH - 24
            )

        pygame.display.flip()
