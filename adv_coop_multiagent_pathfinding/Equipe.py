from search.grid2D import ProblemeGrid2D
from search import probleme
from table_de_collision import TableDeColision
import numpy as np
#Idée faire passer dans le Tableau joueur les Index des joueurs 
#Puis dans la fonction Play on fait avcancer les joueur selon la stratégie
#
class Equipe(object): 
    def __init__(self,name, emprunte):
        self.name = name
        self.i = 0
        self.index_players = []
        self.competing_players = []
        self.players_arrived = []
        self.scoreEquipe = 0
        self.emprunte = emprunte;
    
    def init_algorithme(self):
        pass
    
    def play (self):
        pass

    def setGame(self, game):
        self.game = game;
        self.nbLignes = game.spriteBuilder.rowsize
        self.nbCols = game.spriteBuilder.colsize
    
    def set_wallStates(self, wallStates):
        self.wallStates = wallStates
    
    def setPosPlayers(self, posplayer):
        self.posPlayers = posplayer;

    def setGolaStates(self,goalStates):
        self.goalStates = goalStates;
        self.objectifs = goalStates
    
    def set_legal_position(self, fun):
        self.legal_position = fun;
        self.table_de_collision = TableDeColision(fun);
        
    
    def set_scores(self, scores):
        self.score= scores
    
    def setPlayers(self, players):
        self.players = players
    
    def set_index_players(self, indexs):
        self.index_players.extend(indexs);
        self.competing_players = self.index_players;
        self.nbPlayers = len(indexs);

    def etat_equipe(self):
        print("\t\tÉtat de actuel de l'equipe")
        print("\t\tEquipe : ", self.name);
        print("\t\tJoueurs restants : ",[o for o in filter(lambda x : x not in self.players_arrived,  self.competing_players)]);
        print("\t\tJoueurs arrivés : ", self.players_arrived);
        print("\t\tScore : ", self.scoreEquipe);
    
    def get_score(self):
        return self.scoreEquipe
    
    def set_matrice(self, g):
        self.g = g
    
    def get_index_of_player(self, id):
        if id in self.index_players:
            return self.index_players.index(id)
        return -1
    
    def adverssaire_emprunte(self, emprunte):
        if emprunte not in [1, 0, self.emprunte]:
            return True;
        return False
    
    def is_case_libre(self, case):
        return case == 1;
    
    def set_nombre_de_but_par_joueur(self, nbr):
        self.nombre_de_but = nbr;
   
