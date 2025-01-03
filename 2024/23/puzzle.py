from tqdm import tqdm
import networkx as nx

class Puzzle:
    def __init__(self, data):
        self.graph = nx.Graph()
        self.lanparties = [] #list of lists of connected nodes
        for connection in data:
            pc1, pc2 = connection.split('-')
            self.graph.add_edge(pc1, pc2)

    def identify_lanparties(self, max_size: int):
        """ Stores a list of lists of inter-connected computers (i.e. every node is connected to every other node in the cluster), with a given cluster size. """
        self.lanparties = []
        self.matches = []
        max_size = self.graph.number_of_nodes() if max_size is None else max_size
        for clique in nx.enumerate_all_cliques(self.graph): #i.e. every node is inter-connected
            if 3 <= len(clique) <= max_size:
                    self.lanparties.append(clique)
            elif len(clique) > max_size:
                #enumerate_all_cliques is sorted by size, so we can break here
                break
    
    def find_lanparties_by_computername(self, starts_with: str) -> list[list[str]]:
        """ Returns a set of lanparties (list of connected nodes) which contain at least one computer/node which's name starts with a spezific character. """
        self.matches = []
        for lanparty in self.lanparties:
            for node in lanparty:
                if node.startswith(starts_with):
                    self.matches.append(lanparty)
                    break

    def do(self, starts_with: str = '', max_size: int = None):
        self.identify_lanparties(max_size)
        self.find_lanparties_by_computername(starts_with)

    def checksum(self) -> int:
        return len(self.matches)
    
    def check_p2(self):
        top = self.matches[-1] #or self.lanparties[-1]?
        top.sort()
        return ','.join(top)

def load_puzzle(input_file: str) -> Puzzle:
    """Load Puzzle from input file (path)."""
    with open(input_file, 'r') as file:
        content = file.read()
        lines = content.strip().split('\n')
        data = [x for x in lines]
    return Puzzle(data)