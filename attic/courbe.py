from math import sqrt, atan, degrees
from nodebox.graphics import *
from AppKit import *
from Numeric import zeros

coreimage = _ctx.ximport("coreimage")
reload(coreimage)

supershape = _ctx.ximport("supershape")
reload(supershape)

colors = ximport("colors")
reload(colors)

util = _ctx.ximport("util")
reload(util)
domain = ximport("domain")
reload(domain)

svg = ximport("svg")


def __setup__():
    """ Setup environment """
    size(1000, 600)
    stroke(0)
    fill(0.5)

def density(fr, to , philosophers):
    return len([p for p in philosophers if iscontemporary(p, fr, to)])
    
def count(year, philosophers):
  return len([p for p in philosophers if p.y1 <= year])
    
def iscontemporary(p, yo1, yo2):
      y1, y2 = p.y1, p.y2
      a = y1 >= yo1 and y2 <= yo2
      b = y1 <= yo2 and y2 >= yo2 #and (y2 - yo2) < 50
      c = y1 <= yo1 and y2 >= yo1 #and (yo1 - y1) < 50
      d = y1 <= yo1 and y2 >= yo2
      return a or b or c or d
      
 
def draw_courbe(x0, y0, xmax, philosophers, col, FR, TO):
    line(x0, y0, xmax, y0)
    c= 10
    x1, y1 = x0, y0
    autoclosepath(True)
    beginpath(x0, y0)
    ymax = y0
    for year in range(FR, TO-1, 100):
        d = density(year , year+1, philosophers)
        x, y = (xmax-x0)*(year-FR)/(TO-FR) + x0, (-d*c + y0)
        curveto(x1+20, y1, x-20, y, x, y)
        x1, y1 = x, y
        #util.circle(x, y, 0.5)   
        if year % 100 == 0:
            text(str(year), x, y0+5)
        #line(x, y0, x, y)
    lineto(xmax, y0)
    p = endpath(draw=False)
    colors.gradientfill(p, colors.color("white"), col, type="linear")
    
    
def draw_river(path, philosophers, FR, TO):
	 c = colors.color("skyblue")
	 nostroke()
	 
	 c.alpha = 0.2
	 fill(c)
	 autoclosepath(True)
	 x0, y0 = path.point(0).x, path.point(0).y
	 x1, y1 = x0, y0
	 reverse = []
	 beginpath(x0, y0)
	 for year in range(FR, TO-1, 30):
	 	ct = count(year, philosophers)
	 	t = float(year-FR) / float(TO-FR)
	 	a, b = util.normal(path, t)
	 	angle = degrees(atan(a))
	 	pt = path.point(t)
	 	theta = angle
	 	if angle <0:
	 		theta = angle + 180
	 	x, y = util.coordinates(pt.x, pt.y, ct, theta)
	 	k, v = random(10), random(-5, +5)
	 	if x > x1: 
	 		curveto(x1+k, y1+v, x-k, y -v, x, y)
	 		x1, y1 = x, y
	 	if angle < 0:
	 		theta = angle
	 	else: theta = angle -180
	 	reverse.append((util.coordinates(pt.x, pt.y, ct, theta)))
	 reverse.reverse()
	 x0, y0 = reverse[0]
	 x1, y1 = (x+x0)/2 +50, (y+y0)/2
	 curveto(x +20, y, x1, y1 + 20, x1, y1)
	 curveto(x1, y1-20, x0 + 20, y0, x0, y0)
	 x1, y1 = x0, y0
	 for x,y in reverse:
	 	k, v = random(-10), random(-5, +5)
	 	if x < x1: 
	 		curveto(x1+k, y1+v, x-k, y -v, x, y)
	 		x1, y1 = x, y
	 p = endpath(draw=True)


def __main__():
    
    size(2000, 600)
    col = colors.color("slightgray")
    col.alpha = 0.4
    stroke(col)
    strokewidth(1)
    fontsize(10)
    fill(col)
    
    data = open("river3.svg").read()
    paths = svg.parse(data)
    path = paths[0]
    path.fit(x=0, y=0, width=WIDTH, height = 300, stretch=True)
    nofill()
    drawpath(path)

    
    FR = -700
    TO = 1900
    
    schools_dict = domain.load(4, domain.School)
    philosophers_dict = domain.load(0, domain.Philosopher, schools_dict)
    philosophers = [p for (i,p) in philosophers_dict.iteritems() if p.importance >= 4 ]
    philosophers.sort(key=lambda p: p.y1)
    
    x0 = 10
    y0 = HEIGHT-10
    xmax = WIDTH-10
    draw_courbe(x0, y0, WIDTH-10, philosophers, col, FR,TO)    
    draw_river(path, philosophers, FR, TO)
    
  
if __name__ == '__main__':
	main()

__main__()
