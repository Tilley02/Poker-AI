import pygame, random, time, os
import pygame.gfxdraw

from pygame.locals import *
from shuffle import shuffle_deck
from determine_winner import determine_winner
from ai_actions import Bot
from ai_main import ai
from player_action import Player
from center_asset import center_x, center_y

pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

current_dir = os.path.dirname(os.path.abspath(__file__))

pygame.display.set_caption("Heads Up Poker")

screen = pygame.display.set_mode((screen_width, screen_height - 50))

TITLE_BG = pygame.transform.scale(pygame.image.load(current_dir+"/assets/backgrounds/title_bg.png"), (screen.get_size()))
GAME_BG = pygame.transform.scale(pygame.image.load(current_dir+"/assets/backgrounds/game/game_background_3/game_background_3.1.png"), (screen.get_size()))

SETTINGS_BG = []
settings_bg_filenames = [current_dir+"/assets/backgrounds/settings/clouds_5/1.png",
                        current_dir+"/assets/backgrounds/settings/clouds_5/2.png",
                        current_dir+"/assets/backgrounds/settings/clouds_5/3.png",
                        current_dir+"/assets/backgrounds/settings/clouds_5/4.png",
                        current_dir+"/assets/backgrounds/settings/clouds_5/5.png"]

for filename in settings_bg_filenames:
    background = pygame.image.load(filename)
    background = pygame.transform.scale(background, (screen_width, screen_height))
    SETTINGS_BG.append(background)


#MUSIC
# Load music file
music_main = current_dir+'/assets/music/main.mp3'
music_menu = current_dir+'/assets/music/menu.mp3'

#SFX
click_sound_main = pygame.mixer.Sound(current_dir+"/assets/sfx/menu.mp3") 
click_sound_game_action = pygame.mixer.Sound(current_dir+"/assets/sfx/game_actions.mp3") 
click_sound_play_again = pygame.mixer.Sound(current_dir+"/assets/sfx/play_again.mp3") 

card_images = {
    'Hearts': {'1': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-hearts-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '2': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-hearts-2.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '3': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-hearts-3.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '4': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-hearts-4.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '5': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-hearts-5.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                '6': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-hearts-6.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '7': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-hearts-7.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '8': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-hearts-8.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '9': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-hearts-9.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                  '10': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-hearts-10.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '11': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-hearts-11.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '12': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-hearts-12.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '13': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-hearts-13.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '14': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-hearts-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22)))},

    'Diamonds': {'1': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-diamonds-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '2': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-diamonds-2.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '3': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-diamonds-3.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '4': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-diamonds-4.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '5': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-diamonds-5.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                '6': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-diamonds-6.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '7': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-diamonds-7.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '8': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-diamonds-8.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '9': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-diamonds-9.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                  '10': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-diamonds-10.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '11': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-diamonds-11.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '12': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-diamonds-12.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '13': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-diamonds-13.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '14': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-diamonds-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22)))},

    'Clubs': {'1': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-clubs-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '2': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-clubs-2.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '3': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-clubs-3.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '4': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-clubs-4.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '5': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-clubs-5.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                '6': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-clubs-6.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '7': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-clubs-7.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '8': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-clubs-8.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '9': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-clubs-9.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                  '10': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-clubs-10.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '11': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-clubs-11.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '12': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-clubs-12.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '13': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-clubs-13.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '14': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-clubs-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22)))},

    'Spades': {'1': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-spades-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '2': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-spades-2.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '3': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-spades-3.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '4': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-spades-4.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '5': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-spades-5.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                '6': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-spades-6.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '7': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-spades-7.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '8': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-spades-8.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '9': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-spades-9.png'), (int(screen_width * 0.09), int(screen_height * 0.22))),
                  '10': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-spades-10.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '11': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-spades-11.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '12': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-spades-12.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '13': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-spades-13.png'), (int(screen_width * 0.09), int(screen_height * 0.22))), '14': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-spades-1.png'), (int(screen_width * 0.09), int(screen_height * 0.22)))},

    'Back': {'1': pygame.transform.scale(pygame.image.load(current_dir+'/assets/cards/card-back1.png'), (int(screen_width * 0.09), int(screen_height * 0.22)))}  # Modify this line as needed
}

