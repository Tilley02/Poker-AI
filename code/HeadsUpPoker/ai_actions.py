class Bot:

    def __init__(self, chips=50000):
        self.chips = chips

    def call(self, bet):
        if self.chips > bet:
            return ["call", bet]
        else:
            return ["all_in", self.chips]
        
    def raise_bet(self, raise_amount): # Checks will be handled in use to ensure raise isnt greater than AI chips.
        self.chips -= raise_amount
        return ["raise", raise_amount]


    def fold(self): #AI will fold if it believes it chance of winning is slim
        return ["fold"]
    
    def check(self): 
        return ["check"]
        