import random
import os

# Will the line below print when you import function.py into main.py?
# print("Inside function.py")

# Print out the operating system name
print(f"Operating System: {os.name}")

# Use the platform library to print Python version
import platform
print(f"Python Version: {platform.python_version()}")

def clear_screen():
    """Clear the terminal screen."""
    # Check the operating system and use the appropriate command
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')
    print("Screen cleared!")

def dream_levels(level=0):
    """Display information about dream levels."""
    if level == 0:
        print("Level 0 - Reality")
    elif level == 1:
        print("Level 1 - First dream level")
    elif level == 2:
        print("Level 2 - Second dream level")
    elif level == 3:
        print("Level 3 - Limbo")
    else:
        print("Unknown dream level")

def sword_art():
    """Display sword art ASCII."""
    print("""
     /\\
    /__\\
    |  |
    |__|
    """)

def good_ending():
    """Display the good ending message."""
    print("Congratulations! You have completed the game with the good ending!")

def use_loot(belt, hero, weather_system=None):
    good_loot_options = ["Health Potion", "Leather Boots"]
    bad_loot_options = ["Poison Potion"]
    weather_protection = {
        "Raincoat": ["rainy", "stormy"],
        "Sunglasses": ["sunny", "hot"],
        "Heat Cloak": ["cold"],
        "Wind Barrier": ["windy", "foggy"]
    }

    print("    |    !!You see a monster in the distance! So you quickly use your first item:")
    first_item = belt.pop(0)

    # Check if it's a weather protection item
    if weather_system and first_item in weather_protection:
        protected_weathers = weather_protection[first_item]
        current_weather = weather_system.current_weather[0]

        if current_weather in protected_weathers:
            print(f"    |    You used {first_item} to protect yourself from the {current_weather} weather!")
            # Reverse negative weather effects for hero
            if current_weather in ["rainy", "stormy", "foggy", "hot", "cold", "windy"]:
                effects = weather_system.get_weather_effects()
                hero.combat_strength = max(1, hero.combat_strength - effects["combat_mod"])
                hero.health_points = max(1, hero.health_points - effects["health_mod"])
                print(f"    |    Your protection restores your stats: Combat {hero.combat_strength}, Health {hero.health_points}")
                return belt

        print(f"    |    You used {first_item} but it's not helpful in the current weather")

    # Original loot logic
    elif first_item in good_loot_options:
        # Store the health value explicitly before and after change
        current_health = hero.health_points
        hero.health_points = min(20, (current_health + 2))
        print(f"    |    You used {first_item} to up your health to {hero.health_points}")
    elif first_item in bad_loot_options:
        # Store the health value explicitly before and after change
        current_health = hero.health_points
        hero.health_points = max(0, (current_health - 2))
        print(f"    |    You used {first_item} to hurt your health to {hero.health_points}")
    else:
        print(f"    |    You used {first_item} but it's not helpful")

    return belt

def collect_loot(loot_options, belt):
    ascii_image3 = """
                      @@@ @@                
             *# ,        @              
           @           @                
                @@@@@@@@                
               @   @ @% @*              
            @     @   ,    &@           
          @                   @         
         @                     @        
        @                       @       
        @                       @       
        @*                     @        
          @                  @@         
              @@@@@@@@@@@@          
              """
    print(ascii_image3)
    loot_roll = random.choice(range(1, len(loot_options) + 1))
    loot = loot_options.pop(loot_roll - 1)
    belt.append(loot)
    print("    |    Your belt: ", belt)
    return loot_options, belt

# Recursion
# You can choose to go crazy, but it will reduce your health points
def inception_dream(num_dream_lvls):
    num_dream_lvls = int(num_dream_lvls)

    # Print current dream level info
    if num_dream_lvls == 1:
        print("    |    You are in dream level 1")
    elif num_dream_lvls == 2:
        print("    |    You are in dream level 2")
    elif num_dream_lvls == 3:
        print("    |    You are in the deepest dream level (level 3)")

    print("    |", end="    ")
    # Store the input explicitly to prevent it from being consumed incorrectly
    user_input = input("Start to go back to real life? (Press Enter)")
    print("    |    You start to regress back through your dreams to real life.")

    # Return a bonus based on how deep the dream was
    return num_dream_lvls

