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
        self.sparse_matrix = []
        index = 0
        for simplex in self.simplices:
            if len(simplex.vertices) == 1:
                index += 1
                continue
            boundary = simplex.boundary()
            for edge in boundary:
                order = self.order_dictionary[edge]
                self.sparse_matrix.append((order, index))
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
        self.pivots_sparse = []
        current_column, max_row = self.sparse_matrix[0][1], -1

        # find pivots
        # sparse matrix is ordered by increasing column by construction
        for cell in self.sparse_matrix:
            row, column = cell[0], cell[1]
            # when the iteration over one column is done, the pivot is the cell with max row
            if column != current_column and max_row >=0 :
                self.pivots_sparse.append((max_row, current_column))
                current_column = column
                max_row = -1
            if row > max_row:
                max_row = row
        self.pivots_sparse.append((max_row, current_column))
        print(f'found {len(self.pivots_sparse)} pivots')
        self.pivots = [-1] * self.simplices_number
        for pivot in self.pivots_sparse:
            self.pivots[pivot[1]] = pivot[0]
        # print(f'pivots : {self.pivots}')

        print(f'Starting reduction')
        for column_index in range(self.simplices_number):
            first_occurence = self.pivots.index(self.pivots[column_index])
            while first_occurence < column_index and self.pivots[column_index] >= 0:
                row = sum_sparse(self.sparse_matrix, first_occurence, column_index)
                self.pivots[column_index] = row
                first_occurence = self.pivots.index(self.pivots[column_index])
            if column_index % 100 == 0:
                print(f'index = {column_index}')

        # index = 0
        # for pivot in self.pivots_sparse:
        #     row, column = pivot[0], pivot[1]
        #     first_occurence = find_first_occurence(self.pivots_sparse, row, column)
        #     while first_occurence < column and row >= 0:
        #         row = sum_sparse(self.sparse_matrix, first_occurence, column)
        #         self.pivots_sparse[index] = (row, column)
        #         first_occurence = find_first_occurence(self.pivots_sparse, row, column)
        #     index += 1
      
            # print(index)
            

    def build_diagram(self):
        if self.use_sparse:
            self.build_diagram_sparse()
            return

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
        diagram = self.diagram_sparse if self.use_sparse else self.diagram
        for interval in diagram:
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

# returns the index of the new pivot ; it is -1 if the column is zeroed out
def sum_sparse(sparse_matrix, source, target):
    source_column_rows = [cell[0] for cell in sparse_matrix if cell[1] == source]
    target_column_rows = [cell[0] for cell in sparse_matrix if cell[1] == target]
    for row in source_column_rows:
        if row in target_column_rows:
            sparse_matrix.remove((row, target))
        else:
            sparse_matrix.append((row, target))
    target_column_rows = [cell[0] for cell in sparse_matrix if cell[1] == target]
    if target_column_rows:
        return max(target_column_rows)
    return -1