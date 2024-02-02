import pygame, random

from shuffle import shuffle_deck
from determine_winner import determine_winner
from game_actions import Action

pygame.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Heads Up Poker")

BG = pygame.transform.scale(pygame.image.load("./assets/backgrounds/main_bg.png"), (WIDTH, HEIGHT))
TITLE_BG = pygame.transform.scale(pygame.image.load("./assets/backgrounds/title_bg.png"), (WIDTH, HEIGHT))



card_images = {
    'Hearts': {'1': pygame.image.load('./assets/cards/card-hearts-1.png'), '2': pygame.image.load('./assets/cards/card-hearts-2.png'), '3': pygame.image.load('./assets/cards/card-hearts-3.png'), '4': pygame.image.load('./assets/cards/card-hearts-4.png'), '5': pygame.image.load('./assets/cards/card-hearts-5.png'),
                '6': pygame.image.load('./assets/cards/card-hearts-6.png'), '7': pygame.image.load('./assets/cards/card-hearts-7.png'), '8': pygame.image.load('./assets/cards/card-hearts-8.png'), '9': pygame.image.load('./assets/cards/card-hearts-9.png'),
                  '10': pygame.image.load('./assets/cards/card-hearts-10.png'), '11': pygame.image.load('./assets/cards/card-hearts-11.png'), '12': pygame.image.load('./assets/cards/card-hearts-12.png'), '13': pygame.image.load('./assets/cards/card-hearts-13.png'), '14': pygame.image.load('./assets/cards/card-hearts-1.png')},

    'Diamonds': {'1': pygame.image.load('./assets/cards/card-diamonds-1.png'), '2': pygame.image.load('./assets/cards/card-diamonds-2.png'), '3': pygame.image.load('./assets/cards/card-diamonds-3.png'), '4': pygame.image.load('./assets/cards/card-diamonds-4.png'), '5': pygame.image.load('./assets/cards/card-diamonds-5.png'),
                '6': pygame.image.load('./assets/cards/card-diamonds-6.png'), '7': pygame.image.load('./assets/cards/card-diamonds-7.png'), '8': pygame.image.load('./assets/cards/card-diamonds-8.png'), '9': pygame.image.load('./assets/cards/card-diamonds-9.png'),
                  '10': pygame.image.load('./assets/cards/card-diamonds-10.png'), '11': pygame.image.load('./assets/cards/card-diamonds-11.png'), '12': pygame.image.load('./assets/cards/card-diamonds-12.png'), '13': pygame.image.load('./assets/cards/card-diamonds-13.png'), '14': pygame.image.load('./assets/cards/card-diamonds-1.png')},

    'Clubs': {'1': pygame.image.load('./assets/cards/card-clubs-1.png'), '2': pygame.image.load('./assets/cards/card-clubs-2.png'), '3': pygame.image.load('./assets/cards/card-clubs-3.png'), '4': pygame.image.load('./assets/cards/card-clubs-4.png'), '5': pygame.image.load('./assets/cards/card-clubs-5.png'),
                '6': pygame.image.load('./assets/cards/card-clubs-6.png'), '7': pygame.image.load('./assets/cards/card-clubs-7.png'), '8': pygame.image.load('./assets/cards/card-clubs-8.png'), '9': pygame.image.load('./assets/cards/card-clubs-9.png'),
                  '10': pygame.image.load('./assets/cards/card-clubs-10.png'), '11': pygame.image.load('./assets/cards/card-clubs-11.png'), '12': pygame.image.load('./assets/cards/card-clubs-12.png'), '13': pygame.image.load('./assets/cards/card-clubs-13.png'), '14': pygame.image.load('./assets/cards/card-clubs-1.png')},

    'Spades': {'1': pygame.image.load('./assets/cards/card-spades-1.png'), '2': pygame.image.load('./assets/cards/card-spades-2.png'), '3': pygame.image.load('./assets/cards/card-spades-3.png'), '4': pygame.image.load('./assets/cards/card-spades-4.png'), '5': pygame.image.load('./assets/cards/card-spades-5.png'),
                '6': pygame.image.load('./assets/cards/card-spades-6.png'), '7': pygame.image.load('./assets/cards/card-spades-7.png'), '8': pygame.image.load('./assets/cards/card-spades-8.png'), '9': pygame.image.load('./assets/cards/card-spades-9.png'),
                  '10': pygame.image.load('./assets/cards/card-spades-10.png'), '11': pygame.image.load('./assets/cards/card-spades-11.png'), '12': pygame.image.load('./assets/cards/card-spades-12.png'), '13': pygame.image.load('./assets/cards/card-spades-13.png'), '14': pygame.image.load('./assets/cards/card-spades-1.png')},

    'Back': {'1': pygame.image.load('./assets/cards/card-back1.png')} ## Change colour of card back -> [ card-back1 = blue, card-back2 = orange, card-back3 = green, card-back4 = yellow ]
}

# Title Screen
game_title = pygame.transform.scale(pygame.image.load('./assets/title.png'), (600, 250))
button_title_play = pygame.transform.scale(pygame.image.load('./assets/buttons/start_game.png'), (400, 100))
button_title_play_rect = button_title_play.get_rect(topleft=(300, 400))

