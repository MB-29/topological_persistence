from simplex import Simplex
import functools


class Diagram:

    def __init__(self):
        self.simplices = []

    def read_data(self, file_path):
        with open(file_path, 'r') as data:
            line = data.readline()
            while line:
                self.simplices.append(Simplex(line))
                line = data.readline()
        self.simplices_number = len(self.simplices)

    def to_string(self):
        for simplex in self.simplices:
            print(
                f'time = {simplex.time}, dim = {simplex.dim}, vertices = {simplex.vertices}')

    def sort_simplices(self):
        self.order_dictionary = {}
        self.simplices = sorted(
            self.simplices, key=functools.cmp_to_key(Simplex.compare))
        for index in range(len(self.simplices)):
            self.order_dictionary.update(
                {self.simplices[index].vertices: index})

    def build_matrix(self):
        self.matrix = [[0 for n in range(self.simplices_number)]
                                         for m in range(self.simplices_number)]
        for index in range(len(self.simplices)):
            if len(self.simplices[index].vertices) == 1:
                continue
            boundary = self.simplices[index].boundary()
            for edge in boundary:
                order = self.order_dictionary[edge]
                self.matrix[order][index] = 1

    def reduce_matrix(self):
        self.pivots = []
        for j in range(self.simplices_number):
            self.pivots.append(find_pivot(self.matrix, j))

        for column_index in range(len(self.matrix)):
            print(f'column index ={column_index}')
            first_occurence = self.pivots.index(self.pivots[column_index])
            while first_occurence < column_index and self.pivots[column_index] >= 0:
                sum(self.matrix, first_occurence, column_index)
                self.pivots[column_index] = find_pivot(self.matrix, column_index)
                first_occurence = self.pivots.index(self.pivots[column_index])

    def build_diagram(self):
        self.diagram = []
        for index in range(len(self.simplices_number)):
            if self.pivots[index] < 0 :
                try :
                    self.pivots.index(index)
                except ValueError:
                    interval = [self.simplices[index].time
                    self.diagram.append()





def find_pivot(matrix, column_index):
    index = len(matrix)-1
    while index >=0 and matrix[index][column_index] == 0:
        index -= 1
    return index

def sum(matrix, source, target):
    for i in range(len(matrix)):
        matrix[i][target] = (matrix[i][target] + matrix[i][source] )%2

