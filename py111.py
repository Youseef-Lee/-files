from graphviz import Digraph

dot = Digraph(comment='Test')
dot.node('A', 'Start')
dot.node('B', 'End')
dot.edges(['AB'])
dot.render('test-output/round-table.gv', view=True)