# Display
game_title = pygame.transform.scale(pygame.image.load(current_dir+'/assets/display/title.png'), (screen_width * 0.6, screen_height *0.25))
ai_player_display = pygame.transform.scale(pygame.image.load(current_dir+'/assets/display/ai_player.png'), (screen_width * 0.12, screen_height * 0.07))
ai_checked_display = pygame.transform.scale(pygame.image.load(current_dir+'/assets/display/checked.png'), (screen_width * 0.1, screen_height * 0.05))
ai_raised_display = pygame.transform.scale(pygame.image.load(current_dir+'/assets/display/raised.png'), (screen_width * 0.1, screen_height * 0.05))
ai_win_display = pygame.transform.scale(pygame.image.load(current_dir+'/assets/display/ai_wins.png'), (screen_width * 0.5, screen_height * 0.25))
player_win_display = pygame.transform.scale(pygame.image.load(current_dir+'/assets/display/player_wins.png'), (screen_width * 0.5, screen_height * 0.25))
ai_call_display = pygame.transform.scale(pygame.image.load(current_dir+'/assets/display/ai_calls.png'), (screen_width * 0.4, screen_height * 0.25))
ai_check_display = pygame.transform.scale(pygame.image.load(current_dir+'/assets/display/ai_checks.png'), (screen_width * 0.4, screen_height * 0.25))
ai_raise_display = pygame.transform.scale(pygame.image.load(current_dir+'/assets/display/ai_raises.png'), (screen_width * 0.4, screen_height * 0.25))
ai_fold_display = pygame.transform.scale(pygame.image.load(current_dir+'/assets/display/ai_folds.png'), (screen_width * 0.4, screen_height * 0.25))
chip_total = pygame.transform.scale(pygame.image.load(current_dir+'/assets/display/chip_total.png'), (screen_width * 0.11, screen_height * 0.06))
pot_text = pygame.transform.scale(pygame.image.load(current_dir+'/assets/display/pot_text.png'), (screen_width * 0.09, screen_height *0.09))
pot_chips = pygame.transform.scale(pygame.image.load(current_dir+'/assets/display/pot_chips.png'), (screen_width * 0.06, screen_height *0.06))
pot_font = pygame.font.Font(current_dir+'/assets/fonts/Pacifico-Regular.ttf', 120)
current_bet_display = pygame.transform.scale(pygame.image.load(current_dir+'/assets/display/current_bet.png'), (screen_width * 0.15, screen_height * 0.06))


# Title Screen Buttons
button_title_play = pygame.transform.scale(pygame.image.load(current_dir+'/assets/buttons/GUI/title/start_game.png'), (screen_width * 0.25, screen_height * 0.15))
button_title_play_rect = button_title_play.get_rect(topleft=(center_x(screen_width, screen_width * 0.25), screen_height * 0.32))

button_title_settings = pygame.transform.scale(pygame.image.load(current_dir+'/assets/buttons/GUI/title/settings.png'), (screen_width * 0.25, screen_height * 0.15))
button_title_settings_rect = button_title_play.get_rect(topleft=(center_x(screen_width, screen_width * 0.25), screen_height * 0.50))

button_title_quit = pygame.transform.scale(pygame.image.load(current_dir+'/assets/buttons/GUI/title/quit.png'), (screen_width * 0.25, screen_height * 0.15))
button_title_quit_rect = button_title_play.get_rect(topleft=(center_x(screen_width, screen_width * 0.25), screen_height * 0.68))

# Settings Buttons
button_settings_back = pygame.transform.scale(pygame.image.load(current_dir+'/assets/buttons/GUI/title/back.png'), (screen_width * 0.25, screen_height * 0.15))
button_settings_back_rect = button_title_play.get_rect(topleft=(center_x(screen_width, screen_width * 0.25), screen_height * 0.68))


# Gameplay UI Buttons
button_home = pygame.transform.scale(pygame.image.load(current_dir+'/assets/buttons/GUI/gamestate/home.png'), (screen_width * 0.065, screen_height * 0.075))
button_home_rect = button_home.get_rect(topleft=(screen_width * 0.93, screen_height * 0.01))

button_settings = pygame.transform.scale(pygame.image.load(current_dir+'/assets/buttons/GUI/gamestate/settings.png'), (screen_width * 0.065, screen_height * 0.075))
button_settings_rect = button_settings.get_rect(topleft=(screen_width * 0.86, screen_height * 0.01))


# Gameplay Action Buttons
button_check = pygame.transform.scale(pygame.image.load(current_dir+'/assets/buttons/game_actions/check.png'), (screen_width * 0.1, screen_height * 0.08))
button_check_rect = button_check.get_rect(topleft=(screen_width * 0.448, screen_height * 0.84))

button_raise = pygame.transform.scale(pygame.image.load(current_dir+'/assets/buttons/game_actions/raise.png'), (screen_width * 0.1, screen_height * 0.08))
button_raise_rect = button_raise.get_rect(topleft=(screen_width * 0.578, screen_height * 0.84))

button_increase_raise = pygame.transform.scale(pygame.image.load(current_dir+'/assets/buttons/GUI/gamestate/up.png'), (screen_width * 0.075, screen_height * 0.075))
button_increase_raise_rect = button_increase_raise.get_rect(topleft=(screen_width * 0.59, screen_height * 0.84))

