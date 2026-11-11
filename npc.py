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
#  DADOS DOS NPCs E PISTAS
# ─────────────────────────────────────────────────────
NPC_DATA = [
    {
        "id": 1, "name": "Anderson",
        "color": C_NPC1,                  
        "minigame": "piscina",                
        "intro": [
            "Anderson: Eai, Max! Procurando o prof. Romerito?",
            "Anderson: Eu sei onde ele estava antes de sumir...",
            "Anderson: ...mas só conto se você me vencer numa corrida na piscina!",
            "Anderson: Desvie de mim e chegue ao outro lado!",
            "Anderson: Quero ver voce ganhar!",
        ],
        # após vitória: indica a peruca e o laboratório
        "pista_sucesso": "Anderson: Como venceu,vou dar a dica, Da última vez que o vi foi com Rolim!",
        "pista_falha":   "Anderson: Hahaha, não foi dessa vez. Vai ter que se virar garotinho.",
        # Texto compacto salvo no caderno de pistas do jogador
        "pista_texto":   "[PISTA 1] Romerito foi visto indo a direção academica.",
    },
    {
        "id": 3, "name": "Rolim",
        "color": C_NPC3,                       # quadradinho amarelo
        "minigame": "peruca",                  # aciona PerucaGame
        "intro": [
            "Rolim: Aaai, Max! Que susto!",
            "Rolim: Perdi minha peruca em algum lugar aqui.",
            "Rolim: Se você achar pra mim, te conto um",
            "Rolim: segredo sobre o prof. Romerito!",
            "Rolim: Ache a peruca (P) clicando no lugar certo!",
        ],
        "pista_sucesso": "Rolim: Obrigada! O prof. Romerito me pediu",
        "pista_falha":   "Rolim: Hmm, não era ali... mas acho que ele",
        "pista_texto":   "[PISTA 3] Romerito pediu emprestado um\n   livro de eletricidade para Bianca.",
    },
    {
        "id": 2, "name": "Rickson",
        "color": C_NPC2,                       # quadradinho azul
        "minigame": "gol",                     # aciona GolGame
        "intro": [
            "Rickson: Fala, Max! Tô treinando pro campeonato.",
            "Rickson: Posso te dar uma dica sobre RoRo...",
            "Rickson: ...se você conseguir fazer um gol no",
            "Rickson: momento EXATO que eu indicar!",
            "Rickson: Pressione ESPAÇO na hora certa!",
        ],
        "pista_sucesso": "Rickson: Gol! Tá bom... Ouvi o prof. Romerito\n   falando sobre uns FIOS elétricos quebrados\n   no laboratório.",
        "pista_falha":   "Rickson: Errou o timing... mas ele mencionou\n   o laboratório uma vez.",
        "pista_texto":   "[PISTA 2] Rickon ouviu Romerito falar de fios\n   elétricos no laboratório.",
    },
    {
        "id": 4, "name": "Hugo",
        "color": C_NPC4,                       # quadradinho roxo
        "minigame": "fios",                    # aciona FiosGame
        "intro": [
            "Diego: Max! Menos mal que apareceu.",
            "Diego: Tô com uns fios todos embaralhados aqui.",
            "Diego: Se você conectar os fios certos,",
            "Diego: eu te digo onde o prof. Romerito está!",
            "Diego: Conecte cada fio à cor correta!",
        ],
        "pista_sucesso": "Diego: Perfeito! O prof. Romerito tá na SALA\n   DOS PROFESSORES, preparando uma SURPRESA\n   pro evento da escola!",
        "pista_falha":   "Diego: Quase... ele foi pra sala dos professores.",
        "pista_texto":   "[PISTA 4] Romerito está na sala dos professores\n   preparando uma surpresa.",
    },
]


 # Sprites dos professores
NPC_SPRITES = {
    1: ("anderson.png", 4),
    4: ("hugo.png", 4),
    2: ("rickson.png", 4),
    3: ("rolim.png", 5),
}

 # Numeração visual das salas
NPC_NUMBERS = {
    1: 1,  # Anderson
    4: 2,  # Hugo
    2: 3,  # Rickson
    3: 4,  # Rolim
}


# ─────────────────────────────────────────────────────
#  CLASSE NPC – PERSONAGEM NÃO JOGÁVEL
# ─────────────────────────────────────────────────────
class NPC:
    """
    Representa um personagem suspeito com quem o jogador interage.

    Cada NPC:
        - Fica parado em sua posição no mapa (definida pelo RAW_MAP)
        - Exibe seu nome e "[E]" quando o player se aproxima
        - Ao interagir, inicia diálogo → minigame → resultado
        - Após concluído (done=True), fica escurecido e sem o [E]

    Atributos:
        data    → dicionário de NPC_DATA com falas, cor, minigame, etc.
        x, y    → posição em pixels no mundo
        done    → True após o minigame ser concluído (vitória ou derrota)
        success → True se o jogador venceu o minigame deste NPC
    """

    SIZE = 24   # mesmo tamanho que o player para consistência visual

    def __init__(self, data, tx, ty):
        """
        Inicializa o NPC com seus dados e posição de tile.

        Parâmetros:
            data  → dicionário de NPC_DATA correspondente
            tx,ty → coordenadas de tile retiradas do RAW_MAP
        """
        self.data    = data
        self.x       = tx * TILE + TILE // 2
        self.y       = ty * TILE + TILE // 2
        self.done    = False    # False = ainda disponível para interação
        self.success = False    # resultado do minigame

                # Carrega a sprite do professor
        arquivo, colunas = NPC_SPRITES[self.data["id"]]
        caminho = Path(__file__).parent / "imagens" / arquivo

        sheet = pygame.image.load(str(caminho)).convert_alpha()

        largura = sheet.get_width() // colunas
        altura = sheet.get_height() // 4

        if sheet.get_width() == 1536:
            self.sprite = sheet.subsurface(
                (320, 0, 240, 256)
            ).copy()
        else:
            self.sprite = sheet.subsurface(
                (0, 0, largura, altura)
            ).copy()

        self.sprite = pygame.transform.scale(
            self.sprite, (48, 64)
        )
        
    def rect(self):
        """
        Retorna pygame.Rect de colisão/posição do NPC no espaço do mundo.
        Usado internamente e por near() para verificar proximidade.
        """
        h = self.SIZE
        return pygame.Rect(self.x - h // 2, self.y - h // 2, h, h)

    def near(self, player):
        """
        Verifica se o player está próximo o suficiente para interagir.

        Usa distância euclidiana (math.hypot) entre os centros.
        Limiar: 1.8 × TILE = 57.6 px (~1,8 tiles de distância).

        Retorna:
            True  → player pode pressionar E para conversar
            False → player está longe demais

        Impacto no jogo:
            Controla quando o "[E]" aparece sobre o NPC e quando
            a interação é registrada em Game.interact().
        """
        return math.hypot(self.x - player.x, self.y - player.y) < TILE * 1.8

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
        surf.blit(lb, (sprite_rect.centerx - lb.get_width() // 2,
                       sprite_rect.top - 18))

        # Indicador [E]
        if not self.done:
            hint = font_sm.render("[E]", True, C_ACCENT)
            surf.blit(hint, (sprite_rect.centerx - hint.get_width() // 2,
                             sprite_rect.top - 34))