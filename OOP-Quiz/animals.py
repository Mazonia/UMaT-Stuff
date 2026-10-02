from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, name, weight, food_eaten=0):
        self.name = name
        self.weight = weight
        self.food_eaten = food_eaten
        self.food_that_eats = None  
        self.weight_per_food = 0  

    @abstractmethod
    def make_sound(self):
        pass

    def feed(self, food):
        if self.food_that_eats is None or type(food) not in self.food_that_eats:
            return f"{type(self).__name__} does not eat {type(food).__name__}!"
        
        
        self.food_eaten += 1
        self.weight += self.weight_per_food
        return f"{self.name} has been fed!"

class Bird(Animal):
    def __init__(self, name, weight, wing_size, food_eaten=0):
        super().__init__(name, weight, food_eaten)
        self.wing_size = wing_size

    def __repr__(self):
        return f"{type(self).__name__} [{self.name}, {self.wing_size}, {self.weight}, {self.food_eaten}]"
    



class Mammal(Animal):
    def __init__(self, name, weight, living_region, food_eaten=0):
        super().__init__(name, weight, food_eaten)
        self.living_region = living_region

    def __repr__(self):
        return f"{type(self).__name__} [{self.name}, {self.weight}, {self.living_region}, {self.food_eaten}]"