button_decrease_raise = pygame.transform.scale(pygame.image.load(current_dir+'/assets/buttons/GUI/gamestate/down.png'), (screen_width * 0.075, screen_height * 0.075))
button_decrease_raise_rect = button_decrease_raise.get_rect(topleft=(screen_width * 0.331, screen_height * 0.84))

button_confirm_raise = pygame.transform.scale(pygame.image.load(current_dir+'/assets/buttons/GUI/gamestate/confirm.png'), (screen_width * 0.075, screen_height * 0.075))
button_confirm_raise_rect = button_confirm_raise.get_rect(topleft=(screen_width * 0.69, screen_height * 0.84))

button_cancel_raise = pygame.transform.scale(pygame.image.load(current_dir+'/assets/buttons/GUI/gamestate/cancel.png'), (screen_width * 0.075, screen_height * 0.075))
button_cancel_raise_rect = button_cancel_raise.get_rect(topleft=(screen_width * 0.231, screen_height * 0.84))

button_fold = pygame.transform.scale(pygame.image.load(current_dir+'/assets/buttons/game_actions/fold.png'), (screen_width * 0.1, screen_height * 0.08))
button_fold_rect = button_fold.get_rect(topleft=(screen_width * 0.318, screen_height * 0.84))

button_call = pygame.transform.scale(pygame.image.load(current_dir+'/assets/buttons/game_actions/call.png'), (screen_width * 0.1, screen_height * 0.1))
button_call_rect = button_call.get_rect(topleft=(screen_width * 0.448, screen_height * 0.82))

button_play_again = pygame.transform.scale(pygame.image.load(current_dir+'/assets/buttons/game_actions/play_again.png'), (screen_width * 0.35, screen_height * 0.25))


def update_pot_amount(pot):
    # Render the pot amount as text
    font_size = 145
    text_color = (235, 235, 235)
    pot = int(pot)
    formatted_pot = "{:,}".format(pot)  # Format the pot amount with commas
    font = pygame.font.Font(None, font_size)
    pot_text = font.render("$" + formatted_pot, True, text_color)
    return pot_text

def update_raise_amount(raise_int):
    font_size = 115
    text_color = (235, 235, 235)
    raise_int = int(raise_int)
    formatted_raise = "{:,}".format(raise_int)  # Format the raise amount with commas
    font = pygame.font.Font(None, font_size)
    raise_text = font.render("$" + formatted_raise, True, text_color)
    return raise_text

def update_chips_amount(chips):
    font_size = 72
    text_color = (235, 235, 235)
    chips = int(chips)
    formatted_chips = "{:,}".format(chips)  # Format the number with commas
    font = pygame.font.Font(None, font_size)
    chips_text = font.render("$" + formatted_chips, True, text_color)
    return chips_text

def update_current_bet_amount(current_bet):
    font_size = 100
    text_color = (235, 235, 235)
    current_bet = int(current_bet)
    formatted_current_bet = "{:,}".format(current_bet)  # Format the number with commas
    font = pygame.font.Font(None, font_size)
    current_bet_text = font.render("$" + formatted_current_bet, True, text_color)
    return current_bet_text

def update_ai_current_bet_amount(ai_current_bet):
    font_size = 100
    text_color = (235, 235, 235)
    ai_current_bet = int(ai_current_bet)
    formatted_current_bet = "{:,}".format(ai_current_bet)  # Format the number with commas
    font = pygame.font.Font(None, font_size)
    current_bet_text = font.render("$" + formatted_current_bet, True, text_color)
    return current_bet_text

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


def draw_ai_action(action):
    if action != None:

        if action == "raise":
            screen.blit(ai_raised_display, (screen_width * 0.1, screen_height * 0.02))
            screen.blit(ai_raise_display, (screen_width * 0.3, screen_height * 0.4))

        elif action == "check":
            screen.blit(ai_checked_display, (screen_width * 0.1, screen_height * 0.02))
            screen.blit(ai_check_display, (screen_width * 0.3, screen_height * 0.4))

        elif action ==  "call":
            screen.blit(ai_call_display, (screen_width * 0.3, screen_height * 0.4))

        else:
            screen.blit(ai_fold_display, (screen_width * 0.3, screen_height * 0.4))

        pygame.display.update()


# State where player can increase/decrease raise
def draw_raise_state(raise_amount, player_chips):
    pygame.draw.rect(screen, (210, 210, 210), (0, screen_height - (screen_height * 0.2), screen_width, screen_height * 0.2))
    pygame.draw.rect(screen, (20, 20, 20), (screen_width * 0.004, screen_height - (screen_height * 0.194), screen_width * 0.992, screen_height * 0.139))
    screen.blit(button_confirm_raise, (screen_width * 0.69, screen_height * 0.84))
    screen.blit(button_cancel_raise, (screen_width * 0.231, screen_height * 0.84))
    screen.blit(button_increase_raise, (screen_width * 0.59, screen_height * 0.84))
    screen.blit(button_decrease_raise, (screen_width * 0.331, screen_height * 0.84))
    screen.blit(chip_total, (screen_width * 0.02, screen_height * 0.82))
    player_chips_amount_surface = update_chips_amount(player_chips)
    screen.blit(player_chips_amount_surface, (screen_width * 0.04, screen_height * 0.89))
    raise_amount_surface = update_raise_amount(raise_amount)
    screen.blit(raise_amount_surface, (screen_width * 0.44, screen_height * 0.85))
    pygame.display.update()

