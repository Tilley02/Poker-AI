import pygame, random, time, os

from shuffle import shuffle_deck
from determine_winner import determine_winner
from create_player import Player
from ai_main import AI
from center_asset import center_x, center_y

pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

pygame.display.set_caption("Heads Up Poker")

screen = pygame.display.set_mode((screen_width, screen_height - 50))

MAIN_BG = pygame.transform.scale(pygame.image.load("./assets/backgrounds/main_bg.png"), (screen.get_size()))
TITLE_BG = pygame.transform.scale(pygame.image.load("./assets/backgrounds/title_bg.png"), (screen.get_size()))


SETTINGS_BG = []
settings_bg_filenames = ["./assets/backgrounds/settings/clouds_5/1.png",
                        "./assets/backgrounds/settings/clouds_5/2.png",
                        "./assets/backgrounds/settings/clouds_5/3.png",
                        "./assets/backgrounds/settings/clouds_5/4.png",
                        "./assets/backgrounds/settings/clouds_5/5.png"]

for filename in settings_bg_filenames:
    background = pygame.image.load(filename)
    background = pygame.transform.scale(background, (screen_width, screen_height))
    SETTINGS_BG.append(background)

#MUSIC
# Load music file
music_main = './assets/music/main.mp3'
music_menu = './assets/music/menu.mp3'

#SFX
click_sound_main = pygame.mixer.Sound("./assets/sfx/menu.mp3") 
click_sound_game_action = pygame.mixer.Sound("./assets/sfx/game_actions.mp3") 
click_sound_play_again = pygame.mixer.Sound("./assets/sfx/play_again.mp3") 

