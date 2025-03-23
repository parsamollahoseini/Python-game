from character import Character
import random

class Hero(Character):
    def __init__(self, combat_strength=None, health_points=None):
        # Call parent constructor
        super().__init__(combat_strength, health_points)

    def __del__(self):
        print("The Hero object is being destroyed by the garbage collector")
        super().__del__()

    def hero_attacks(self):
        """Hero's attack function that returns the damage dealt (equal to combat strength)"""
        ascii_image = """
                                    @@   @@ 
                                    @    @  
                                    @   @   
                   @@@@@@          @@  @    
                @@       @@        @ @@     
               @%         @     @@@ @       
                @        @@     @@@@@     
                   @@@@@        @@       
                   @    @@@@                
              @@@ @@                        
           @@     @                         
       @@*       @                          
       @        @@                          
               @@                                                    
             @   @@@@@@@                    
            @            @                  
          @              @                  
        """
        print(ascii_image)
        return self.combat_strength