
import sys
import pygame

from config import SW, SH
from screens import screen_title, screen_pause
from game import Game


def main():
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
