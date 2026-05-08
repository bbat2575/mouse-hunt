'''
Interface Class
'''

import hunter
import cshop
import trap

class Interface:
    def __init__(self):
        self.menu = {1: "Exit game", 2: "Join the Hunt", 3: "The Cheese Shop", 4: "Change Cheese"}
        self.player = hunter.Hunter()

    def set_player(self, player: hunter.Hunter()):
        if type(player) == Hunter:
            self.player = player

    def get_menu(self) -> str:
        keys = list(self.menu.keys())
        return f'{keys[0]}. {self.menu[1]}\n{keys[1]}. {self.menu[2]}\n{keys[2]}. {self.menu[3]}\n{keys[2]}. {self.menu[4]}'

    def change_cheese(self):
        # Declare variables
        trap_cheese = None

        while True:
            trap_cheese = None

            print(f"Hunter {self.player.get_name()}, you currently have:")
            print(self.player.get_cheese()+'\n')

            trap_cheese = input("State [cheese name] to arm trap or type 'back' to exit: ").lower().strip().capitalize()

            if trap_cheese == "Back":
                self.player.trap.set_trap_cheese(None)
                break
            # If cheese unknown
            elif trap_cheese != self.player.cheese[0][0] and trap_cheese != self.player.cheese[1][0] and trap_cheese != self.player.cheese[2][0]:
                print("No such cheese!\n")
            # If out of cheese
            elif (trap_cheese == self.player.cheese[0][0] and self.player.cheese[0][1] == 0) or (trap_cheese == self.player.cheese[1][0] and self.player.cheese[1][1] == 0) or (trap_cheese == self.player.cheese[2][0] and self.player.cheese[2][1] == 0):
                print("Out of cheese!\n")
            else:
                # If trap is enchanted display the benefit to the user
                if self.player.trap.one_time_enchantment:
                    print(f"Your {self.player.trap.get_trap_name()} has a one-time enchantment granting {trap.Trap.get_benefit(trap_cheese)}.")

                arm_trap = input(f"Do you want to arm your trap with {trap_cheese}? ").lower().strip()

                if arm_trap == "back":
                    self.player.trap.set_trap_cheese(None)
                    break
                elif arm_trap == "yes":
                    self.player.trap.set_arm_status()
                    self.player.set_trap_cheese(trap_cheese)
                    print(f"{trap} is now armed with {trap_cheese}!")
                print()
        
    def cheese_shop(self):
        cs = cshop.CheeseShop()
        cs.move_to(self.player)

    def hunt(self):
        pass

    def move_to(self, choice: int):
        pass

