# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals
import time
import random 
import numpy as np
import sys
from itertools import chain

#from equipe import Equipe
import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme
from equipeA import EquipeA
from EquipeB import EquipeB
from EquipeR import EquipeR
from EquipePs import EquipePS
from EquipePleusieursObjectifs import EquipePluesieursButs
from Equipe3CaseALavance import Equipe3CaseALavance
from Partie import Partie



# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----




# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'demoMap'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    
    
def main():
    iterations = 50 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)
    
    equipes = [Equipe3CaseALavance("Equipe 1 ", 15), EquipePS("Equipe 2 ", 26)]
    partie1 = Partie("exAdvCoopMap", equipes,200)
    partie1.lancer_la_partie();
    pygame.quit()
    exit()
    #-------------------------------
        
  

if __name__ == '__main__':
    main()
    


