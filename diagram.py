from simplex import Simplex
import functools


class Diagram:

    def __init__(self, use_sparse=False):
        self.simplices = []
        self.use_sparse = use_sparse

    def read_data(self, file_path):
        with open(file_path, 'r') as data:
            line = data.readline()
            while line:
                self.simplices.append(Simplex(line))
                line = data.readline()
        self.simplices_number = len(self.simplices)

    def to_string(self):
        string = 'Diagram object with following simplices :\n'
        for simplex in self.simplices:
            string += f'time = {simplex.time}, dim = {simplex.dim}, vertices = {simplex.vertices}\n'
        return string

    def sort_simplices(self):
        self.order_dictionary = {}
        self.simplices = sorted(
            self.simplices, key=functools.cmp_to_key(Simplex.compare))
        for index in range(len(self.simplices)):
            self.order_dictionary.update(
                {self.simplices[index].vertices: index})

    def build_matrix(self):
        if self.use_sparse:
            self.build_sparse_matrix()
            return

        self.matrix = [[0 for n in range(self.simplices_number)]
                       for m in range(self.simplices_number)]
        index = 0
        for simplex in self.simplices:
            if len(simplex.vertices) == 1:
                index += 1
                continue
            boundary = simplex.boundary()
            for edge in boundary:
                order = self.order_dictionary[edge]
                self.matrix[order][index] = 1
            index += 1

    def build_sparse_matrix(self):
        self.sparse_matrix = [set() for _ in range(self.simplices_number)]
        index = 0
        for simplex in self.simplices:
            if len(simplex.vertices) == 1:
                index += 1
                continue
            boundary = simplex.boundary()
            for edge in boundary:
                order = self.order_dictionary[edge]
                self.sparse_matrix[index].add(order)
            index += 1
        self.matrix = self.sparse_matrix

    def reduce_matrix(self):

        # Find pivots
        if self.use_sparse:
            self.reduce_sparse_matrix()
            return
        self.pivots = []
        for j in range(self.simplices_number):
            self.pivots.append(find_pivot(self.matrix, j))
        print(f'pivots : {self.pivots}')

        # Reduce
        for column_index in range(len(self.matrix)):
            first_occurence = self.pivots.index(self.pivots[column_index])
            while first_occurence < column_index and self.pivots[column_index] >= 0:
                sum(self.matrix, first_occurence, column_index)
                self.pivots[column_index] = find_pivot(
                    self.matrix, column_index)
                first_occurence = self.pivots.index(self.pivots[column_index])

    def reduce_sparse_matrix(self):
   
        # find pivots
        self.pivots_sparse = [ max(column) if len(column) > 0 else - 1 for column in self.sparse_matrix]    
        self.pivots = self.pivots_sparse

        print(f'Starting reduction')
        for column_index in range(self.simplices_number):
            first_occurence = self.pivots.index(self.pivots[column_index])
            while first_occurence < column_index and self.pivots[column_index] >= 0:
                source, target = self.sparse_matrix[first_occurence], self.sparse_matrix[column_index]
                intersection, union = source.union(target), source.intersection(target)
                self.sparse_matrix[column_index] = union.difference(intersection) 
                column = self.sparse_matrix[column_index]
                pivot_row = max(column) if len(column) > 0 else -1
                self.pivots[column_index] = pivot_row
                first_occurence = self.pivots.index(pivot_row)
            if column_index % 1000 == 0:
                print(f'index = {column_index}')
            

    def build_diagram(self):
        self.diagram = []
        index = 0
        for pivot in self.pivots:
            if pivot < 0:
                try:
                    end = self.pivots.index(index)
                    interval = (
                        self.simplices[index].dim, self.simplices[index].time, self.simplices[end].time)
                except ValueError:
                    interval = (self.simplices[index].dim,
                                self.simplices[index].time, "inf")
                self.diagram.append(interval)
            index += 1

    def build_diagram_sparse(self):
        self.diagram_sparse = []

        for pivot in self.pivots_sparse:
            row, column = pivot[0], pivot[1]
            if pivot[0] >= 0:
                interval = (self.simplices[row].dim,
                                self.simplices[row].time, self.simplices[column].time)
            else:
                interval = ('dim', 'start','inf')
            self.diagram_sparse.append(interval)

    def print_diagram(self):
        for interval in self.diagram:
            print("{} {} {}".format(*interval))


def find_pivot(matrix, column_index):
    # The function returns a negative integer iff no pivot is found
    index = len(matrix)-1
    while index >= 0 and matrix[index][column_index] == 0:
        index -= 1
    return index


def find_first_occurence(pivots_sparse, row, column_index):
    index = 0
    for pivot in pivots_sparse:
        if pivot[0] == row:
            return pivot[1]
        index += 1


def sum(matrix, source, target):
    for i in range(len(matrix)):
        matrix[i][target] = (matrix[i][target] + matrix[i][source]) % 2

