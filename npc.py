"""
npc.py — Dados dos NPCs (pistas/falas) e a classe NPC.
"""

import math
import pygame
from config import TILE
from colors import C_NPC1, C_NPC2, C_NPC3, C_NPC4, C_BLACK, C_ACCENT
from utils import draw_rect_border
from config import font_sm


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
        """
        Desenha o NPC na tela com ajuste de câmera.

        Visual:
            - Quadrado colorido (cor do data["color"]) se disponível
            - Se done=True, cor escurecida pela metade (tom sombrio)
            - Dois "olhos" e uma "boca" (similar ao player)
            - Nome do NPC 18px acima do quadrado
            - "[E]" 34px acima (só quando não concluído e player próximo —
              o controle de proximidade é feito em Game.draw())

        Nota: o label "[E]" é sempre desenhado se not done;
              a lógica de proximidade para mostrar/ocultar pode
              ser refinada ligando near() aqui.
        """
        r   = self.rect().move(-cam_x, -cam_y)
        col = self.data["color"]

        # Escurece o NPC quando já interagido
        if self.done:
            col = tuple(c // 2 for c in col)

        draw_rect_border(surf, col, r, radius=3)

        # Olhos
        ex = r.x + 5
        ey = r.y + 7
        pygame.draw.rect(surf, C_BLACK, (ex,      ey, 4, 4))
        pygame.draw.rect(surf, C_BLACK, (ex + 11, ey, 4, 4))

        # Boca: reta se concluído (neutro), espessa se disponível
        if self.done:
            pygame.draw.rect(surf, C_BLACK, (ex + 2, ey + 10, 8, 2))  # boca reta
        else:
            pygame.draw.rect(surf, C_BLACK, (ex + 2, ey + 9,  8, 3))  # boca normal

        # Nome do NPC acima do sprite
        lb = font_sm.render(self.data["name"], True, col)
        surf.blit(lb, (r.centerx - lb.get_width() // 2, r.y - 18))

        # Indicador de interação "[E]"
        if not self.done:
            hint = font_sm.render("[E]", True, C_ACCENT)
            surf.blit(hint, (r.centerx - hint.get_width() // 2, r.y - 34))

