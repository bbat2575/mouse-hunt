'''
Mouse Generator
'''

import random
import art

TYPE_OF_MOUSE = (None, "Brown", "Field", "Grey", "White", "Tiny")

def generate_mouse(cheese = "Cheddar", enchant = False) -> str | None:
    # Generate a tuple of probabilities based on cheese type and if trap is enchanted
    probs = generate_probabilities(cheese, enchant)

    # Generate a random number between 0 and 1
    rand = random.random()
    
    # Generate/Catch a mouse based on probabilities stored in variable total
    total = probs[0]
    i = 0
    
    while i < len(probs):
        # if random number is within range of total for last iteration minus total for this iteration
        if rand < total:
            return TYPE_OF_MOUSE[i]
        else:
            # total = the accumulation of probabilities of catching each mouse
            total += probs[i+1]

        i += 1

# Returns the probabilites of catching a mouse based on cheese type and if trap is enchanted
def generate_probabilities(cheese_type = "Cheddar", enchant = False) -> tuple:
    if cheese_type == "Cheddar":
        return 0.5, 0.1, 0.15, 0.1, 0.1, 0.05
    elif cheese_type == "Marble":
        return 0.6, 0.05, 0.2, 0.05, 0.02, 0.08
    elif cheese_type == "Swiss" and enchant == False:
        return 0.7, 0.01, 0.05, 0.05, 0.04, 0.15
    elif cheese_type == "Swiss" and enchant == True:
        return 0.45, 0.01, 0.05, 0.05, 0.04, 0.4

# Returns the amount of gold and points a type of mouse rewards
def loot_lut(mouse_type: str | None) -> tuple:
    if mouse_type == TYPE_OF_MOUSE[0]:
        return 0, 0
    elif mouse_type == TYPE_OF_MOUSE[1]:
        return 125, 115
    elif mouse_type == TYPE_OF_MOUSE[2]:
        return 200, 200
    elif mouse_type == TYPE_OF_MOUSE[3]:
        return 125, 90
    elif mouse_type == TYPE_OF_MOUSE[4]:
        return 100, 70
    elif mouse_type == TYPE_OF_MOUSE[5]:
        return 900, 200

# Text art representing each mouse type
def generate_coat(mouse_type: str) -> str:
    if mouse_type == "Brown":
        return art.BROWN
    elif mouse_type == "Field":
        return art.FIELD
    elif mouse_type == "Grey":
        return art.GREY
    elif mouse_type == "White":
        return art.WHITE
    elif mouse_type == "Tiny":
        return art.TINY


class Mouse:
    def __init__(self, cheese = "Cheddar", enchant = False):
        self.name = generate_mouse(cheese, enchant)
        self.gold, self.points = loot_lut(self.name)
        self.coat = generate_coat(self.name)

    def get_name(self) -> str:
        return self.name

    def get_gold(self) -> int:
        return self.gold
    
    def get_points(self) -> int:
        return self.points
    
    def __str__(self) -> str:
        return str(self.name)