# State where player can call bet
def draw_call_state(player_chips, current_bet):
    pygame.draw.rect(screen, (210, 210, 210), (0, screen_height - (screen_height * 0.2), screen_width, screen_height * 0.2))
    pygame.draw.rect(screen, (20, 20, 20), (screen_width * 0.004, screen_height - (screen_height * 0.194), screen_width * 0.992, screen_height * 0.139))

    screen.blit(button_fold, (screen_width * 0.318, screen_height * 0.84))
    screen.blit(button_raise, (screen_width * 0.578, screen_height * 0.84))
    screen.blit(button_call, (screen_width * 0.448, screen_height * 0.82))
    screen.blit(chip_total, (screen_width * 0.02, screen_height * 0.82))
    player_chips_amount_surface = update_chips_amount(player_chips)
    screen.blit(player_chips_amount_surface, (screen_width * 0.04, screen_height * 0.89))

    screen.blit(ai_player_display, (screen_width * 0.02, screen_height * 0.02))
    screen.blit(current_bet_display, (screen_width * 0.8, screen_height * 0.82))
    current_bet_surface = update_chips_amount(current_bet)
    screen.blit(current_bet_surface, (screen_width * 0.845, screen_height * 0.89))
    pygame.display.update()

# State 1 - Community Cards not shown
def drawState1(deck, pot, player_chips, current_bet, ai_current_bet):
    #Background
    screen.blit(GAME_BG, (0, 0)) 

    #UI Bar
    pygame.draw.rect(screen, (210, 210, 210), (0, screen_height - (screen_height * 0.2), screen_width, screen_height * 0.2))
    pygame.draw.rect(screen, (20, 20, 20), (screen_width * 0.004, screen_height - (screen_height * 0.194), screen_width * 0.992, screen_height * 0.139))

    # Player chip display
    screen.blit(chip_total, (screen_width * 0.02, screen_height * 0.82))
    player_chips_amount_surface = update_chips_amount(player_chips)
    screen.blit(player_chips_amount_surface, (screen_width * 0.04, screen_height * 0.89))

    # Betting Buttons
    screen.blit(button_fold, (screen_width * 0.318, screen_height * 0.84))
    screen.blit(button_check, (screen_width * 0.448, screen_height * 0.84))
    screen.blit(button_raise, (screen_width * 0.578, screen_height * 0.84))

    # Home and Settings Buttons
    screen.blit(button_home, (screen_width * 0.93, screen_height * 0.01))
    screen.blit(button_settings, (screen_width * 0.86, screen_height * 0.01))

    # Pot display
    screen.blit(pot_text, (screen_width * 0.785, screen_height * 0.29))
    screen.blit(pot_chips, (screen_width * 0.875, screen_height * 0.315))
    pot_amount_surface = update_pot_amount(pot)
    screen.blit(pot_amount_surface, (screen_width * 0.785, screen_height * 0.38))

    # Current Bet display
    current_bet_surface = update_chips_amount(current_bet)
    screen.blit(current_bet_surface, (screen_width * 0.845, screen_height * 0.89))

    # AI Player display
    screen.blit(ai_player_display, (screen_width * 0.02, screen_height * 0.02))
    screen.blit(current_bet_display, (screen_width * 0.8, screen_height * 0.82))
    ai_current_bet_surface = update_chips_amount(ai_current_bet)
    screen.blit(ai_current_bet_surface, (screen_width * 0.15, screen_height * 0.04))

    # Card Display
    player_hand = deck[0:2]
    ai_hand = [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]
    community_cards = [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]
    draw_cards(player_hand, screen_width * 0.405, screen_height * 0.55)
    draw_cards(ai_hand, screen_width * 0.405, screen_height * 0.04)
    draw_cards(community_cards, screen_width * 0.2625, screen_height * 0.295)

    pygame.display.update()


