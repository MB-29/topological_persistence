from diagram import Diagram

diagram = Diagram()
diagram.read_data('filtration.txt')
diagram.to_string()
diagram.sort_simplices()
diagram.to_string()
diagram.build_matrix()
diagram.reduce_matrix()
diagram.build_diagram()
diagram.print_diagram()