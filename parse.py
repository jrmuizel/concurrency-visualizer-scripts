import csv
import sys
class Node:
    def __init__(self, parent, name, incsamples, samples):
        self.parent = parent
        self.name = name
        self.incsamples = incsamples
        self.samples = samples
        self.children = []
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

head = Node(None, "root", 0, 0)
with open(sys.argv[1], 'rb') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t', fieldnames=['level', 'name', 'incsamples', 'exsamples', 'perinc', 'perex', 'details'])
    next(reader, None) # skip the header
    level = -1
    cur = head
    for row in reader:
        if int(row['level']) == level + 2:
            cur = cur.children[-1]
            level += 1
        else:
            while int(row['level']) < level + 1:
                level -= 1
                cur = cur.parent
        #print 'cur', id(cur), cur, id(cur.children), cur.children
        cur.children.append(Node(cur, row['name'], int(row['incsamples']), int(row['exsamples'])))
        #print " " * int(row['level']), row['name'], row['incsamples'], row['exsamples']

def incsamples(node):
    x = node.samples
    for c in node.children:
        x += incsamples(c)
    return x
head.incsamples = incsamples(head)
print "tree"
def print_tree(node, indent):
    print " " * indent, node.name, node.incsamples, incsamples(node)
    assert node.incsamples == incsamples(node)
    for x in list(node.children):
        print_tree(x, indent+1)

def charge(node, name):
    newsamples = 0
    before = incsamples(node)
    for x in node.children:
        charge(x, name)
    newchildren = []
    for x in node.children:
        if name in x.name:
            node.samples += x.samples
            newchildren += x.children
        else:
            newchildren.append(x)
    node.children = newchildren
    after = incsamples(node)
    assert before == after
charge(head, "igd10")
charge(head, "unknown")
def allnodes(node):
    l = [node]
    for x in node.children:
        l += allnodes(x)
    return l

print_tree(head, 0)

import collections
heavy = collections.defaultdict(int)
for x in allnodes(head):
    heavy[x.name] += x.samples
totalsamples = 0
for x in sorted(list(heavy.iteritems()), key=lambda node: node[1], reverse=True):
    totalsamples += x[1]
    print x[0], x[1]
print totalsamples
