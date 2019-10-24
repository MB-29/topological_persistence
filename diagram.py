from simplex import Simplex
import functools
from matplotlib import pyplot as plt
import os


FIGURE_FOLDER = "figures"
BARCODE_FOLDER = "barcodes"

class Diagram:

    def __init__(self, title = "diagram", use_sparse=False):
        
        #initialise list of simplices
        self.simplices = []

        #Boolean to determine whether or not to use sparse representation of matrix
        self.use_sparse = use_sparse

        #String title to name output files
        self.title = title


    #method to read diagram data from a file with the given format
    def read_data(self, file_path):
        with open(file_path, 'r') as data:
            line = data.readline()
            while line:
                self.simplices.append(Simplex.simplex_from_line(line))
                line = data.readline()
        self.simplices_number = len(self.simplices)


    #method for printing data in Diagram object, used for debugging
    def to_string(self):
        string = 'Diagram object with following simplices :\n'
        for simplex in self.simplices:
            string += f'time = {simplex.time}, dim = {simplex.dim}, vertices = {simplex.vertices}\n'
        return string

    #method to sort the list of simplices, such that they have an increasing apperance time, and in case of equality increasing dimension
    def sort_simplices(self):
        self.order_dictionary = {}
        self.simplices = sorted(
            self.simplices, key=functools.cmp_to_key(Simplex.compare))

        # The order dictionary allows us to quickly find the index of a simplex from its vertices
        # To have a unique representation of a simplex, we always store the vertices as a sorted tuple
        # There is no need to keep track of the orientation of simplices since our field is Z/2Z
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

        #The sparse matrix is a list of sets
        #Each column's set contains the lines which intersect the column a value of 1 
        self.sparse_matrix = [set() for _ in range(self.simplices_number)]

        #To build the matrix we add into the column corresponding to a simplex the indices of the columns corresponding to all the elements of the simplex's boundary
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
        if self.use_sparse:
            self.reduce_sparse_matrix()
            return

        #self.pivots_inverse = [set() for _ in range(self.simplices_number)]

        # Find pivots
        self.pivots = []
        for j in range(self.simplices_number):
            self.pivots.append(find_pivot(self.matrix, j))

        # Reduce
        # I was too lazy to optimise the non-sparse method so it's slow, using a naive way to find the first occurence of a pivot
        for column_index in range(len(self.matrix)):
            first_occurence = self.pivots.index(self.pivots[column_index])
            while first_occurence < column_index and self.pivots[column_index] >= 0:
                sum(self.matrix, first_occurence, column_index)
                self.pivots[column_index] = find_pivot(self.matrix, column_index)
                first_occurence = self.pivots.index(self.pivots[column_index])

    def reduce_sparse_matrix(self):
   
        # find pivots
        self.pivots = [ max(column) if len(column) > 0 else - 1 for column in self.sparse_matrix]    

        # To help find the first occurance of a pivot quickly, we build self.pivots_inverse,
        # for each potential value v of a pivot it contains all the indices of column which have v as a pivot
        self.pivots_inverse = [set() for _ in range(self.simplices_number)]
        for k in range(self.simplices_number):
            if self.pivots[k] >= 0:
                self.pivots_inverse[self.pivots[k]].add(k)

        print(f'Starting reduction')
        for column_index in range(self.simplices_number):
            if self.pivots[column_index] >= 0: #check if there is a pivot (a pivot of -1 means the column is zeroed out)

                #find the index of the first column with the same pivot
                first_occurence = min(self.pivots_inverse[self.pivots[column_index]])

                while self.pivots[column_index] >= 0 and first_occurence < column_index:

                    #if there is a column with a lower index and the same pivot, we add them together
                    source, target = self.sparse_matrix[first_occurence], self.sparse_matrix[column_index]
                    union, intersection = source.union(target), source.intersection(target)
                    self.sparse_matrix[column_index] = union.difference(intersection) 

                    #find the new pivot
                    column = self.sparse_matrix[column_index]
                    pivot_row = max(column) if len(column) > 0 else -1

                    #update self.pivots, self.pivots_inverse and first occurrence
                    self.pivots_inverse[self.pivots[column_index]].remove(column_index)
                    self.pivots[column_index] = pivot_row
                    if pivot_row >= 0: #if pivot_row<0 then the column is zeroed out, we just move on
                        self.pivots_inverse[pivot_row].add(column_index)
                        first_occurence = min(self.pivots_inverse[self.pivots[column_index]])

            

    def build_diagram(self):
        self.diagram = []
        index = 0
        for pivot in self.pivots:
            if pivot < 0: #column zeroed out, corresponding simplex is the beginning of a bar
                try: 
                    #we look for a pivot on the line, if we find one, the corresponding simplex is the end of the bar
                    if self.use_sparse:
                        end = self.pivots_inverse[index].pop() 
                    else:
                        end = self.pivots.index(index)
                    interval = (self.simplices[index].dim, self.simplices[index].time, self.simplices[end].time)


                except(KeyError, ValueError):
                    # if we don't find one, the bar goes to infinity
                    interval = (self.simplices[index].dim,
                                self.simplices[index].time, "inf")
                self.diagram.append(interval)
            index += 1


    # method to save barcode 
    def print_diagram(self):
        S = ""
        file_path = os.path.join(BARCODE_FOLDER, "{}_barcode.txt".format(self.title))
        for interval in self.diagram:
            S += "{} {} {}\n".format(*interval)
        with open(file_path, 'w+') as f:
            f.write(S)
        
    # method to display barcode, each dimension corresponds to a color
    def display_diagram(self):
        diagram = self.diagram

        #lines that go to infinity don't actually go to infinity but go further than any other and off the right of the graph
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
    # The function returns -1 iff no pivot is found
    index = len(matrix)-1
    while index >= 0 and matrix[index][column_index] == 0:
        index -= 1
    return index


#performs sum of 2 columns of matrix (indices source and target), result goes in target
def sum(matrix, source, target):
    for i in range(len(matrix)):
        matrix[i][target] = (matrix[i][target] + matrix[i][source]) % 2

