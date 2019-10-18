from diagram import Diagram

diagram = Diagram()
diagram.read_data('filtration.txt')
diagram.to_string()
diagram.sort_simplices()
print('simplices sorted')
diagram.to_string()
diagram.build_matrix()
print(f'matrix = {diagram.matrix}')
diagram.reduce_matrix()
print(f'reduced matrix = {diagram.matrix}')