from __future__ import absolute_import, print_function, unicode_literals
import time
import random 
import numpy as np
import sys
from itertools import chain

import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
import time
class Partie: 
    def __init__(self,name_of_map, equipes, iteration = 100, objectifs = []):
        self.init(name_of_map)
        self.equipes = equipes;
        self.iteration = iteration
        self.nbEquipe = len(self.equipes);
        self.players = [o for o in self.game.layers['joueur']]
        self.nbPlayers = len(self.players)
        self.score = [0]*self.nbPlayers
        self.initStates = [o.get_rowcol() for o in self.game.layers['joueur']]
        self.goalStates = [o.get_rowcol() for o in self.game.layers['ramassable']]
        """
        objectif3 = self.goalStates[2]
        objectif1 = self.goalStates[0]
        self.goalStates[0] = objectif3
        self.goalStates[2] = objectif1
        """
        if( objectifs==[] or len(objectifs)!=len(self.goalStates) ):
            random.shuffle(self.goalStates)
        else:
            print("anciens objectifs = ", self.goalStates)
            new_objectifs = []
            for obj in objectifs:
                new_objectifs.append(self.goalStates[obj])
            self.goalStates = new_objectifs
            print("nouveaux objectifs = ", self.goalStates)

        self.wallStates = [w.get_rowcol() for w in self.game.layers['obstacle']]
        self.repartition_joueur();
        nbLignes = self.game.spriteBuilder.rowsize
        nbCols = self.game.spriteBuilder.colsize

        def legal_position(row,col):
            # une position legale est dans la carte et pas sur un mur
            return ((row,col) not in self.wallStates) and row>=0 and row<nbLignes and col>=0 and col<nbCols
        
        self.legal_position = lambda x, y: legal_position(x,y)
        self.g =np.ones((nbLignes,nbCols),dtype=int)  # par defaut la matrice comprend des True  
        for w in self.wallStates:            # putting False for walls
            self.g[w]=0

        for e in equipes:
            e.set_matrice(self.g)
            e.setGame(self.game)
            e.set_nombre_de_but_par_joueur(len(self.goalStates) // self.nbPlayers);
            print("Golas state ", self.goalStates)
            e.setGolaStates(self.goalStates);
            e.setPlayers(self.players);
            e.set_wallStates(self.wallStates);
            e.setPosPlayers(self.initStates);
            e.set_scores(self.score);
            e.set_legal_position(self.legal_position);
        
    def init(self, _boardname=None):
        self.name = _boardname if _boardname is not None else 'demoMap'
        self.game = Game('Cartes/' + self.name + '.json', SpriteBuilder)
        self.game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
        self.game.populate_sprite_names(self.game.O)
        self.game.fps = 5  # frames per second
        self.game.mainiteration()
        self.player = self.game.player
    
    def repartition_joueur(self):
        reaminder = self.nbPlayers // self.nbEquipe;
        print("remainder", reaminder)
        print("nb Players", self.nbPlayers)
        print("nb Equipes", self.nbEquipe)
        start = 0
        end = reaminder
        for e in self.equipes:
            e.set_index_players([o for o in range(start, end)]);
            start = end;
            end += reaminder
        #dans le cas ou les joueur ne peuvent être réparti equitablement, on à pris le choix d'assigner le surplus à l'equipe 0
        if((reaminder * self.nbEquipe) < self.nbPlayers):
            self.equipes[0].set_index_players([o for o in range(end, self.nbPlayers)]);

    def lancer_la_partie(self):
        for e in self.equipes:
            e.init_algorithme();

        for i in range(self.iteration):
            print("******  Tour  num : {} ******".format(i))
            self.game.mainiteration()
            #time.sleep(0.25)
            if(self.equipes[i%self.nbEquipe].play()):
                print("Equipe, {} à gagner par KO".format(i%self.nbEquipe+1))
                #print(self.equipes[i%self.nbEquipe].g)
                #self.equipes[i%self.nbEquipe].print_reservation_table()
                return True;
            self.game.draw();
        
        maxScore  = self.equipes[0].get_score();
        indexWin = 0
        
        for index, e in enumerate(self.equipes):
            if(maxScore < e.get_score()):
                maxScore = e.get_score();
                indexWin = index;
        
        print("Equipe, {} à gagner par points avec {} ".format(indexWin+1, maxScore))
        exit()
        

        

        

        
        