card_images = {
    'Hearts': {'1': pygame.transform.scale(pygame.image.load('./assets/cards/card-hearts-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '2': pygame.transform.scale(pygame.image.load('./assets/cards/card-hearts-2.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '3': pygame.transform.scale(pygame.image.load('./assets/cards/card-hearts-3.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '4': pygame.transform.scale(pygame.image.load('./assets/cards/card-hearts-4.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '5': pygame.transform.scale(pygame.image.load('./assets/cards/card-hearts-5.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                '6': pygame.transform.scale(pygame.image.load('./assets/cards/card-hearts-6.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '7': pygame.transform.scale(pygame.image.load('./assets/cards/card-hearts-7.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '8': pygame.transform.scale(pygame.image.load('./assets/cards/card-hearts-8.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '9': pygame.transform.scale(pygame.image.load('./assets/cards/card-hearts-9.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                  '10': pygame.transform.scale(pygame.image.load('./assets/cards/card-hearts-10.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '11': pygame.transform.scale(pygame.image.load('./assets/cards/card-hearts-11.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '12': pygame.transform.scale(pygame.image.load('./assets/cards/card-hearts-12.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '13': pygame.transform.scale(pygame.image.load('./assets/cards/card-hearts-13.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '14': pygame.transform.scale(pygame.image.load('./assets/cards/card-hearts-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22)))},

    'Diamonds': {'1': pygame.transform.scale(pygame.image.load('./assets/cards/card-diamonds-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '2': pygame.transform.scale(pygame.image.load('./assets/cards/card-diamonds-2.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '3': pygame.transform.scale(pygame.image.load('./assets/cards/card-diamonds-3.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '4': pygame.transform.scale(pygame.image.load('./assets/cards/card-diamonds-4.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '5': pygame.transform.scale(pygame.image.load('./assets/cards/card-diamonds-5.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                '6': pygame.transform.scale(pygame.image.load('./assets/cards/card-diamonds-6.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '7': pygame.transform.scale(pygame.image.load('./assets/cards/card-diamonds-7.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '8': pygame.transform.scale(pygame.image.load('./assets/cards/card-diamonds-8.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '9': pygame.transform.scale(pygame.image.load('./assets/cards/card-diamonds-9.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                  '10': pygame.transform.scale(pygame.image.load('./assets/cards/card-diamonds-10.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '11': pygame.transform.scale(pygame.image.load('./assets/cards/card-diamonds-11.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '12': pygame.transform.scale(pygame.image.load('./assets/cards/card-diamonds-12.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '13': pygame.transform.scale(pygame.image.load('./assets/cards/card-diamonds-13.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '14': pygame.transform.scale(pygame.image.load('./assets/cards/card-diamonds-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22)))},

    'Clubs': {'1': pygame.transform.scale(pygame.image.load('./assets/cards/card-clubs-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '2': pygame.transform.scale(pygame.image.load('./assets/cards/card-clubs-2.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '3': pygame.transform.scale(pygame.image.load('./assets/cards/card-clubs-3.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '4': pygame.transform.scale(pygame.image.load('./assets/cards/card-clubs-4.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '5': pygame.transform.scale(pygame.image.load('./assets/cards/card-clubs-5.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                '6': pygame.transform.scale(pygame.image.load('./assets/cards/card-clubs-6.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '7': pygame.transform.scale(pygame.image.load('./assets/cards/card-clubs-7.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '8': pygame.transform.scale(pygame.image.load('./assets/cards/card-clubs-8.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '9': pygame.transform.scale(pygame.image.load('./assets/cards/card-clubs-9.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                  '10': pygame.transform.scale(pygame.image.load('./assets/cards/card-clubs-10.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '11': pygame.transform.scale(pygame.image.load('./assets/cards/card-clubs-11.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '12': pygame.transform.scale(pygame.image.load('./assets/cards/card-clubs-12.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '13': pygame.transform.scale(pygame.image.load('./assets/cards/card-clubs-13.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '14': pygame.transform.scale(pygame.image.load('./assets/cards/card-clubs-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22)))},

    'Spades': {'1': pygame.transform.scale(pygame.image.load('./assets/cards/card-spades-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '2': pygame.transform.scale(pygame.image.load('./assets/cards/card-spades-2.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '3': pygame.transform.scale(pygame.image.load('./assets/cards/card-spades-3.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '4': pygame.transform.scale(pygame.image.load('./assets/cards/card-spades-4.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '5': pygame.transform.scale(pygame.image.load('./assets/cards/card-spades-5.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                '6': pygame.transform.scale(pygame.image.load('./assets/cards/card-spades-6.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '7': pygame.transform.scale(pygame.image.load('./assets/cards/card-spades-7.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '8': pygame.transform.scale(pygame.image.load('./assets/cards/card-spades-8.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '9': pygame.transform.scale(pygame.image.load('./assets/cards/card-spades-9.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                  '10': pygame.transform.scale(pygame.image.load('./assets/cards/card-spades-10.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '11': pygame.transform.scale(pygame.image.load('./assets/cards/card-spades-11.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '12': pygame.transform.scale(pygame.image.load('./assets/cards/card-spades-12.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '13': pygame.transform.scale(pygame.image.load('./assets/cards/card-spades-13.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '14': pygame.transform.scale(pygame.image.load('./assets/cards/card-spades-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22)))},

    'Back': {'1': pygame.transform.scale(pygame.image.load('./assets/cards/card-back1.png'), (int(screen_width * 0.09), int(screen_height * 0.22)))}  # Modify this line as needed
}

# Display
game_title = pygame.transform.scale(pygame.image.load('./assets/display/title.png'), (screen_width * 0.6, screen_height *0.25))
ai_win_display = pygame.transform.scale(pygame.image.load('./assets/display/ai_win.png'), (500, 175))
player_win_display = pygame.transform.scale(pygame.image.load('./assets/display/player_win.png'), (500, 175))


# Title Screen Buttons
button_title_play = pygame.transform.scale(pygame.image.load('./assets/buttons/GUI/title/start_game.png'), (screen_width * 0.25, screen_height * 0.15))
button_title_play_rect = button_title_play.get_rect(topleft=(center_x(screen_width, screen_width * 0.25), screen_height * 0.32))

button_title_settings = pygame.transform.scale(pygame.image.load('./assets/buttons/GUI/title/settings.png'), (screen_width * 0.25, screen_height * 0.15))
button_title_settings_rect = button_title_play.get_rect(topleft=(center_x(screen_width, screen_width * 0.25), screen_height * 0.50))

button_title_quit = pygame.transform.scale(pygame.image.load('./assets/buttons/GUI/title/quit.png'), (screen_width * 0.25, screen_height * 0.15))
button_title_quit_rect = button_title_play.get_rect(topleft=(center_x(screen_width, screen_width * 0.25), screen_height * 0.68))

# Settings Buttons
button_settings_back = pygame.transform.scale(pygame.image.load('./assets/buttons/GUI/title/back.png'), (screen_width * 0.25, screen_height * 0.15))
button_settings_back_rect = button_title_play.get_rect(topleft=(center_x(screen_width, screen_width * 0.25), screen_height * 0.68))


# Gameplay UI Buttons
button_home = pygame.transform.scale(pygame.image.load('./assets/buttons/GUI/gamestate/home.png'), (screen_width * 0.075, screen_height * 0.075))
button_home_rect = button_home.get_rect(topleft=(screen_width * 0.92, screen_height * 0.01))

button_settings = pygame.transform.scale(pygame.image.load('./assets/buttons/GUI/gamestate/settings.png'), (screen_width * 0.075, screen_height * 0.075))
button_settings_rect = button_settings.get_rect(topleft=(screen_width * 0.84, screen_height * 0.01))


# Gameplay Action Buttons
button_check = pygame.transform.scale(pygame.image.load('./assets/buttons/game_actions/check.png'), (150, 75))
button_check_rect = button_check.get_rect(topleft=(25, 500))

button_raise = pygame.transform.scale(pygame.image.load('./assets/buttons/game_actions/raise.png'), (150, 75))
button_raise_rect = button_raise.get_rect(topleft=(215, 500))

button_fold = pygame.transform.scale(pygame.image.load('./assets/buttons/game_actions/fold.png'), (150, 75))
button_fold_rect = button_fold.get_rect(topleft=(405, 500))

button_play_again = pygame.transform.scale(pygame.image.load('./assets/buttons/game_actions/play_again.png'), (600, 250))


# Title Screen
def draw_title_screen():
    screen.blit(TITLE_BG, (0, 0))
    screen.blit(game_title, (center_x(screen_width, screen_width * 0.6), screen_height * 0.02))
    screen.blit(button_title_play, (center_x(screen_width, screen_width * 0.25), screen_height * 0.32))
    screen.blit(button_title_settings, (center_x(screen_width, screen_width * 0.25), screen_height * 0.50))
    screen.blit(button_title_quit, (center_x(screen_width, screen_width * 0.25), screen_height * 0.68))

    pygame.display.update()


# Settings 
def draw_settings():
    for background in SETTINGS_BG:
        screen.blit(background, (0, 0))
    screen.blit(button_settings_back, (center_x(screen_width, screen_width * 0.25), screen_height * 0.68))
    
    pygame.display.update()
    #Background


def draw_cards(cards, x, y):
    for card in cards:

        suit = card['suit']
        rank = card['rank']
        card_image = card_images[suit][rank]
        screen.blit(card_image, (x, y))
        x += screen_width * 0.095

# State 1 - Community Cards not shown
def drawState1(deck):
    screen.blit(MAIN_BG, (0, 0))

    screen.blit(button_check, (25, 500))
    screen.blit(button_raise, (215, 500))
    screen.blit(button_fold, (405, 500))
    screen.blit(button_home, (screen_width * 0.92, screen_height * 0.01))
    screen.blit(button_settings, (screen_width * 0.84, screen_height * 0.01))


    player_hand = deck[0:2]
    ai_hand = [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]
    community_cards = [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]

    draw_cards(player_hand, screen_width * 0.405, screen_height * 0.65)
    draw_cards(ai_hand, screen_width * 0.405, screen_height * 0.08)
    draw_cards(community_cards, screen_width * 0.2625, screen_height * 0.365)

    pygame.display.update()


# State 2 = Three Community Cards Shown
def drawState2(deck):
    screen.blit(MAIN_BG, (0, 0))

    screen.blit(button_check, (25, 500))
    screen.blit(button_raise, (215, 500))
    screen.blit(button_fold, (405, 500))
    screen.blit(button_home, (screen_width * 0.92, screen_height * 0.01))
    screen.blit(button_settings, (screen_width * 0.84, screen_height * 0.01))

    player_hand = deck[0:2]
    ai_hand = [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]
    community_cards = deck[4:7] + [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]

    draw_cards(player_hand, screen_width * 0.405, screen_height * 0.65)
    draw_cards(ai_hand, screen_width * 0.405, screen_height * 0.08)
    draw_cards(community_cards, screen_width * 0.2625, screen_height * 0.365)

    pygame.display.update()


# State 3 = Four Community Cards Shown
def drawState3(deck):
    screen.blit(MAIN_BG, (0, 0))

    screen.blit(button_check, (25, 500))
    screen.blit(button_raise, (215, 500))
    screen.blit(button_fold, (405, 500))
    screen.blit(button_home, (screen_width * 0.92, screen_height * 0.01))
    screen.blit(button_settings, (screen_width * 0.84, screen_height * 0.01))

    player_hand = deck[0:2]
    ai_hand = [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]
    community_cards = deck[4:8] + [{'suit': 'Back', 'rank': '1'}]

    draw_cards(player_hand, screen_width * 0.405, screen_height * 0.65)
    draw_cards(ai_hand, screen_width * 0.405, screen_height * 0.08)
    draw_cards(community_cards, screen_width * 0.2625, screen_height * 0.365)

    pygame.display.update()


# State 4 = All Community Cards Shown
def drawState4(deck):
    screen.blit(MAIN_BG, (0, 0))

    screen.blit(button_check, (25, 500))
    screen.blit(button_raise, (215, 500))
    screen.blit(button_fold, (405, 500))
    screen.blit(button_home, (screen_width * 0.92, screen_height * 0.01))
    screen.blit(button_settings, (screen_width * 0.84, screen_height * 0.01))

    player_hand = deck[0:2]
    ai_hand = [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]
    community_cards = deck[4:9]

    draw_cards(player_hand, screen_width * 0.405, screen_height * 0.65)
    draw_cards(ai_hand, screen_width * 0.405, screen_height * 0.08)
    draw_cards(community_cards, screen_width * 0.2625, screen_height * 0.365)

    pygame.display.update()


# State 5 = Reveal Winner
def drawState5(deck):
    screen.blit(MAIN_BG, (0, 0))

    player_hand = deck[0:2]
    ai_hand = deck[2:4]
    community_cards = deck[4:9]

    draw_cards(player_hand, screen_width * 0.405, screen_height * 0.65)
    draw_cards(ai_hand, screen_width * 0.405, screen_height * 0.08)
    draw_cards(community_cards, screen_width * 0.2625, screen_height * 0.365)

    pygame.display.update()



def drawState6(winner):
    if winner == "AI Wins":
        screen.blit(ai_win_display, (300, 200))


    else:
        screen.blit(player_win_display, (250, 300))


    pygame.display.update()

    time.sleep(3)
    screen.blit(TITLE_BG, (0, 0))
    screen.blit(button_play_again, (200, 250))
    pygame.display.update()




#### ----------------------------------------------------------------------------------------------------------------- ###



def main():
    run = True
    game_state = 0
    pot = 0
    outcome = ""
    settings_return_state = game_state

    title_state, settings_state, state1, state2, state3, state4, state5, state6 = False, False, False, False, False, False, False, False
    play_title_music = True
    # Purpose of the above variables is so we only draw each game game_state once, as it is unneccesary for the states to be infinitely drawn while waiting for player action.
    
    deck = shuffle_deck() # Shuffle a deck of cards.
    player_blind_status = random.randint(0, 1) # Initial random allocation of Big and Little Blind. 0 indicates a player is Big Blind.
    ai_blind_status = 1 ^ player_blind_status # Assigns AI with the number not selected.
    ai_action, player_action = ["ai"], ["player"]

    big_blind, little_blind = 200, 100. # Big and little blind increase by 200 and 100 respectively, after every hand.
    ai_bot = Player()
    player = Player()

    # We can already determine if the AI or player will win based on the cards that were dealt. If no one folds, we will use this to determine the winner.
    winner = determine_winner(deck[0:2], deck[2:4], deck[4:9])
    print(deck[0:2])

    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    
                    # Title Screen Buttons
                    if button_title_play_rect.collidepoint(event.pos) and game_state == 0: # Start game button
                        click_sound_main.play()
                        game_state = 1
                        title_state = False
                        pygame.mixer.music.load(music_main)
                        pygame.mixer.music.set_volume(0.1)
                        pygame.mixer.music.play(-1)  # -1 loops the music indefinitely

                    elif button_title_settings_rect.collidepoint(event.pos) and game_state != 7: # Home button
                        click_sound_main.play()
                        settings_return_state = game_state
                        game_state = 7

                    elif button_title_quit_rect.collidepoint(event.pos) and game_state == 0: # Quit game button
                        click_sound_main.play()
                        time.sleep(0.5)
                        run = False
                        break


                    # Settings Buttons
                    elif button_settings_back_rect.collidepoint(event.pos) and game_state == 7: # Back button
                        click_sound_main.play()
                        game_state = settings_return_state
                        title_state, settings_state, state1, state2, state3, state4, state5, state6 = False, False, False, False, False, False, False, False


                    # In-game Buttons
                    elif button_check_rect.collidepoint(event.pos) and 0 < game_state < 5: # Check button
                        click_sound_game_action.play()
                        game_state += 1


                    elif button_raise_rect.collidepoint(event.pos) and 0 < game_state < 5: # Raise button
                        click_sound_game_action.play()
                        game_state += 1

                    elif button_fold_rect.collidepoint(event.pos) and 0 < game_state < 5: # Fold button
                        click_sound_game_action.play()
                        game_state += 1


                    # Misc Buttons
                    elif button_home_rect.collidepoint(event.pos) and 0 < game_state < 5: # Home button
                        click_sound_main.play()
                        state1, state2, state3, state4, state5, state6 = False, False, False, False, False, False
                        game_state = 0
                        play_title_music = True

                    elif button_settings_rect.collidepoint(event.pos) and 0 < game_state < 5:  # Settings Button
                        click_sound_main.play()
                        settings_return_state = game_state
                        game_state = 7

                    

                    
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN and game_state == 6 and waiting_for_enter:
                    click_sound_play_again.play()
                    print("\n -------- New Hand -------- \n")
                    deck = shuffle_deck()
                    winner = determine_winner(deck[0:2], deck[2:4], deck[4:9])
                    game_state = 1
                    state6 = False
                    waiting_for_enter = False  # Set flag to False to prevent further processing of Enter key


        # Title Screen
        if game_state == 0:
            if not title_state:
                draw_title_screen()
                title_state = True
                if play_title_music == True:
                    pygame.mixer.music.load(music_menu)
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)  # -1 loops the music indefinitely
                    play_title_music = False
                        

        # Show player cards, but community cards are all face down.
        if game_state == 1:
            if not state1:
                pot += (big_blind + little_blind) # Add the blinds to the pot
                drawState1(deck)
                state6, state1 = False, True
                
                if play_title_music == True:
                    pygame.mixer.music.load(music_menu)
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)  # -1 loops the music indefinitely
            
            '''
                if player_blind_status == 0:
                    player.chips -= big_blind
                    ai_bot.chips -= little_blind 
                
                else: 
                    ai_bot.chips -= big_blind
                    player.chips -= little_blind 

                while(True):
                    # subtract little and big blind from player's chips

                    player_action = 1 #ASK PLAYER FOR ACTION
                    ai_action = AI(ai_bot, game_state, deck[2:4]) #AI Actions

                    #Handle if one player folds preflop first
                    if player_action[0] == "fold" or ai_action == "fold":
                        if player_action[0] == "fold":
                            ai_bot.chips += pot
                            outcome == "AI"
                            pot = 0
                            game_state = 6
                            break

                        else:
                            player.chips += pot
                            outcome == "Player"
                            pot = 0
                            game_state = 6
                            break

                            
                    if player_action[0] == "call" and ai_action == "call":
                        game_state == 2
                        break

                    if player_action[0] == "raise" or ai_action == "raise":
                            
                        if player_action[0] == "raise":
                            break
                        '''


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

            time.sleep(3)# Wait before displaying winner
            game_state = 6

        if game_state == 6:
            if not state6:
                state6, state5 = True, False
                drawState6(winner)
                waiting_for_enter = True


        if game_state == 7:
            if not settings_state:
                settings_state = True
                draw_settings()

        #pygame.display.flip()




    pygame.quit()

if __name__ == "__main__":
    main()