from diagram import Diagram
import time
import os
import json

FILTRATIONS_FOLDER = "filtrations"

balls = ["{}-ball".format(k) for k in range(11)]
spheres = ["{}-sphere".format(k) for k in range(11)]
example_filtrations = ["filtration_{}".format(s)for s in ["A","B","C", "D"]]
classical_spaces = ["mobius", "torus", "klein_bottle", "projective_plane"]

timing_dic = {}


for filtration in classical_spaces:
    start_time = time.time()

    filtration_path = os.path.join(FILTRATIONS_FOLDER, "{}.txt".format(filtration))
    use_sparse_matrix = True

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

    matrix_build_time = time.time() - matrix_start_time
    print(f'Matrix of size {len(diagram.matrix)} built in {matrix_build_time} seconds ---' )


    print('Reducing boundary matrix')
    reduction_start_time = time.time()
    diagram.reduce_matrix()

    matrix_reduction_time = time.time() - reduction_start_time
    print(f'Matrix reduced in {matrix_reduction_time} seconds ---' )

    print('Building diagram')
    diagram.build_diagram()

    diagram.print_diagram()
    #print(f'final pivots : {diagram.pivots}')
    #print("Displaying diagram")
    #diagram.display_diagram()
    total_time = time.time() - start_time
    print(f'Total execution time : {total_time} seconds ---' )

    timing_dic[m] = (matrix_build_time, matrix_reduction_time, total_time)

with open("timing.json", 'w+') as f:
    json.dump(timing_dic, f)


