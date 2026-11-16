"""
=======================================================
  EU SEI O QUE VOCÊS FIZERAM NA CORRIDA PASSADA
=======================================================
  CONTROLES:
    W A S D   - Movimentação
    E / Espaço - Interagir com NPCs
    ESC       - Pausar / Sair
=======================================================

  ESTRUTURA GERAL DO PROJETO (dividida em módulos):
    config.py    → constantes globais, mapa (RAW_MAP) e fontes
    colors.py    → paleta de cores
    utils.py     → funções utilitárias de desenho/texto e HUD
    dialog.py    → DialogBox (caixa de diálogo)
    player.py    → Player (personagem controlável)
    npc.py       → NPC_DATA (falas/pistas) e classe NPC
    map.py       → GameMap (mapa e colisão com paredes)
    minigames/   → base.py + piscina.py + gol.py + peruca.py + fios.py
    screens.py   → telas de título, pausa, pistas e fim de jogo
    game.py      → Game (gerenciador de estado principal)
    main.py      → main() – loop principal do jogo (este arquivo)
=======================================================

Ponto de entrada do programa. Inicializa a janela e executa o loop externo.

Estrutura de loops:
    Loop externo (while True):
        Exibe tela de título → cria Game → entra no loop interno

    Loop interno (while running):
        clock.tick(FPS) → limita a 60 FPS
        Coleta eventos → filtra ESC (pausa) e QUIT (sair)
        game.update(events) → lógica do frame
        game.draw()         → renderização do frame

Tratamento de ESC:
    Durante o jogo, ESC aciona screen_pause(). Se a pausa retornar
    algo diferente de "resume" (atualmente não acontece), sai do loop.

Ao sair do loop interno, volta ao externo → tela de título → novo jogo.
Game.reset() é chamado pela própria tela final, então um novo objeto
Game é criado a cada partida para garantir estado limpo.
"""

import sys
import pygame

from config import SW, SH
from screens import screen_title, screen_pause
from game import Game


def main():
    """
    Ponto de entrada do programa. Inicializa a janela e executa o loop externo.

    Estrutura de loops:
        Loop externo (while True):
            Exibe tela de título → cria Game → entra no loop interno

        Loop interno (while running):
            clock.tick(FPS) → limita a 60 FPS
            Coleta eventos → filtra ESC (pausa) e QUIT (sair)
            game.update(events) → lógica do frame
            game.draw()         → renderização do frame

    Tratamento de ESC:
        Durante o jogo, ESC aciona screen_pause(). Se a pausa retornar
        algo diferente de "resume" (atualmente não acontece), sai do loop.

    Ao sair do loop interno, volta ao externo → tela de título → novo jogo.
    Game.reset() é chamado pela própria tela final, então um novo objeto
    Game é criado a cada partida para garantir estado limpo.
    """
    screen = pygame.display.set_mode((SW, SH))
    pygame.display.set_caption("Eu Sei o Que Vocês Fizeram na Corrida Passada")
    clock = pygame.time.Clock()

    while True:
        # Exibe título e aguarda ENTER
        screen_title(screen, clock)

        # Cria uma nova sessão de jogo
        game = Game(screen, clock)

        running = True
        while running:
            clock.tick(60)   # mantém 60 FPS; bloqueia se necessário

            events = []
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    # Pausa o jogo; se o resultado não for "resume", sai
                    result = screen_pause(screen, clock)
                    if result != "resume":
                        running = False
                else:
                    events.append(ev)   # repassa todos os outros eventos ao jogo

            if not running:
                break

            game.update(events)
            game.draw()


# ─────────────────────────────────────────────────────
#  PONTO DE ENTRADA
# ─────────────────────────────────────────────────────
if __name__ == "__main__":
    # Garante que main() só é chamado quando o script é executado diretamente,
    # não quando importado como módulo por outro arquivo.
    main()
