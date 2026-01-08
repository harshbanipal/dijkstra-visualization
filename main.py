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
gray = (150, 150, 150)
orange = (255, 172, 121)

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


# get source
def getSource(parents):
    for parent in parents:
        if parents[parent] == None:
            source = parent
    return source


# text font
def text_font(size):
    font = pygame.font.SysFont('Arial', size)
    return font


# node class
class Node():
    def __init__(self, name, x, y, color):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        
        
        self.location = (x,y)
        self.children = {}
        self.clicked = False

    def draw(self, surface):
        action = False

        pos = pygame.mouse.get_pos()

        self.rect = pygame.draw.circle(surface, self.color, self.location, 25)

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == True and self.clicked == False:
                self.clicked = True
                action = True
                print("node " + self.name + " clicked")
        
        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False

        pygame.draw.circle(surface, self.color, self.location, 25)
        drawText(self.name, text_font(12), red, self.x - 5, self.y - 5)

        return action



# button class
class Button():
    def __init__(self, x, y, width, length, color, label, label_size, label_x, label_y, border_rad):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.color = color
        self.label = label
        self.label_x = label_x
        self.label_y = label_y
        self.label_size = label_size
        self.border_rad = border_rad

        self.rect = pygame.Rect(self.x, self.y, self.width, self.length)
        self.clicked = False 

    def draw(self, surface):
        action = False

        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == True and self.clicked == False:
                self.clicked = True
                action = True
                print(self.label + " click")

        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False


        pygame.draw.rect(surface, self.color, self.rect, border_radius = self.border_rad)
        drawText(self.label, text_font(self.label_size), white, self.label_x, self.label_y)

        return action

# create button instances
exit_button = Button(800, 100, 150, 50, gray, "exit", 50, 825, 95, 15)
prev_button = Button(300, 800, 100, 75, gray, "prev", 20, 330, 820, 10)
next_button = Button(600, 800, 100, 75, gray, "next", 20, 630, 820, 10)
run_button = Button(450, 800, 100, 75, gray, "run", 20, 480, 820, 10)




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
    drawEdges(graph, locations, white, True)
    drawNodes(graph, locations)
    

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
            record.append(("fail discover", u))
            continue
        
        # check if node is undiscovered
        record.append(("discover", u))

        # For each neighbor v of u
        for v, weight_uv in G[u].items():
            # Update the best path length to v using edge (u, v) if it improves pi[v]

            # check if current best dist > new dist
            record.append(("check dist", u, v, pi[v], d[u], weight_uv))

            if (pi[v], numEdges[v]) > (d[u] + weight_uv, edge_length_u + 1):
                new_priority = (d[u] + weight_uv, edge_length_u +1)
                Q.decrease_key(v, new_priority)
                pi[v] = new_priority[0]
                parents[v] = u
                numEdges[v] = edge_length_u + 1

                # edge being added to shortest paths tree
                record.append(("update", u, v, d[u] + weight_uv))
        
        record.append(("finalize", u))


    return d, parents, record

