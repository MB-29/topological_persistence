class Simplex:

    def __init__(self, time,dim,vertices):
        self.time = time
        self.dim = dim
        self.vertices = vertices


    @classmethod
    def simplex_from_line(cls, line):
        string_coords = line.split()
        time = float(string_coords[0])
        dim = int(string_coords[1])
        vertices = tuple(sorted([int(vertex) for vertex in string_coords[2::]]))
        return cls(time,dim,vertices)

    def __str__(self):
        return f'dim : {self.dim}, time = {self.time}, vertices = {self.vertices}'

    def __hash__(self):
        return hash(self.vertices)
    
    def __equals__(self, other):
        return self.vertices == other.vertices

    @staticmethod
    def compare(source, target):
        if source.time != target.time:
            return source.time - target.time
        return source.dim - target.dim 

    def boundary(self):
        boundary = []
        for vertex_index in range(len(self.vertices)):
            vertices_list = list(self.vertices)
            edge = list(vertices_list).copy()
            del edge[vertex_index]
            boundary.append(tuple(edge))
        return boundary

    def filtration_from_simplex(self):
        if self.dim == 0:
            return [self]
        else:
            res = [self]
            for edge in self.boundary():
                res.extend(Simplex(self.time-1,self.dim-1,edge).filtration_from_simplex())
            return res
    
