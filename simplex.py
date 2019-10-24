class Simplex:

    def __init__(self, time,dim,vertices):
        self.time = time
        self.dim = dim
        self.vertices = vertices


    #class method to get instance from a line of a file
    @classmethod
    def simplex_from_line(cls, line):
        string_coords = line.split()
        time = float(string_coords[0])
        dim = int(string_coords[1])
        vertices = tuple(sorted([int(vertex) for vertex in string_coords[2::]]))
        return cls(time,dim,vertices)

    #comparison method used to sort the simplices before building the matrix
    @staticmethod
    def compare(source, target):
        if source.time != target.time:
            return source.time - target.time
        return source.dim - target.dim 


    def __str__(self):
        return f'dim : {self.dim}, time = {self.time}, vertices = {self.vertices}'

    # returns a list of tuples
    # each tuple has the vertices of an element of the boundary of self
    # Note: if vertices_list is sorted (which it should be) then so are the results
    def boundary(self):
        boundary = []
        for vertex_index in range(len(self.vertices)):
            vertices_list = list(self.vertices)
            edge = list(vertices_list).copy()
            del edge[vertex_index]
            boundary.append(tuple(edge))
        return boundary


    