# parse through record
def parseRecord(record, index):
    parents = dijkstra(my_graph, 'A')[1]
    source = getSource(parents)

    path_lengths = {}
    revealed = set()   

    #   go until index given-- allows me to create entire state of dijkstras in one call of parseRecord, 
    #   easy to go back and forth between states
    for i in range(index + 1):
        # init, discover, and finalize events
        event = record[i][0]
        node = record[i][1]
        node_loc = locations[node]
        node_x = node_loc[0]
        node_y = node_loc[1]

        # other events
        if len(record[i]) > 2:
            child = record[i][2]
            child_loc = locations[child]
            child_x = child_loc[0]
            child_y = child_loc[1]

            # check dist
            if event == "check dist":
                pi = record[i][3]
                d = record[i][4]
                edge_len = record[i][5]
            # update
            else:
                path_len = record[i][3]


        if event == "init": 
            # display starting path dist by node (either inf or 0)
            # change color of node to gray

            drawNode(node, red, gray, (node_x, node_y), 25)

            if node == source:
                path_lengths[node] = 0
                #drawText("0", text_font(15), blue, node_x - 25, node_y - 40)

                
            else:
                path_lengths[node] = inf
                #drawText("inf", text_font(15), blue, node_x - 25, node_y - 40)
            
            revealed.add(node)


        elif event == "discover":
            # change color of node to white / light yellow
            drawNode(node, red, yellow, (node_x, node_y), 25)

        elif event == "check dist":
            # draw light yellow line or arrow from node x to y
            # display above node if the path it has is > than the edge weight plus path to node x
            
            if i == index: 
                drawEdge(yellow, node_loc, child_loc)
                conditional = str(d) + ' + ' + str(edge_len) + ' < ' + str(pi) + ' ?'
                drawText(conditional, text_font(20), white, child_x - 50, child_y + 25)


        elif event == "update":
            # change path dist of node to new path dist
            # indicate path dist has been updated
            path_lengths[child] = path_len

            if i == index:
                drawText("UPDATE", text_font(15), white, child_x - 25, child_y - 55)


            #print("update printed at index " + str(index))
            updated_dist = str(path_len)
            #drawText(updated_dist, text_font(15), orange, child_x - 25, child_y - 40)
            revealed.add(child)

        else:
            # if record index is "finalize"
            # change color of node to green, add edge to shortest dist tree
            # write done next to node
            if node != source:
                for parent in parents[node]:
                    parent_loc = locations[parent]
                    drawEdge(green, node_loc, parent_loc)

            drawNode(node, red, green, (node_x, node_y), 25)

            drawText("DONE", text_font(10), green, node_x + 25, node_y - 25)

            revealed.add(node)
    

    # draw only path distances that are revealed after parsing record indicies
    for node in revealed:
        dist = path_lengths[node]
        if dist == inf:
            text = "inf"
            color = blue
        elif dist == 0:
            text = "0"
            color = yellow
        else:
            text = str(dist)
            color = orange
        
        drawText(text, text_font(15), color, locations[node][0] - 25, locations[node][1] - 40)    


    print(path_lengths)
    print(revealed)

    return

def main(): 
    
    user_graph = {}
    user_locations = {}
    node_objs = set()
    x = 0

    '''
    parents = dijkstra(my_graph, 'A')[1]
    print(parents)
    record = dijkstra(my_graph, 'A')[2]
    print(str(record))
    '''
    clock = pygame.time.Clock()

    dijkstra_running = False
    index = -1


    # game loop
    running = True  
    while running:

        screen.fill(black)
        #drawGraph(my_graph, locations)     # initial event for now, later initial event will be adding graph

        mouse_pos = pygame.mouse.get_pos()
        
        if exit_button.draw(screen):
            running = False

 
        for node in user_locations:
            new_node = Node(str(node), user_locations[node][0], user_locations[node][1], white)
            #new_node.draw(screen)
            node_objs.add(new_node)

        for node_obj in node_objs: 
            if node_obj.draw(screen):
                node_obj.color = gray


        #print(user_locations)


        '''
        run through dijkstra on graph
        if run_button.draw(screen):
            dijkstra_running = True
            index = 0

        if prev_button.draw(screen):
            index = max(index - 1, -1)
            
        if next_button.draw(screen):
            index = min(index + 1, len(record) - 1)
           
        if index >= 0:
            parseRecord(record, index)

        '''


        
        '''
        # dijkstra button
        pygame.draw.rect(screen, yellow, (730, 800, 190, 85), border_radius = 25)
        drawText("shortest paths", text_font(12), black, 775, 830)
        leftClick = pygame.mouse.get_pressed()[0] == True
        '''


        '''
        # dijkstra event
        if leftClick and (730 <= mouse_pos[0] <= 920) and (800 <= mouse_pos[1] <= 885):
            drawShortestPaths(my_graph, parents, locations)
            drawNodes(my_graph, locations)
            pygame.draw.rect(screen, (255, 200, 75), (730, 800, 190, 85), border_radius = 25)
            drawText("shortest paths", (text_font(12)), black, 775, 830)
        '''

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                # check if user is clicking on node (don't want to draw another node)
                if event.button == 1:
                    # draw node, add to user_locations and user_graph, increment index
                    user_locations[x] = mouse_pos
                    user_graph[x] = {}
                    x += 1
                    print("created node " + str(x))


        pygame.display.flip()
        
    
    pygame.quit()
    

main()
        