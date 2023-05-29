class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"


class Bridge:
    def __init__(self, coordinate1, coordinate2):
        self.island1 = Coordinate(coordinate1.x, coordinate1.y)
        self.island2 = Coordinate(coordinate2.x,coordinate2.y)
        self.num_bridges = 1  # comienza con 1 puente
    
    def add_bridge(self):
        if self.num_bridges < 2:
            self.num_bridges += 1
    
    def remove_bridge(self):
        if self.num_bridges > 0:
            self.num_bridges -= 1
    
    def __repr__(self):
        return f"Bridge between {self.island1} and {self.island2} ({self.num_bridges} bridge{'s' if self.num_bridges > 1 else ''})"


class Island:
    def __init__(self, x, y, num_bridges):
        self.x = x
        self.y = y
        self.num_bridges = num_bridges
        self.sum = 0
        self.options = []
        self.heuristic = 0
    
    def __str__(self):
        return f"Island ({self.x}, {self.y}) with {self.num_bridges} bridges"

    def addOne(self):
        self.sum += 1

    def subtractOne(self):
        self.sum -= 1

    def __le__(self, other):
        return (len(self.options) <= len(other.options))

    def __lt__(self, other):
        return (len(self.options) < len(other.options))

    def returnSum(self):
        return self.sum

    def returnOptionsLength(self):
        return len(self.options)