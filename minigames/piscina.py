
"""
minigames/piscina.py — Minigame: corrida aquática contra Anderson.
"""

import random
import math
import pygame

from config import SW, SH, font_lg
from colors import C_WHITE, C_BLACK, C_PLAYER, C_NPC1, C_BLUE, C_GREEN, C_RED
from utils import draw_rect_border, draw_text_center
from minigames.base import Minigame


class PiscinaGame(Minigame):

    LANES = 5
    LANE_W = 80

    def __init__(self, screen):
        super().__init__(screen)

                # Carrega a imagem do nadador
        sheet = pygame.image.load("maxstill-POO--main/assets/aluno.jpg").convert()
        sheet.set_colorkey((0, 0, 0))

        self.swim_frames = []

        frame_w = sheet.get_width() // 4
        frame_h = sheet.get_height() // 3

        for row in range(3):
            for col in range(4):
                frame = sheet.subsurface((
                    col * frame_w,
                    row * frame_h,
                    frame_w,
                    frame_h
                ))

                frame = pygame.transform.scale(frame, (72, 72))
                self.swim_frames.append(frame)

        self.anim_frame = 0

        self.player_lane = 2
        self.player_y = SH - 80

        self.enemies = []
        self.items = []

        self.spawn_timer = 0
        self.item_timer = 0

        self.distance = 0
        self.goal = 1800

        self.lives = 3
        self.cooldown = 0

        # Sistema de coleta
        self.collected = 0
        self.items_goal = 6

        # Progressão
        self.difficulty = 0

    def _lane_x(self, lane):
        return (
            (SW - self.LANES * self.LANE_W) // 2
            + lane * self.LANE_W
            + self.LANE_W // 2
        )

    def handle_event(self, event):

        if self.done:
            return

        if event.type == pygame.KEYDOWN:

            if event.key in (pygame.K_a, pygame.K_LEFT):
                self.player_lane = max(0, self.player_lane - 1)

            if event.key in (pygame.K_d, pygame.K_RIGHT):
                self.player_lane = min(
                    self.LANES - 1,
                    self.player_lane + 1
                )

    def update(self):

        if self.done:
            self.timer += 1
            return

        # Avanço da corrida
        self.distance += 2

        # Aumenta a dificuldade progressivamente
        self.difficulty = min(self.distance / 400, 1)

        # Velocidade dos obstáculos aumenta
        velocidade_base = 3.5 + self.difficulty * 4.5

        # Obstáculos aparecem cada vez mais rápido
        intervalo = max(18, 42 - int(self.distance / 70))

        self.spawn_timer += 1

        if self.spawn_timer >= intervalo:

            self.spawn_timer = 0

            lane = random.randint(0, self.LANES - 1)

            velocidade = velocidade_base + random.uniform(0, 1.5)

            self.enemies.append([
                lane,
                -40,
                velocidade
            ])

        # Cria itens para coletar
        self.item_timer += 1

        if self.item_timer >= 32:

            self.item_timer = 0

            lane = random.randint(0, self.LANES - 1)

            self.items.append([
                lane,
                -30
            ])

        # Move obstáculos
        for enemy in self.enemies:
            enemy[1] += enemy[2]

        self.enemies = [
            e for e in self.enemies
            if e[1] < SH + 50
        ]

        # Move itens
        for item in self.items:
            item[1] += 3.5 + self.difficulty * 2

        self.items = [
            item for item in self.items
            if item[1] < SH + 30
        ]

        # Posição do jogador
        px = self._lane_x(self.player_lane)
        py = self.player_y

        player_rect = pygame.Rect(
            px - 20,
            py - 28,
            40,
            56
        )

        # Verifica coleta dos itens
        for item in self.items[:]:

            ix = self._lane_x(item[0])
            iy = int(item[1])

            item_rect = pygame.Rect(
                ix - 15,
                iy - 15,
                30,
                30
            )

            if player_rect.colliderect(item_rect):

                self.collected += 1
                self.items.remove(item)

        # Verifica colisões com obstáculos
        if self.cooldown > 0:

            self.cooldown -= 1

        else:

            for enemy in self.enemies[:]:

                ex = self._lane_x(enemy[0])
                ey = int(enemy[1])

                enemy_rect = pygame.Rect(
                    ex - 20,
                    ey - 28,
                    40,
                    56
                )

                if player_rect.colliderect(enemy_rect):

                    self.lives -= 1
                    self.cooldown = 60

                    self.enemies.remove(enemy)

                    if self.lives <= 0:

                        self.done = True
                        self.success = False
                        self.msg = "Você perdeu! Tente novamente!"

                    break

        # Vitória: chegar ao final e coletar os itens necessários
        if (
            self.distance >= self.goal
            and self.collected >= self.items_goal
        ):

            self.done = True
            self.success = True
            self.msg = "Parabéns! Você venceu a corrida!"

    def draw(self):

        self.screen.fill((20, 40, 80))

        ox = (SW - self.LANES * self.LANE_W) // 2

        t = pygame.time.get_ticks() / 1000

        # Fundo da piscina
        for i in range(self.LANES):

            x = ox + i * self.LANE_W

            col = (
                30,
                100,
                int(160 + 40 * math.sin(t + i))
            )

            pygame.draw.rect(
                self.screen,
                col,
                (x, 0, self.LANE_W, SH)
            )

            pygame.draw.line(
                self.screen,
                (50, 150, 220),
                (x, 0),
                (x, SH),
                2
            )

        # Marcas das raias em movimento
        offset = int(self.distance * 2) % 48

        for lane in range(self.LANES):

            x = ox + lane * self.LANE_W + self.LANE_W // 2

            for y in range(-48, SH + 48, 48):

                pygame.draw.line(
                    self.screen,
                    (75, 160, 210),
                    (x, y + offset),
                    (x, y + offset + 22),
                    3
                )

        # Linha de chegada
        for i in range(0, self.LANES * self.LANE_W, 20):

            col = C_WHITE if (i // 20) % 2 == 0 else C_BLACK

            pygame.draw.rect(
                self.screen,
                col,
                (ox + i, 10, 20, 14)
            )

        # Desenha os itens coletáveis
        for item in self.items:

            ix = self._lane_x(item[0])
            iy = int(item[1])

            pygame.draw.circle(
                self.screen,
                (255, 210, 30),
                (ix, iy),
                12
            )

            pygame.draw.circle(
                self.screen,
                (255, 245, 150),
                (ix - 3, iy - 3),
                4
            )

        # Desenha os obstáculos
        for enemy in self.enemies:

            ex = self._lane_x(enemy[0])

            er = pygame.Rect(
                ex - 22,
                int(enemy[1]) - 30,
                44,
                60
            )

            draw_rect_border(
                self.screen,
                C_NPC1,
                er,
                radius=4
            )

            pygame.draw.rect(
                self.screen,
                C_BLACK,
                (er.x + 8, er.y + 12, 6, 6)
            )

            pygame.draw.rect(
                self.screen,
                C_BLACK,
                (er.x + 22, er.y + 12, 6, 6)
            )

        # Desenha o jogador
                # Desenha o jogador nadando
        px = self._lane_x(self.player_lane)

        self.anim_frame += 1

        frame = self.swim_frames[
            (self.anim_frame // 6) % len(self.swim_frames)
        ]

        if self.cooldown > 0 and self.cooldown % 8 >= 4:
            frame = frame.copy()
            frame.set_alpha(100)

        player_rect = frame.get_rect(
            center=(px, self.player_y)
        )

        self.screen.blit(frame, player_rect)

        # HUD
        self.draw_hud(
            "CORRIDA NA PISCINA",
            "A/D para mudar de raia - Desvie e colete os itens!"
        )

        self.draw_bar(
            "Progresso:",
            min(self.distance, self.goal),
            self.goal,
            20, 80, 300, 16,
            C_BLUE
        )

        self.draw_bar(
            "Vidas:",
            self.lives,
            3,
            20, 118, 100, 16,
            C_RED
        )

        # Contador de itens
        texto_itens = font_lg.render(
            f"Itens: {self.collected}/{self.items_goal}",
            True,
            (255, 220, 50)
        )

        self.screen.blit(
            texto_itens,
            (SW - texto_itens.get_width() - 25, 80)
        )

        # Resultado
        if self.msg:

            s = pygame.Surface(
                (SW, 60),
                pygame.SRCALPHA
            )

            s.fill((0, 0, 0, 160))

            self.screen.blit(
                s,
                (0, SH // 2 + 70)
            )

            draw_text_center(
                self.screen,
                self.msg,
                font_lg,
                C_GREEN if self.success else C_RED,
                SW // 2,
                SH // 2 + 100
            )


