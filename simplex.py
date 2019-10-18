class Simplex:

    def __init__(self, line):
        string_coords = line.split()
        self.time = float(string_coords[0])
        self.dim = int(string_coords[1])
        self.vertices = tuple(sorted([int(vertex) for vertex in string_coords[2::]]))


    def __str__(self):
        return f'dim : {self.dim}, time = {self.time}, vertices = {self.vertices}'


    @staticmethod
    def compare(source, target):
        if source.time != target.time:
            return source.time - target.time
        return source.dim - target.dim 

    def boundary(self):
        boundary = []
        for vertex_index in range(len(self.vertices)):
            vertices_list = list(self.vertices)
            edge = list(vertices_list).copy()[:vertex_index] + list(vertices_list.copy())[vertex_index+1:]
            boundary.append(tuple(sorted(edge)))
        return boundary
