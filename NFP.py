import numpy as np
import matplotlib.pyplot as plt
import time

class Rectangle:
    def __init__(self, width, height, demand):
        self.width = width
        self.height = height
        self.demand = demand
        self.x = 0
        self.y = 0
    
    def __repr__(self):
        return f"Rectangle({self.width}x{self.height}, demand={self.demand}, position=({self.x}, {self.y}))"

    def sortShape(shape):
        # Sort the shapes based on their area in descending order
        shape.sort(key=lambda temp: temp.width * temp.height, reverse=True)
        return shape

class NFP:
    def __init__(self, stock_w, stock_h):
        self.stock_w = stock_w
        self.stock_h = stock_h
        self.stock = []
        self.stock_count = 0  # Biến đếm số lượng không gian đã sử dụng
        self.total_waste = stock_w * stock_h

    def place_shape(self, shape):
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
        best_position = None
        best_x, best_y = None, None

        # Duyệt qua tất cả các vị trí khả thi
        for x in range(self.stock_w - shape.width + 1):
            for y in range(self.stock_h - shape.height + 1):
                if self.can_place(shape, x, y):
                    if best_y is None or (y < best_y) or (y == best_y and x < best_x):
                        best_x, best_y = x, y
        if not self.stock and self.can_place(shape, 0, 0):
            best_x, best_y = 0, 0
        return best_x, best_y

    def can_place(self, shape, x, y):
        if x + shape.width > self.stock_w or y + shape.height > self.stock_h:
            return False
        for placed_shape in self.stock:
            if not (x + shape.width <= placed_shape.x or x >= placed_shape.x + placed_shape.width or
                    y + shape.height <= placed_shape.y or y >= placed_shape.y + placed_shape.height):
                return False
        return True

    def display_stock(self):
        for temp in range(len(self.stock)):
            print("shape:", self.stock[temp].width, self.stock[temp].height, self.stock[temp].x, self.stock[temp].y)

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

    def update_stock_count(self):
        self.stock_count += 1  # Tăng số lượng không gian khi không thể đặt thêm hình vào không gian hiện tại
if __name__ == "__main__":
    with open('input.txt', 'r') as file:
        width = [int(x) for x in file.readline().strip().split(' ')]
        height = [int(x) for x in file.readline().strip().split(' ')]
        demand = [int(x) for x in file.readline().strip().split(' ')]
    nfp = NFP(100, 100)
    shapes = []
    for width, height, demand in zip(width, height, demand):

        start_time = time.time()
        shapes.append(Rectangle(width, height, demand))
    shapes = Rectangle.sortShape(shapes)
    count = 0
    for temp in shapes:
        count = temp.demand
        while temp.demand > 0:
            if not nfp.place_shape(temp):
                for temp1 in shapes:
                    while temp1.demand > 0:
                        if not nfp.place_shape(temp1):
                            break
                        else:
                            nfp.total_waste  = nfp.total_waste - (temp1.width * temp1.height)
                            temp1.demand -= 1
                nfp.update_stock_count()
                nfp.stock_h = 100
                nfp.stock_w = 100
                #nfp.display_stock()
                #nfp.draw_stock()
                nfp.stock = []
                nfp.total_waste = nfp.total_waste + nfp.stock_w * nfp.stock_h 
            else:
                nfp.total_waste = nfp.total_waste - (temp.width * temp.height)
                temp.demand -= 1
                #print(count - temp.demand)
    # if len(nfp.stock) != 0:
    #     #nfp.display_stock()
    #     nfp.draw_stock()
    print("Total stock: ", nfp.stock_count + 1)
    print("Total area: ", (nfp.stock_count + 1)*100*100)
    print("Total waste: ", nfp.total_waste, "percentage: ", nfp.total_waste / ((nfp.stock_count + 1) * 100 * 100))
    # Kết thúc đo thời gian
    end_time = time.time()

    # Tính toán và in ra thời gian thực thi
    execution_time = end_time - start_time
    print("Execution time: ", execution_time, "seconds")