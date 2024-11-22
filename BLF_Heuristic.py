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
        for _ in range(shape.demand):
            x, y = self.find_position(shape)
            if x is not None and y is not None:
                new_shape = Rectangle(x, y, 1)
                self.stock.append(new_shape)
            else:
                return False
        return True
    def find_position(self, shape):
        best_x, best_y = None, None
        for position in self.stock:
            temp=[(position.x + shape.width, shape.height),(shape.x, position.y + shape.height)]
            for (x, y) in temp:
                if self.can_place(shape, x, y):
                    best_x, best_y = x, y
                    
        if not self.stock and self.can_place(shape, 0, 0):
            best_x, best_y = 0, 0

        return best_x, best_y
    def can_place (self, shape, width, height):
        if shape.x + width > self.stock_w or shape.y + height > self.stock_h:
            return False
        else:
            for position in self.stock:
                if shape.x + width < position.x and shape.y + height < position.y:
                    return False
        return True
    
    
    
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
    flag = 1
    for temp in shapes:
        for i in range(len(shapes)):
            if shapes[i].demand == 0:
                flag =0
                break
        if not blf.place_shape(temp):
            for temp1 in shapes[1:]:
                blf.place_shape(temp1)
            blf.stock_h = 100
            blf.stock_w = 100
            blf.stock = []
            blf.stock_idx += 1
        else:
            if flag:
                blf.place_shape(temp)
        
    print ("stock_index: ", blf.stock_idx)
    
    