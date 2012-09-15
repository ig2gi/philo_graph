from math import pi, degrees

var ("H", NUMBER, 800, 800, 3000)

size(H, H)



util = ximport("util")
reload(util)

domain = ximport("domain")
reload(domain)

xc, yc = WIDTH/2, HEIGHT/2
FR = -700.0
TO = 1950.0
dmin, dmax = 50.0, float(WIDTH-50)

nofill()
stroke(0)
util.circle(xc, yc, dmin)
util.circle(xc, yc, dmax)
util.circle(xc, yc, 2)

# philosophers
philosophers_dict = domain.load(0, domain.Philosopher)
philosophers = [p for (i,p) in philosophers_dict.iteritems()  if p.importance > 4 and p.y2 <> 0 and p.name <> '' and p. in_range(FR, TO)]
philosophers.sort()



def to_d(year, fr = FR):
    return (year - fr) / (TO - FR) *  (dmax - dmin) / 2 + dmin/2
    


    
fontsize(9)
for year in range(FR, TO, 100):
    d =  to_d(year)
    util.circle(xc, yc, 2*d)
    fill(0)
    push()
    for a in range(-45, 360, 45):
        x, y = util.coordinates(xc, yc, d, a)
        rotate(-45)
        text(str(year), x, y)
    pop()

    nofill()
    

    
cpt = 0
fill(0)
for p in philosophers:
    angle = degrees(cpt * 4 * pi / len(philosophers))
    d1 = to_d(p.y1)
    d2 = to_d(p.y2)
    x1, y1 = util.coordinates(xc, yc, d1, angle)
    x2, y2 = util.coordinates(xc, yc, d2, angle)
    line(x1, y1, x2, y2)
    text(p.name, x1, y1)
    cpt += 1

    
    
    