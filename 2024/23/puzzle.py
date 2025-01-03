from tqdm import tqdm
import networkx as nx

class Puzzle:
    def __init__(self, data):
        self.graph = nx.Graph()
        self.lanparties = [] #list of lists of connected nodes
        for connection in data:
            pc1, pc2 = connection.split('-')
            self.graph.add_edge(pc1, pc2)

    def identify_lanparties(self, size: int = 3):
        """ Stores a list of lists of inter-connected computers (i.e. every node is connected to every other node in the cluster), with a given cluster size. """
        for clique in nx.enumerate_all_cliques(self.graph): #i.e. every node is inter-connected
            if len(clique) == size:
                    self.lanparties.append(clique)
            elif len(clique) > size:
                #enumerate_all_cliques is sorted by size, so we can break here
                break
    
    def find_lanparties_by_computername(self, starts_with: str) -> list[list[str]]:
        """ Returns a set of lanparties (list of connected nodes) which contain at least one computer/node which's name starts with a spezific character. """
        matches = []
        for lanparty in self.lanparties:
            for node in lanparty:
                if node.startswith(starts_with):
                    matches.append(lanparty)
                    break
        return matches

    def do(self):
        self.identify_lanparties()

    def checksum(self, starts_with: str = None) -> int:
        if starts_with:
            return sum(1 for clusters in self.find_lanparties_by_computername(starts_with))
        else:
            return len(self.lanparties)
    
    def check_p2(self):
        pass

def load_puzzle(input_file: str) -> Puzzle:
    """Load Puzzle from input file (path)."""
    with open(input_file, 'r') as file:
        content = file.read()
        lines = content.strip().split('\n')
        data = [x for x in lines]
    return Puzzle(data)