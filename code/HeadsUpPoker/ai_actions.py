class Bot:

    def __init__(self, chips=50000):
        self.chips = chips

    def call(self, bet):
        if self.chips > bet:
            self.chips -= bet
            return ["call", bet]
        else:
            raise_amount = self.chips
            self.chips = 0
            return ["all_in", raise_amount]
        
    def raise_bet(self, raise_amount): # Checks will be handled in use to ensure raise isnt greater than AI chips.
        if self.chips < raise_amount:
            raise_amount = self.chips
            self.chips = 0
            return ["raise", raise_amount]
        else:
            self.chips -= raise_amount
            return ["raise", raise_amount]


    def fold(self): #AI will fold if it believes it chance of winning is slim
        return ["fold"]
    
    def check(self): 
        return ["check"]
        