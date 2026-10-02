import unittest
from birds import Owl, Hen
from mammals import Mouse, Dog, Cat, Tiger
from food import Vegetable, Fruit, Meat, Seed

class WildFarmTests(unittest.TestCase):
    def test_owl_feeding(self):
        owl = Owl("Pip", 10, 10)
        self.assertEqual(str(owl), "Owl [Pip, 10, 10, 0]")
        
        meat = Meat(4)
        self.assertEqual(owl.make_sound(), "Hoot Hoot")
        
        owl.feed(meat)
        veg = Vegetable(1)
        self.assertEqual(owl.feed(veg), "Owl does not eat Vegetable!")
        self.assertEqual(str(owl), "Owl [Pip, 10, 10.25, 1]")

    def test_hen_feeding(self):
        hen = Hen("Clucky", 2.0, 5.0)
        self.assertEqual(hen.make_sound(), "Cluck")
        seed = Seed(2)
        hen.feed(seed)
        self.assertEqual(hen.food_eaten, 1)
        self.assertEqual(hen.weight, 2.35)

    def test_mammal_sounds_and_feeding(self):
        dog = Dog("Rex", 20.0, "Yard")
        self.assertEqual(dog.make_sound(), "Woof")
        self.assertEqual(dog.feed(Vegetable(1)), "Dog does not eat Vegetable!")
        dog.feed(Meat(1))
        self.assertEqual(dog.weight, 20.4)

        cat = Cat("Whiskers", 3.0, "House")
        self.assertEqual(cat.make_sound(), "Meow")

        tiger = Tiger("Apex", 150.0, "Jungle")
        self.assertEqual(tiger.make_sound(), "Roar")

if __name__ == '__main__':
    unittest.main()