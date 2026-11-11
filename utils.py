"""
utils.py — Funções utilitárias de desenho e texto.

Usadas por praticamente todos os outros módulos para renderizar
texto, retângulos com borda e a barra de HUD superior do jogo.
"""

import pygame
from config import SW, font_lg, font_md, font_sm
from colors import C_WHITE, C_GRAY, C_ACCENT, C_YELLOW


def draw_rect_border(surf, color, rect, radius=4, border=2):
    """
    Desenha um retângulo colorido com borda mais escura.

    Parâmetros:
        surf   → surface do Pygame onde será desenhado
        color  → cor de preenchimento (RGB)
        rect   → pygame.Rect definindo posição e tamanho
        radius → arredondamento dos cantos em pixels (padrão 4)
        border → espessura da borda em pixels (padrão 2)

    Efeito no jogo:
        Dá volume e profundidade aos sprites de personagens (player,
        NPCs, inimigos) tornando-os visualmente distintos do fundo.
        A borda mais escura é calculada subtraindo 60 de cada canal RGB,
        limitando no mínimo 0 para evitar valores negativos.
    """
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    # Gera cor mais escura diminuindo cada componente RGB em 60 unidades
    darker = tuple(max(0, c - 60) for c in color)
    pygame.draw.rect(surf, darker, rect, border, border_radius=radius)


def draw_text_center(surf, text, font, color, cx, cy):
    """
    Renderiza texto centralizado horizontalmente em torno de (cx, cy).

    Parâmetros:
        surf  → surface de destino
        text  → string a exibir
        font  → objeto Font do Pygame
        color → cor RGB
        cx    → coordenada X do centro desejado
        cy    → coordenada Y do centro desejado

    Efeito no jogo:
        Utilizado em títulos de telas (título, pausa, fim de jogo),
        mensagens de resultado dos minigames e textos de HUD centrados.
        Garante alinhamento automático independente do tamanho do texto.
    """
    img = font.render(text, True, color)
    # Desloca o blit para que o centro da imagem coincida com (cx, cy)
    surf.blit(img, (cx - img.get_width() // 2, cy - img.get_height() // 2))


def draw_text(surf, text, font, color, x, y):
    """
    Renderiza texto alinhado à esquerda a partir de (x, y).

    Parâmetros:
        surf  → surface de destino
        text  → string a exibir
        font  → objeto Font do Pygame
        color → cor RGB
        x, y  → coordenada do canto superior esquerdo do texto

    Efeito no jogo:
        Usada para labels de NPCs, indicadores de vidas/tentativas,
        linhas de diálogo e qualquer texto que não precise de centralização.
    """
    surf.blit(font.render(text, True, color), (x, y))


def wrap_text(text, font, max_width):
    """
    Quebra uma string longa em múltiplas linhas respeitando max_width pixels.

    Parâmetros:
        text      → string original a quebrar
        font      → fonte usada para medir o tamanho de cada palavra
        max_width → largura máxima em pixels que uma linha pode ocupar

    Retorna:
        Lista de strings, cada uma respeitando o limite de largura.

    Efeito no jogo:
        Permite exibir textos longos dentro do DialogBox sem que
        ultrapassem as bordas do painel de diálogo.
        (Função preparada para uso; o DialogBox atual usa \n manual.)
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


