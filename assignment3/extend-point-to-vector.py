import math

class Point:
    
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other):
        
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Vector(Point):
   

    def __str__(self):
       
        return f"Vector<{self.x}, {self.y}>"

    def __add__(self, other):
       
        if not isinstance(other, Point):
            raise TypeError("Operand must be a Vector or Point")
        return Vector(self.x + other.x, self.y + other.y)


if __name__ == "__main__":
    print("--- Demonstrating Point and Vector Classes ---")
    
  
    p1 = Point(3, 4)
    p2 = Point(3, 4)
    p3 = Point(1, 1)
    
    print(f"Point 1: {p1}")
    print(f"Point 2: {p2}")
    
   
    print(f"p1 == p2: {p1 == p2}")
    print(f"p1 == p3: {p1 == p3}")
    
    # 3. Test Euclidean distance
    dist = p1.distance_to(p3)
    print(f"Distance between {p1} and {p3}: {dist:.2f}")
    
    print("-" * 40)
    
   
    v1 = Vector(2, 3)
    v2 = Vector(4, 5)
    
    print(f"Vector 1: {v1}")
    print(f"Vector 2: {v2}")
    
    
    v3 = v1 + v2
    print(f"Result of {v1} + {v2} = {v3}")
    print(f"Is result an instance of Vector? {isinstance(v3, Vector)}")