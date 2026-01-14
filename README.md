# dijkstra-visualization
Personal project for visualizing dijkstra's algorithm on a graph\
Contact: harshveerbanipal9@gmail.com

---

## Instructions to build
1. Install [Python](https://www.python.org/install) if you don't already have it
    > **Note:** At the time of writing this, I don't think pygame supports the latest version of Python (3.14), so you can instead install pygame-ce--which supports 3.14--or just an earlier version of python (3.13 or before)

2. Install [pygame](https://www.pygame.org/wiki/GettingStarted) or [pygame-ce](https://www.pypi.org/project/pygame-ce/)

3. Download the repo, access the folder in the terminal (`cd Downloads/dijkstra-visualization-main`), and enter `py -your_python_version -m main.py` (so if you downloaded Python 3.13, you would type `py -3.13 -m main.py`)

---

## Instructions to run/interface explained
You first start with a blank graph with exit, clear, draw, and select source buttons. 
- **EXIT:**             When clicked, program is exited

- **CLEAR:**            When clicked, screen is cleared to initial, empty graph state

- **DRAW:**             When clicked, the user can draw nodes by left clicking anywhere until draw is toggled off by clicking the button again. Once a node is initially drawn, a run button will appear.
    - **RUN:**          When clicked, it requires a source node to be selected and then runs dijkstra's algorithm on the user generated graph with the selected source node. This will cause init, prev, next, skip buttons to appear
        - **INIT:**     When clicked, the graph goes to its initial state
        - **PREV:**     When clicked, the graph goes to the previous state of dijkstra's until initial state is hit
        - **NEXT:**     When clicked, the graph goes to the next state of dijkstra's until final state is hit
        - **SKIP:**     When clicked, the graph goes to the final state of dijkstra's

- **SOURCE SELECT:**    When clicked, the user can select a source node for running dijkstra's on

When draw is toggled off and there are nodes on the screen, the user can click and drag on a node to move it. Right clicking on a node selects it, where after selecting at least two nodes, the user can press 'e' to form an edge between the selected nodes. If more than two nodes are selected, the edges are created in order of selection. Edges are initialized with a weight of 1, but the weight can be changed by clicking on the weight and typing the desired weight. 

### Bugs/Unexpected behavior
Note that while editing edge weight, if your weight is 1nand you press backspace, you can still change it to your desired weight, its just that visually it will still appear as 1 until you change it.
Also sometimes if you try to select a node and it isn't selecting, you can left click on it first and then try to select it again. 






    