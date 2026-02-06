from combinations import*
from math import*
from random import*
from probability import*

class Bot :
    def __init__ (self, hand, table, chips, indice, level) :
        self.hand = hand
        self.table = table
        self.chips = chips
        self.chips_raised = 0
        self.chipsinpot = 0
        self.indice = indice
        self.level = level

    def is_bluff(self) :
        return self.indice > randint(0, 10)
    
    def level_1 (self) :
        combo = combinations(self.hand, self.table)

        if self.indice < combo :
            return 'bet'
        
        elif self.indice == combo :
            return 'call'
        
        else :
            return 'fold'
        
    def level_2 (self) :
        combo = combinations(self.hand, self.table)
        global_combo = combinations([], self.table)
        bluff = self.is_bluff()

        if combo == global_combo :
            if bluff :
                return 'bet'
            return 'call'
        
        if self.indice < combo :
            if bluff :
                return 'call'
            return 'bet'
        
        elif self.indice == combo :
            if bluff :
                return 'bet'
            return 'call'
        
        else :
            if bluff :
                return 'bet'
            return 'fold'
        
    def level_max (self) :



    def bot_turn (self) :
        pass