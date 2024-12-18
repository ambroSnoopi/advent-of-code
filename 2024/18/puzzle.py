from enum import Enum
from dataclasses import dataclass
import numpy as np
from tqdm import tqdm
import networkx as nx
import matplotlib.pyplot as plt

class Ptype(Enum):
    WALL  = '#'
    EMPTY = '.'
    GOAL = 'E'

    def __str__(self):
        return self.value

@dataclass
class Cell:
    x: int
    y: int
    ptype: Ptype #transient

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (self.x, self.y) == (other.x, other.y)
        return False
    
    def __str__(self):
        return str(self.ptype)
    
    def to_node(self):
        return (self.y, self.x)

class Map:
    def __init__(self, byte_list: list[tuple[int, int]], falling_bytes: int, map_size: int):
        self.cells = np.array([
            [Cell(x, y, Ptype.EMPTY) for x in range(map_size)]
            for y in range(map_size)
        ], dtype=object)
        self.doomed = byte_list[falling_bytes:]
        self.corrupted = byte_list[:falling_bytes]
        self.start: Cell = self.cells[0][0]
        self.goal: Cell = self.cells[map_size-1][map_size-1]
        
        self.graph = nx.grid_2d_graph(map_size, map_size)
        for x, y in self.corrupted: #or just in byte_list[:falling_bytes] and remove self.corrupted
            self.cells[y][x].ptype = Ptype.WALL
            self.graph.remove_node((y, x))

    def find_critical_corruption(self) -> tuple[int, int]:
        """ Drops another byte until the critical path from start to goal is broken. Returns the byte that caused the critical corruption. """
        #articulation_points = list(nx.articulation_points(self.graph)) # all nodes that would disconnect the graph if removed
        for byte in tqdm(self.doomed, desc="Finding critical corruption...:", unit="byte"):
            x, y = byte
            self.cells[y][x].ptype = Ptype.WALL
            self.graph.remove_node((y, x))
            if not nx.has_path(self.graph, self.start.to_node(), self.goal.to_node()):
                return (x, y)

    def do(self):
        self.shortest_path = nx.shortest_path(self.graph, self.start.to_node(), self.goal.to_node())

    def checksum(self) -> int:
        return len(self.shortest_path)-1
    
    def viz(self, title="Grid Cell Connections"):
        """ Draws a plot of the graph. """
        plt.figure(figsize=(15, 15))
        
        # Get positions for plotting
        pos = {(i, j): (j, -i) for i, j in self.graph.nodes()}
        
        # Draw the graph
        nx.draw_networkx_edges(self.graph, pos, edge_color='lightgray', alpha=0.5)
        
        # Draw nodes
        node_colors = ['lightblue' for _ in self.graph.nodes()]
        
        # Highlight start and end nodes
        start_idx = list(self.graph.nodes()).index(self.start.to_node())
        end_idx = list(self.graph.nodes()).index(self.goal.to_node())
        node_colors[start_idx] = 'green'
        node_colors[end_idx] = 'red'
        
        nx.draw_networkx_nodes(self.graph, pos, 
                            node_color=node_colors,
                            node_size=20)
        
        nx.draw_networkx_labels(self.graph, pos, 
                            {self.start.to_node(): 'Start', self.goal.to_node(): 'End'},
                            font_size=12)
        
        # Plot
        plt.title(title)
        plt.axis('equal')
        plt.show()

def load_puzzle(input_file: str, falling_bytes: int, map_size: int) -> Map:
    with open(input_file, 'r') as file:
        data = file.read()
        byte_list = [tuple(map(int, line.split(','))) for line in data.splitlines()]
        return Map(byte_list, falling_bytes, map_size)