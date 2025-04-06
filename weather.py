# weather.py
import random

class WeatherSystem:
    def __init__(self):
        # Weather types and their attributes (condition, description, combat_mod, health_mod)
        self.weather_types = [
            ("sunny", "The sun shines brightly overhead", 1, 0),
            ("cloudy", "Gray clouds fill the sky", 0, 0),
            ("rainy", "Rain pours down from the dark sky", -1, -1),
            ("stormy", "Lightning flashes and thunder booms", -2, -2),
            ("foggy", "A thick fog limits visibility", -1, 0),
            ("windy", "Strong winds whip around you", 0, -1),
            ("hot", "The scorching heat drains your energy", -1, -2),
            ("cold", "The biting cold stiffens your movements", -2, -1),
            ("perfect", "The weather is absolutely perfect for an adventure", 2, 2)
        ]

        self.current_weather = None
        self.generate_weather()

    def generate_weather(self):
        # Generate weather based on weighted probabilities
        weights = [20, 20, 15, 5, 10, 10, 10, 10, 5]  # Perfect weather is rare
        self.current_weather = random.choices(self.weather_types, weights=weights, k=1)[0]
        return self.current_weather

    def get_weather_effects(self):
        # Get current combat and health modifiers
        return {
            "combat_mod": self.current_weather[2],
            "health_mod": self.current_weather[3]
        }

    def apply_weather_effects(self, character, character_type="hero"):
        # Apply weather effects to a character
        effects = self.get_weather_effects()
        combat_mod = effects["combat_mod"]
        health_mod = effects["health_mod"]

        # Use list comprehension to determine situational bonuses/penalties
        # Heroes and monsters might react differently to weather
        situational_bonus = [
            (1 if character_type == "hero" and self.current_weather[0] == "sunny" else 0),
            (1 if character_type == "monster" and self.current_weather[0] == "stormy" else 0),
            (-1 if character_type == "hero" and self.current_weather[0] == "foggy" else 0)
        ]

        total_combat_mod = combat_mod + sum(situational_bonus)

        # Apply the modifications
        character.combat_strength = max(1, character.combat_strength + total_combat_mod)
        character.health_points = max(1, character.health_points + health_mod)

        return total_combat_mod, health_mod

    def weather_ascii_art(self):
        # Return ASCII art based on weather
        weather_art = {
            "sunny": """
               \\   /
                .-.
             ― (   ) ―
                `-'
               /   \\
            """,
            "cloudy": """
                 .--.
              .-(    ).
             (___.__)__)
            """,
            "rainy": """
                 .-.
                (   ).
               (___(__)
                ʻ ʻ ʻ ʻ
               ʻ ʻ ʻ ʻ
            """,
            "stormy": """
                 .-.
                (   ).
               (___(__)
              ⚡ʻ ʻ⚡ʻ
               ʻ⚡ʻ ʻ
            """,
            "foggy": """
              _ - _ - _ -
             _ - _ - _ -
              _ - _ - _ -
             _ - _ - _ -
            """,
            "windy": """
              ~  ~  ~  ~
            ~  ~  ~  ~
              ~  ~  ~  ~
            ~  ~  ~  ~
            """,
            "hot": """
              \\   /
               .-.
            ― (   ) ―
               `-'
              /   \\
            🔥 🔥 🔥
            """,
            "cold": """
              *  *  *
             *  *  *
              *  *  *
            *  *  *
            """,
            "perfect": """
               \\   /
                .-.
             ― (   ) ―
                `-'
             🌈  🌈  🌈
            """
        }

        return weather_art.get(self.current_weather[0], "")