#!/usr/local/bin/python2.6
# encoding: utf-8
# Add the upper directory (where the nodebox module is) to the search path.
import os, sys; sys.path.insert(0, os.path.join("..","..","lib"))

from nodebox.graphics import *
from nodebox.graphics.physics import Flock
  
flock = Flock(40, 0, 0, 500, 500)
flock.sight = 300
  
def draw(canvas):
    background(1)
    fill(0, 0.75)
    flock.update(cohesion=0.15)
    for boid in flock:
        push()
        translate(boid.x, boid.y)
        scale(0.5 + 1.5 * boid.depth)
        rotate(boid.heading)
        arrow(0, 0, 15)
        pop()
      
canvas.fps = 30
canvas.size = 600, 400
canvas.run(draw)

