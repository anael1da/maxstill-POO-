

import pygame
from config import SW, font_lg, font_md, font_sm
from colors import C_WHITE, C_GRAY, C_ACCENT, C_YELLOW


def draw_rect_border(surf, color, rect, radius=4, border=2):
    """
    Desenha um retângulo colorido com borda mais escura.

    """
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    # Gera cor mais escura diminuindo cada componente RGB em 60 unidades
    darker = tuple(max(0, c - 60) for c in color)
    pygame.draw.rect(surf, darker, rect, border, border_radius=radius)


def draw_text_center(surf, text, font, color, cx, cy):
    """
    Renderiza texto centralizado horizontalmente em torno de (cx, cy).

    """
    img = font.render(text, True, color)
    # Desloca o blit para que o centro da imagem coincida com (cx, cy)
    surf.blit(img, (cx - img.get_width() // 2, cy - img.get_height() // 2))


def draw_text(surf, text, font, color, x, y):
    """
    Renderiza texto alinhado à esquerda a partir de (x, y).

    """
    surf.blit(font.render(text, True, color), (x, y))


def wrap_text(text, font, max_width):
    """
    Quebra uma string longa em múltiplas linhas respeitando max_width pixels.

    """
    words = text.split()
    lines, line = [], ""
    for w in words:
        test = (line + " " + w).strip()
        if font.size(test)[0] <= max_width:
            line = test
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines

# ─────────────────────────────────────────────────────
#  HUD SUPERIOR DO JOGO
# ─────────────────────────────────────────────────────
def draw_hud(surf, player, phase_label):
    """
    Desenha a barra de HUD no topo da tela durante a exploração.

    Parâmetros:
        surf        → surface principal
        player      → objeto Player (para pistas e pontuação)
        phase_label → string descrevendo o estado atual do jogo
                      (ex.: "Explore a escola..." ou "CONVERSA")

    Layout da barra (46px de altura):
        Esquerda → título do jogo e phase_label
        Direita  → contador de pistas e pontuação

    Impacto no jogo:
        Mantém o jogador informado sobre seu progresso (pistas coletadas)
        e o estado atual sem interromper a gameplay.
    """
    s = pygame.Surface((SW, 46), pygame.SRCALPHA)
    s.fill((5, 3, 15, 210))
    surf.blit(s, (0, 0))
    pygame.draw.line(surf, C_ACCENT, (0, 46), (SW, 46), 1)   # linha separadora

    draw_text(surf, "EU SEI O QUE VOCÊS FIZERAM", font_sm, C_ACCENT, 10,  6)
    draw_text(surf, phase_label,                  font_sm, C_WHITE,  10, 24)

    pts_txt = f"Pistas: {len(player.pistas)}/4   Pontos: {player.score}"
    pts_img = font_md.render(pts_txt, True, C_YELLOW)
    surf.blit(pts_img, (SW - pts_img.get_width() - 10, 12))


