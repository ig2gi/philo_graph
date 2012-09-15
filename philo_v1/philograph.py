# pyhon core libraries
from math import sqrt, atan, degrees
from nodebox.graphics import *
from AppKit import *
from time import time

# nodebox libraries
coreimage = ximport("coreimage")
reload(coreimage)
colors = ximport("colors")
reload(colors)
graph =  ximport("graph")

# philo libraries 
util = ximport("util")
reload(util)
from domain import *


# load philo DB
global db
db = PhiloDb(fr=-700, to=1900)
db.load()

N = len(db.philosophers)

size(6000, 4000)

def years_in(philosopher, century):
    years = philosopher.y2 - philosopher.y1
    if century.y1 >= philosopher.y1:
        years = years - (century.y1 - philosopher.y1)
    if philosopher.y2 >= century.y2:
        years = years - (philosopher.y2 - century.y2)
    return years
    
def philosopher_label(philosopher):
    return "%s (%i:%i)" % (philosopher.name, philosopher.y1, philosopher.y2)



# create graph
g = graph.create(iterations=600, distance=1.4, layout="spring", depth=False)


# add periods nodes
g.styles.back.fontsize = 20
g.styles.back.textwidth = 200
for p in db.periods:
    n = g.add_node(p.name, category="period",  style="back")
    n.r = 10.0 * len(p.contemporaries(db.philosophers)) 

# add century nodes and link between century and periods
previous = ""
for c in db.centuries:
    n = g.add_node(c.name, category="century", style="root")
    n.weight=1
    if previous <> "":
        g.add_edge(previous, c.name, length=400)
    previous = c.name
    for p in c.contemporaries(db.periods):
        g.add_edge(p.name, c.name, weight=0)
        
# add philosopher nodes
g.styles.dark.fontsize = 12
for p in db.philosophers:
     label = philosopher_label(p)
     n = g.add_node(label, category="philosopher", style="dark")
     n.r = 10
     for c in p.contemporaries(db.centuries):
        w = years_in(p, c)  /  100.0
        g.add_edge(label, c.name, label="lived in", weight=w, length=10)
     #for c in p.contemporaries(db.periods):
        #g.add_edge(p.name, c.name, label="lived in")
        
# add school nodes
g.styles.important.fontsize = 16
g.styles.important.textwidth = 150
for s in db.schools:
     n = g.add_node(s.name, category="school", style="important")
     n.r = 20
     for p in s.philosophers:
         g.add_edge(philosopher_label(p),s.name,  weight=1, length=100, label="member of")
    
      
# add event nodes
for e in db.events:
     label = "%s: %i"  % (e.name, e.y1)
     g.add_node(label, category="event", style="light")
     for c in e.contemporaries(db.centuries):
        g.add_edge(label, c.name)
        

        
# add book nodes
for b in db.books:
     g.add_node(b.name, category="book", style="marked")
     g.add_edge(b.name, philosopher_label(b.author), label="author", weight=0)







#
# DRAW GRAPH
#
g.layout.orbits = 10
g.layout.tweak(k=3, m=0.01, w=15, d=0.5, r=30)

g.prune(depth=0)

g.update(iterations=10)

g.solve()

highlight = [c.name for c in db.centuries]
g.draw(weighted=False, directed=True, highlight=highlight, traffic=None)