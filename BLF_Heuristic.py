import numpy as np

class Rectangle:
    def __init__(self, width, height, demand):
        self.width = width
        self.height = height
        self.demand = demand
        self.x = 0
        self.y = 0
    def sortShape(shape):
        # Sort the shapes based on their area in descending order
        shape.sort(key=lambda temp: temp.width * temp.height, reverse=True)
        return shape

class BLF:
    def __init__(self, stock_w, stock_h):
        self.stock_w = stock_w
        self.stock_h = stock_h
        self.stock_idx = -1
        self.stock = []
    def place_shape (self, shape):
        x, y = self.find_position(shape)
        if x is not None and y is not None:
            new_shape = Rectangle(shape.width, shape.height, 0)
            new_shape.x = x
            new_shape.y = y
            self.stock.append(new_shape)
        else:
            return False
        return True
    def find_position(self, shape):
        best_x, best_y = None, None
        for position in self.stock:
            temp=[(position.x + shape.width, position.y),(position.x, position.y + shape.height)]
            for (x, y) in temp:
                if self.can_place(shape, x, y):
                    if best_y is None or (y < best_y) or (y == best_y and x < best_x):
                        best_x, best_y = x, y 
                        
        if not self.stock and self.can_place(shape, 0, 0):
            best_x, best_y = 0, 0

        return best_x, best_y
    def can_place (self, shape, x, y):
        if shape.width + x > self.stock_w or shape.height + y > self.stock_h:
            return False
        else:
            for position in self.stock:
                if shape.width + x <= position.x + position.width and shape.height + y <= position.y + position.height:
                    return False
        return True
    def display_stock (self,):
        for temp in range(len(self.stock)):
            print ("shape:", self.stock[temp].width, self.stock[temp].height, self.stock[temp].x, self.stock[temp].y)
            
            
        
if __name__ == "__main__":
    with open('input.txt', 'r') as file:
        width = [int(x) for x in file.readline().strip().split(' ')]
        height = [int(x) for x in file.readline().strip().split(' ')]
        demand = [int(x) for x in file.readline().strip().split(' ')]
    blf = BLF(100, 100)    
    shapes = []
    for width, height, demand in zip(width, height, demand):
        shapes.append(Rectangle( width, height, demand))
    shapes= Rectangle.sortShape(shapes)
    print(shapes)
    count = 0
    for temp in shapes:
        count = 0
        while temp.demand != 0:
            if not blf.place_shape(temp):
                blf.stock_h = 100
                blf.stock_w = 100
                blf.display_stock()
                blf.stock = []
                blf.stock_idx += 1
            temp.demand = temp.demand - 1
            count += 1
        blf.stock_idx += 1
        blf.stock = []
        print(count)
    print("Total stock: ", blf.stock_idx)    
    
    