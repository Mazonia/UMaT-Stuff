from food import Meat, Fruit, Vegetable, Seed
from animals import Bird

class Hen(Bird):
    def __init__(self, name, weight, wing_size, food_eaten=0):
        super().__init__(name, weight, wing_size, food_eaten)
        self.food_that_eats = [Meat, Vegetable, Fruit, Seed]
        self.weight_per_food = 0.35

    def make_sound(self):
        return "Cluck"

class Owl(Bird):
    def __init__(self, name, weight, wing_size, food_eaten=0):
        super().__init__(name, weight, wing_size, food_eaten)
        self.food_that_eats = [Meat]
        self.weight_per_food = 0.25

    def make_sound(self):
        return "Hoot Hoot"
    
    