from search.grid2D import ProblemeGrid3DAvecVoisinInterdit
from search import probleme
import random 
import time
class TableDeColision:
    def __init__(self, isLegal):
        self.dict = dict();
        self.isLegal = isLegal;

    def codage(self,x,y,id):
        return "{},{},{}".format(x,y,id);

    def sauvgarder_une_colision(self,x,y,id):
        key = self.codage(x,y,id);
        if key in self.dict:
            self.dict[key] += 1
        else:
            self.dict[key] = 1
        #Colision de TROP détécter 
        #Il faut agir en conséquence
        return self.dict[key] >= 2
    
    def peut_t_il_bouger(self,x,y,matrice):
        a = [(0,1),(0,-1),(1,0),(-1,0)]
        random.shuffle(a)
        for pos in a:
            (xx,yy) = pos;
            if self.isLegal(x+xx, y+yy):
                if(matrice[(x+xx, y+yy)]==1):
                    return (x+xx, y+yy);
        return False
    
    def recalculer_le_chemin (self, init, objectif, matrice, old_path, table, noued_interdit,debut_temps, id):
        p = ProblemeGrid3DAvecVoisinInterdit(init, objectif, matrice, 'manhattan', table,id,noued_interdit,)
        newPath = probleme.astar(p);
        print('but ', objectif)
        print('Voisin interdit', noued_interdit)

        print("successeur",p.successeurs(init))
        print("depart", init)
        print("Path", newPath)

        print("OLD PATH", old_path)

        print(old_path.pop(debut_temps-1))
        print(old_path.pop(debut_temps-1))
        print(old_path.pop(debut_temps-1))

        for index,j in enumerate(newPath):
            old_path.insert(debut_temps+index-1, j)
        print("new PATH", old_path)
        #time.sleep(12)
        return old_path;

    #Recalculer le chemin de la position actuelle vers le but en évitant le case self.
    def recalculer_le_chemin_vers_le_but (self, init, objectif, matrice, old_path, table, noued_interdit,debut_temps, id):
        p = ProblemeGrid3DAvecVoisinInterdit(init, objectif, matrice, 'manhattan', table,id,noued_interdit,)
        table.annuler_des_reservation(id, debut_temps)
        newPath = probleme.astar(p);
        taille = len(newPath);
        print('but ', objectif)
        print('Voisin interdit', noued_interdit)

        print("successeur",p.successeurs(init))
        print("depart", init)
        print("Path", newPath)
        
        if(newPath[taille-1] != objectif):
            old_path.insert(debut_temps, init);
            return old_path;
        
        print("OLD PATH", old_path);
        old_path = old_path[:debut_temps];
        for index, j in enumerate(newPath):
            old_path.insert(index+debut_temps, j);
        (x,y) = init

        key = self.codage(x,y,id);
        self.dict[key] = 0
        print("New PATH", old_path);
        return old_path;


    def doit_il_changer_de_but(self, old_path, liste_objectif, objectif_actuel, id_player, nombre_de_but, temps):
        pos_actuelle = old_path[temps - 1];
        distance_restante = len(old_path[temps-1:]);
        newObjectif = objectif_actuel
        print("Doit t'il changer de but")
        for b in range(nombre_de_but):
            access = (id_player*nombre_de_but)+b;

            if access == objectif_actuel:
                continue;

            print("Distante restante est : ",distance_restante);
            distance_manatane = probleme.distManhattan(pos_actuelle, liste_objectif[access])
            print("Distante Manatane est : ",distance_manatane);

            if ( distance_manatane<= distance_restante):
                newObjectif = access
        
        if (newObjectif==objectif_actuel):
            return False;
        return newObjectif;

    def get_plus_proche_but(sef, liste_objectif, objectif_actuel, id_player, nombre_de_but, position):
        min_h = 999999
        min_but = None
        for i in range(nombre_de_but):
            access = (id_player * nombre_de_but) + i
            if access == objectif_actuel:
                continue;
            distance_manatane = probleme.distManhattan(position, liste_objectif[access]);
            if(distance_manatane< min_h):
                min_but = access;
        
        return min_but;


    def y_a_t_il_un_adversaire_dans_mon_chemin(self,path, matrice, temps, champ_de_vision):
        longeur = len(path)-1
        for i in range(champ_de_vision):
            if((temps+i) > longeur):
                return False
            else:
                if (matrice[path[i+temps]]!=1):
                    return True
        
        return False;

            
