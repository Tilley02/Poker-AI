'''
This class defines the different actions a player can take.
'''

class Action:

    def __init__(self, blind_status, chips):
        self.blind_status = blind_status
        self.chips = chips

    def check(self):
        return ["check"]

    def raise_bet(self, current_bet, new_bet):
        if(new_bet > current_bet) and (new_bet <= self.chips):
            return ["raise", new_bet]
        if(new_bet < current_bet):
            return self.raise_bet()

    def fold(self):
        return ["fold"]

    def call(self):
        return ["call"]

    def next_hand(self):
        ["next_hand"]