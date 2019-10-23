from simplex import Simplex
import os

FOLDER_NAME = "classical_spaces"

def remove_duplicates(simplex_list):
    tuple_list = []
    result = []
    for simplex in simplex_list:
        if not simplex.vertices in tuple_list:
            tuple_list.append(simplex.vertices)
            result.append(simplex)
    return result

def write_file(file_path, simplex_list):
    data = ""
    for simplex in simplex_list:
        vertex_string = " ".join([str(v) for v in simplex.vertices])
        data += "{} {} {}\n".format(simplex.time, simplex.dim, vertex_string)
    with open(file_path, 'w+') as f:
        f.write(data)

def generate_d_ball(d):
    filename = os.path.join(FOLDER_NAME,"{}-ball.txt".format(d))
    s = Simplex(10, d, tuple(range(d+1)))
    simplex_list = s.filtration_from_simplex()
    simplex_list = remove_duplicates(simplex_list)
    write_file(filename, simplex_list)

def generate_d_sphere(d):
    filename = os.path.join(FOLDER_NAME,"{}-sphere.txt".format(d))
    s = Simplex(10, d+1, tuple(range(d+2)))
    simplex_list = s.filtration_from_simplex()
    simplex_list = remove_duplicates(simplex_list)
    simplex_list.remove(s)
    write_file(filename, simplex_list)      

for d in range(10):
    generate_d_ball(d)
    generate_d_sphere(d)
