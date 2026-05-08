'''
Mini Mousehunt Game (Incomplete Version)
'''

import random
import title
import name
import train
import trains
import shop

# you can make more functions or global read-only variables here if you please!

def get_game_menu():
    return "1. Exit game\n2. Join the Hunt\n3. The Cheese Shop\n4. Change Cheese"

def cheese_shop(gold: int, cheese: list, trap: str):
    # Greeting message
    print("Welcome to The Cheese Shop!")
    print("Cheddar - 10 gold")
    print("Marble - 50 gold")
    print("Swiss - 100 gold")

    choice = 0

    while choice != 3:
        # Cheese shop menu
        print("\nHow can I help ye?")
        print("1. Buy cheese")
        print("2. View inventory")
        print("3. Leave shop")
        choice = input()

        # Typecast done only if isdigit() is True. This prevents strings from crashing the program
        if choice.isdigit():
            choice = int(choice)

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
def change_cheese(hunter_name: str, trap: str, cheese: list, e_flag: bool = False) -> tuple:
    # Declare variables
    trap_status = False
    trap_cheese = None
    
    while True:
        trap_cheese = None

        print(f"Hunter {hunter_name}, you currently have:")
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
            arm_trap = input(f"Do you want to arm your trap with {trap_cheese}? ").lower().strip()
            if arm_trap == "back":
                return False, None
            elif arm_trap == "yes":
                trap_status = True
                print(f"{trap} is now armed with {trap_cheese}!")
                return trap_status, trap_cheese
            else:
                print()

# Consume one cheese from the amount of the cheese type parsed to this function
def consume_cheese(to_eat: str, cheese: list) -> None:
    # No need for return statement - cheese is a list (mutable/passed by reference) and so modified in local scope
    # If to_eat == Cheddar
    if to_eat == cheese[0][0] and cheese[0][1] > 0:
        cheese[0][1] -= 1
    # If to_eat == Marble
    elif to_eat == cheese[1][0] and cheese[1][1] > 0:
        cheese[1][1] -= 1
    # If to_eat == Swiss
    elif to_eat == cheese[2][0] and cheese[2][1] > 0:
        cheese[2][1] -= 1


def hunt(gold: int, cheese: list, trap_cheese: str | None, points: int) -> tuple:
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
            horn_input = trains.sound_horn()
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
                counter += 1
            # Time to hunt!
            elif horn_input == "yes":
                # Unsuccessful hunt
                if random.random() > 0.5:
                    print("Nothing happens.")
                    consume_cheese(trap_cheese, cheese) # Update cheese
                    cheese_count -= 1
                    # Display total
                    print(f"My gold: {gold}, My points: {points}\n")
                    counter += 1
                # Successful hunt
                else:
                    print("Caught a Brown mouse!")
                    consume_cheese(trap_cheese, cheese) # Update cheese
                    cheese_count -= 1
                    points += 115
                    gold += 125
                    # Display total
                    print(f"My gold: {gold}, My points: {points}\n")
                 
        if again != "no":
            again = input("Do you want to continue to hunt? ").lower()

    return gold, points


def main():
    # Declare variables
    cheese = [["Cheddar", 0], ["Marble", 0], ["Swiss", 0]]
    gold = 125
    points = 0
    trap = "Cardboard and Hook Trap"
    option = 0
    trap_status = False
    trap_cheese = None

    # Display game title
    title.main()
    username = input("What's ye name, Hunter?\n")
    if not name.is_valid_name(username):
        username = "Bob"
    
    print(f"Welcome to the Kingdom, Hunter {username}!")  
    print("Before we begin, let's train you up!")
    user = input('Press "Enter" to start training or "skip" to Start Game: ').lower()

    if user != "skip":
        print()
        trap = train.training()[0]

    # Game loop
    while option != 1:      
        print(f"\nWhat do ye want to do now, Hunter {username}?")
        # Game menu
        print(get_game_menu())
        option = input()
    
        # Typecast done only if isdigit() is True. This prevents strings from crashing the program
        if option.isdigit():
            option = int(option)

        # Join the Hunt
        if option == 2:
            gold, points = hunt(gold, cheese, trap_cheese, points)
            # Disarm the trap if run out of cheese
            if trap_cheese == cheese[0][0] and cheese[0][1] == 0:
                trap_cheese = None
            elif trap_cheese == cheese[1][0] and cheese[1][1] == 0:
                trap_cheese = None
            elif trap_cheese == cheese[2][0] and cheese[2][1] == 0:
                trap_cheese = None        
        # The Cheese Shop
        elif option == 3:
            gold, cheese[0][1], cheese[1][1], cheese[2][1] = cheese_shop(gold, cheese, trap)
        elif option == 4:
            # Note: trap_status not used yet
            trap_status, trap_cheese = change_cheese(username, trap, cheese)


if __name__ == '__main__':
    main()
