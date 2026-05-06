🎮 Eu Sei o Que Vocês Fizeram na Corrida Passada
- Um jogo de investigação com humor e desafios em um ambiente escolar.


 1. Descrição Geral

Eu Sei o Que Vocês Fizeram na Corrida Passada é um jogo 2D desenvolvido em Python utilizando a biblioteca Pygame.
 O jogo combina elementos de investigação, aventura e minigames, sendo ambientado em uma escola,o IFRN Campus Caicó. Nele, o jogador assume o papel de um aluno,MAX,que decide investigar o misterioso desaparecimento do professor Romerito.
 Durante a jornada, o jogador deve explorar diferentes espaços da escola e interagir com quatro suspeitos. Cada suspeito propõe um desafio único, como corrida, precisão de tempo, busca de objetos e resolução de puzzles. Ao completar esses desafios, o jogador recebe informações que ajudam a avançar na investigação.
 A proposta do jogo é unir narrativa leve, humor e desafios interativos, incentivando o raciocínio e a atenção do jogador enquanto ele progride na história.

2. Objetivo do Jogo

O jogador deve:

* Completar desafios propostos pelos suspeitos
* Coletar informações/pistas
* Descobrir o paradeiro do professor

Meta final: Encontrar o professor Romerito.

3. Personagem Principal

* Nome: (Max)
* Descrição: Aluno curioso
* Movimentação: Livre (W, A, S, D, E)
* Atributos:
  Posição: define a localização do personagem no mapa
  Velocidade: determina a rapidez da movimentação
  Pontuação: representa o progresso do jogador através das pistas obtidas

4. Inimigos e Obstáculos

Os obstáculos variam por desafio:

  * Piscina: Anderson(que está tentando avançar)
  * Gol: erro de timing
  * Peruca: objeto escondido
  * Fios: fios desordenados

* Comportamento:
Baseados em mecânica do minigame

* Consequência:
  * Falha no desafio + Perda de informação

5. Cenário (Mapa)
* Ambiente principal: Escola
Locais:

  * Sala de aula
  * Corredor da escola
  * Piscina
  * Quadra
  * Sala dos professores
  * Laboratório 

* Elementos:

  * Paredes: delimitam os espaços e impedem a passagem do jogador
  * Caminhos: áreas livres onde o personagem pode se movimentar
  * Áreas bloqueadas: locais acessíveis apenas após cumprir certos objetivos
  * NPCs (personagens): responsáveis por interações e desafios
  * Objetos interativos: itens que podem ser coletados ou utilizados durante o jogo

6. Sistema de Pontuação
Ganho de pontos por:

  * Completar desafios
  * Obter pistas


8. Controles

| Tecla   | Função                 |
| ------- | ---------------------- |
| W A S D | Movimentação           |
| Espaço  | Interação e execução   |
| Mouse   | Interações específicas |
| ESC     | Pausar/Sair            |


9. Fluxo do Jogo

1. Tela inicial
2. Jogador entra no mapa(escola)
3. Interage com suspeitos e outros
4. Realiza desafios
5. Coleta pistas
6. Avança de fase
7. Final encontra o professor


10. Regras do Jogo
* Interagir apenas quando permitido
* Completar desafios para obter informações
* Falhar não impede progresso, mas dificulta o final


11. Estrutura do Projeto
*******ESBOÇO*******
```
jogo/
│
├── main.py
├── player.py
├── npc.py
├── minigames/
│   ├── piscina.py
│   ├── gol.py
│   ├── peruca.py
│   └── fios.py
│
├── assets/
│   ├── player/
│   ├── npcs/
│   ├── backgrounds/
│   └── sounds/
│
└── utils/
```

12. Funcionalidades Mínimas

* Movimentação do jogador
* Interação com NPCs
* Pelo menos 1 minigame funcional
* Tela inicial


13. Melhorias Futuras

* Animações de personagens
* Sons e trilha sonora
* Interface gráfica mais detalhada

14. Storyboard do Jogo

**terminar os designs do storboard

1. Desafio da piscina
2. Desafio do gol
3. Desafio da peruca
4. Desafio dos fios
5. Cena final (pista de corrida)

(Colocar imagem do storyboard aqui)


Equipe

Integrante 1: (Ana Élida N. de Souza)
Integrante 2: (Ana Allyce da Silva Albino)
Integrante 3: (Lays Eduarda Araújo Silva)
