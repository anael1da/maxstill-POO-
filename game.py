
"""
game.py — Classe Game: gerenciador de estado principal.
"""

import pygame
from config import SW, SH
from colors import C_BLACK, C_GRAY, C_PLAYER
from utils import draw_hud
from dialog import DialogBox
from player import Player
from npc import NPC, NPC_DATA
from map import GameMap
from screens import screen_pistas, screen_final
from minigames import PiscinaGame, GolGame, PerucaGame, FiosGame
from corrida import Corrida


class Game:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.reset()

    def reset(self):
        self.gmap = GameMap()

        tx, ty = self.gmap.player_start()
        self.player = Player(tx, ty)

        self.npcs = [
            NPC(d, *self.gmap.npc_pos(d["id"]))
            for d in NPC_DATA
        ]

        self.dialog = DialogBox()
        self.minigame = None
        self.active_npc = None

        self.cam_x = max(
            0,
            min(self.player.x - SW // 2, self.gmap.width - SW)
        )

        self.cam_y = max(
            0,
            min(self.player.y - SH // 2, self.gmap.height - SH)
        )

        self.phase = "explore"
        self.scene = "escola"
        self.corrida = None

        self.found_professor = False
        self.race_unlocked = False

    # ── CÂMERA ─────────────────────────────

    def update_camera(self):

        target_x = self.player.x - SW // 2
        target_y = self.player.y - SH // 2

        max_x = max(0, self.gmap.width - SW)
        max_y = max(0, self.gmap.height - SH)

        self.cam_x += (target_x - self.cam_x) * 0.15
        self.cam_y += (target_y - self.cam_y) * 0.15

        self.cam_x = max(0, min(self.cam_x, max_x))
        self.cam_y = max(0, min(self.cam_y, max_y))

    # ── LIBERAR CORRIDA ─────────────────────

    def check_final(self):

        if self.race_unlocked:
            return

        if all(npc.done for npc in self.npcs):

            self.race_unlocked = True

            self.dialog.start([
                "Voce conseguiu completar os quatro desafios!",
                "Agora procure a portinha da escola.",
                "Entre por ela para comecar a corrida!"
            ])

            self.phase = "dialog"

    # ── INICIAR MINIGAME ─────────────────────

    def start_minigame(self, npc):

        mg = npc.data["minigame"]

        if mg == "piscina":
            self.minigame = PiscinaGame(self.screen)

        elif mg == "gol":
            self.minigame = GolGame(self.screen)

        elif mg == "peruca":
            self.minigame = PerucaGame(self.screen)

        elif mg == "fios":
            self.minigame = FiosGame(self.screen)

        self.active_npc = npc
        self.phase = "minigame"

        print("MINIGAME INICIADO:", mg)

    # ── FINALIZAR MINIGAME ───────────────────

    def finish_minigame(self):

        npc = self.active_npc

        npc.done = True
        npc.success = self.minigame.success

        if self.minigame.success:

            pista = npc.data["pista_texto"]
            self.player.pistas.append(pista)
            self.player.score += 100

            result_lines = npc.data["pista_sucesso"].split("\n")

        else:

            result_lines = npc.data["pista_falha"].split("\n")

        self.dialog.start(
            result_lines,
            callback=self.check_final
        )

        self.phase = "dialog"
        self.minigame = None

    # ── DIÁLOGO APÓS A CORRIDA ───────────────

    def finish_race_dialog(self):

        self.phase = "final"

    # ── INTERAÇÃO COM NPCs ───────────────────

    def interact(self):

        for npc in self.npcs:

            if npc.near(self.player) and not npc.done:

                intro = npc.data["intro"]

                self.dialog.start(
                    intro,
                    callback=lambda n=npc: self.start_minigame(n)
                )

                self.phase = "dialog"
                return

    # ── UPDATE ──────────────────────────────

    def update(self, events):

        keys = pygame.key.get_pressed()

        # EXPLORAÇÃO
        if self.phase == "explore":

            # FASE DA CORRIDA
            if self.scene == "corrida":

                self.corrida.update(self.player, keys)

                if self.corrida.done:

                    if self.corrida.winner == "max":
                        resultado = [
                            "MAX VENCEU A CORRIDA!",
                            "Voce conseguiu chegar primeiro!"
                        ]
                    else:
                        resultado = [
                            "ROMERITO VENCEU A CORRIDA!",
                            "Dessa vez ele chegou primeiro."
                        ]

                    self.dialog.start(
                        resultado,
                        callback=self.finish_race_dialog
                    )

                    self.phase = "dialog"
                    self.scene = "escola"
                    self.corrida = None

                    tx, ty = self.gmap.player_start()
                    self.player.x = tx * 32 + 16
                    self.player.y = ty * 32 + 16
                    self.player.stop()

            # FASE DA ESCOLA
            else:

                dx = keys[pygame.K_d] - keys[pygame.K_a]
                dy = keys[pygame.K_s] - keys[pygame.K_w]

                if dx or dy:
                    self.player.move(dx, dy, self.gmap.walls)
                else:
                    self.player.stop()

                # PORTINHA DA CORRIDA
                if (
                    self.race_unlocked
                    and self.gmap.door_trigger.colliderect(
                        self.player.rect()
                    )
                ):

                    self.scene = "corrida"
                    self.corrida = Corrida()

                    self.player.x = 80
                    self.player.y = self.corrida.player_y

                    self.player.stop()

                    print("FASE DA CORRIDA INICIADA!")

            # TECLAS DA ESCOLA
            if self.scene == "escola":

                for ev in events:

                    if ev.type == pygame.KEYDOWN:

                        if ev.key in (pygame.K_e, pygame.K_SPACE):
                            self.interact()

                        elif ev.key == pygame.K_TAB:
                            screen_pistas(
                                self.screen,
                                self.clock,
                                self.player
                            )

        # DIÁLOGO
        elif self.phase == "dialog":

            for ev in events:

                if ev.type == pygame.KEYDOWN and ev.key in (
                    pygame.K_e,
                    pygame.K_SPACE
                ):

                    self.dialog.advance()

                    print("DIÁLOGO AVANÇOU")
                    print("DIÁLOGO ATIVO:", self.dialog.active)
                    print("FASE:", self.phase)

                    if (
                        not self.dialog.active
                        and self.phase == "dialog"
                    ):
                        self.phase = "explore"

        # MINIGAME
        elif self.phase == "minigame":

            for ev in events:
                self.minigame.handle_event(ev)

            self.minigame.update()

            if self.minigame.done:

                self.screen.fill(C_BLACK)
                self.minigame.draw()

                pygame.display.flip()
                pygame.time.wait(1800)

                self.finish_minigame()

        # TELA FINAL
        elif self.phase == "final":

            screen_final(
                self.screen,
                self.clock,
                self.player
            )

            self.reset()

        if self.scene == "escola":
            self.update_camera()

    # ── DRAW ─────────────────────────────────

    def draw(self):

        # CORRIDA
        if self.scene == "corrida" and self.corrida is not None:

            self.corrida.draw(self.screen)
            self.player.draw(self.screen, 0, 0)

            pygame.display.flip()
            return

        # MINIGAMES
        if self.phase == "minigame":

            self.minigame.draw()
            pygame.display.flip()
            return

        # ESCOLA
        self.gmap.draw(
            self.screen,
            int(self.cam_x),
            int(self.cam_y)
        )

        for npc in self.npcs:

            npc.draw(
                self.screen,
                int(self.cam_x),
                int(self.cam_y)
            )

        self.player.draw(
            self.screen,
            int(self.cam_x),
            int(self.cam_y)
        )

        self.dialog.draw(self.screen)

        phase_labels = {
            "explore": "Explore a escola e fale com os suspeitos (E) | TAB = pistas",
            "dialog": "CONVERSA | ESPAÇO para avançar",
        }

        draw_hud(
            self.screen,
            self.player,
            phase_labels.get(self.phase, "")
        )

        self._draw_minimap()

        pygame.display.flip()

    # ── MINIMAPA ─────────────────────────────

    def _draw_minimap(self):

        if self.gmap.width <= SW and self.gmap.height <= SH:
            return

        mw, mh = self.gmap.minimap.get_size()

        mx0 = SW - mw - 8
        my0 = 50

        self.screen.blit(
            self.gmap.minimap,
            (mx0, my0)
        )

        pygame.draw.rect(
            self.screen,
            C_GRAY,
            (mx0, my0, mw, mh),
            1
        )

        sx = mw / self.gmap.width
        sy = mh / self.gmap.height

        for npc in self.npcs:

            nx = int(mx0 + npc.x * sx)
            ny = int(my0 + npc.y * sy)

            pygame.draw.rect(
                self.screen,
                npc.data["color"],
                (nx - 2, ny - 2, 5, 5)
            )

        px = int(mx0 + self.player.x * sx)
        py = int(my0 + self.player.y * sy)

        pygame.draw.rect(
            self.screen,
            C_PLAYER,
            (px - 3, py - 3, 6, 6)
        )
