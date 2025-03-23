from character import Character
import random

class Monster(Character):
    def __init__(self, combat_strength=None, health_points=None):
        # Call parent constructor
        super().__init__(combat_strength, health_points)

    def __del__(self):
        print("The Monster object is being destroyed by the garbage collector")
        super().__del__()

    def monster_attacks(self):
        """Monster's attack function that returns the damage dealt (equal to combat strength)"""
        ascii_image2 = """                                                                 
               @@@@ @                           
          (     @*&@  ,                         
        @               %                       
         &#(@(@%@@@@@*   /                      
          @@@@@.                                
                   @       /                    
                    %         @                 
                ,(@(*/           %              
                   @ (  .@#                 @   
                              @           .@@. @
                       @         ,              
                          @       @ .@          
                                 @              
                              *(*  *      
                 """
        print(ascii_image2)
        return self.combat_strength