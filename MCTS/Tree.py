from asciitree import LeftAligned
from collections import OrderedDict as OD

def DFS(root):
    if not root.children:
        return OD()
    children = []
    for move in root.children:
        txt = str(move) + ' ' + str(root.children[move].V)
        children.append((txt, DFS(root.children[move])))
    return OD(children)

# def write_tree_to_file(root, file_name):
#     x = DFS(root)
#     tree = {'root': x}
#     tr = LeftAligned()
#     with open(file_name,'a') as f: 
#         f.write('\n\n')
#         f.write(tr(tree))

def print_tree(root):
    x = DFS(root)
    tree = {'root': x}
    tr = LeftAligned()
    print(tr(tree))

# x, y = ('to', OD([])), ('draw', OD([]))
# a = ('want', OD([x, y]))
# b = ('sometimes', {'you': OD([])})
# c = ('just', OD([]))
# tree = {'asciitree': OD([a, b])}


