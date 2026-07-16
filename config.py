
import pygame

pygame.init()

SW, SH = 960, 640          # SW = Screen Width (largura), SH = Screen Height (altura)

TILE = 32

FPS = 60


RAW_MAP = [
       "##############################",   # linha 0  – parede superior
       "#............................#",   # linha 1
       "#............................#",   # linha 2
       "#...##...............##......#",   # linha 3  – paredes internas (sala NPC 1 e 4)
       "#.. 1................4 ......#",   # linha 4  – NPCs Anderson(1) e Diego(4)
       "#...##...............##......#",   # linha 5
       "#............................#",   # linha 6
       "#............................#",   # linha 7
       "#...##...............##......#",   # linha 8  – salas NPCs 2/3 + piscina
       "#.. 2.......   .......3 .....#",   # linha 9  – NPCs Carlos(2) e Bianca(3)
       "#...##......   ......##......#",   # linha 10
       "#.......GGGG   GGGG..........#",   # linha 11
       "#..........G   G.............#",   # linha 12
       "#..........G   G.............#",   # linha 13 – quadra/grama
       "#..........G   G.............#",   # linha 14
       "#..........G   G.............#",   # linha 15
       "#..........G...G.............#",   # linha 16
       "#............................#",   # linha 17 – spawn do jogador (P)
       "#......P.....................#",   # linha 18
       "##############################",   # linha 19 – parede inferior
]

MAP_COLS = len(RAW_MAP[0])   # número de colunas (largura em tiles) = 30
MAP_ROWS = len(RAW_MAP)      # número de linhas  (altura  em tiles) = 20


font_lg = pygame.font.SysFont("monospace", 28, bold=True)  # títulos e mensagens importantes
font_md = pygame.font.SysFont("monospace", 18)             # texto de diálogo e HUD
font_sm = pygame.font.SysFont("monospace", 14)             # rótulos pequenos e dicas
