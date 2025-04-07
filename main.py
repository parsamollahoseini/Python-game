import random
import os
import platform
from hero import Hero
from monster import Monster
from function import clear_screen, dream_levels, sword_art, good_ending, use_loot, collect_loot, inception_dream, save_game, load_game, adjust_combat_strength, describe_weather
from weather import WeatherSystem
from function import clear_screen, dream_levels, sword_art, good_ending, use_loot, collect_loot, inception_dream, save_game, load_game, adjust_combat_strength, get_available_pets
# Import check_crafting and remove use_loot if no longer needed elsewhere (keeping it for now)
from function import clear_screen, dream_levels, sword_art, good_ending, use_loot, collect_loot, inception_dream, save_game, load_game, adjust_combat_strength, check_crafting

# Print OS and Python version information
print(f"Operating System: {os.name}")
print(f"Python Version: {platform.python_version()}")

# Global variables
monsters_killed = 0
weather_system = WeatherSystem()

# Define the Weapons
weapons = ["Fist", "Knife", "Club", "Gun", "Bomb", "Nuclear Bomb"]

# Define the Loot - separated regular loot from weather gear
loot_options = ["Health Potion", "Poison Potion", "Secret Note", "Leather Boots", "Flimsy Gloves"]
weather_gear = ["Raincoat", "Sunglasses", "Heat Cloak", "Wind Barrier", "Weather Orb"]
belt = []

# Define the Monster's Powers
monster_powers = {
    "Fire Magic": 2,
    "Freeze Time": 4,
    "Super Hearing": 6
}

# Function to collect weather gear
def collect_weather_gear(weather_gear_options):
    ascii_image_weather = """
             .-.
          .-(    ).
         (___.__)__)
           /  |  \\
          /  /|\\  \\
         '-------'
          """
    print(ascii_image_weather)
    gear_roll = random.randint(0, len(weather_gear_options)-1)
    gear = weather_gear_options[gear_roll]
    print(f"    |    You found: {gear}")
    return gear

