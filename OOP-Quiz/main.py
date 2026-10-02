"""
Wild Farm Simulator - Object-Oriented Programming (OOP) Demonstration
"""

from birds import Owl, Hen
from mammals import Mouse, Dog, Cat, Tiger
from food import Vegetable, Fruit, Meat, Seed

def run_simulation():
    print("==================================================")
    print("      WILD FARM OOP SIMULATOR (UMaT Coursework)   ")
    print("==================================================")
    
    animals = [
        Owl("Pip", 10.0, 15.0),
        Hen("Clucky", 2.5, 8.0),
        Mouse("Jerry", 0.5, "Kitchen"),
        Dog("Rex", 25.0, "Yard"),
        Cat("Whiskers", 4.0, "Living Room"),
        Tiger("Apex", 180.0, "Jungle")
    ]
    
    foods = [
        Meat(2),
        Vegetable(3),
        Fruit(1),
        Seed(5)
    ]
    
    print("\n[+] Initial Animals in Farm:")
    for a in animals:
        print(f"  - {a} | Sound: '{a.make_sound()}'")
        
    print("\n[+] Simulating Feeding Sessions:")
    for animal in animals:
        print(f"\n---> Feeding {animal.name} ({type(animal).__name__}):")
        for food in foods:
            result = animal.feed(food)
            print(f"     Offered {food}: {result}")
            
    print("\n[+] Final State of Farm Animals:")
    for a in animals:
        print(f"  - {a}")

if __name__ == '__main__':
    run_simulation()
