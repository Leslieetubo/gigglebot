# Student agent: Add your own agent here
from collections import defaultdict, namedtuple
from random import random, choice, randint
from shutil import move
from agents.agent import Agent
from store import register_agent
from threading import Thread

graph = defaultdict(list)

@register_agent("student_agent")
class StudentAgent(Agent):
    """
    A dummy class for your implementation. Feel free to use this class to
    add any helper functionalities needed for your agent.
    """
    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "Thanos"
        self.autoplay = True
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }
    
    def step(self, chess_board, my_pos, adv_pos, max_step):
        dim = (max_step * 2) - 1
        i, j = my_pos
        pos_bars = chess_board[i, j]
        """
        Implement the step function of your agent here.
        You can use the following variables to access the chess board:
        - chess_board: a numpy array of shape (x_max, y_max, 4)
        - my_pos: a tuple of (x, y)
        - adv_pos: a tuple of (x, y)
        - max_step: an integer

        You should return a tuple of ((x, y), dir),
        where (x, y) is the next position of your agent and dir is the direction of the wall
        you want to put on.

        Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
        """
        # dummy return
        
        # analyzer = Thread(target=self.analyze, name="Analyzer", args=(my_pos, chess_board, adv_pos, max_step), daemon=True)
        # analyzer.start()
        # analyzer.join()
        self.analyze(my_pos, chess_board, adv_pos, max_step)
        return my_pos, self.dir_map[dir]

    def analyze(self, my_pos: tuple, chess_board, adv_pos: tuple, max_steps: int):
        dimension = (max_steps * 2) - 1
        print("=" * 30)
        print("Starting Thread...")
        x, y = my_pos
        graphView = Graph()
        node = Vertex(l=None, r=None, u=None, d=None, adv=False, x_val=x, y_val=y)
        for i in range(max_steps):
            for d in range(4):
                if self.is_barrier(chess_board, my_pos, d, dimension) == False:
                    next_x, next_y = self.move(my_pos, d)
                    nextnode = Vertex(l=None, r=None, u=None, d=None, adv=False, x_val=next_x, y_val=next_y)
                    if d  == 0:
                        node.up = nextnode
                    if d == 1:
                        node.right = nextnode
                    if d == 2:
                        node.down = nextnode
                    if d == 3:
                        node.left = nextnode
                    # graphView.setVertex(nextnode)
                    # graphView.setEdge({node, nextnode})
                    # node = nextnode
        print(node)
        print("-" * 30)
        print("Thread just ended")
        print("=" * 30)

    def move(self, position: tuple, direction: int):
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        x, y = position
        movex, movey = moves[direction]
        pos = (x + movex, y + movey)
        return pos

    def putbarrier(self, position: tuple, direction: int):
        if self.is_barrier(position, direction):
            for i in range(4):
                self.putbarrier(position, i)
        else:
            dir = self.dir_map.get(direction)
        return dir       

    def is_boundary(self, position: tuple, dimension: int):
        x, y = position
        return 0 == x == dimension or 0 == y == dimension

    def is_barrier(self, board, position: tuple, direction: int, dimension: int):
        x, y = position
        value = board[x, y]
        if self.is_boundary(position, dimension):
            return True
        return value[direction]

    def barrier_count(self, position: tuple, dimension: int, board):
        barrier = 0
        for i in self.dir_map.values():
            if self.is_barrier(board, position, i, dimension):
                barrier = barrier + 1 
        return barrier

class Vertex(object):
    
    def __init__(self, l, r, u, d, adv, x_val, y_val):
        self.name = "cell (" + str(x_val) + "," + str(y_val) + ")"
        self.has_enemy = adv
        self.right = r
        self.left = l
        self.up = u
        self.down = d
        self.x_val = x_val
        self.y_val = y_val

    def __repr__(self):
        return str({
            'name': self.name,
            'has_enemy': self.has_enemy,
            'right': self.right,
            'left': self.left,
            'up': self.up,
            'down': self.down,
            'x': self.x_val,
            'y' : self.y_val
        })

class Graph(object):

    # G = (V, E)
    # V = Vertext
    # E = Edge: (V1 - V2)

    graph =  defaultdict(list)

    def __init__(self, graphdic = None):
        if graphdic is None:
            graphdic = {}
        self.graphdic = graphdic

    def getVertices(self):
        return list(self.graphdic.keys())

    def getEdges(self):
        return list(self.graphdic.values())

    def setVertex(self, vertex):
        if vertex.name not in self.graphdic:
         self.graphdic[vertex] = []

    def setEdge(self, edge):
        edge = set(edge)
        (vertex_1, vertex_2) = tuple(edge)
        if vertex_1 in self.graphdic:
            self.graphdic[vertex_1].append(vertex_2)
        else:
            self.graphdic[vertex_1] = [vertex_2]
    
    def find_distinct_edges(self):
        edgename = []
        for vertex in self.graphdic:
            for next_vertex in self.graphdic[vertex]:
                if {next_vertex, vertex} not in edgename:
                    edgename.append({vertex, next_vertex})
        return edgename
