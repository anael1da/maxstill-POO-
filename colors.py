"""
colors.py — Paleta de cores usada em todo o jogo.
"""

#ambiente
C_BLACK  = (10,  10,  20)   # fundo quase preto 
C_WHITE  = (240, 240, 240)  # branco suave
C_GRAY   = (100, 100, 110)  # cinza médio (textos secundários)
C_DGRAY  = (50,  50,  60)   # cinza escuro (painéis, barras)
C_WALL   = (70,  60,  80)   # cor das paredes do mapa
C_FLOOR  = (45,  42,  55)   # cor do chão 
C_FLOOR2 = (50,  47,  60)   # cor do chão alternado (cria efeito de grade)
C_DOOR   = (180, 140,  60)  # cor de portas normais 
C_LOCKED = (140,  50,  50)  # cor de portas trancadas 

#personagens 
C_PLAYER = (80,  200, 120)  # verde: o protagonista MAX
C_NPC1   = (220, 100, 100)  # vermelho: Anderson (piscina)
C_NPC2   = (100, 180, 220)  # azul: Rickson (gol)
C_NPC3   = (220, 180,  80)  # amarelo-ouro: Rolim (peruca)
C_NPC4   = (180, 100, 220)  # roxo: Hugo (fios)
C_NPCE   = (255, 215,   0)  # dourado: professor Romerito (final)

#cenário
C_WATER  = (40,  120, 200)  # azul da piscina
C_GRASS  = (60,  130,  60)  # verde da quadra/grama

#destaques
C_ACCENT = (255, 180,  50)  # laranja-dourado: bordas de UI, HUD
C_RED    = (220,  60,  60)  # vermelho: erros, vidas, alertas
C_GREEN  = (60,  200,  80)  # verde: sucesso, progresso
C_BLUE   = (60,  120, 220)  # azul: barra de progresso na piscina
C_YELLOW = (240, 220,  60)  # amarelo: pontuação, dicas
C_PURPLE = (160,  60, 220)  # roxo: reservado para uso futuro
