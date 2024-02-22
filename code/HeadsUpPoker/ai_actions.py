class Bot:

    def __init__(self, chips=50000):
        self.chips = chips

    def call(self, bet, initial_chips):
        if self.chips - bet > 0: # AI has enough chips to call
            self.chips = initial_chips - bet
            return ["call", bet]
        else: # AI has to go all in
            raise_amount = self.chips
            difference = bet - self.chips
            self.chips = 0
            return ["all_in", raise_amount, difference]
        
    def raise_bet(self, raise_amount, initial_chips, ai_current_bet): # Checks will be handled in use to ensure raise isnt greater than AI chips.
        if self.chips < raise_amount + ai_current_bet:
            raise_amount = self.chips
            self.chips = 0
            return ["all_in", raise_amount]
        else:
            bet = raise_amount + ai_current_bet
            self.chips = initial_chips - bet
            return ["raise", raise_amount]


    def fold(self): #AI will fold if it believes it chance of winning is slim
        return ["fold"]
    
    def check(self): 
        return ["check"]
        