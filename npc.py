
"""
npc.py — Dados dos NPCs (pistas/falas) e a classe NPC.
"""

import math
import pygame
from config import TILE
from colors import C_NPC1, C_NPC2, C_NPC3, C_NPC4, C_BLACK, C_ACCENT
from utils import draw_rect_border
from config import font_sm
from pathlib import Path


# ─────────────────────────────────────────────────────
# DADOS DOS NPCs E PISTAS
# ─────────────────────────────────────────────────────

NPC_DATA = [
    {
        "id": 3, "name": "Rolim",
        "color": C_NPC3,
        "minigame": "peruca",
        "intro": [
            "Max: Alessandro? Você é careca?",
            "Rolim: Oi Max KKKKKKK! Pois é... O que deseja?",
            "Max: Preciso saber por onde anda Romerito, você sabe me dizer algo?",
            "Rolim: Sei sim. Acontece que estou com um problemão...",
            "Rolim: Perdi minha peruca em algum lugar desta sala.",
            "Rolim: Sem ela, não posso sair daqui!",
            "Rolim: Mas podemos fazer um acordo...",
            "Rolim: Se encontrar minha peruca, posso te dizer onde",
            "o professor Romerito pode estar.",
            "Max: Pode ser!",
            "Rolim: Procure bem! Ela está escondida por aqui.",
            "Rolim: Clique no lugar certo para encontrar a peruca!"
        ],
        "pista_sucesso": "Rolim: AEEE, você conseguiu!\nRolim: Acho que vi Romerito ali na quadra!",
        "pista_falha": "Rolim: KKKKK, não foi dessa vez! Tente novamente.",
        "pista_texto": "[PISTA 1] Romerito pode estar na quadra.",
    },

    {
        "id": 2, "name": "Rickson",
        "color": C_NPC2,
        "minigame": "gol",
        "intro": [
            "Rickson: Fala, Max! Tô treinando pro campeonato.",
            "Rickson: Posso te dar uma dica sobre RoRo...",
            "Rickson: ...se você conseguir fazer um gol no",
            "Rickson: momento EXATO que eu indicar!",
            "Rickson: Pressione ESPAÇO na hora certa!",
        ],
        "pista_sucesso": "Rickson: BOA! Você conseguiu!\nRickson: Acho que vi Romerito ali na piscina!",
        "pista_falha": "Rickson: Errou o timing, hein! Não foi dessa vez.",
        "pista_texto": "[PISTA 2] Romerito pode estar na piscina.",
    },

    {
        "id": 1, "name": "Anderson",
        "color": C_NPC1,
        "minigame": "piscina",
        "intro": [
            "Anderson: Eai, Max! Procurando o que por aqui?",
            "Max: Tava atrás de Romerito, me disseram que você sabia onde ele estava.",
            "Anderson: Sei sim...",
            "Anderson: ...mas antes preciso de um favor!",
            "Max: Diz aí!",
            "Anderson: Tenho que coletar alguns objetos na piscina,mas estou com preguiça!",
            "Anderson: Se você fizer tudo, eu posso dizer onde ele deve estar!",
            "Max: KKKKKKKKKK Ta bom,ze buchinho!",
        ],
        "pista_sucesso": "Anderson: Aí sim! Você conseguiu!\nAnderson: Acho que vi Romerito mexendo em uns fios ali!",
        "pista_falha": "Anderson: Eita, não conseguiu! Fica pra próxima.",
        "pista_texto": "[PISTA 3] Romerito pode estar mexendo em uns fios.",
    },

    {
        "id": 4, "name": "Hugo",
        "color": C_NPC4,
        "minigame": "fios",
        "intro": [
            "Hugo: Max! Menos mal que apareceu.",
            "Hugo: Tô com uns fios todos embaralhados aqui.",
            "Hugo: Se você conectar os fios certos,",
            "Hugo: eu te digo onde o prof. Romerito está!",
            "Hugo: Conecte cada fio à cor correta!",
        ],
        "pista_sucesso": "Hugo: Perfeito! Você conseguiu!\nHugo: Acho que vi Romerito na pista de corrida, se não me engano!",
        "pista_falha": "Hugo: Eita! Esses fios deram um nó na minha cabeça. Tente novamente.",
        "pista_texto": "[PISTA 4] Romerito pode estar na pista de corrida.",
    },
]


# Sprites dos professores
NPC_SPRITES = {
    1: ("anderson_parado.png", 1),
    4: ("hugo_parado.png", 1),
    2: ("rickson_parado.png", 1),
    3: ("rolim.png", 7),
}


# Numeração visual das salas
NPC_NUMBERS = {
    3: 1,  # Rolim
    2: 2,  # Rickson
    1: 3,  # Anderson
    4: 4,  # Hugo
}


# ─────────────────────────────────────────────────────
# CLASSE NPC – PERSONAGEM NÃO JOGÁVEL
# ─────────────────────────────────────────────────────

class NPC:

    SIZE = 24

    def __init__(self, data, tx, ty):

        self.data = data
        self.x = tx * TILE + TILE // 2
        self.y = ty * TILE + TILE // 2
        self.done = False
        self.success = False

        # Carrega a sprite do professor

        arquivo, colunas = NPC_SPRITES[self.data["id"]]
        caminho = Path(__file__).parent / "imagens" / arquivo

        sheet = pygame.image.load(str(caminho)).convert_alpha()

        if self.data["id"] == 3:
            largura = sheet.get_width() // colunas
            altura = sheet.get_height() // 4

            self.sprite = sheet.subsurface(
                (120, 0, 70, 100)
            ).copy()

            bounds = self.sprite.get_bounding_rect()
            self.sprite = self.sprite.subsurface(bounds).copy()

            altura = 64
            largura = round(
                self.sprite.get_width() * altura / self.sprite.get_height()
            )

            self.sprite = pygame.transform.scale(
                self.sprite, (largura, altura)
            )
        else:
            self.sprite = pygame.transform.scale(sheet, (48, 64))

    def rect(self):
        h = self.SIZE
        return pygame.Rect(
            self.x - h // 2,
            self.y - h // 2,
            h,
            h
        )

    def near(self, player):
        return math.hypot(
            self.x - player.x,
            self.y - player.y
        ) < TILE * 1.8

    def draw(self, surf, cam_x, cam_y):

        r = self.rect().move(-cam_x, -cam_y)
        col = self.data["color"]

        if self.done:
            col = tuple(c // 2 for c in col)

        # Desenha a sprite
        sprite_rect = self.sprite.get_rect(
            midbottom=(r.centerx, r.bottom + 12)
        )
        surf.blit(self.sprite, sprite_rect)

        # Nome do NPC
        lb = font_sm.render(self.data["name"], True, col)
        surf.blit(
            lb,
            (
                sprite_rect.centerx - lb.get_width() // 2,
                sprite_rect.top - 18
            )
        )

        # Indicador [E]
        if not self.done:
            hint = font_sm.render("[E]", True, C_ACCENT)
            surf.blit(
                hint,
                (
                    sprite_rect.centerx - hint.get_width() // 2,
                    sprite_rect.top - 34
                )
            )
