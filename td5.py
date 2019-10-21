from diagram import Diagram
import time

start_time = time.time()

filtration_path = 'filtration.txt'
filtration_path = 'filtrations/filtration_B.txt'

use_sparse_matrix = True
# use_sparse_matrix = False

diagram = Diagram(use_sparse=use_sparse_matrix)
print(f'Reading data from {filtration_path}')
diagram.read_data(filtration_path)
m = diagram.simplices_number
print(f'Simplices count is m = {m}')

print('Sorting simplices')
diagram.sort_simplices()

print('Building boundary matrix')
matrix_start_time = time.time()
diagram.build_matrix()
print(f'Matrix of size {len(diagram.matrix)} built in {time.time() - matrix_start_time} seconds ---' )


print('Reducing boundary matrix')
reduction_start_time = time.time()
diagram.reduce_matrix()
print(f'Matrix reduced in {time.time() - reduction_start_time} seconds ---' )

print('Building diagram')
diagram.build_diagram()

# print(f'final pivots : {diagram.pivots}')
diagram.print_diagram()

print(f'Total execution time : {time.time() - start_time} seconds ---' )
