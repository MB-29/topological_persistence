from simplex import Simplex
import functools
from matplotlib import pyplot as plt
import os


FIGURE_FOLDER = "figures"
BARCODE_FOLDER = "barcodes"

class Diagram:

    def __init__(self, title = "diagram", use_sparse=False):
        
        self.simplices = []
        self.use_sparse = use_sparse
        self.title = title

    def read_data(self, file_path):
        with open(file_path, 'r') as data:
            line = data.readline()
            while line:
                self.simplices.append(Simplex.simplex_from_line(line))
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
        self.pivots = [ max(column) if len(column) > 0 else - 1 for column in self.sparse_matrix]    
        self.pivots_inverse = [set() for _ in range(self.simplices_number)]
        for k in range(self.simplices_number):
            if self.pivots[k] >= 0:
                self.pivots_inverse[self.pivots[k]].add(k)

        print(f'Starting reduction')
        for column_index in range(self.simplices_number):
            if self.pivots[column_index] >= 0:
                first_occurence = min(self.pivots_inverse[self.pivots[column_index]])
                while self.pivots[column_index] >= 0 and first_occurence < column_index:
                    source, target = self.sparse_matrix[first_occurence], self.sparse_matrix[column_index]
                    union, intersection = source.union(target), source.intersection(target)
                    self.sparse_matrix[column_index] = union.difference(intersection) 
                    column = self.sparse_matrix[column_index]
                    pivot_row = max(column) if len(column) > 0 else -1
                    self.pivots_inverse[self.pivots[column_index]].remove(column_index)
                    self.pivots[column_index] = pivot_row
                    if pivot_row >= 0:
                        self.pivots_inverse[pivot_row].add(column_index)
                        first_occurence = min(self.pivots_inverse[self.pivots[column_index]])
                    #first_occurence = self.pivots.index(pivot_row)
                if column_index % 1000 == 0:
                    print(f'index = {column_index}')
            

    def build_diagram(self):
        self.diagram = []
        index = 0
        for pivot in self.pivots:
            if pivot < 0:
                try:
                    end = self.pivots_inverse[index].pop()
                    interval = (
                        self.simplices[index].dim, self.simplices[index].time, self.simplices[end].time)
                except KeyError:
                    interval = (self.simplices[index].dim,
                                self.simplices[index].time, "inf")
                self.diagram.append(interval)
            index += 1

    def print_diagram(self):
        S = ""
        file_path = os.path.join(BARCODE_FOLDER, "{}_barcode.txt".format(self.title))
        for interval in self.diagram:
            S += "{} {} {}\n".format(*interval)
        with open(file_path, 'w+') as f:
            f.write(S)
        

    def display_diagram(self):
        diagram = self.diagram

        infinity = max([simplex.time for simplex in self.simplices]) + 1
        i = 0
        plt.figure()
        for interval in diagram:
            if interval[2] == 'inf':
                X = [interval[1], infinity + 2]
            else:
                X = interval[1:]
            plt.plot(X, [i,i], color = "C{}".format(interval[0]) if interval[0]<10 else "black")
            i += 1
            if i%20 == 0:
                print("step {} out of {}".format(i, len(diagram)))
        axes = plt.gca()
        axes.set_xlim([0,infinity + 1])
        plt.title(self.title)
        plt.savefig(os.path.join(FIGURE_FOLDER, "{}.png".format(self.title)))


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