# State 2 = Three Community Cards Shown
def drawState2(deck, pot, player_chips, current_bet, ai_current_bet):
    #Background
    screen.blit(GAME_BG, (0, 0)) 

    #UI Bar
    pygame.draw.rect(screen, (210, 210, 210), (0, screen_height - (screen_height * 0.2), screen_width, screen_height * 0.2))
    pygame.draw.rect(screen, (20, 20, 20), (screen_width * 0.004, screen_height - (screen_height * 0.194), screen_width * 0.992, screen_height * 0.139))

    # Player chip display
    screen.blit(chip_total, (screen_width * 0.02, screen_height * 0.82))
    player_chips_amount_surface = update_chips_amount(player_chips)
    screen.blit(player_chips_amount_surface, (screen_width * 0.04, screen_height * 0.89))

    # Betting Buttons
    screen.blit(button_fold, (screen_width * 0.318, screen_height * 0.84))
    screen.blit(button_check, (screen_width * 0.448, screen_height * 0.84))
    screen.blit(button_raise, (screen_width * 0.578, screen_height * 0.84))

    # Home and Settings Buttons
    screen.blit(button_home, (screen_width * 0.93, screen_height * 0.01))
    screen.blit(button_settings, (screen_width * 0.86, screen_height * 0.01))

    # Pot display
    screen.blit(pot_text, (screen_width * 0.785, screen_height * 0.29))
    screen.blit(pot_chips, (screen_width * 0.875, screen_height * 0.315))
    pot_amount_surface = update_pot_amount(pot)
    screen.blit(pot_amount_surface, (screen_width * 0.785, screen_height * 0.38))

    # Current Bet display
    current_bet_surface = update_chips_amount(current_bet)
    screen.blit(current_bet_surface, (screen_width * 0.845, screen_height * 0.89))

    # AI Player display
    screen.blit(ai_player_display, (screen_width * 0.02, screen_height * 0.02))
    screen.blit(current_bet_display, (screen_width * 0.8, screen_height * 0.82))
    ai_current_bet_surface = update_chips_amount(ai_current_bet)
    screen.blit(ai_current_bet_surface, (screen_width * 0.15, screen_height * 0.04))

    # Card Display
    player_hand = deck[0:2]
    ai_hand = [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]
    community_cards = deck[4:7] + [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]
    draw_cards(player_hand, screen_width * 0.405, screen_height * 0.55)
    draw_cards(ai_hand, screen_width * 0.405, screen_height * 0.04)
    draw_cards(community_cards, screen_width * 0.2625, screen_height * 0.295)


    pygame.display.update()


# State 3 = Four Community Cards Shown
def drawState3(deck, pot, player_chips, current_bet, ai_current_bet):
    #Background
    screen.blit(GAME_BG, (0, 0)) 

    #UI Bar
    pygame.draw.rect(screen, (210, 210, 210), (0, screen_height - (screen_height * 0.2), screen_width, screen_height * 0.2))
    pygame.draw.rect(screen, (20, 20, 20), (screen_width * 0.004, screen_height - (screen_height * 0.194), screen_width * 0.992, screen_height * 0.139))

    # Player chip display
    screen.blit(chip_total, (screen_width * 0.02, screen_height * 0.82))
    player_chips_amount_surface = update_chips_amount(player_chips)
    screen.blit(player_chips_amount_surface, (screen_width * 0.04, screen_height * 0.89))

    # Betting Buttons
    screen.blit(button_fold, (screen_width * 0.318, screen_height * 0.84))
    screen.blit(button_check, (screen_width * 0.448, screen_height * 0.84))
    screen.blit(button_raise, (screen_width * 0.578, screen_height * 0.84))

    # Home and Settings Buttons
    screen.blit(button_home, (screen_width * 0.93, screen_height * 0.01))
    screen.blit(button_settings, (screen_width * 0.86, screen_height * 0.01))

    # Pot display
    screen.blit(pot_text, (screen_width * 0.785, screen_height * 0.29))
    screen.blit(pot_chips, (screen_width * 0.875, screen_height * 0.315))
    pot_amount_surface = update_pot_amount(pot)
    screen.blit(pot_amount_surface, (screen_width * 0.785, screen_height * 0.38))

    # Current Bet display
    current_bet_surface = update_chips_amount(current_bet)
    screen.blit(current_bet_surface, (screen_width * 0.845, screen_height * 0.89))

    # AI Player display
    screen.blit(ai_player_display, (screen_width * 0.02, screen_height * 0.02))
    screen.blit(current_bet_display, (screen_width * 0.8, screen_height * 0.82))
    ai_current_bet_surface = update_chips_amount(ai_current_bet)
    screen.blit(ai_current_bet_surface, (screen_width * 0.15, screen_height * 0.04))

    # Card Display
    player_hand = deck[0:2]
    ai_hand = [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]
    community_cards = deck[4:8] + [{'suit': 'Back', 'rank': '1'}]
    draw_cards(player_hand, screen_width * 0.405, screen_height * 0.55)
    draw_cards(ai_hand, screen_width * 0.405, screen_height * 0.04)
    draw_cards(community_cards, screen_width * 0.2625, screen_height * 0.295)


    pygame.display.update()


