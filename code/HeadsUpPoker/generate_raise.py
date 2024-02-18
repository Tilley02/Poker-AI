import numpy as np

def generate_raise(min_bet, max_bet, shape):
    rand_exp_better_pocket = np.random.exponential(scale=shape) # Generate a random number
    scaled_value_better_pocket = min_bet * 2 + (max_bet - min_bet * 2) * (1 - np.exp(-rand_exp_better_pocket)) # Scale the random number to fit within the desired range
    raise_amount = min(max_bet, max(min_bet * 2, int(scaled_value_better_pocket))) # Ensure that the scaled value is within the desired range
    raise_amount = round(raise_amount / 100) * 100 #Scale up by 100
    return raise_amount