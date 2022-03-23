# Student agent: Add your own agent here
from array import array
from collections import deque
from random import random, choice, randint
from unicodedata import name
from agents.agent import Agent
from store import register_agent
from threading import Thread


@register_agent("student_agent")
class StudentAgent(Agent):
    """
    A dummy class for your implementation. Feel free to use this class to
    add any helper functionalities needed for your agent.
    """
    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "Gigglebot;)"
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
        
        analyzer = Thread(target=self.analyze, name="Analyzer", args=(my_pos, chess_board, adv_pos, max_step), daemon=True)
        analyzer.start()
        analyzer.join()
        return my_pos, self.dir_map[dir]

    def analyze(self, my_pos: tuple, chess_board, adv_pos: tuple, max_steps: int):
        return self.move(my_pos, 1)

    @staticmethod
    def move(position: str, direction: int):
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        x, y = position
        movex, movey = moves[direction]
        pos = (x + movex, y + movey)
        return pos

    def putbarrier(self, position: tuple, direction: int):
        if self.is_barrier(position, direction):
            for i in range(0, 5):
                self.putbarrier(position, i)
        else:
            dir = self.dir_map.get(direction)
        return dir       

    def is_boundary(self, position: tuple, direction: int, dimension: int):
        x, y = position
        if direction == 3 or direction == 1:
            if x == 0 or x == (dimension - 1) :
                return True
        if direction == 0 or direction == 2:
            if y == 0 or y == (dimension - 1) :
                return True
        else:
            return False

    def is_barrier(self, board: array, position: tuple, direction: int, dimension: int):
        index = self.dir_map[dir]
        x, y = position
        value = board[x, y]
        if self.is_boundary(position, direction, dimension):
            return True
        return value[index]

    def barrier_count(self, position: tuple, dimension: int, board: array):
        x, y = position
        if 0 == x == dimension:
            barrier = barrier + 1
        if 0 == y == dimension:
            barrier = barrier + 1
        for i in self.dir_map.keys():
            if self.is_barrier(board, position, i, dimension):
                barrier = barrier + 1 
        return barrier
    
    
    def path(maxsteps: int):
        path = []
        return path[:-1]
    
    def bfs(adj, s):
        parent = {s: None}
        d = {s: 0}

        queue = deque()
        queue.append(s)

        while queue:
            u = queue.popleft()
            for n in adj[u]:
                if n not in d:
                    parent[n] = u
                    d[n] = d[u] + 1
                    queue.append(n)
            return parent, d
    
class Cell():
    def __init__(self, barriers):
        self.barrier = None # list of barries [up, down, left, right]
        self.up = None
        self.down = None
        self.left = None
        self.right = None

