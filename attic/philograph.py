size(3000, 2500)
"""
untitled.py

Created by Gilbert Perrin on 2008-01-30.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import sys
import os

domain = ximport("domain")
reload(domain)

colors = ximport("colors")
reload(colors)

graph = ximport("graph")


# periods
periods_dict = domain.load(2, domain.Period)
periods = [e for (i, e) in periods_dict.iteritems() if e.parentid]

# schools & theories
schools_dict = domain.load(4, domain.School)
schools = [s for (i, s) in schools_dict.iteritems() if s.type == "school"]
theories = [s for (i, s) in schools_dict.iteritems() if s.type == "theory"]

# philosophers
philosophers_dict = domain.load(0, domain.Philosopher, schools_dict)
philosophers = [p for (i,p) in philosophers_dict.iteritems()  if p.importance > 1 and p.y2 <> 0 and p.name <> '' and p. in_range(-700, 1900)]
philosophers.sort()

# centuries
centuries = domain.load(3, domain.Century)
centuries = [e for (i, e) in centuries.iteritems()]
centuries.sort()

# events
events_dict = domain.load(1, domain.Event)
events = [e for (i, e) in events_dict.iteritems() if e.y1 > -700]
events.sort()

def key(obj):
    return  "%i  %s" % ( obj.y1, obj.name)


# A graph object.
g = graph.create(iterations=500, distance=2.6,  layout = "spring", depth=True)

def curly_edge(style, path, edge, alpha=1.0):
    path.moveto(edge.node1.x, edge.node1.y)
    path.curveto(
        edge.node1.x - 40,
        edge.node1.y,
        edge.node2.x + 40,
        edge.node2.y,
        edge.node2.x,
        edge.node2.y,
    )
g.styles.highlight.edge = curly_edge

s = g.styles.create("red")
s.fill = color(1, 0, 0.25, 0.75)

g.styles.apply()

for c in centuries:
    node = g.add_node(key(c), category="century")
    node.style = "red"
    
    
for p in periods:
    node = g.add_node(p.name, category="period")
    
for c in centuries:
    for p in c.contemporaries(periods):
         g.add_edge(key(c), p.name , label="in")

for p in philosophers:
    node = g.add_node(p.name, category="philosopher")

for c in centuries:   
    for  p in c.contemporaries(philosophers):
        g.add_edge(p.name, key(c), label="live in")

for e in events:
    node = g.add_node(key(e), category="event")
    for c in e.contemporaries(centuries):
        g.add_edge(key(e), key(c), label="")



    

# Colorize nodes.
# Nodes with higher importance are blue.
g.styles.apply()

# Update the graph layout until it's done.
g.solve()

path = [p for p in centuries]
for e in events:
    path.append(e)
path.sort()
path = [key(x) for x in path]

g.layout.tweak(k=5, c=0.01, w=15, vm=0.8, fm=32)

# Draw the graph and display the shortest path.
g.draw(highlight=path, weighted=True, directed=True)



