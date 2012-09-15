from math import sqrt, atan, degrees
from nodebox.graphics import *
from AppKit import *

coreimage = _ctx.ximport("coreimage")
reload(coreimage)


colors = ximport("colors")
reload(colors)

util = ximport("util")

domain = ximport("domain")

C = colors.color(0.6, 0.1, 0.1)



size(600,600)

# philosopher path
autoclosepath(close=False)
beginpath(100, 100)
curveto(200, 350, 300, 450, 500,500)
p = endpath(draw=False)

philosopher = domain.Philosopher(1, "St Thomas D'Aquin", 1000, 1000, 1 , 1, color=C)


########################


#
#
#
def draw_lifeline(path, philosopher):
    ''' Draw a philosopher:
        - path: philosopher path
        - philosopher: philosopher object
        
    '''
    dt = 0.001
    font("Courier New Bold")
    fontsize(14)
    
    # get philosopher color (assume that this color has been created with colors library!)
    c = philosopher.color
    
    # get philosopher name
    name = philosopher.name
    
    # draw first part
    fill(c)
    stroke(c)
    strokewidth(10)
    p = util.sub_path(path, 0, 0.05+dt, dt = 0.001)
    drawpath(p)    
    
    # compute letters coordinates
    n = len(name)
    ti = 0.05
    tp = []
    for i in range(n):
        dw = textwidth(name[i]) / path.length
        ti +=  dw + 0.005
        direc = util.direction(path, ti)
        pti = path.point(ti+ dt)
        a,b = util.tangent(path, ti)
        angle = degrees(atan(a))
        tp.append((name[i], pti.x, pti.y, angle))
        if direc == 3 or direc == 4:
           i = n - i - 1

    # draw second part
    ti +=2*dw
    c2 = c.lighter()
    c2.alpha= 0.4
    fill(c2)
    stroke(c2)
    strokewidth(10)
    p = util.sub_path(path,0.05-dt, ti+dw, dt = dt)
    drawpath(p)    

    # draw letters
    fill(c)
    stroke(c)
    for k in range(len(tp)):
        pk = tp[k]
        push()
        rotate(-pk[3])
        translate(0, textheight(pk[0])/4)
        text(pk[0], pk[1], pk[2])
        pop()
        
    # draw third part
    m = (1-ti) / dt
    p = util.sub_path(path, ti-dt,1, dt = dt)
    drawpath(p)    

draw_lifeline(p, philosopher)
