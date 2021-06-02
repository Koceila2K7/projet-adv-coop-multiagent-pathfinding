from Equipe import Equipe
#Idée faire passer dans le Tableau joueur les Index des joueurs 
#Puis dans la fonction Play on fait avcancer les joueur selon la stratégie
#
from search.grid2D import ProblemeGrid3D
from search import probleme
import time
import numpy as np
from TableDeReservation import Table
class EquipeB(Equipe): 
    def __init__(self,name, emprunte):
        Equipe.__init__(self,name, emprunte)
        self.paths = [];
        self.table = Table();
    
    ##Trouver les path pour tout les joueurs
    def init_algorithme(self):
         
        for i in self.index_players:
            p = ProblemeGrid3D(self.posPlayers[i],self.objectifs[i],self.g,'manhattan', self.table, i);
            ##AJouter les path dans la table de reservation
            self.paths.append(probleme.astar3(p));

        print ("Chemin trouver sont :", self.paths)
    
    def print_reservation_table(self):
        print(self.table.table);

    def play (self):
        print(self.name + " Joue--------------:");
        self.i+=1
        for index, id_player in enumerate(self.competing_players):
            if id_player in self.players_arrived:
                continue;
            p = self.paths[index]
            row, col = self.paths[index][self.i]
            colis = False
            (prev_row, prev_col) = self.paths[index][self.i-1]
            #Gestion de colision Externe 
            if not self.is_case_libre(self.g[(row, col)]):
                self.paths[index] = self.table_de_collision.recalculer_le_chemin_vers_le_but((prev_row, prev_col), self.goalStates[id_player], self.g, self.paths[index], self.table, [(row, col)], self.i, id_player)
                


                """
                    (prev_row, prev_col) = self.paths[index][self.i-1]
                    self.paths[index].insert(self.i, (prev_row, prev_col));
                    #self.paths[index] = self.table_de_collision.recalculer_le_chemin((prev_row,prev_col), self.paths[index][self.i+2], self.paths[index], self.table, self.g, [(row, col)], self.i)
                """
            
            
            row, col = self.paths[index][self.i]
            self.posPlayers[id_player] = (row, col)
            self.g[(prev_row,prev_col)] = 1
            self.g[(row, col)] = self.emprunte
            self.players[id_player].set_rowcol(row, col)
            print("\tPos {id} : ".format(id=id_player), row, col)
                
            if(row, col) == self.objectifs[id_player]:
                self.score[id_player]+=1
                self.scoreEquipe+=1
                print("\tLe joueur {id} a atteint son but !".format(id=id_player))
                p = self.paths[index];
                #self.paths.remove(p);
                #self.competing_players.remove(id_player);
                self.players_arrived.append(id_player);
                self.etat_equipe()

        return len(self.players_arrived) == self.nbPlayers;


        