# State 4 = All Community Cards Shown
def drawState4(deck, pot, player_chips, current_bet, ai_current_bet):
    #Background
    screen.blit(GAME_BG, (0, 0)) 

    #UI Bar
    pygame.draw.rect(screen, (210, 210, 210), (0, screen_height - (screen_height * 0.2), screen_width, screen_height * 0.2))
    pygame.draw.rect(screen, (20, 20, 20), (screen_width * 0.004, screen_height - (screen_height * 0.194), screen_width * 0.992, screen_height * 0.139))

    # Player chip display
    screen.blit(chip_total, (screen_width * 0.02, screen_height * 0.82))
    player_chips_amount_surface = update_chips_amount(player_chips)
    screen.blit(player_chips_amount_surface, (screen_width * 0.04, screen_height * 0.89))

    # Betting Buttons
    screen.blit(button_fold, (screen_width * 0.318, screen_height * 0.84))
    screen.blit(button_check, (screen_width * 0.448, screen_height * 0.84))
    screen.blit(button_raise, (screen_width * 0.578, screen_height * 0.84))

    # Home and Settings Buttons
    screen.blit(button_home, (screen_width * 0.93, screen_height * 0.01))
    screen.blit(button_settings, (screen_width * 0.86, screen_height * 0.01))

    # Pot display
    screen.blit(pot_text, (screen_width * 0.785, screen_height * 0.29))
    screen.blit(pot_chips, (screen_width * 0.875, screen_height * 0.315))
    pot_amount_surface = update_pot_amount(pot)
    screen.blit(pot_amount_surface, (screen_width * 0.785, screen_height * 0.38))

    # Current Bet display
    current_bet_surface = update_chips_amount(current_bet)
    screen.blit(current_bet_surface, (screen_width * 0.845, screen_height * 0.89))

    # AI Player display
    screen.blit(ai_player_display, (screen_width * 0.02, screen_height * 0.02))
    screen.blit(current_bet_display, (screen_width * 0.8, screen_height * 0.82))
    ai_current_bet_surface = update_chips_amount(ai_current_bet)
    screen.blit(ai_current_bet_surface, (screen_width * 0.15, screen_height * 0.04))

    # Card Display
    player_hand = deck[0:2]
    ai_hand = [{'suit': 'Back', 'rank': '1'}, {'suit': 'Back', 'rank': '1'}]
    community_cards = deck[4:9]
    draw_cards(player_hand, screen_width * 0.405, screen_height * 0.55)
    draw_cards(ai_hand, screen_width * 0.405, screen_height * 0.04)
    draw_cards(community_cards, screen_width * 0.2625, screen_height * 0.295)


    pygame.display.update()


# State 5 = Reveal Winner
def drawState5(deck, pot):
    screen.blit(GAME_BG, (0, 0))

    player_hand = deck[0:2]
    ai_hand = deck[2:4]
    community_cards = deck[4:9]

    screen.blit(pot_text, (screen_width * 0.785, screen_height * 0.29))
    screen.blit(pot_chips, (screen_width * 0.875, screen_height * 0.315))
    pot_amount_surface = update_pot_amount(pot)
    screen.blit(pot_amount_surface, (screen_width * 0.785, screen_height * 0.33))

    draw_cards(player_hand, screen_width * 0.405, screen_height * 0.55)
    draw_cards(ai_hand, screen_width * 0.405, screen_height * 0.04)
    draw_cards(community_cards, screen_width * 0.2625, screen_height * 0.295)


    pygame.display.update()



def drawState6(winner):
    if winner == "AI Wins":
        screen.blit(ai_win_display, (300, 200))


    else:
        screen.blit(player_win_display, (250, 300))


    pygame.display.update()

    time.sleep(3)
    screen.blit(GAME_BG, (0, 0))
    screen.blit(button_play_again, (center_x(screen_width, screen_width * 0.35), center_y(screen_height, screen_height * 0.25)))
    pygame.display.update()




#### ----------------------------------------------------------------------------------------------------------------- ###



