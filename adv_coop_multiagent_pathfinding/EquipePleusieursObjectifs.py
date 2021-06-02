from Equipe import Equipe
#Idée faire passer dans le Tableau joueur les Index des joueurs 
#Puis dans la fonction Play on fait avcancer les joueur selon la stratégie
#

"""
L'idée avoir des joueurs qui ont plus de 1 objectifs par equipes:  (supposer que la map offre au moins 2 objectif par agents)
Pour le démarage l'agent se fixera comme objectif (celui qui donne la valeur d'heuristique la plus petite)
En cas de colision la gestion de colision est la suivant:
        #*Si H(vers_un_autre_but) < Longeur (Chemin qui reste actuellement vers le but)
            #*Changer de but

        #*Sinnon un choix Random de l'une de ces stratégies:
                #*Avancer vers une case voisine libre (Random):
                #*Recalculer le chemins (Avec des contraintes)
                #*Recalculer un autre chemin vers la case aprés l'obstacle
"""
from search.grid2D import ProblemeGrid3D
from search import probleme
import time
import random
import numpy as np
from TableDeReservation import Table
class EquipePluesieursButs(Equipe): 
    def __init__(self,name, emprunte):
        Equipe.__init__(self,name, emprunte)
        self.paths = [];
        self.table = Table();
       

    
    ##Trouver les path pour tout les joueurs
    def init_algorithme(self):
        self.list_objectif_actuelle = self.index_players.copy()
        if self.nombre_de_but > 1:
            #Exemple si on a 2 buts par joueurs
            #Le joueur 1 peut prendre l'objectif 1 et 1+1
            for index, player_id in enumerate(self.index_players):
                access = self.nombre_de_but * player_id;
                min_but = access;
                h_min = probleme.distManhattan(self.posPlayers[player_id], self.objectifs[access]);

                for b in range(self.nombre_de_but):
                    print("b: ",b)
                    new_h_min = probleme.distManhattan(self.posPlayers[player_id], self.objectifs[access + b]);
                    if (new_h_min < h_min):
                        min_but = access + b;
                        h_min = new_h_min;

                self.list_objectif_actuelle[index] = min_but;
            print("Objectifs : ", self.list_objectif_actuelle);


                
        for index, id_player in enumerate(self.index_players):
            print(self.index_players);
            index_objectif = self.list_objectif_actuelle[index];
            but = self.goalStates[index_objectif];
            init_position = self.posPlayers[id_player];
            p = ProblemeGrid3D(init_position, but, self.g, "manhattan", self.table, id_player);
            self.paths.append(probleme.astar3(p))

        """
        for index,id_player in enumerate(self.index_players):
            print("index  :  ",index,"   :  player:",id_player)
            objectif = self.list_objectif_actuelle[index]
            but  = self.goalStates[objectif]
            position_init = self.posPlayers[id_player]
            p = ProblemeGrid3D(position_init,but,self.g,'manhattan', self.table, id_player);
            ##AJouter les path dans la table de reservation
            self.paths.append(probleme.astar3(p));
        """
        print ("Chemin trouver sont :", self.paths)
    
    def print_reservation_table(self):
        print(self.table.table);

    def play (self):
        print(self.name + " Joue--------------:");
        self.i += 1
        for index, id_player in enumerate(self.competing_players):
            if id_player in self.players_arrived:
                continue;
         
            row, col = self.paths[index][self.i]
            colis = False
            (prev_row, prev_col) = self.paths[index][self.i-1]
            """
            #Gestion de colision Externe 
            if not self.is_case_libre(self.g[(row, col)]):
                #Vérifier si on doit changer de but
                rest = self.table_de_collision.doit_il_changer_de_but(self.paths[index], self.goalStates, self.list_objectif_actuelle[index], id_player,self.nombre_de_but, self.i)
                if rest != False:
                    self.list_objectif_actuelle[index] = rest

                    self.paths[index] = self.table_de_collision.recalculer_le_chemin_vers_le_but((prev_row, prev_col), self.goalStates[rest], self.g, self.paths[index], self.table, [(row, col)], self.i, id_player)
                    colis = True
                    print("RESUTAT DU CHANGEMENT", self.paths[index])
                    print("Noued en colision", row, col)
                    

                    print("CHANGEMENT DE BUTT ************")
                else:
                    if self.i+1 <= len(self.paths[index])-1:
                        self.paths[index] = self.table_de_collision.recalculer_le_chemin((prev_row, prev_col), self.paths[index][self.i+1], self.g, self.paths[index], self.table, [(row, col)], self.i, id_player)
                    else:
                        self.paths[index] = self.table_de_collision.recalculer_le_chemin_vers_le_but((prev_row, prev_col), self.goalStates[self.list_objectif_actuelle[index]], self.g, self.paths[index], self.table, [(row, col)], self.i, id_player)
            """
            if not self.is_case_libre(self.g[(row, col)]):
                random_choise = random.randint(0, 99);
                old_path = self.paths[index].copy();

                if((random_choise%3)==0):
                    print("#####*/*/*/Recalcule de chemin")
                    #si i est pair faire du path slicing 
                    newPath = self.paths[index] = self.table_de_collision.recalculer_le_chemin_vers_le_but((prev_row, prev_col), self.goalStates[self.list_objectif_actuelle[index]], self.g, self.paths[index], self.table, [(row, col)], self.i, id_player)
                elif((random_choise%2)==0):
                    print("#####*/*/*/Path slicing")
                    if self.i+1 <= len(self.paths[index])-1:
                        newPath = self.table_de_collision.recalculer_le_chemin((prev_row, prev_col), self.paths[index][self.i+1], self.g, self.paths[index], self.table, [(row, col)], self.i, id_player)
                    else:
                        newPath = self.table_de_collision.recalculer_le_chemin_vers_le_but((prev_row, prev_col), self.goalStates[self.list_objectif_actuelle[index]], self.g, self.paths[index], self.table, [(row, col)], self.i, id_player)
                else:
                    print("#####*/*/*/Changement de but")
                    index_but_actuel = self.list_objectif_actuelle[index]
                    min_but = self.table_de_collision.get_plus_proche_but(self.goalStates, self.goalStates[index_but_actuel],id_player,self.nombre_de_but,old_path[self.i]);
                    newPath = self.table_de_collision.recalculer_le_chemin_vers_le_but((prev_row, prev_col), self.goalStates[min_but], self.g, old_path.copy(), self.table, [(row, col)], self.i, id_player)
              
                self.paths[index] = newPath;
                 

                    
                #L'idée c'est de choisir au random (entre, le path slicing et le recalcul de chemin)
                #puis comparer la longeur du chemin résultant avec la distance manathan de du plus proche but (autre que but actuel);



            row, col = self.paths[index][self.i]
            self.posPlayers[id_player] = (row, col)
            self.g[(prev_row,prev_col)] = 1
            self.g[(row, col)] = self.emprunte
            self.players[id_player].set_rowcol(row, col)
            print("\tPos {id} : ".format(id=id_player), row, col)
            index_objectif = self.list_objectif_actuelle[index];
            but = self.goalStates[index_objectif];
            
            if(row, col) == but:
                self.score[id_player]+=1
                self.scoreEquipe+=1
                print("\tLe joueur {id} a atteint son but !".format(id=id_player))
                p = self.paths[index];
                #self.paths.remove(p);
                #self.competing_players.remove(id_player);
                self.players_arrived.append(id_player);
                self.etat_equipe()
            
            
        return len(self.players_arrived) == self.nbPlayers;


        




