'''
Determining the strength of a hand will be done using a ranking system.
First we will have to rank a particular hand type using the following system, with '10' being
the strongest hand type possible, and '1' being the weakest
    
    Royal Flush --- 10
    Straight Flush --- 9
    Four of a Kind --- 8
    Full House --- 7
    Flush --- 6
    Straight --- 5
    Three of a Kind --- 4
    Two pair --- 3
    Pair --- 2
    High Card --- 1

Following this ranking, we will have to have an additional system for ranking a particular hand in
the case both the player and the AI have the same hand type.
In poker, the winner is determined by the highest card in the hand that is not shared among the players.
Thus, we will have to keep track of the value of the cards in a particular hand type. 

3-4 values will be returned using a list following correct identification of a hand type:
    ["Boolean Value of True", "Hand type's ranking (1-10)", "Values of Cards in hand", "Additional Values if needed"] 

Else a list [False] will be returned.


'''

class Hand:

    def __init__(self, full_hand, ranks, suits):
        self.full_hand = full_hand #Dictionary indicating a suit and its associated value
        self.ranks = ranks #List of Card values
        self.suits = suits #List of the suits of cards


    def has_difference_of_one(self, values): #To check for Straights
        for i in range(len(values) - 1):
            if abs(values[i] - values[i+1]) != 1:
                return False
            
        return True


    #6
    def isFlush(self):
        suits = {}

        for card in self.full_hand:
            suit = card['suit']
            if suit != 0:
                if suit not in suits:
                    suits[suit] = [card['rank']]
                else:
                    suits[suit].append(card['rank'])

        for suit, ranks in suits.items():
            if len(ranks) >= 5:
                # Sort the ranks in descending order and take the top 5
                flush_ranks = sorted(ranks, key=lambda x: int(x), reverse=True)[:5]
                return [True, flush_ranks]

        return [False]
    

    #5
    def isStraight(self, ranks): #Takes list of ranks

        ranks = [int(rank) for rank in ranks]        
        sorted_ranks = sorted(ranks, key=int, reverse=True) #Values with ace as 14 sorted in Descending order
        converted_ranks = ['1' if rank == '14' else rank for rank in ranks] #Values with ace as 1 sorted in Descending order
        sorted_ranks1 = sorted(converted_ranks, key=int, reverse=True)


        if len(ranks) > 5: #List of more than 5 numbers
            #Ace is 14
            if self.has_difference_of_one(sorted_ranks[0:5]):
                return [True, 5, sorted_ranks1[0]] 

            if self.has_difference_of_one(sorted_ranks[1:6]):
                return [True, 5, sorted_ranks1[1]]
    
            if self.has_difference_of_one(sorted_ranks[2:7]):
                return [True, 5, sorted_ranks1[2]]

            #Ace is 1
            if self.has_difference_of_one(sorted_ranks1[2:7]):
                return [True, 5, sorted_ranks1[2]]
            

        else: #List of 5 (Used for Straight Flush)
            
            #Ace is 14
            if self.has_difference_of_one(sorted_ranks):
                return [True, 5, sorted_ranks1[0]]

            #Ace is 1
            if self.has_difference_of_one(sorted_ranks1):
                return [True, 5, sorted_ranks1[2]]

    
        return [False]


    #4
    def isThreeOfAKind(self):
        rank_counts = {}
        int_ranks = [int(element) for element in self.ranks]

        for rank in self.ranks:
            if rank not in rank_counts:
                rank_counts[rank] = 1
            else:
                rank_counts[rank] += 1

            if rank_counts[rank] == 3 and len(set(self.ranks)) == 5: #Ensure it is not full house
                self.ranks = [r for r in int_ranks if r != rank]
                kickers = sorted(self.ranks, reverse=True)[0:2]
                return [True, 4, rank, kickers]

        return [False]


    #2
    #We will return additional values in the case we need to compare highest cards.
    def isPair(self):
        count_dict = {}

        for rank in self.ranks:
            if rank in count_dict:
                count_dict[rank] += 1
            else:
                count_dict[rank] = 1

        pair_rank = None
        non_pair_ranks = []

        for rank, count in count_dict.items():
            if count == 2:
                pair_rank = rank
            else:
                non_pair_ranks.append(rank)

        non_pair_ranks = sorted(non_pair_ranks, key=lambda x: int(x), reverse=True)[:3]

        return [True, 2, pair_rank, non_pair_ranks] if pair_rank is not None else [False]

    
    #3
    #We return four values if True: [True, hand_rank, two pairs rank, kicker]
    def isTwoPair(self):
        count_dict = {}

        for rank in self.ranks:
            if rank in count_dict:
                count_dict[rank] += 1
            else:
                count_dict[rank] = 1

        pairs = [rank for rank, count in count_dict.items() if count == 2]

        if len(pairs) >= 2:
            pairs = sorted(pairs, key=lambda x: int(x), reverse=True)[:2]

            unused = [rank for rank in self.ranks if rank not in pairs]
            kicker = max(map(int, unused)) #change to int
            
            return [True, 3, list(map(int, pairs)), kicker]

        return [False]


    #7
    def isFullHouse(self):
        count_dict = {}

        for rank in self.ranks:
            if rank in count_dict:
                count_dict[rank] += 1
            else:
                count_dict[rank] = 1

        three_of_a_kind = None
        two_of_a_kind = None

        for rank, count in count_dict.items():
            if count == 3:
                three_of_a_kind = rank
            elif count == 2:
                two_of_a_kind = rank

        if three_of_a_kind is not None and two_of_a_kind is not None:
            return [True, 7, three_of_a_kind, two_of_a_kind]

        return [False]


    #10
    def isRoyalFlush(self):

        perfect_straight = [14, 13, 12, 11, 10]  # Perfect Straight

        if self.isFlush()[0] and [int(rank) for rank in self.isFlush()[1]] == perfect_straight:
            return [True, 10]
        
        return [False]


    #9
    def isStraightFlush(self):
        
        if self.isFlush()[0] and self.isStraight(self.isFlush()[1])[0]:
            return [True, 9, self.isFlush()[1][0]]
        
        return [False]


    #8 
    #Returns Boolean, Hand Rank, Rank of Four of a kind, and kicker
    def isFourOfAKind(self):
        rank_counts = {}

        for rank in self.ranks:
            if rank != 0:
                if rank not in rank_counts:
                    rank_counts[rank] = 1
                else:
                    rank_counts[rank] += 1

                if rank_counts[rank] == 4:
                    # Remove the four cards of the same rank from the list
                    self.ranks = [r for r in self.ranks if r != rank]

                    if len(self.ranks) != 0:
                        # Find the highest kicker from the remaining cards
                        kicker = max(self.ranks, key=lambda x: int(x))
                        return [True, 8, rank, kicker]
                    else:
                        return [True, 8, rank]

        return [False]
    

    #1
    def highest_card(self):

        ranks = [int(rank) for rank in self.ranks]        
        sorted_ranks = sorted(ranks, key=int, reverse=True)
        return [1, max(sorted_ranks), sorted_ranks[1:]]    

com = [
    {'suit': 'Hearts', 'rank': '5'},  # Jack of Hearts
    {'suit': 'Hearts', 'rank': '5'},  # Ace of Hearts
    {'suit': 'Hearts', 'rank': '10'}, 
    {'suit': 'Diamonds', 'rank': '5'},  
    {'suit': 'Clubs', 'rank': '5'}   
]

pocket = [
    {'suit': 'Hearts', 'rank': '12'},  # King of Hearts
    {'suit': 'Hearts', 'rank': '9'}
    ] # Queen of Hearts

full_hand = pocket + com

# Changing values of aces to 14
for card in full_hand:
    if card['rank'] == '1':
        card['rank'] = '14'

