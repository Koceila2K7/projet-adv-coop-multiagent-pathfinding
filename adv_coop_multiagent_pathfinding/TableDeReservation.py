class Table:
    def __init__(self):
        self.table = dict();
    
    def codage(self,x,y,t):
        return "{},{},{}".format(x,y,t);
    
    def is_reserved(self, x, y, t):
        return self.codage(x,y,t) in self.table;
    
    def precendent_reserved(self, x, y, t):
        key = self.codage(x,y,t);
        if key in self.table:
            return self.table[key];
        return -1

    def reserve(self, x, y, t, id):
        if self.is_reserved(x,y,t):
            return False;
        
        self.table[self.codage(x,y,t)] = id;
        return True;

    def annuler_des_reservation(self,id, t):
        list_a_suprimer = []
        for key in self.table:
            value = self.table[key]
            keys = key.split(',');
            if value == id and int(keys[2])>=t:
                list_a_suprimer.append(key)
        
        for i in list_a_suprimer:
            self.table.pop(key, None)
        return True;
                
    



        