# Game Action Buttons
button_check = pygame.transform.scale(pygame.image.load('./assets/buttons/check.png'), (150, 75))
button_check_rect = button_check.get_rect(topleft=(25, 500))

def draw_title_screen():
    WIN.blit(TITLE_BG, (0, 0))

    WIN.blit(game_title, (200, 0))
    WIN.blit(button_title_play, (300, 400))

    #WIN.blit(button_title_play, (500, 400))
    
    pygame.display.update()


def draw_cards(cards, x, y):
    for card in cards:

        suit = card['suit']
        rank = card['rank']
        card_image = card_images[suit][rank]
        WIN.blit(card_image, (x, y))
        x += 100

# State 1 - Community Cards not shown
def drawState1(deck):
    WIN.blit(BG, (0, 0))

    WIN.blit(button_check, (25, 500))


    player_hand = deck[0:2]
    ai_hand = [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]
    community_cards = [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]

    draw_cards(player_hand, 200, 600)
    draw_cards(ai_hand, 200, 50)
    draw_cards(community_cards, 50, 325)

    pygame.display.update()


# State 2 = Three Community Cards Shown
def drawState2(deck):
    WIN.blit(BG, (0, 0))
    WIN.blit(button_check, (25, 500))

    player_hand = deck[0:2]
    ai_hand = [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]
    community_cards = deck[4:7] + [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]

    draw_cards(player_hand, 200, 600)
    draw_cards(ai_hand, 200, 50)
    draw_cards(community_cards, 50, 325)

    pygame.display.update()


# State 3 = Four Community Cards Shown
def drawState3(deck):
    WIN.blit(BG, (0, 0))
    WIN.blit(button_check, (25, 500))

    player_hand = deck[0:2]
    ai_hand = [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]
    community_cards = deck[4:8] + [{'suit': 'Back', 'rank': '1'}]

    draw_cards(player_hand, 200, 600)
    draw_cards(ai_hand, 200, 50)
    draw_cards(community_cards, 50, 325)

    pygame.display.update()


# State 4 = All Community Cards Shown
def drawState4(deck):
    WIN.blit(BG, (0, 0))
    WIN.blit(button_check, (25, 500))

    player_hand = deck[0:2]
    ai_hand = [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]
    community_cards = deck[4:9]

    draw_cards(player_hand, 200, 600)
    draw_cards(ai_hand, 200, 50)
    draw_cards(community_cards, 50, 325)

    pygame.display.update()


# State 5 = Reveal Winner
def drawState5(deck):
    WIN.blit(BG, (0, 0))
    WIN.blit(button_check, (25, 500))

    player_hand = deck[0:2]
    ai_hand = deck[2:4]
    community_cards = deck[4:9]

    draw_cards(player_hand, 200, 600)
    draw_cards(ai_hand, 200, 50)
    draw_cards(community_cards, 50, 325)

    pygame.display.update()



def main():
    run = True
    game_state = 0

    title_state, state1, state2, state3, state4, state5 = False, False, False, False, False, False 
    # Purpose of the above variables is so we only draw each game game_state once, as it is unneccesary for the states to be infinitely drawn while waiting for player action.
    
    deck = shuffle_deck() # Shuffle a deck of cards.
    player_blind_status = random.randint(0, 1) # Initial random allocation of Big and Little Blind. 0 indicates a player is Big Blind.
    ai_blind_status = 1 ^ player_blind_status # Assigns AI with the number not selected.

    player = Action(player_blind_status, 10000) # Creation of Player. We can later change this to connect with player from database.
    ai = Action(ai_blind_status, 10000) # Creation of AI.
    big_blind, small_blind = 200, 100. # Big and little blind increase by 200 and 100 respectively, after every hand.

    # We can already determine if the AI or player will win based on the cards that were dealt. If no one folds, we will use this to determine the winner.
    winner = determine_winner(deck[0:2], deck[2:4], deck[4:9])

    while run:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                break
            
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if button_check_rect.collidepoint(event.pos) and game_state != 0:
                        if game_state == 5:
                            print("\n -------- New Hand -------- \n")
                            deck = shuffle_deck()
                            winner = determine_winner(deck[0:2], deck[2:4], deck[4:9])
                            game_state = 1
                        else:
                            game_state += 1

                    elif button_title_play_rect.collidepoint(event.pos) and game_state == 0:
                        game_state = 1
                        title_state = False


        # Title Screen
        if game_state == 0:
            if not title_state:
                draw_title_screen()
                title_state = True
                        

        # Show player cards, but community cards are all face down.
        if game_state == 1:
            if not state1:
                drawState1(deck)
                state5, state1 = False, True

        # Reveal 3 of the Community Cards
        if game_state == 2:
            if not state2:
                drawState2(deck)
                state1, state2 = False, True

        # Reveal fourth community card
        if game_state == 3:
            if not state3:
                drawState3(deck)
                state2, state3 = False, True

        # Reveal the 5th and final community card.
        if game_state == 4:
            if not state4:
                drawState4(deck)
                state3, state4 = False, True

        # Reveal AI cards to show winner!
        if game_state == 5:
            if not state5:
                drawState5(deck)
                state4, state5 = False, True
                print("\n", winner)

    pygame.quit()

if __name__ == "__main__":
    main()