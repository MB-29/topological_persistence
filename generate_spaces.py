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

def filtration_from_simplex_list(simplex_list):
    if simplex_list == []:
        return []
    if simplex_list[0].dim == 0:
        return simplex_list
    else:
        res = []
        for simplex in simplex_list:
            for edge in simplex.boundary():
                res.append(Simplex(simplex.time-1,simplex.dim-1,edge))
        res = remove_duplicates(res)
        simplex_list.extend(filtration_from_simplex_list(remove_duplicates(res)))
        return simplex_list

def generate_d_ball(d):
    filename = os.path.join(FOLDER_NAME,"{}-ball.txt".format(d))
    s = Simplex(d, d, tuple(range(d+1)))
    simplex_list = filtration_from_simplex_list([s])
    write_file(filename, simplex_list)

def generate_d_sphere(d):
    filename = os.path.join(FOLDER_NAME,"{}-sphere.txt".format(d))
    s = Simplex(d+1, d+1, tuple(range(d+2)))
    simplex_list = filtration_from_simplex_list([s])
    simplex_list.remove(s)
    write_file(filename, simplex_list)      


def generate_from_table(table, file_name, mobius = False):
    L = []
    K = []
    for i in range(3 if not mobius else 1):
        for j in range(3):
            L.append(Simplex(2,2,tuple(sorted([table[i][j],table[i+1][j],table[i][j+1]]))))
            L.append(Simplex(2,2,tuple(sorted([table[i+1][j+1],table[i+1][j],table[i][j+1]]))))
    for simplex in L:
        K.extend(simplex.filtration_from_simplex())
    K = remove_duplicates(K)
    write_file(file_name, K)      

def generate_torus():
    file_name = os.path.join(FOLDER_NAME,"torus.txt")
    table = [
        [1,2,3,1],
        [4,5,6,4],
        [7,8,9,7],
        [1,2,3,1]
    ]
    generate_from_table(table, file_name)

def generate_klein_bottle():
    file_name = os.path.join(FOLDER_NAME,"klein_bottle.txt")
    table = [
        [1,2,3,1],
        [4,5,6,7],
        [7,8,9,4],
        [1,2,3,1]
    ]
    generate_from_table(table, file_name)

def generate_projective_plane():
    file_name = os.path.join(FOLDER_NAME,"projective_plane.txt")
    table = [
        [1,2,3,4],
        [10,5,6,7],
        [7,8,9,10],
        [4,3,2,1]
    ]
    generate_from_table(table, file_name)

def generate_mobius():
    file_name = os.path.join(FOLDER_NAME,"mobius.txt")
    table = [
        [1,2,3,4],
        [4,5,6,1],
    ]
    generate_from_table(table, file_name, mobius = True)


#for d in range(10):
#    generate_d_ball(d)
#    generate_d_sphere(d)
generate_torus()
generate_projective_plane()
generate_klein_bottle()
generate_mobius()

for d in range(11):
    generate_d_sphere(d)
    generate_d_ball(d)
