from algo import dijkstra
import pygame
pygame.init()  

# inititalize window
screen = pygame.display.set_mode((1000,1000))    # create window 
pygame.display.set_caption("dijkstra")


# colors
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
yellow = (255, 255, 0)


# dummy graph for now, will implement adding your own graph later
my_graph = {
    'A': [('B', 1), ('C', 5), ('D', 3)],
    'B': [('A', 1), ('C', 2)],
    'C': [('A', 5), ('B', 2), ('D', 1), ('E', 7)],
    'D': [('A', 3), ('C', 1), ('E', 4)],
    'E': [('D', 4), ('C', 7)]
} 

locations = {
    'A' : (275, 350),
    'B' : (625, 250),
    'C' : (625, 450),
    'D' : (275, 550),
    'E' : (625, 650)
}


# text font
text_font = pygame.font.SysFont('Arial', 12)


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

def drawGraph(graph, locations):

    for node in graph: 
        node_pos = locations[node]

        # draw edges
        for child in graph[node]:
            child_key = child[0]
            child_pos = locations[child_key]
            weight = child[1]
            pygame.draw.line(screen, white, node_pos, child_pos)
            
            # find midpoint of line
            if node_pos[0] < child_pos[0]:
                weight_xpos = node_pos[0] + abs(node_pos[0] - child_pos[0])/2
            else:
                weight_xpos = child_pos[0] + abs(node_pos[0] - child_pos[0])/2

            if node_pos[1] < child_pos[1]:
                weight_ypos = node_pos[1] + abs(node_pos[1] - child_pos[1])/2
            else:
                weight_ypos = child_pos[1] + abs(node_pos[1] - child_pos[1])/2

            drawText(str(weight), text_font, red, weight_xpos + 5, weight_ypos + 5)

        # draw nodes
        pygame.draw.circle(screen, white, node_pos, 25)
        drawText(node, text_font, red, node_pos[0] - 5, node_pos[1] - 5)
    
            
    return


def drawText(text, font, color, x, y,):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))

def main(): 
     
    print(dijkstra(my_graph, 'A'))

    # game loop
    running = True  
    while running:

        screen.fill(black)

        # draw my own graph
        if pygame.mouse.get_pressed()[0] == True:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.circle(screen, white, mouse_pos, 25)
            mouse_posStr = str(mouse_pos)
            drawText(mouse_posStr, text_font, red, mouse_pos[0], mouse_pos[1])
       
        drawGraph(my_graph, locations)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
    
    pygame.quit()

main()
        