'''
Mousehunt (The Full Game)
'''

import setup
import title
import time
from datetime import datetime
import os
import name
import shop
import train
import mouse

def get_game_menu():
    return "1. Exit game\n2. Join the Hunt\n3. The Cheese Shop\n4. Change Cheese"

# Initial game setup to verify files whether or not files are tampered with
def run_setup():
    tamper_flag = False

    # Get current date and time
    timestamp = datetime.fromtimestamp(time.time()).strftime("%d %b %Y %H:%M:%S")

    # Run verification and assign output to verify
    cwd = os.getcwd() + "/"
    verify = setup.verification(cwd, timestamp)

    # Check the last line of the verification to see if abnormalities are detected    
    if verify[-1] == "Abnormalities detected...":
        user = input("Do you want to repair the game? ").lower()

        # If yes, reinstall
        if user == "yes":
            setup.installation("/home/game_master/", timestamp)
        # If anything else, warn the player
        else:
            print("Game may malfunction and personalization will be locked.")
            user = input("Are you sure you want to proceed? ").lower()
            
            # If player refuses to repair the game warn them and proceed
            if user == "yes":
                print("You have been warned!!!")
                tamper_flag = True
            else:
                exit(0)
        
    print("Launching game...")

    return tamper_flag


def personalization(tamper_flag: bool):
    if tamper_flag == True:
        return "Bob"

    user = input("What's ye name, Hunter? ")
    
    # If name is not valid, offer the user 3 attempts to input a valid name
    if not name.is_valid_name(user):
        print("That's not nice!")
        print("I'll give ye 3 attempts to get it right or I'll name ye!")
        print("Let's try again...")
    else:
        return user
    
    i = 1
    while i <= 3:
        user = input("What's ye name, Hunter? ")

        # If user fails 1 or 2 attempts
        if not name.is_valid_name(user):
            print(f"Nice try. Strike {i}!")
            # If user fails 3 attempts generate a name for them
            if i == 3:
                print(f"I told ye to be nice!!!")
                return name.generate_name(user)
        else:
            return user
        
        i += 1

# Returns the benefits of each cheese if trap is enchanted
def get_benefit(cheese: str) -> str:
    if cheese == "Cheddar":
        return "+25 points drop by next Brown mouse"
    elif cheese == "Marble":
        return "+25 gold drop by next Brown mouse"
    elif cheese == "Swiss":
        return "+0.25 attraction to Tiny mouse"


def hunt(gold: int, cheese: list, trap_cheese: str | None, points: int, enchant: bool) -> tuple:
    again = ""

    # Get the amount of cheese available for the trap_cheese and assign it to cheese_count
    if trap_cheese == cheese[0][0]:
        cheese_count = cheese[0][1]
    elif trap_cheese == cheese[1][0]:
        cheese_count = cheese[1][1]
    elif trap_cheese == cheese[2][0]:
        cheese_count = cheese[2][1]
    else:
        cheese_count = 0

    while again != "no":  
        counter = 0

        while counter < 5:
            print("Sound the horn to call for the mouse...")
            horn_input = input('Sound the horn by typing "yes" or type "stop hunt" to exit: ').lower().strip()
            
            if horn_input == "stop hunt":
                again = "no"
                break
            # Invalid command
            elif horn_input != "yes":
                print("Do nothing.")
                # Display total
                print(f"My gold: {gold}, My points: {points}\n")
                counter += 1
            # No cheese
            elif cheese_count < 1:
                print("Nothing happens. You are out of cheese!")
                # Display total
                print(f"My gold: {gold}, My points: {points}\n")
                # Use enchantment
                if enchant == True:
                    enchant = False
                counter += 1
            # Time to hunt!
            elif horn_input == "yes":
                new_mouse = mouse.Mouse(trap_cheese, enchant)
                # Unsuccessful hunt
                if new_mouse.name == None:
                    print("Nothing happens.")
                    consume_cheese(trap_cheese, cheese) # Update cheese
                    cheese_count -= 1
                    # Display total
                    print(f"My gold: {gold}, My points: {points}\n")
                    counter += 1
                    # Use up enchantment
                    if enchant == True:
                        enchant = False
                # Successful hunt
                else:
                    print(f"Caught a {new_mouse.name} mouse!")
                    print(new_mouse.coat)
                    consume_cheese(trap_cheese, cheese) # Update cheese
                    cheese_count -= 1
                    # If trap enchanted and caught a Brown mouse, apply benefit of +25 points
                    if enchant == True and new_mouse.name == "Brown":
                        points += new_mouse.points + 25
                    else:
                        points += new_mouse.points
                    gold += new_mouse.gold
                    # Display total
                    print(f"My gold: {gold}, My points: {points}\n")
                    # Use up enchantment
                    if enchant == True:
                        enchant = False
                 
        if again != "no":
            again = input("Do you want to continue to hunt? ").lower()

    return gold, points, enchant

