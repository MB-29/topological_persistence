from diagram import Diagram
<<<<<<< Updated upstream

diagram = Diagram()
diagram.read_data('filtration.txt')
print(diagram.to_string())
diagram.sort_simplices()
print(diagram.to_string())
diagram.build_matrix()
diagram.reduce_matrix()
diagram.build_diagram()
diagram.print_diagram()
=======
import time
import os

balls = ["{}-ball".format(k) for k in range(10)]
spheres = ["{}-sphere".format(k) for k in range(10)]
classical_spaces = spheres
for filtration in :
    start_time = time.time()

    filtration_path = os.path.join('classical_spaces', "{}.txt".format(filtration))
    use_sparse_matrix = False

    diagram = Diagram(title = filtration, use_sparse=use_sparse_matrix)
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
    diagram.display_diagram()
    print(f'Total execution time : {time.time() - start_time} seconds ---' )
>>>>>>> Stashed changes
