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


# dummy graph and locations for now, will implement adding your own graph later
my_graph = {
    'A': {
        'B' : 1,
        'C' : 5, 
        'D' : 3
        },
    'B': {
        'A' : 1, 
        'C' : 2
        },
    'C': {
        'A' : 5, 
        'B' : 2, 
        'D' : 1, 
        'E' : 7
        },
    'D': {
        'A' : 3, 
        'C' : 1, 
        'E' : 4
        },
    'E': {
        'D' : 4, 
        'C' : 7
        }
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


def drawNode(name, text_color, node_color, pos, size):
    pygame.draw.circle(screen, node_color, pos, size)
    drawText(name, text_font, text_color, pos[0] - 5, pos[1] - 5)


def drawNodes(graph, locations):
    for node in graph:
        node_pos = locations[node]
        drawNode(node, red, white, node_pos, 25)


def drawEdge(color, pos1, pos2):
    pygame.draw.line(screen, color, pos1, pos2)


def drawEdges(graph, locations, edge_color, weights_bool):
    for node in graph:
        node_pos = locations[node]


        for child in graph[node]:
            child_pos = locations[child]
            weight = graph[node][child]
            
            drawEdge(edge_color, node_pos, child_pos)
            
            if weights_bool: 
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


def drawGraph(graph, locations):
    drawNodes(graph, locations)
    drawEdges(graph, locations, white, True)
    

def drawText(text, font, color, x, y,):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))


# draw resulting shortest paths graph
def drawShortestPaths(graph, parents, locations):
    
    for node in parents:
        child = parents[node]

        if parents[node] != None:
            drawEdge(green, locations[node], locations[child])

        drawNode(node, red, white, locations[node], 25)


def main(): 
     
    parents = dijkstra(my_graph, 'A')[1]
    
    clock = pygame.time.Clock()

    # game loop
    running = True  
    while running:

        screen.fill(black)
        drawGraph(my_graph, locations)     # initial event for now, later initial event will be adding graph

        # creating UI
        mouse_pos = pygame.mouse.get_pos()
        mouse_posStr = str(mouse_pos)
        
        # dijkstra button
        rect_pos = (730, 800)
        pygame.draw.rect(screen, yellow, (730, 800, 190, 85), border_radius = 25)
        leftClick = pygame.mouse.get_pressed()[0] == True
       
        # dijkstra event
        if leftClick and rect_pos <= mouse_pos <= (rect_pos[0] + 190, rect_pos[1] + 85):
            drawNodes(my_graph, locations)
            drawShortestPaths(my_graph, parents, locations)
            pygame.draw.rect(screen, yellow, (730, 800, 190, 85), border_radius = 25)

        # create my own graph event
        '''
        if pygame.mouse.get_pressed()[0] == True:
            pygame.draw.circle(screen, yellow, mouse_pos, 25)
            drawText(mouse_posStr, text_font, red, mouse_pos[0], mouse_pos[1])
        '''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        
    
    pygame.quit()
    

main()
        