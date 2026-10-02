from food import Meat, Fruit, Vegetable, Seed
from animals import Mammal

class Mouse(Mammal):
    def __init__(self, name, weight, living_region, food_eaten=0):
        super().__init__(name, weight, living_region, food_eaten)
        self.food_that_eats = [Vegetable, Fruit]
        self.weight_per_food = 0.1

    def make_sound(self):
        return "Squeak"

class Dog(Mammal):
    def __init__(self, name, weight, living_region, food_eaten=0):
        super().__init__(name, weight, living_region, food_eaten)
        self.food_that_eats = [Meat]
        self.weight_per_food = 0.4

    def make_sound(self):
        return "Woof"

class Cat(Mammal):
    def __init__(self, name, weight, living_region, food_eaten=0):
        super().__init__(name, weight, living_region, food_eaten)
        self.food_that_eats = [Meat, Vegetable]
        self.weight_per_food = 0.3

    def make_sound(self):
        return "Meow"

class Tiger(Mammal):
    def __init__(self, name, weight, living_region, food_eaten=0):
        super().__init__(name, weight, living_region, food_eaten)
        self.food_that_eats = [Meat, Vegetable]
        self.weight_per_food = 1.0

    def make_sound(self):
        return "Roar"