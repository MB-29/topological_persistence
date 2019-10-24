from simplex import Simplex
import os

FOLDER_NAME = "filtrations"

# removes duplicates from a list of simplices
# 2 simplices are considered to be the same if they have the same vertices
# (the tuples of vertices are assumed to be sorted)
def remove_duplicates(simplex_list):
    tuple_list = []
    result = []
    for simplex in simplex_list:
        if not simplex.vertices in tuple_list:
            tuple_list.append(simplex.vertices)
            result.append(simplex)
    return result

# function to write a filtration to a text file
def write_file(file_path, simplex_list):
    data = ""
    for simplex in simplex_list:
        vertex_string = " ".join([str(v) for v in simplex.vertices])
        data += "{} {} {}\n".format(simplex.time, simplex.dim, vertex_string)
    with open(file_path, 'w+') as f:
        f.write(data)

# recursive function which from a list of simplices (assumed to be of same dimension and appearing at the same time) returns a possible filtration, with all the simplices necessary to build up to the list
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
        simplex_list.extend(filtration_from_simplex_list(res))
        return remove_duplicates(simplex_list)

#function to generate d-ball
def generate_d_ball(d):
    filename = os.path.join(FOLDER_NAME,"{}-ball.txt".format(d))
    s = Simplex(d, d, tuple(range(d+1)))
    simplex_list = filtration_from_simplex_list([s])
    write_file(filename, simplex_list)

#function to generate d-sphere
def generate_d_sphere(d):
    filename = os.path.join(FOLDER_NAME,"{}-sphere.txt".format(d))
    s = Simplex(d+1, d+1, tuple(range(d+2)))
    simplex_list = filtration_from_simplex_list([s])
    simplex_list.remove(s)
    write_file(filename, simplex_list)      


# function to generate filtration from a grid similar to those found in Figure 1 of the report
# The grid is represented by a 4 x 4 table. The value of the table at each point corresponds to the vertex found on the grid at that point
# Note: the Moebius Band is generated using the same principal but a 2 x 4 grid
def generate_from_table(table, file_name, mobius = False):
    L = []
    for i in range(3 if not mobius else 1):
        for j in range(3):
            # Add triangle with right angle at top
            L.append(Simplex(2,2,tuple(sorted([table[i][j],table[i+1][j],table[i][j+1]]))))

            # Add triangle with right angle at bottom
            L.append(Simplex(2,2,tuple(sorted([table[i+1][j+1],table[i+1][j],table[i][j+1]]))))
    
    # add edges and points
    L =  filtration_from_simplex_list(L)

    # save filtration
    write_file(file_name,L)      

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


generate_torus()
generate_projective_plane()
generate_klein_bottle()
generate_mobius()

for d in range(11):
    generate_d_sphere(d)
    generate_d_ball(d)
