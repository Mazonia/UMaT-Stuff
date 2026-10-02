from abc import ABC, abstractmethod

class Food(ABC):
    def __init__(self, quantity):
        self.quantity = quantity

    @abstractmethod
    def __repr__(self):
        pass

class Fruit(Food):
    def __init__(self, quantity):
        super().__init__(quantity)

    def __repr__(self):
        return f"Fruit(quantity={self.quantity})"

class Meat(Food):
    def __init__(self, quantity):
        super().__init__(quantity)

    def __repr__(self):
        return f"Meat(quantity={self.quantity})"

class Vegetable(Food):
    def __init__(self, quantity):
        super().__init__(quantity)

    def __repr__(self):
        return f"Vegetable(quantity={self.quantity})"

class Seed(Food):
    def __init__(self, quantity):
        super().__init__(quantity)

    def __repr__(self):
        return f"Seed(quantity={self.quantity})"
    