def main():
    run = True
    game_state = 0
    fresh_hand = True
    settings_return_state = game_state

    title_state, call_state, settings_state, state1, state2, state3, state4, state5, state6, player_raise_state = False, False, False, False, False, False, False, False, False, False
    play_title_music = True
    # Purpose of the above variables is so we only draw each game game_state once, as it is unneccesary for the states to be infinitely drawn while waiting for player action.
    
    player_blind_status = 1 #random.randint(0, 1) # Initial random allocation of Big and Little Blind. 0 indicates a player is Big Blind.

    big_blind, little_blind = 200, 100. # Big and little blind increase by 200 and 100 respectively, after every hand.
    ai_bot = Bot()
    player = Player()

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
                    elif button_check_rect.collidepoint(event.pos) and 0 < game_state < 5 and player_raise_state == False and waiting_for_player_input == True and call_state == False: # Check button
                        click_sound_game_action.play()
                        player_action = ["check"]
                        waiting_for_player_input = False


                    elif button_raise_rect.collidepoint(event.pos) and 0 < game_state < 5 and player_raise_state == False and waiting_for_player_input == True: # Raise button
                        click_sound_game_action.play()
                        player_raise_state = True
                        temp_raise_amount = current_bet + 100
                        draw_raise_state(temp_raise_amount, player.chips)


                    elif button_fold_rect.collidepoint(event.pos) and 0 < game_state < 5 and player_raise_state == False and waiting_for_player_input == True: # Fold button
                        click_sound_game_action.play()
                        player_action = ["fold"]
                        waiting_for_player_input = False

                    elif button_call_rect.collidepoint(event.pos) and 0 < game_state < 5 and player_raise_state == False and waiting_for_player_input == True and call_state == True: # Call button
                        click_sound_game_action.play()
                        player_action = ["call"]
                        waiting_for_player_input = False


                    # Raise Buttons
                    elif button_increase_raise_rect.collidepoint(event.pos) and 0 < game_state < 5 and player_raise_state == True: # Increase Raise button
                        click_sound_game_action.play()
                        if temp_raise_amount < player.chips:
                            temp_raise_amount += 100
                        draw_raise_state(temp_raise_amount, player.chips)

                    elif button_decrease_raise_rect.collidepoint(event.pos) and 0 < game_state < 5 and player_raise_state == True: # Decrease Raise button
                        click_sound_game_action.play()
                        if temp_raise_amount > current_bet + 100:
                            temp_raise_amount -= 100
                        draw_raise_state(temp_raise_amount, player.chips)

                    elif button_cancel_raise_rect.collidepoint(event.pos) and 0 < game_state < 5 and player_raise_state == True: # Cancel Raise button
                        click_sound_game_action.play()
                        player_raise_state, state1, state2, state3, state4 = False, False, False, False, False
                        temp_raise_amount = raise_amount

                    elif button_confirm_raise_rect.collidepoint(event.pos) and 0 < game_state < 5 and player_raise_state == True: # Confirm Raise button
                        click_sound_game_action.play()
                        player_raise_state, state1, state2, state3, state4 = False, False, False, False, False
                        raise_amount = temp_raise_amount
                        current_bet = raise_amount
                        player_action = ["raise", int(raise_amount)]
                        waiting_for_player_input = False


                    # Misc Buttons
                    elif button_home_rect.collidepoint(event.pos) and 0 < game_state < 5: # Home button
                        click_sound_main.play()
                        call_state, settings_state, state1, state2, state3, state4, state5, state6, player_raise_state = False, False, False, False, False, False, False, False, False
                        game_state = 0
                        fresh_hand = True
                        play_title_music = True

                    elif button_settings_rect.collidepoint(event.pos) and 0 < game_state < 5:  # Settings Button
                        click_sound_main.play()
                        settings_return_state = game_state
                        game_state = 7    



                elif event.button == 2:  # Middle mouse button

                    if button_increase_raise_rect.collidepoint(event.pos) and 0 < game_state < 5 and player_raise_state == True: # Increase Raise button
                        click_sound_game_action.play()
                        if temp_raise_amount != player.chips:
                            temp_raise_amount = player.chips
                        draw_raise_state(temp_raise_amount, player.chips)

                    elif button_decrease_raise_rect.collidepoint(event.pos) and 0 < game_state < 5 and player_raise_state == True: # Decrease Raise button
                        click_sound_game_action.play()
                        if temp_raise_amount != current_bet + 100:
                            temp_raise_amount = raise_amount
                        draw_raise_state(temp_raise_amount, player.chips)



                elif event.button == 3:  # Right mouse button

                    if button_increase_raise_rect.collidepoint(event.pos) and 0 < game_state < 5 and player_raise_state == True: # Increase Raise button
                        click_sound_game_action.play()
                        if temp_raise_amount < player.chips:
                            if temp_raise_amount + 1000 <= player.chips:
                                temp_raise_amount += 1000
                            else:
                                temp_raise_amount = player.chips
                        draw_raise_state(temp_raise_amount, player.chips)

                    elif button_decrease_raise_rect.collidepoint(event.pos) and 0 < game_state < 5 and player_raise_state == True: # Decrease Raise button
                        click_sound_game_action.play()
                        if temp_raise_amount > current_bet + 100:
                            if temp_raise_amount - 1000 < current_bet + 100:
                                temp_raise_amount = current_bet + 100
                            else:
                                temp_raise_amount -= 1000
                        draw_raise_state(temp_raise_amount, player.chips)



                    
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN and game_state == 6 and waiting_for_enter:
                    click_sound_play_again.play()
                    print("\n -------- New Hand -------- \n")
                    game_state = 1
                    state6 = False
                    fresh_hand = True
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

            if fresh_hand:
                pot = 0
                raise_amount = 0
                player_action = None
                first_call = True
                pot += (big_blind + little_blind) # Add the blinds to the pot
                raise_amount = big_blind + 100
                fresh_hand = False

                deck = shuffle_deck() # Shuffle a deck of cards.
                # We can already determine if the AI or player will win based on the cards that were dealt. If no one folds, we will use this to determine the winner.
                winner = determine_winner(deck[0:2], deck[2:4], deck[4:9])
                print(deck[0:2])

                if player_blind_status == 1:
                    waiting_for_player_input = True
                    current_bet = big_blind - little_blind
                    ai_current_bet = big_blind
                    player.chips -= little_blind
                    little_blind_call = True
                else:
                    waiting_for_player_input = False
                    ai_current_bet = big_blind - little_blind
                    current_bet = big_blind
                    player.chips -= big_blind
                    little_blind_call = False

            if not state1:
                drawState1(deck, pot, player.chips, current_bet, ai_current_bet)
                state1 = True
                
                if play_title_music == True:
                    pygame.mixer.music.load(music_menu)
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)  # -1 loops the music indefinitely

                  
            # Player is Small Blind and bets first. 
            if player_blind_status == 1:

                if little_blind_call == True:
                    call_state = True
                    draw_call_state(player.chips, current_bet)
                    little_blind_call = False
                
                if player_action != None:
                    time.sleep(0.5)
                    p_action = player_action
                    player_action = None

                    if p_action[0] == "call" and first_call: # Player calls big blind amount.
                        player.chips -= (big_blind - little_blind)
                        first_call = False
                        current_bet = big_blind
                        pot += (big_blind - little_blind)
                        ai_action = ai(ai_bot, game_state, deck[2:4], [False], little_blind)
                        draw_ai_action(ai_action[0])
                        time.sleep(2)

                        if ai_action[0] == "check": # Ai Checks following player call
                            game_state += 1
                            call_state = False
                        
                        elif ai_action[0] == "raise": # AI raises following player calling big blind.
                            ai_current_bet = ai_action[1]
                            raise_amount = ai_current_bet
                            drawState1(deck, pot, player.chips, current_bet, ai_current_bet)
                            draw_call_state(player.chips, current_bet)
                            waiting_for_player_input = True 
  
                        else: # AI folded
                            game_state = 6
                            winner = "Player Wins"
                            player.chips += pot

                    # AI can only raise following a big blind call, not other calls
                    elif p_action[0] == "call" and not first_call: 
                        player.chips -= ai_current_bet
                        call_state = False
                        pot = ai_current_bet * 2
                        current_bet = ai_current_bet
                        game_state += 1

                    #Player Raises
                    elif p_action[0] == "raise":
                        first_call = False
                        current_bet = raise_amount
                        drawState1(deck, pot, player.chips, current_bet, ai_current_bet)
                        ai_action = ai(ai_bot, game_state, deck[2:4], [True, raise_amount], little_blind)
                        draw_ai_action(ai_action[0])
                        time.sleep(2)

                        if ai_action[0] == "call": # Ai Calls following player raise
                            player.chips -= raise_amount - little_blind
                            ai_current_bet = raise_amount
                            call_state = False
                            pot = raise_amount * 2
                            game_state += 1
                        
                        elif ai_action[0] == "raise": # AI re-raises
                            ai_current_bet = ai_action[1]
                            raise_amount = ai_current_bet
                            drawState1(deck, pot, player.chips, current_bet, ai_current_bet)
                            draw_call_state(player.chips, current_bet)
                            waiting_for_player_input = True 
  
                        else: # AI folded
                            game_state = 6
                            winner = "Player Wins"
                            player.chips += pot


                    elif p_action[0] == "fold":
                        game_state = 6
                        winner = "AI Wins"




                        





            


            #Player is Big Blind and bets second.
            else:
                pass
                    

                


        # Reveal 3 of the Community Cards
        if game_state == 2:
            if not state2:
                drawState2(deck, pot, player.chips, current_bet, ai_current_bet)
                state1, state2 = False, True

        # Reveal fourth community card
        if game_state == 3:
            if not state3:
                drawState3(deck, pot, player.chips, current_bet, ai_current_bet)
                state2, state3 = False, True

        # Reveal the 5th and final community card.
        if game_state == 4:
            if not state4:
                drawState4(deck, pot, player.chips, current_bet, ai_current_bet)
                state3, state4 = False, True

        # Reveal AI cards to show winner!
        if game_state == 5:
            if not state5:
                drawState5(deck, pot)
                state4, state5 = False, True
                print("\n", winner)

            time.sleep(3)# Wait before displaying winner
            game_state = 6

        if game_state == 6:
            if not state6:
                state6, state5, state4, state3, state2, state1 = True, False, False, False, False, False
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