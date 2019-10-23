from simplex import Simplex
import functools
from matplotlib import pyplot as plt
import os


FIGURE_FOLDER = "figures"

class Diagram:

<<<<<<< Updated upstream
    def __init__(self):
=======
    def __init__(self, title = "diagram", use_sparse=False):
        self.title = title
>>>>>>> Stashed changes
        self.simplices = []

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
            first_occurence = self.pivots.index(self.pivots[column_index])
            while first_occurence < column_index and self.pivots[column_index] >= 0:
                sum(self.matrix, first_occurence, column_index)
                self.pivots[column_index] = find_pivot(
                    self.matrix, column_index)
                first_occurence = self.pivots.index(self.pivots[column_index])

    def build_diagram(self):
        self.diagram = []
        for index in range(self.simplices_number):
            if self.pivots[index] < 0:
                try:
                    end = self.pivots.index(index)
                    interval = (
                        self.simplices[index].dim, self.simplices[index].time, self.simplices[end].time)
                except ValueError:
                    interval = (self.simplices[index].dim,
                                self.simplices[index].time, "inf")
                self.diagram.append(interval)

    def print_diagram(self):
        for interval in self.diagram:
            print("{} {} {}".format(*interval))

    def display_diagram(self):
        diagram = self.diagram_sparse if self.use_sparse else self.diagram
        infinity = max([simplex.time for simplex in self.simplices])
        print(infinity)
        i = 0
        plt.figure()
        for interval in diagram:
            if interval[2] == 'inf':
                X = [interval[1], infinity + 2]
            else:
                X = interval[1:]
            plt.plot(X, [i,i], color = "C{}".format(interval[0]))
            i += 1
        axes = plt.gca()
        axes.set_xlim([0,infinity + 1])
        plt.title(self.title)
        plt.savefig(os.path.join(FIGURE_FOLDER, "{}.png".format(self.title)))


def find_pivot(matrix, column_index):
    index = len(matrix)-1
    while index >= 0 and matrix[index][column_index] == 0:
        index -= 1
    return index


def sum(matrix, source, target):
    for i in range(len(matrix)):
        matrix[i][target] = (matrix[i][target] + matrix[i][source]) % 2
