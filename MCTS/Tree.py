from asciitree import LeftAligned
from collections import OrderedDict as OD

def DFS(root):
    if not root.children:
        return OD()
    children = []
    for move in root.children:
        children.append((str(move), DFS(root.children[move])))
    return OD(children)


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