def main():
    global monsters_killed
    global weather_system

    # Load a saved game if available
    _, num_stars, loaded_monsters_killed = load_game()
    monsters_killed = loaded_monsters_killed
    print(f"Starting game with {monsters_killed} monsters previously killed.")

    # Loop to get valid input for Hero and Monster's Combat Strength
    i = 0
    input_invalid = True

    while input_invalid and i in range(5):
        print("    ------------------------------------------------------------------")
        print("    |", end="    ")
        try:
            combat_strength = input("Enter your combat Strength (1-6): ")
            print("    |", end="    ")
            m_combat_strength = input("Enter the monster's combat Strength (1-6): ")

            # Validate input by converting to integers (will raise ValueError if not numeric)
            combat_strength_int = int(combat_strength)
            m_combat_strength_int = int(m_combat_strength)

            # Check range
            if (combat_strength_int not in range(1, 7)) or (m_combat_strength_int not in range(1, 7)):
                print("    |    Enter a valid integer between 1 and 6 only")
                i = i + 1
                continue
            else:
                input_invalid = False
                combat_strength = combat_strength_int
                m_combat_strength = m_combat_strength_int
                break
        except ValueError:
            print("    |    One or more invalid inputs. Player needs to enter integer numbers for Combat Strength    |")
            i = i + 1
            continue

    if not input_invalid:
        # Create hero and monster objects
        hero = Hero(combat_strength)
        monster = Monster(m_combat_strength)

        # Check the weather and apply effects
        print("    ------------------------------------------------------------------")
        print("    |", end="    ")
        input("Check the weather forecast (Press enter)")
        describe_weather(weather_system)

        # Apply weather effects to both characters
        hero_combat_mod, hero_health_mod = weather_system.apply_weather_effects(hero, "hero")
        monster_combat_mod, monster_health_mod = weather_system.apply_weather_effects(monster, "monster")

        print(f"    |    Weather affects your combat strength by {hero_combat_mod} and health by {hero_health_mod}")
        print(f"    |    Your combat strength is now {hero.combat_strength} and health is {hero.health_points}")
        print(f"    |    Weather affects the monster's combat strength by {monster_combat_mod} and health by {monster_health_mod}")
        print(f"    |    Monster's combat strength is now {monster.combat_strength} and health is {monster.health_points}")

        # Roll for weapon
        print("    |", end="    ")
        input("Roll the dice for your weapon (Press enter)")
        ascii_image5 = """
                , %               .           
       *      @./  #         @  &.(         
      @        /@   (      ,    @       # @ 
      @        ..@#% @     @&*#@(         % 
       &   (  @    (   / /   *    @  .   /  
         @ % #         /   .       @ ( @    
                     %   .@*                
                   #         .              
                 /     # @   *              
                     ,     %                
                @&@           @&@
                """
        print(ascii_image5)
        weapon_roll = random.randint(1, 6)

        # Limit the combat strength to 6
        hero.combat_strength = min(6, (hero.combat_strength + weapon_roll))
        print("    |    The hero\'s weapon is " + str(weapons[weapon_roll - 1]))

        # Adjust combat strength based on previous game
        adjust_combat_strength(hero, monster)

        # Weapon Roll Analysis
        print("    ------------------------------------------------------------------")
        print("    |", end="    ")
        input("Analyze the Weapon roll (Press enter)")
        print("    |", end="    ")
        if weapon_roll <= 2:
            print("--- You rolled a weak weapon, friend")
        elif weapon_roll <= 4:
            print("--- Your weapon is meh")
        else:
            print("--- Nice weapon, friend!")

        # If the weapon rolled is not a Fist, print out "Thank goodness you didn't roll the Fist..."
        if weapons[weapon_roll - 1] != "Fist":
            print("    |    --- Thank goodness you didn't roll the Fist...")

        # Roll for player health points
        print("    |", end="    ")
        input("Roll the dice for your health points (Press enter)")
        hero.health_points = random.randint(1, 20)
        print(f"    |    Player rolled {hero.health_points} health points")

        # Roll for monster health points
        print("    |", end="    ")
        input("Roll the dice for the monster's health points (Press enter)")
        monster.health_points = random.randint(1, 20)
        print(f"    |    Player rolled {monster.health_points} health points for the monster")

        # Collect Loot
        print("    ------------------------------------------------------------------")
        print("    |    !!You find a loot bag!! You look inside to find 2 items:")
        print("    |", end="    ")
        input("Roll for first item (enter)")

        # Collect Loot First time
        loot_options_local = loot_options.copy()
        belt_local = belt.copy()
        loot_options_local, belt_local = collect_loot(loot_options_local, belt_local)
        print("    ------------------------------------------------------------------")
        print("    |", end="    ")
        input("Roll for second item (Press enter)")

        # Collect Loot Second time
        loot_options_local, belt_local = collect_loot(loot_options_local, belt_local)

        print("    |    You're super neat, so you organize your belt alphabetically:")
        belt_local.sort()
        print("    |    Your belt (after random loot): ", belt_local)

        # --- Start: Ensure crafting materials are present for demonstration ---
        print("    |    (DEBUG: Ensuring crafting materials 'Flimsy Gloves' and 'Scrap Metal' are present for demo)")
        if "Flimsy Gloves" not in belt_local:
            belt_local.append("Flimsy Gloves")
            print("    |    (DEBUG: Added missing 'Flimsy Gloves')")
        if "Scrap Metal" not in belt_local:
            belt_local.append("Scrap Metal")
            print("    |    (DEBUG: Added missing 'Scrap Metal')")
        # Re-sort if items were added
        belt_local.sort()
        print("    |    Your belt (after ensuring materials): ", belt_local)
        # --- End: Ensure crafting materials ---

        # Check for crafting opportunities instead of automatically using loot
        belt_local = check_crafting(hero, belt_local)

        # The check_crafting function now handles the separator line and potential item usage prompts
        # print("    ------------------------------------------------------------------") # Removed this line as check_crafting adds its own separator
        # Add separate weather gear collection
        print("    ------------------------------------------------------------------")
        print("    |    !!You notice a strange weather device on the ground!!")
        print("    |", end="    ")
        input("Roll for weather protection gear (enter)")

        # Get weather gear
        player_weather_gear = collect_weather_gear(weather_gear)

        # Check if the gear helps with current weather
        weather_protection = {
            "Raincoat": ["rainy", "stormy"],
            "Sunglasses": ["sunny", "hot"],
            "Heat Cloak": ["cold"],
            "Wind Barrier": ["windy", "foggy"],
            "Weather Orb": ["rainy", "stormy", "sunny", "hot", "cold", "windy", "foggy"]  # Works for all
        }

        current_weather = weather_system.current_weather[0]
        if current_weather in weather_protection.get(player_weather_gear, []):
            print(f"    |    Your {player_weather_gear} protects you from the {current_weather} weather!")
            # Reverse negative weather effects for hero if there are any
            effects = weather_system.get_weather_effects()
            if effects["combat_mod"] < 0:
                hero.combat_strength = max(1, hero.combat_strength - effects["combat_mod"])
                print(f"    |    Your protection restores your combat strength to {hero.combat_strength}")
            if effects["health_mod"] < 0:
                hero.health_points = max(1, hero.health_points - effects["health_mod"])
                print(f"    |    Your protection restores your health to {hero.health_points}")
        else:
            print(f"    |    Your {player_weather_gear} isn't useful in the current {current_weather} weather.")

        print("    ------------------------------------------------------------------")
        print("    |", end="    ")
        input("Analyze the roll (Press enter)")
        # Compare Player vs Monster's strength
        print(f"    |    --- You are matched in strength: {hero.combat_strength == monster.combat_strength}")

        # Check the Player's overall strength and health
        print(f"    |    --- You have a strong player: {(hero.combat_strength + hero.health_points) >= 15}")

        # Roll for the monster's power
        print("    |", end="    ")
        input("Roll for Monster's Magic Power (Press enter)")
        ascii_image4 = """
                    @%   @                      
             @     @                        
                 &                          
          @      .                          

         @       @                    @     
                  @                  @      
          @         @              @  @     
           @            ,@@@@@@@     @      
             @                     @        
                @               @           
                     @@@@@@@                

                                          """
        print(ascii_image4)
        power_roll = random.choice(["Fire Magic", "Freeze Time", "Super Hearing"])

        # Increase the monster's combat strength by its power
        monster.combat_strength += min(6, monster.combat_strength + monster_powers[power_roll])
        print(f"    |    The monster's combat strength is now {monster.combat_strength} using the {power_roll} magic power")

        available_pets = get_available_pets(hero)

        if available_pets:
            print("\nYou found a companion!")
            for i, pet in enumerate(available_pets):
                print(f"{i + 1}. {pet['name']} - {pet['effect']}")
            choice = int(input("Choose your companion: ")) - 1
            companion = available_pets[choice]
            print(f"{companion['name']} has joined you!")
        else:
            companion = None

        # Lab Week 06 - Question 6
        num_dream_lvls = -1 # Initialize the number of dream levels
        while (num_dream_lvls < 0 or num_dream_lvls > 3):
            # Call Recursive function
            print("    |", end="    ")
            try:
                dream_input = input("How many dream levels do you want to go down? (Enter a number 0-3)")
                num_dream_lvls = int(dream_input)

                if (num_dream_lvls < 0 or num_dream_lvls > 3):
                    num_dream_lvls = -1
                    print("Number entered must be a whole number between 0-3 inclusive, try again")
                elif (not num_dream_lvls == 0):
                    hero.health_points -= 1
                    crazy_level = inception_dream(num_dream_lvls)
                    hero.combat_strength += crazy_level
                    print("combat strength: " + str(hero.combat_strength))
                    print("health points: " + str(hero.health_points))
            except ValueError:
                print("Invalid input. Please enter a number between 0-3.")
                num_dream_lvls = -1
            print("num_dream_lvls: ", num_dream_lvls)

        # Weather can change before combat
        print("    ------------------------------------------------------------------")
        print("    |", end="    ")
        input("The weather suddenly shifts as you prepare for battle! (Press enter)")
        weather_system.generate_weather()
        describe_weather(weather_system)

        # Apply new weather effects
        hero_combat_mod, hero_health_mod = weather_system.apply_weather_effects(hero, "hero")
        monster_combat_mod, monster_health_mod = weather_system.apply_weather_effects(monster, "monster")

        print(f"    |    The new weather affects your combat strength by {hero_combat_mod} and health by {hero_health_mod}")
        print(f"    |    Your combat strength is now {hero.combat_strength} and health is {hero.health_points}")
        print(f"    |    The new weather affects the monster's combat strength by {monster_combat_mod} and health by {monster_health_mod}")
        print(f"    |    Monster's combat strength is now {monster.combat_strength} and health is {monster.health_points}")

        # Check if the previously found weather gear helps with the new weather
        current_weather = weather_system.current_weather[0]
        if current_weather in weather_protection.get(player_weather_gear, []):
            print(f"    |    Your {player_weather_gear} protects you from the new {current_weather} weather!")
            # Reverse negative weather effects for hero if there are any
            effects = weather_system.get_weather_effects()
            if effects["combat_mod"] < 0:
                hero.combat_strength = max(1, hero.combat_strength - effects["combat_mod"])
                print(f"    |    Your protection restores your combat strength to {hero.combat_strength}")
            if effects["health_mod"] < 0:
                hero.health_points = max(1, hero.health_points - effects["health_mod"])
                print(f"    |    Your protection restores your health to {hero.health_points}")
        else:
            print(f"    |    Your {player_weather_gear} isn't useful in the new {current_weather} weather.")

        # Fight Sequence
        # Loop while the monster and the player are alive. Call fight sequence functions
        print("    ------------------------------------------------------------------")
        print("    |    You meet the monster. FIGHT!!")
        num_stars = 0

        while monster.health_points > 0 and hero.health_points > 0:
            # Fight Sequence
            print("    |", end="    ")

            # Roll to see who strikes first
            input("Roll to see who strikes first (Press Enter)")
            attack_roll = random.randint(1, 6)

            if not (attack_roll % 2 == 0):
                print("    |    You strike!")

                # Hero attacks
                damage = hero.hero_attacks()

                if companion and companion["name"] == "Wolf":
                    if random.randint(1, 6) > 3:  
                        print("Wolf strikes with you! +2 damage!")
                        damage += companion["power"]
                
                print(f"    |    Player's weapon ({damage}) ---> Monster ({monster.health_points})")

                if damage >= monster.health_points:
                    # Player was strong enough to kill monster in one blow
                    monster.health_points = 0
                    print("    |    You have killed the monster")
                    num_stars = 3
                else:
                    # Player only damaged the monster
                    monster.health_points -= damage
                    print(f"    |    You have reduced the monster's health to: {monster.health_points}")

                if monster.health_points > 0:
                    print("    ------------------------------------------------------------------")
                    print("    |    The monster strikes!!!")

                    # Monster attacks
                    if companion and companion["name"] == "Hawk":
                        if random.random() < companion["chance"]:  # Nested condition
                            print("🦅 Hawk dodges the attack for you!")
                            damage = 0
                        else:
                            damage = monster.monster_attacks()
                    else:
                        damage = monster.monster_attacks()

                    print(f"    |    Monster's Claw ({damage}) ---> Player ({hero.health_points})")

                    if damage >= hero.health_points:
                        # Monster was strong enough to kill player in one blow
                        hero.health_points = 0
                        print("    |    Player is dead")
                        num_stars = 1
                    else:
                        # Monster only damaged the player
                        hero.health_points -= damage
                        print(f"    |    The monster has reduced Player's health to: {hero.health_points}")
                        num_stars = 2
            else:
                print("    |    The Monster strikes!")

                # Monster attacks
                damage = monster.monster_attacks()
                print(f"    |    Monster's Claw ({damage}) ---> Player ({hero.health_points})")

                if damage >= hero.health_points:
                    # Monster was strong enough to kill player in one blow
                    hero.health_points = 0
                    print("    |    Player is dead")
                    num_stars = 1
                else:
                    # Monster only damaged the player
                    hero.health_points -= damage
                    print(f"    |    The monster has reduced Player's health to: {hero.health_points}")

                    if hero.health_points > 0:
                        print("    ------------------------------------------------------------------")
                        print("    |    The hero strikes!!")

                        # Hero attacks
                        damage = hero.hero_attacks()
                        print(f"    |    Player's weapon ({damage}) ---> Monster ({monster.health_points})")

                        if damage >= monster.health_points:
                            # Player was strong enough to kill monster in one blow
                            monster.health_points = 0
                            print("    |    You have killed the monster")
                            num_stars = 3
                        else:
                            # Player only damaged the monster
                            monster.health_points -= damage
                            print(f"    |    You have reduced the monster's health to: {monster.health_points}")
                            num_stars = 2

        if monster.health_points <= 0:
            winner = "Hero"
            monsters_killed += 1
            print(f"You killed a monster! Total monsters killed now: {monsters_killed}")
        else:
            winner = "Monster"

        # Final Score Display
        tries = 0
        input_invalid = True
        while input_invalid and tries in range(5):
            print("    |", end="    ")
            try:
                hero_name = input("Enter your Hero's name (in two words)")
                name = hero_name.split()
                if len(name) != 2:
                    print("    |    Please enter a name with two parts (separated by a space)")
                    tries += 1
                else:
                    if not name[0].isalpha() or not name[1].isalpha():
                        print("    |    Please enter an alphabetical name")
                        tries += 1
                    else:
                        short_name = name[0][0:2:1] + name[1][0:1:1]
                        print("    |    I'm going to call you " + short_name + " for short")
                        input_invalid = False
            except Exception as e:
                print(f"    |    Error with hero name: {e}")
                tries += 1

        if not input_invalid:
            stars_display = "*" * num_stars

            # Weather bonus for final score
            weather_bonus = 0
            if weather_system.current_weather[0] == "perfect":
                weather_bonus = 1
                print("    |    You get a bonus star for fighting in perfect weather!")

            final_stars = min(5, num_stars + weather_bonus)
            stars_display = "*" * final_stars

            print(f"    |    Hero {short_name} gets <{stars_display}> stars")

            # Save the game with the updated monsters_killed count
            save_game(winner, hero_name=short_name, num_stars=final_stars, monsters_killed=monsters_killed)

            print(f"Total monsters killed (all games): {monsters_killed}")

if __name__ == "__main__":
    main()