# Save game function
def save_game(winner, hero_name="", num_stars=0, monsters_killed=0):
    with open("save.txt", "a") as file:
        if winner == "Hero":
            file.write(f"Hero {hero_name} has killed a monster and gained {num_stars} stars.\n")
        elif winner == "Monster":
            file.write("Monster has killed the hero previously\n")

    # Save the number of monsters killed explicitly
    with open("save_game.txt", "w") as file:
        file.write(f"{num_stars}\n")
        file.write(f"{monsters_killed}\n")
    print("Game saved! Monsters killed:", monsters_killed)

# Load game function
def load_game():
    try:
        # Load from the original save file
        last_game = None
        try:
            with open("save.txt", "r") as file:
                print("    |    Loading from saved file ...")
                lines = file.readlines()
                if lines:
                    last_game = lines[-1].strip()
                    print(last_game)
        except FileNotFoundError:
            print("No previous game found in save.txt. Starting fresh.")

        # Load from the new save_game.txt file
        monsters_killed = 0
        num_stars = 0
        try:
            with open("save_game.txt", "r") as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    num_stars = int(lines[0].strip())
                    monsters_killed = int(lines[1].strip())
                    print(f"Loaded game stats: Stars: {num_stars}, Monsters killed: {monsters_killed}")
        except (FileNotFoundError, ValueError, IndexError) as e:
            print(f"Error loading game stats: {e}")
            num_stars = 0
            monsters_killed = 0

        return last_game, num_stars, monsters_killed
    except Exception as e:
        print(f"General error in load_game: {e}")
        return None, 0, 0

def adjust_combat_strength(hero, monster):
    # Lab Week 06 - Question 5 - Load the game
    last_game, _, _ = load_game()
    if last_game:
        if "Hero" in last_game and "gained" in last_game:
            num_stars = int(last_game.split()[-2])
            if num_stars > 3:
                print("    |    ... Increasing the monster's combat strength since you won so easily last time")
                monster.combat_strength += 1
        elif "Monster has killed the hero" in last_game:
            hero.combat_strength += 1
            print("    |    ... Increasing the hero's combat strength since you lost last time")
        else:
            print("    |    ... Based on your previous game, neither the hero nor the monster's combat strength will be increased")


def describe_weather(weather_system):
    """Display current weather conditions and effects."""
    weather = weather_system.current_weather
    print("    ------------------------------------------------------------------")
    print(f"    |    WEATHER REPORT: {weather[0].upper()}")
    print(f"    |    {weather[1]}")
    print(weather_system.weather_ascii_art())

    effects = weather_system.get_weather_effects()
    print(f"    |    Combat Modifier: {effects['combat_mod']} | Health Modifier: {effects['health_mod']}")

    # Use list comprehension to generate weather tips
    weather_tips = [tip for condition, tip in [
        ("rainy", "The rain makes weapons slippery, be careful!"),
        ("stormy", "Monsters gain power from the storm's energy."),
        ("hot", "Stay hydrated to maintain your health."),
        ("cold", "Keep moving to prevent your joints from stiffening."),
        ("perfect", "This exceptional weather grants you additional strength!")
    ] if weather[0] == condition]

    if weather_tips:
        print(f"    |    TIP: {weather_tips[0]}")
    print("    ------------------------------------------------------------------")

def get_available_pets(hero):
    pets = [
        {"name": "Wolf", "type": "melee", "effect": "extra_damage", "power": 2},
        {"name": "Hawk", "type": "aerial", "effect": "block_damage", "chance": 0.3}
    ]
    # List comprehension: filter based on hero's strength
    return [pet for pet in pets if hero.combat_strength >= 3]