import graphviz as gv

def make_course_graph(courses):
    values = courses.values()
    graph = gv.Digraph(format='svg')
    # We need to build a representation for it:
    
