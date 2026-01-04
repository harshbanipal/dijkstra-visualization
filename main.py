import pygame

from math import inf
from priorityQue import MinPriorityQueue

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
blue = (0, 0, 255)


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
def text_font(size):
    font = pygame.font.SysFont('Arial', size)
    return font


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
    drawText(name, text_font(12), text_color, pos[0] - 5, pos[1] - 5)


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

                drawText(str(weight), text_font(12), red, weight_xpos + 5, weight_ypos + 5)


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




# added dijkstra algo here instead to avoid circular import when updating display within dijkstra
def dijkstra(G, s):

    """
    dijkstra implementation from my algorithms class homework 
    Graph format: G[u][v] = weight l(u, v) the weights might be integers or floats
    Returns:    d: a dict mapping node -> shortest distance from s, 
                parents: dict mapping node -> parent in shortest-path tree (s has parent None)
    """
    
    # edge cases
    for u, neighbors in G.items():
        for v, weight in neighbors.items():
            if weight < 0:
                raise ValueError("Dijkstra requires non-negative edge weights; found negative weight")


    # Collect all vertices (include isolated / sink nodes that might only appear as neighbors)
    vertices = set(G.keys())

    # pi: current best-known distances (keys)
    pi = {}

    # d: finalized shortest distances
    d = {}

    # parents in shortest paths tree
    parents = {s: None}

    # number of edges to reach source 
    numEdges = {}


    # your implementation from part 1
    Q = MinPriorityQueue()


    # Initialize source
    pi[s] = 0.0
    numEdges[s] = 0
    Q.insert(s, (0.0, 0))

    # create record of actions performed by dijkstras so i can animate
    record = []

    # Initialize all other vertices to infinity
    for v in vertices:        
        if v == s:
            # source is initialized to zero
            record.append(("init", s))
            continue
        pi[v] = inf
        numEdges[v] = inf
        parents.setdefault(v, None)
        Q.insert(v, (inf, inf))

        # node is initialized to infinity
        record.append(("init", v))


    # Main loop
    while Q.heap:
        u, (path_length_u, edge_length_u) = Q.extract_min()  # returns (element, priority)
        d[u] = path_length_u
        if path_length_u == inf:
            # node is unreachable from source
            record.append("fail discover", u)
            continue
        
        # check if node is undiscovered
        record.append(("discover", u))

        # For each neighbor v of u
        for v, weight_uv in G[u].items():
            # Update the best path length to v using edge (u, v) if it improves pi[v]

            # check if current best dist > new dist
            record.append("check dist", u, v, weight_uv)

            if (pi[v], numEdges[v]) > (d[u] + weight_uv, edge_length_u + 1):
                new_priority = (d[u] + weight_uv, edge_length_u +1)
                Q.decrease_key(v, new_priority)
                pi[v] = new_priority[0]
                parents[v] = u
                numEdges[v] = edge_length_u + 1

                # edge being added to shortest paths tree
                record.append("update", u, v, weight_uv)
        
        record.append("finalize", u)


    return d, parents



def main(): 
     
    
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
        pygame.draw.rect(screen, yellow, (730, 800, 190, 85), border_radius = 25)
        drawText("shortest paths", text_font(12), black, 775, 830)
        leftClick = pygame.mouse.get_pressed()[0] == True
        
        # dijkstra event
        parents = dijkstra(my_graph, 'A')[1]
        if leftClick and (730 <= mouse_pos[0] <= 920) and (800 <= mouse_pos[1] <= 885):
            drawNodes(my_graph, locations)
            drawShortestPaths(my_graph, parents, locations)
            pygame.draw.rect(screen, (255, 200, 75), (730, 800, 190, 85), border_radius = 25)
            drawText("shortest paths", (text_font(12)), black, 775, 830)
            

        # create my own graph event
            '''
            in this event, 
            1)  let user drop nodes anywhere on screen
                    -   record location of node and give the node key '0' and add 1 to key per node added
                    -   create hashtable of nodes with empty values
            2)  when two nodes are clicked on, create an edge between those two nodes
                    -   give default weight of 1 to edge and add relationship to hash table: n1: {n2: 1}, n2: {n1: 1}
                    -   record edge parents?
            3)  maybe when user clicks on any sequence of nodes, each click is added to a queue and then create edges
                in the order the user clicked the nodes in
                    -   give default weight of 1, add relationships to hashtable?
                            pop node from queue, peek at next node and update hash table
            4)  user can click on an edge and edit the edge weight
                    -   check if user clicks on rect, and then take in user input for weight-- check nodes between edges
                        and update hashtable
            '''
        '''
        if pygame.mouse.get_pressed()[0] == True:
            pygame.draw.circle(screen, yellow, mouse_pos, 25)
            drawText(mouse_posStr, text_font(12), red, mouse_pos[0], mouse_pos[1])
        '''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        
    
    pygame.quit()
    

main()
        