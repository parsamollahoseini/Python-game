import random

class Character:
    def __init__(self, combat_strength=None, health_points=None):
        # Make properties private
        self.__combat_strength = combat_strength if combat_strength is not None else random.randint(1, 6)
        self.__health_points = health_points if health_points is not None else random.randint(1, 20)

    def __del__(self):
        print("Character object is being destroyed")

    # Complex getters and setters for combat_strength
    @property
    def combat_strength(self):
        return self.__combat_strength

    @combat_strength.setter
    def combat_strength(self, value):
        self.__combat_strength = value

    # Complex getters and setters for health_points
    @property
    def health_points(self):
        return self.__health_points

    @health_points.setter
    def health_points(self, value):
        self.__health_points = value