def cheese_shop(gold: int, cheese: list, trap: str):
    # Greeting message
    print("\nWelcome to The Cheese Shop!")
    print("Cheddar - 10 gold")
    print("Marble - 50 gold")
    print("Swiss - 100 gold")

    choice = 0

    # Cheese shop menu
    while choice != 3:
        print("\nHow can I help ye?")
        print("1. Buy cheese")
        print("2. View inventory")
        print("3. Leave shop")
        choice = input()

        # Typecast done only if isdigit() is True. This prevents strings from crashing the program
        if choice.isdigit():
            choice = int(choice)
            # Check that number entered is within range
            if choice < 1 or choice > 3:
                print("I did not understand.")
        # If user input is not a number
        else:
            print("I did not understand.")

        # Buy cheese
        if choice == 1:
            diff = shop.buy_cheese(gold)
            gold -= diff[0]
            cheese[0][1] += diff[1][0]
            cheese[1][1] += diff[1][1]
            cheese[2][1] += diff[1][2]
        # View inventory
        elif choice == 2:
            shop.display_inventory(gold, cheese, trap)
    
    return gold, cheese[0][1], cheese[1][1], cheese[2][1]

# Allows the player to arms their trap with different cheeses
def change_cheese(hunter_name: str, trap: str, cheese: list, enchant: bool = False) -> tuple:
    # Declare variables
    trap_status = False
    trap_cheese = None
    
    while True:
        trap_cheese = None

        print(f"\nHunter {hunter_name}, you currently have:")
        print(f"{cheese[0][0]} - {cheese[0][1]}")
        print(f"{cheese[1][0]} - {cheese[1][1]}")
        print(f"{cheese[2][0]} - {cheese[2][1]}\n")

        trap_cheese = input("State [cheese name] to arm trap or type 'back' to exit: ").lower().strip().capitalize()

        if trap_cheese == "Back":
            return False, None
        # If cheese unknown
        elif trap_cheese != cheese[0][0] and trap_cheese != cheese[1][0] and trap_cheese != cheese[2][0]:
            print("No such cheese!\n")
        # If out of cheese
        elif (trap_cheese == cheese[0][0] and cheese[0][1] == 0) or (trap_cheese == cheese[1][0] and cheese[1][1] == 0) or (trap_cheese == cheese[2][0] and cheese[2][1] == 0):
            print("Out of cheese!\n")
        else:
            # If trap is enchanted display the benefit to the user
            if trap.find("One-time Enchanted") != -1:
                print(f"Your {trap} has a one-time enchantment granting {get_benefit(trap_cheese)}.")

            arm_trap = input(f"Do you want to arm your trap with {trap_cheese}? ").lower().strip()

            if arm_trap == "back":
                return False, None
            elif arm_trap == "yes":
                trap_status = True
                print(f"{trap} is now armed with {trap_cheese}!")
                return trap_status, trap_cheese

# Consume one cheese from the amount of the cheese type parsed to this function
def consume_cheese(to_eat: str, my_cheese: list) -> None:
    # No need for return statement - cheese is a list (mutable/passed by reference) and so modified in local scope
    # If to_eat == Cheddar
    if to_eat == my_cheese[0][0] and my_cheese[0][1] > 0:
        my_cheese[0][1] -= 1
    # If to_eat == Marble
    elif to_eat == my_cheese[1][0] and my_cheese[1][1] > 0:
        my_cheese[1][1] -= 1
    # If to_eat == Swiss
    elif to_eat == my_cheese[2][0] and my_cheese[2][1] > 0:
        my_cheese[2][1] -= 1


def main():
    # Declare variables
    cheese = [["Cheddar", 0], ["Marble", 0], ["Swiss", 0]]
    gold = 125
    points = 0
    trap = "Cardboard and Hook Trap"
    option = 0
    trap_status = False
    trap_cheese = None
    enchant = False
    
    # Run setup to check validate files
    tamper_flag = run_setup()
    # tamper_flag = 0
    print(".\n.\n.")

    # Title screen
    title.main()

    # Get username
    username = personalization(tamper_flag)

    print(f"Welcome to the Kingdom, Hunter {username}!")
    print("Before we begin, let's train you up!")
    # Ask user if they would like to train
    user = input('Press "Enter" to start training or "skip" to Start Game: ').lower()

    if user != "skip":
        print()
        trap = train.training()[0]

    if trap != "Cardboard and Hook Trap":
        enchant = True
        trap = f"One-time Enchanted {trap}"
    
    # Game loop
    while option != 1:      
        print(f"\nWhat do ye want to do now, Hunter {username}?")
        # Game Menu
        print(get_game_menu())

        while True:
            option = input("Enter a number between 1 and 4: ")
    
            # Typecast done only if isdigit() is True. This prevents strings from crashing the program
            if option.isdigit():
                option = int(option)
                # Check that number entered is within range
                if option < 1 or option > 4:
                    print("Must be between 1 and 4.")
                else:
                    break
            # If user input is not a number
            else:
                print("Invalid input.")

        # Join the Hunt
        if option == 2:
            gold, points, enchant = hunt(gold, cheese, trap_cheese, points, enchant)
            # Disarm the trap if run out of cheese
            if trap_cheese == cheese[0][0] and cheese[0][1] == 0:
                trap_cheese = None
            elif trap_cheese == cheese[1][0] and cheese[1][1] == 0:
                trap_cheese = None
            elif trap_cheese == cheese[2][0] and cheese[2][1] == 0:
                trap_cheese = None

            # Amend trap name if no longer enchanted (if one hunt has been carried out)
            if enchant == False and trap.find("One-time Enchanted") != -1:
                trap = trap.replace("One-time Enchanted ", "")

        # The Cheese Shop
        elif option == 3:
            gold, cheese[0][1], cheese[1][1], cheese[2][1] = cheese_shop(gold, cheese, trap)
        elif option == 4:
            # Note: trap_status not used yet
            trap_status, trap_cheese = change_cheese(username, trap, cheese)


if __name__ == '__main__':
    main()
