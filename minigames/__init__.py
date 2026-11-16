"""
Pacote minigames — os 4 minigames do jogo, todos derivados de Minigame (base.py).
"""

from minigames.base import Minigame
from minigames.piscina import PiscinaGame
from minigames.gol import GolGame
from minigames.peruca import PerucaGame
from minigames.fios import FiosGame

__all__ = ["Minigame", "PiscinaGame", "GolGame", "PerucaGame", "FiosGame"]
