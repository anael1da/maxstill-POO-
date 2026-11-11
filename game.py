"""
game.py — Classe Game: gerenciador de estado principal.

Controla as fases do jogo (explore, dialog, minigame, final),
a câmera, o mapa, os NPCs, o player e a integração com os
4 minigames e as telas auxiliares (pistas, final).
"""

import pygame
from config import SW, SH
from colors import C_BLACK, C_GRAY, C_WALL, C_BLUE, C_GRASS, C_PLAYER
from utils import draw_hud
from dialog import DialogBox
from player import Player
from npc import NPC, NPC_DATA
from map import GameMap
from screens import screen_pistas, screen_final
from minigames import PiscinaGame, GolGame, PerucaGame, FiosGame


class Game:
    """
    Núcleo do jogo: gerencia todos os objetos e coordena as transições de estado.

    Estados (self.phase):
        "explore"  → jogador se move, interage com NPCs, acessa pistas (TAB)
        "dialog"   → DialogBox ativo; movimento bloqueado
        "minigame" → minigame ativo; tudo mais pausado
        "final"    → tela de desfecho após coletar 4 pistas

    Fluxo principal de jogo:
        explore → (E perto de NPC) → dialog (intro)
               → (diálogo termina, callback) → minigame
               → (minigame done) → dialog (resultado)
               → (diálogo termina) → explore
               → (4 pistas coletadas) → final
               → (ENTER) → reset() → explore (novo jogo)

    Câmera:
        Segue o player com suavização (lerp 15%) e é limitada
        às bordas do mapa para não exibir área fora do RAW_MAP.

    Minimap:
        Desenhado no canto superior direito da tela, mostrando
        paredes, água, grama, NPCs e player em escala reduzida.
    """

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock  = clock
        self.reset()

    def reset(self):
        """
        Reinicia todos os objetos do jogo para o estado inicial.

        Chamado na inicialização e após o jogador retornar da tela final.
        Garante que um novo jogo comece limpo sem precisar recriar
        o objeto Game.
        """
        self.gmap    = GameMap()
        tx, ty       = self.gmap.player_start()
        self.player  = Player(tx, ty)
        # Cria um NPC para cada entrada de NPC_DATA, na posição do mapa
        self.npcs    = [NPC(d, *self.gmap.npc_pos(d["id"])) for d in NPC_DATA]
        self.dialog  = DialogBox()
        self.minigame    = None    # instância do minigame ativo (ou None)
        self.active_npc  = None   # NPC atualmente em interação
        self.cam_x = max(0, min(self.player.x - SW // 2, self.gmap.width - SW))
        self.cam_y = max(0, min(self.player.y - SH // 2, self.gmap.height - SH))
        self.phase   = "explore"
        self.found_professor = False  # flag para evitar acionar a tela final mais de uma vez

    # ── CÂMERA ──────────────────────────────────────
    def update_camera(self):
        """
        Atualiza a posição da câmera com suavização (lerp).

        Alvo da câmera: player centralizado na tela.
        A câmera é limitada (clamped) entre 0 e o máximo do mapa
        para não mostrar área além das bordas.

        O fator 0.15 cria um efeito de "câmera flutuante":
        a câmera se aproxima 15% da diferença com o alvo por frame,
        resultando em movimento suave e responsivo.
        """
        target_x = self.player.x - SW // 2
        target_y = self.player.y - SH // 2
        max_x    = max(0, self.gmap.width - SW)
        max_y    = max(0, self.gmap.height - SH)

        self.cam_x += (target_x - self.cam_x) * 0.15
        self.cam_y += (target_y - self.cam_y) * 0.15

        self.cam_x = max(0, min(self.cam_x, max_x))
        self.cam_y = max(0, min(self.cam_y, max_y))

    # ── VERIFICAÇÃO DE FIM DE JOGO ───────────────────
    def check_final(self):
        """
        Verifica se o jogo deve terminar (vitória ou derrota).

        Chamada como callback após o diálogo de resultado de cada minigame.

        Condição de VITÓRIA:
            Todas as 4 pistas foram coletadas (o jogador venceu os 4 minigames).

        Condição de DERROTA:
            Todos os 4 NPCs já foram procurados (npc.done) mas o jogador
            não conseguiu as 4 pistas (perdeu em pelo menos um minigame).
            Sem essa checagem, o jogo nunca terminaria nesse caso.

        Em ambos os casos muda para a fase "final" e seta found_professor=True
        para evitar que seja acionada novamente. O desfecho exibido (vitória
        ou derrota) é decidido em screen_final() com base em player.pistas.
        """
        if self.found_professor:
            return
        if len(self.player.pistas) >= 4:
            self.found_professor = True
            self.phase = "final"
        elif all(npc.done for npc in self.npcs):
            self.found_professor = True
            self.phase = "final"

    # ── INICIAR MINIGAME ────────────────────────────
    def start_minigame(self, npc):
        """
        Instancia e ativa o minigame correspondente ao NPC.

        Parâmetro:
            npc → objeto NPC cujo minigame será iniciado

        Mapeia data["minigame"] → classe de Minigame:
            "piscina" → PiscinaGame
            "gol"     → GolGame
            "peruca"  → PerucaGame
            "fios"    → FiosGame

        Salva o NPC ativo em self.active_npc para uso em finish_minigame().
        Chamado como callback do DialogBox de introdução do NPC.
        """
        mg = npc.data["minigame"]
        if   mg == "piscina": self.minigame = PiscinaGame(self.screen)
        elif mg == "gol":     self.minigame = GolGame(self.screen)
        elif mg == "peruca":  self.minigame = PerucaGame(self.screen)
        elif mg == "fios":    self.minigame = FiosGame(self.screen)
        self.active_npc = npc
        self.phase = "minigame"

    # ── PÓS-MINIGAME ────────────────────────────────
    def finish_minigame(self):
        """
        Processa o resultado do minigame e inicia o diálogo de resposta.

        Sequência:
            1. Marca o NPC como done (escurece visualmente).
            2. Se vitória: adiciona pista_texto ao caderno do player,
               soma 100 pontos e usa pista_sucesso como falas do NPC.
            3. Se derrota: usa pista_falha como falas do NPC.
            4. Inicia DialogBox com essas falas e check_final() como callback.
            5. Volta para a fase "dialog" e limpa self.minigame.

        Impacto no jogo:
            Conecta o resultado do minigame à narrativa e à progressão.
            O callback check_final() pode desencadear a tela final se
            todas as pistas foram coletadas.
        """
        npc         = self.active_npc
        npc.done    = True
        npc.success = self.minigame.success

        if self.minigame.success:
            pista = npc.data["pista_texto"]
            self.player.pistas.append(pista)
            self.player.score += 100
            result_lines = npc.data["pista_sucesso"].split("\n")
        else:
            result_lines = npc.data["pista_falha"].split("\n")

        self.dialog.start(result_lines, callback=self.check_final)
        self.phase    = "dialog"
        self.minigame = None

    # ── INTERAÇÃO COM NPCs ───────────────────────────
    def interact(self):
        """
        Verifica proximidade com NPCs disponíveis e inicia diálogo.

        Percorre todos os NPCs; para o primeiro encontrado que:
            - Esteja perto do player (NPC.near())
            - Ainda não tenha sido concluído (not npc.done)

        Inicia o DialogBox com as falas de intro do NPC,
        com callback que chamará start_minigame(npc) ao terminar.

        Chamada quando o jogador pressiona E ou ESPAÇO na fase "explore".
        """
        for npc in self.npcs:
            if npc.near(self.player) and not npc.done:
                intro = npc.data["intro"]
                self.dialog.start(intro, callback=lambda n=npc: self.start_minigame(n))
                self.phase = "dialog"
                return

    # ── UPDATE (lógica por frame) ─────────────────────
    def update(self, events):
        """
        Atualiza a lógica do jogo com base na fase atual.

        Parâmetro:
            events → lista de eventos Pygame do frame atual
                     (ESC já filtrado pelo main loop)

        Fase "explore":
            - Lê teclas WASD para movimentação contínua
            - E/ESPAÇO → interact() (inicia diálogo com NPC próximo)
            - TAB → screen_pistas() (caderno de pistas, blocante)

        Fase "dialog":
            - E/ESPAÇO → dialog.advance()
            - Quando dialog.active se torna False e phase ainda é "dialog",
              volta para "explore" (o callback pode ter mudado a fase)

        Fase "minigame":
            - Repassa eventos para minigame.handle_event()
            - Chama minigame.update() a cada frame
            - Se minigame.done:
                * Exibe o frame final do minigame por 1800ms
                * Chama finish_minigame() para processar resultado

        Fase "final":
            - Chama screen_final() (blocante)
            - Após retorno (ENTER), chama reset() para novo jogo

        Sempre chama update_camera() ao final.
        """
        keys = pygame.key.get_pressed()

        if self.phase == "explore":
            dx = keys[pygame.K_d] - keys[pygame.K_a]
            dy = keys[pygame.K_s] - keys[pygame.K_w]
            if dx or dy:
                self.player.move(dx, dy, self.gmap.walls)
            for ev in events:
                if ev.type == pygame.KEYDOWN:
                    if ev.key in (pygame.K_e, pygame.K_SPACE):
                        self.interact()
                    if ev.key == pygame.K_TAB:
                        screen_pistas(self.screen, self.clock, self.player)

        elif self.phase == "dialog":
            for ev in events:
                if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_e, pygame.K_SPACE):
                    self.dialog.advance()
                    # Se o diálogo terminou e nenhum callback mudou a fase
                    if not self.dialog.active and self.phase == "dialog":
                        self.phase = "explore"

        elif self.phase == "minigame":
            for ev in events:
                self.minigame.handle_event(ev)
            self.minigame.update()
            if self.minigame.done:
                # Exibe o último frame do minigame por 1.8 segundo
                self.screen.fill(C_BLACK)
                self.minigame.draw()
                pygame.display.flip()
                pygame.time.wait(1800)
                self.finish_minigame()

        elif self.phase == "final":
            screen_final(self.screen, self.clock, self.player)
            self.reset()   # reinicia completamente para novo jogo

        self.update_camera()

    # ── DRAW (renderização por frame) ─────────────────
    def draw(self):
        """
        Renderiza o frame atual do jogo de acordo com a fase.

        Fase "minigame":
            Delega completamente para minigame.draw() e retorna.
            (Os minigames têm sua própria tela e HUD.)

        Demais fases (explore, dialog):
            1. Mapa (fundo, tiles, água animada)
            2. NPCs (com labels e indicador [E])
            3. Player (MAX)
            4. DialogBox (se ativo)
            5. HUD superior (título, fase, pistas/pontos)
            6. Minimap (canto superior direito)

        Chama pygame.display.flip() ao final para atualizar a tela.
        """
        if self.phase == "minigame":
            self.minigame.draw()
            pygame.display.flip()
            return

        # Renderização da cena principal
        self.gmap.draw(self.screen, int(self.cam_x), int(self.cam_y))

        for npc in self.npcs:
            npc.draw(self.screen, int(self.cam_x), int(self.cam_y))

        self.player.draw(self.screen, int(self.cam_x), int(self.cam_y))

        self.dialog.draw(self.screen)

        # Rótulos de fase para o HUD
        phase_labels = {
            "explore": "Explore a escola e fale com os suspeitos (E)  |  TAB = pistas",
            "dialog":  "CONVERSA  |  ESPAÇO para avançar",
        }
        draw_hud(self.screen, self.player, phase_labels.get(self.phase, ""))

        self._draw_minimap()
        pygame.display.flip()

    def _draw_minimap(self):
        """
        Renderiza o minimapa no canto superior direito da tela.

        Dimensões: 180×120 px
        Posição:   (SW - 188, 50) — 8px da borda direita, 50px do topo

        Conteúdo:
            - Fundo semi-transparente + borda cinza
            - Tiles do mapa em escala reduzida (apenas paredes, água, grama)
            - Pontos coloridos dos NPCs (escurecidos se done)
            - Ponto do player em verde

        Escala:
            sx = mw / (MAP_COLS * TILE)  → fator de escala horizontal
            sy = mh / (MAP_ROWS * TILE)  → fator de escala vertical
            Cada tile fica com ~6×6 px no minimapa.

        Impacto no jogo:
            Orienta o jogador no mapa sem precisar de uma tela separada.
            Permite ver onde estão os NPCs ainda disponíveis.
        """
        if self.gmap.width <= SW and self.gmap.height <= SH:
            return  # O cenário inteiro já está visível.
        mw, mh = self.gmap.minimap.get_size()
        mx0, my0 = SW - mw - 8, 50
        self.screen.blit(self.gmap.minimap, (mx0, my0))
        pygame.draw.rect(self.screen, C_GRAY, (mx0, my0, mw, mh), 1)
        sx, sy = mw / self.gmap.width, mh / self.gmap.height

        # NPCs no minimapa (ponto 5×5 px)
        for npc in self.npcs:
            nx   = int(mx0 + npc.x * sx)
            ny   = int(my0 + npc.y * sy)
            # Usa sempre a cor original (a linha com col2 = generator era um bug de display;
            # a cor do dicionário é acessada diretamente para clareza)
            pygame.draw.rect(self.screen, npc.data["color"], (nx - 2, ny - 2, 5, 5))

        # Player no minimapa (ponto 6×6 px verde)
        px = int(mx0 + self.player.x * sx)
        py = int(my0 + self.player.y * sy)
        pygame.draw.rect(self.screen, C_PLAYER, (px - 3, py - 3, 6, 6))


