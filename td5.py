from diagram import Diagram
import time

start_time = time.time()

# filtration_path = 'filtrations/filtration_B.txt'
filtration_path = 'filtration.txt'


diagram = Diagram()
print('Reading data')
diagram.read_data(filtration_path)
print('Sorting simplices')
diagram.sort_simplices()
print('Building boundary matrix')
matrix_start_time = time.time()
diagram.build_matrix()
print(f'Matrix built in {time.time() - matrix_start_time} seconds ---' )

print('Reducing boundary matrix')
reduction_start_time = time.time()
diagram.reduce_matrix()
print(f'Matrix reduced in {time.time() - reduction_start_time} seconds ---' )

print('Building diagram')
diagram.build_diagram()
diagram.print_diagram()
m = diagram.simplices_number

print(f'Simplices count is m = {m}')
print(f'Total execution time : {time.time() - start_time} seconds ---' )
