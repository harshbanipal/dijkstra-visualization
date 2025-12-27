import pygame

pygame.init()   # initialize pygame

screen = pygame.display.set_mode((640,640))    # create window with dimensions x by y
pygame.display.set_caption("dijkstra")

white = (255,255,255)

# node class
class Node():
    # constructor
    def __init__(self, x, y, radius, color, children):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.children = children

    # getters
    def getLoc(self):
        return (self.x, self.y)
    
    def getColor(self):
        return self.color
    
    def getRadius(self):
        return self.radius
    
    def getChildren(self):
        return self.children
    
    # setters
    def setChildren(self, children):
        self.children = children

def main(): 
    # dummy graph for now, will implement adding your own graph later
    graph = {
        'A': [('B', 1), ('D', 5), ('C', 3)],
        'B': [('A', 1), ('D', 2)],
        'C': [('A', 3), ('D', 1), ('E', 4)],
        'D': [('A', 5), ('B', 2), ('C', 1), ('E', 7)],
        'E': [('C', 4), ('D', 7)]
    }
        
    # game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


    pygame.quit()
        