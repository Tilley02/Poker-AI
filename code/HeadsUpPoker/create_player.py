class Player:

    def __init__(self, chips=10000):
        self.chips = chips

    def call(self, pot):
        return ["call"]
        

    def raise_bet(self, pot, current_bet, new_bet):
        if new_bet > current_bet and new_bet <= self.chips:
            self.chips -= new_bet
            pot += new_bet
            return ["raise", new_bet]


    def fold(self, pot):
        return ["fold"]
        