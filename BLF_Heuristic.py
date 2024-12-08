import numpy as np
import matplotlib.pyplot as plt

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
        self.stock_idx = 0
        self.stock = []
        self.waste = self.stock_w * self.stock_h
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
            temp=[(position.x + position.width, position.y),(position.x, position.y + position.height)]
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
                if  x < position.x + position.width and y < position.y + position.height:
                    return False
        return True
    def display_stock (self):
        for temp in range(len(self.stock)):
            print ("shape:", self.stock[temp].width, self.stock[temp].height, self.stock[temp].x, self.stock[temp].y)
    
    def draw_stock(self):
        fig, ax = plt.subplots()
        ax.add_patch(plt.Rectangle((0, 0), self.stock_w, self.stock_h, edgecolor='black', facecolor='lightgrey'))

        color_map = {}
        
        for shape in self.stock:
            size_key = (shape.width, shape.height)
            if size_key not in color_map:
                color_map[size_key] = np.random.rand(3,)
            color = color_map[size_key]
            
            ax.add_patch(plt.Rectangle((shape.x, shape.y), shape.width, shape.height, edgecolor='black', facecolor=color, lw=2))
            ax.text(shape.x + shape.width / 2, shape.y + shape.height / 2, 
                    f'{shape.width}x{shape.height}', 
                    ha='center', va='center', color='black', fontsize=8)

        ax.set_xlim(0, self.stock_w)
        ax.set_ylim(0, self.stock_h)
        ax.set_aspect('equal')
        plt.title('2D Cutting Stock Problem')
        plt.xlabel('Width')
        plt.ylabel('Height')

        plt.show()        

       
        
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
        count = temp.demand
        while temp.demand > 0:
            if not blf.place_shape(temp):
                blf.stock_h = 100
                blf.stock_w = 100
                blf.display_stock()
                blf.draw_stock()
                blf.stock = []
                blf.waste=blf.waste + blf.stock_w*blf.stock_h
                blf.stock_idx += 1
            else:
                blf.waste = blf.waste - (temp.width * temp.height)
                temp.demand = temp.demand - 1
                print(count-temp.demand)
    print("Total stock: ", blf.stock_idx + 1)
    print("Total area: ",(blf.stock_idx + 1)*100*100) 
    print("Total waste: ", blf.waste, "percentage: ", blf.waste/((blf.stock_idx + 1)*100*100))
    if(len(blf.stock)!=0):
        blf.display_stock()
        blf.draw_stock()
   