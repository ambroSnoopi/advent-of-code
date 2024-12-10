from itertools import repeat
from tqdm import tqdm
    
class DiskMap:
    def __init__(self, data: str):
        self.image: list[tuple[int, int]] = [] #Tuple(block_size, file_id or -1)... we don't rly need this, do we? we could just "expand" directly, but whelp...
        self.files: list[int] = [] #blocksize
        self.spaces: list[int] = [] #blocksize
        for idx, digit in enumerate(data):
            block_size = int(digit)
            if idx % 2 == 0:
                file_id = int(idx/2) 
                self.image.append((block_size, file_id))
                self.files.append(block_size)
            else:
                self.image.append((block_size, -1))
                self.spaces.append(block_size)
        self.blocks: list[int] = self.expand()

    def expand(self) -> list[int]:
        """ Returns the file_id (or -1 if free) for each block in the image (block by block). """
        blocks = []
        for block_size, file_id in self.image:
            blocks.extend(repeat(file_id, block_size))
        return blocks

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return 'Blocks: ' + ''.join('.' if file_id == -1 else str(file_id) for file_id in self.blocks)

    def compact(self):
        """ Fill free spaces (processed from left to right) by shifting file blocks into them (processed from right to left), thereby fragmentating the files if necessary. """
        for idx in range(len(self.blocks)):
            try:
                while self.blocks[idx] == -1:
                    self.blocks[idx] = self.blocks.pop()
            except IndexError:
                break
    
    def checksum(self):
        sum = 0
        for idx, file_id in enumerate(self.blocks):
            if file_id > -1:
                sum += idx*file_id
        return int(sum)
    
    def compact_files(self):
        """ Shift entire files (processed from right to left) into free spaces (processed left to right), without fragmentating the files. """
        for file_id, file_size in tqdm(reversed(list(enumerate(self.files))), desc="Compacting Files", unit="file"):
            free_blocks = 0
            for idx, space_id in enumerate(self.blocks):
                if space_id == -1: 
                    free_blocks += 1
                    if free_blocks == file_size:
                        if idx > self.blocks.index(file_id):
                            break
                        for _ in range(file_size):
                            file_idx = self.blocks.index(file_id)
                            self.blocks[file_idx] = -1
                        self.blocks[idx-file_size+1:idx+1] = [file_id]*file_size #slicing in Python is end-exclusive...
                        break
                else:
                    free_blocks = 0


def load_puzzle(filename: str) -> DiskMap:
    with open(filename, 'r') as file:
        return DiskMap(file.read())