
var ("DRAW_BACKGROUND", BOOLEAN, default=False)
var ("DRAW_RIVER", BOOLEAN, default=True)
var ("DRAW_PERIODS", BOOLEAN, default=False)
var ("DRAW_EVENTS", BOOLEAN, default=True)
var ("DRAW_SCHOOLS", BOOLEAN, default=True)
var ("DRAW_CENTURIES", BOOLEAN, default=True)
var ("ALL", BOOLEAN, default=False)

"""  
  Author:     Gilbert Perrin <gilbert.perrin@gmail.com>
  Project:    POSTER PHILO
  Date:        2007-2008
  Description:  Program generation of a philosophy poster.
"""

############################
#                                                            
#   IMPORTS                                       
#                                                            
# ###########################

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

util = ximport("util")
reload(util)

domain = ximport("domain")
reload(domain)

svg = ximport("svg")

############################
#  
#   SETUP
#
# ###########################

def __setup__():
    """ Setup environment """
    
    global cc, FR, TO, c, c2, c3, c4, c5, c6, c7, c8, c9, BORDER_TOP, BORDER_DOWN, BORDER_LEFT, BORDER_RIGHT, dt, img_dir
    
    size(6600, 2700)

    FR = -700
    TO = 1950
    
    cc = CollisionController(WIDTH, HEIGHT)
    
    BORDER_TOP = 400
    BORDER_LEFT, BORDER_RIGHT = 600, 600
    BORDER_DOWN = 400
    
    dt = 1/float(TO-FR) # time unit

    img_dir = "images/"

    colormode(RGB, range=255)

    c =  colors.rgb(132, 162, 212, a=100, range=255)

    c2 = colors.rgb(175,201,81, a=100, range=255)
    c3 = colors.rgb(195,203,65,a=100, range=255)
    c4 = colors.rgb(204,183,64, a=100, range=255)
    c5 = colors.rgb(204,156,64, a=100, range=255)
    c6 = colors.rgb(203,109,113, a=100, range=255)
    c7 = colors.rgb(100,158,178, a=100, range=255)
    c8 = colors.rgb(137,128,201, a=100, range=255)
    c9 = colors.rgb(201,128,170, a=100, range=255)

    colors.list(c2, c3, c4, c5, c6, c7, c8, c9, "periods")

    colormode(RGB, range=1)


############################
#  
#   RIVER PATH
#
# ###########################

def get_river_path():
    """ Returns the river as a path object. """
    

    data = open("river3.svg").read()
    paths = svg.parse(data)
    path = paths[0]
    path.fit(x=BORDER_LEFT, y=2*BORDER_TOP)
    return path
    

############################
#  
#   UTILS
#
# ###########################

#
def to_t(year):
    """ Returns the t coordinate in (0,1) that corresponds to the given year."""
    
    return float(year - FR)  / float(TO - FR)
    
#
def count(year, philosophers):
  return len([p for p in philosophers if p.y1 <= year])
  

#        
def density(fr, to , philosophers):
    return len([p for p in philosophers if p.haslivedin(fr, to)])

 
 
#
class CollisionController:
    #
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = zeros([width, height])
    
    #
    def add_object(self, x, y, w, h):
        xmax = min(x+w, self.width-1)
        ymax = min(y+h, self.height-1)
        for i in range(x, xmax):
            for j in range(y, ymax):
                self.matrix[i][j] = 1
    
    #
    def overlap(self, x, y, w, h):
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)
        xmax = min(x+w, self.width-1)
        ymax = min(y+h, self.height-1)
        # top
        for i in range(x, xmax):
                if self.matrix[i][y] == 1:
                    return True
        # down
        for i in range(x, xmax):
                if self.matrix[i][ymax] == 1:
                    return True
        # left
        for i in range(y, ymax):
                if self.matrix[x][i] == 1:
                    return True
        # left
        for i in range(y, ymax):
                if self.matrix[xmax][i] == 1:
                    return True                
        return False
        
    def __str__(self):
        return str(self.matrix)



############################
#  
#   DRAW FUNCTIONS
#
# ###########################

#
def draw_title():
	''' '''
	title = "  LA RIVIERE PHILOSOPHIQUE  " 
	font("Arial")
	fontsize(55)
	align(CENTER)
	W = textwidth(title)
	stroke(colors.color("slategray"))
	strokewidth(1)
	nofill()
	rect(10, 10 , WIDTH-20, HEIGHT-20)
	fill(colors.color("slategray"))
	text(title, WIDTH/2 - W/2, 60)
	

#
def draw_background(river):
    """ Draw the background"""
    if not ALL and not DRAW_BACKGROUND:
    	return
    strokewidth(0.5)
    fontsize(20)
    c = colors.color("slategray")
    stroke(c)
    fill(c)
    for year in range(FR, TO, 100):
    	t = to_t(year)
    	x = river.point(t).x
    	util.linedash(x, BORDER_TOP, x, HEIGHT -BORDER_DOWN)
    	util.linedash(x, BORDER_TOP - 300, x, BORDER_TOP - 80)
    	util.linedash(x, HEIGHT -BORDER_DOWN + 300, x, HEIGHT -BORDER_DOWN +80)
    	w, h = textmetrics(str(year))
    	text(str(year), x - w/2, BORDER_TOP + 20)
    	text(str(year), x - w/2, BORDER_TOP - 270)
    	text(str(year), x - w/2, HEIGHT -BORDER_DOWN - 20)
 
#
def draw_riverarea(path, philosophers):
	 #c = colors.color("skyblue")
	 nostroke()
	 
	 c.alpha = 0.2
	 fill(c)
	 autoclosepath(True)
	 x0, y0 = path.point(0).x, path.point(0).y
	 x1, y1 = x0, y0
	 reverse = []
	 beginpath(x0, y0)
	 for year in range(FR, TO-1, 30):
	 	ct = 1.2*count(year, philosophers)
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

#
def draw_river(path):
    """ Draw the given river path """
    if not ALL and not DRAW_RIVER:
    	return
    
    nofill()
    c.alpha = 0.8
    stroke(c)
    strokewidth(3)
    path = get_river_path()
    drawpath(path)
    fontsize(11)
    nostroke()
    D=30
    d=10
    for year in range(FR,TO,100):
        p = path.point(to_t(year))
        nostroke()
        c.alpha = 0.8
        fill(c)
        util.circle(p.x, p.y, D)
        w,h = textmetrics(str(year))
        fill(1)
        text(str(year), p.x-w/2, p.y+2.5)
        




#
def draw_courbe(river, philosophers, col):
    fontsize(20)
    align(LEFT)
    x0, y0 = river.point(0).x, HEIGHT - BORDER_DOWN + 200
    xmax = river.point(1).x
    line(x0, y0, xmax, y0)
    c= 8
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
        	 w, h = textmetrics(str(year))
        	 text(str(year), x - w/2, y0 + h)
        #line(x, y0, x, y)
    lineto(xmax, y0)
    p = endpath(draw=False)
    colors.gradientfill(p, colors.color("white"), col, type="linear")
	


#
def draw_period(txt, c, year1,year2, path, pas=40):
    """ Draw the period. """
    
    if not ALL and not DRAW_PERIODS:
    	return
    
    c.alpha=1
    w=40
    fill(c)
    nostroke()
    fontsize(20)
    p1=path.point(to_t(year1))
    p2=path.point(to_t(year2))
    x1 = p1.x
    x2 = p2.x
    h = textheight(txt)
    strokewidth(0.8)
    c.alpha = 0.7
    stroke(c)
    # top
    ytop = BORDER_TOP -w
    fill(c)
    util.rectround(x1+ (x2-x1)/2, ytop+h/2, x2-x1-6, h, clr = c)
    fill(1)
    text(txt, x1 + (x2-x1)/2 - textwidth(txt)/2, ytop -1+ textheight(txt)/1.5)

    # down
    ydown = HEIGHT - BORDER_DOWN +w 
    util.rectround(x1 + (x2-x1)/2, ydown -h , x2-x1-6, h, clr = c, txt = txt)
    
    #c.alpha = 0.05
    #fill(c)
    #nostroke()
    #rect(x1, ytop, (x2 - x1), (ydown - ytop))
    
    
#
#
def draw_zone(path, y1, y2, col, txt='', D = 50):
    """ Draw a zone. """
        	
    t1= to_t(y1)
    t2= to_t(y2)
    pt1 = path.point(t1)
    pt2 = path.point(t2)
    x = (pt1.x + pt2.x)/2
    y = HEIGHT - BORDER_DOWN - 20
    col.alpha = 0.25
    fill(col)
    font("Cochin")
    fontsize(65)
    strokewidth(1)
    text(txt, x - textwidth(txt)/2, y -D/2)
    y = BORDER_TOP + 20
    text(txt, x - textwidth(txt)/2, y +D/2)
    

#
#
#
def draw_centuries(path):
    """ Draw centuries. """
    
    if not ALL and not DRAW_CENTURIES:
    	return
    
    for k, cent in centuries.iteritems():
        txt = cent.name
        #util.shadow(blur=40.0)
        draw_zone(path, cent.y1, cent.y2, c, txt)
        
#
#
#
def draw_philosopher(p, path, cpt, D) :
    """ Draw the given philosopher. """
    
    fs = 9
    fontsize(fs)
    font("Arial Black")
    fill(p.color)
    stroke(p.color)
    
    t1 = to_t(p.y1)
    t2 = to_t(p.y2)
    orig = path.point(t1)
           
    
    pth = util.get_parallel_path(path, t1, t2, D, dt)
    
    p.x = pth.point(0).x
    p.y = pth.point(0).y
    
    draw_lifeline(pth, p)
    
    #p.color.alpha = 150
    #stroke(p.color)
    #strokewidth(12)
    #drawpath(pth)
    #p.color.alpha = 255
    
    #w = textwidth(p.name)
    #h = textheight(p.name)
    
    #n = len(p.name)
    #ti = 0
    #fill(90)
    #for c in range(n):
    #    ti = float(c) / float( n)
    #    direc = util.direction(pth, ti)
    #    pti = pth.point(ti+ dt)
    #    a,b = util.tangent(pth, ti)
    #    angle = degrees(atan(a))
    #    push()
    #    rotate(-angle)
    #    if direc == 3 or direc == 4:
    #        c = n - c - 1
    #    text(p.name[c], pti.x, pti.y)
    #    pop()
    	
    stroke(p.color)
    
    # draw image if any
    draw_image(p, cpt, D)
 
#
#
#
def draw_lifeline(path, philosopher):
    ''' Draw a philosopher:
        - path: philosopher path
        - philosopher: philosopher object
        
    '''
    dt = 0.001
    font("Courier New")
    fontsize(16)
    
    # get philosopher color (assume that this color has been created with colors library!)
    c = philosopher.color
    c.alpha = 250
    
    # get philosopher name
    name = philosopher.name
    
    # draw first part
    fill(c)
    strokewidth(1)
    stroke(colors.color("slategray"))
    p = util.sub_path(path, 0, 0.05+dt, dt = 0.001)
    drawpath(p)     
    util.circle(philosopher.x, philosopher.y, 6)
    
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
    strokewidth(5)
    p = util.sub_path(path,0.05-dt, ti+dw, dt = dt)
    drawpath(p)    

    # draw letters
    c3 = colors.color("slategray")
    fill(c3)
    stroke(c)
    for k in range(len(tp)):
        pk = tp[k]
        push()
        rotate(-pk[3])
        translate(0, textheight(pk[0])/4)
        text(pk[0], pk[1], pk[2])
        pop()
        
    # draw third part
    strokewidth(1)
    stroke(colors.color("slategray"))
    m = (1-ti) / dt
    p = util.sub_path(path, ti-dt,1, dt = dt)
    drawpath(p)  
    

#
#
#
def draw_image(p, cpt, D=0):
    """ Draw philosopher image."""
    
    if not p.image:
        pass
    nofill()
    fontsize(9)
    font("Arial")
    strokewidth(2)
    x, y = p.x, p.y
    if p.image != "":
        file = img_dir + p.image
        w, h = imagesize(file)
        y = BORDER_TOP - 70 - h
        if cpt % 2 == 0:
        	   y += -h -20
        x = x - w/2
        image(file, x , y)
        c = colors.color("slategray")
        c.alpha = 100
        stroke(c)
        rect(x, y, w, h)
        strokewidth(0.5)
        wtext, htext = textmetrics(p.name)
        toy = y + h + htext
        line(p.x, p.y, x + w/2, toy)
        #fill(p.color)
        c.alpha = 200
        fill(c)
        align(CENTER)
        toy = y + h + 10 
        text(p.name, x + w/2 - wtext/2, toy)
        
#
#
#
def draw_schools(river_path, schools):
    """ Draw schools. """
    
    if not ALL and not DRAW_SCHOOLS:
    	return
    
    fill(colors.color("chocolate"))
    strokewidth(0.8)
    c = colors.color("chocolate")
    c.alpha = 100
    stroke(c)
    align(LEFT)
    fontsize(17)
    cpt = 0
    #
    #schools.sort(lambda s1, s2: s1.year() - s2.year())
    for s in schools:
    	if s.philosophers:
    	  if s.type == "theory":
    	  	col = colors.color("chocolate")
    	  else: col = colors.color("cadetblue")
    	  cpt += 1
    	  sig = -1 + 2*(cpt%2)
    	  delta = random(70)
    	  fromyear, toyear = s.dates()
    	  fromx, tox = river_path.point(to_t(fromyear)).x,  river_path.point(to_t(toyear)).x
    	  fromy =  river_path.point(to_t(fromyear)).y
    	  fill(col)
    	  N = len(s.philosophers) 
    	  FS = 13
    	  if N == 1:
   	  	FS = 13
   	  elif N==2: 
   	  	FS = 15
   	  else: FS = 17
      	  fontsize(FS) 
    	  w, h = textmetrics(s.name)
    	  s.x, s.y = fromx, fromy + 600
    	  stroke(0)
    	  k = -50
       	  while cc.overlap(s.x, s.y, tox-fromx, h+10):
    	  	s.y += k
           
 	  cc.add_object(s.x, s.y, tox-fromx, h+10)
    	  
       	  col.alpha = 100
    	  stroke(col)
    	  text(s.name, s.x + (tox - fromx)/2 -w/2, s.y + 10)
        	  # philosophers
	  fontsize(9)
	  align(LEFT)
    	  col.alpha = 100
    	  fill(col)
    	  rect(s.x, s.y, tox - fromx, 10, roundness=0.5)
    	  nofill()
    	  rect(s.x, s.y, tox - fromx, h +10)
    	  for p in  s.philosophers:
    	  	fill(col)
    	  	txt = "%s" % (p.name)
    	  	w, h = textmetrics(p.name)
    	  	text(txt, p.x - w/2 , s.y + 10 + 2*h/3)
    	  	util.circle(p.x, s.y+10, 5)
    	  	fill(255)
    	  	w = textwidth(str(p.y1))
    	  	text(str(p.y1), p.x - w/2, s.y + h/2)
    	  fill(col)
    	  
  
    	  
#
#
#
def draw_schools_wiki(schools):
	
  if not ALL and not DRAW_SCHOOLS:
    	return
    	
  # sort by name
  textw = 200
  schools.sort() 
  y = BORDER_TOP / 2 
  x = (BORDER_LEFT - textw) / 2
  align(JUSTIFY)
  for s in schools:
    # wiki text
    txt = util.wikipedia(s.name)
    if txt and s.philosophers:
      if s.type == "theory":
    	  col = colors.color("chocolate")
      else: col = colors.color("peru")
      fontsize(9)
      H = textheight(txt, width= textw)
      h = textheight(s.name)
      if y > HEIGHT - BORDER_TOP / 2 :
      	y = BORDER_TOP / 2
      	x = WIDTH - (BORDER_RIGHT - textw) / 2 - textw
      fill(col)
      text(s.name, x, y, width= textw)
      fill(colors.color("dimgray"))
      text(txt, x, y + h, width= textw)
      y += H + h + 15
      
#
#
#
def draw_books(river_path):
	
	wmax = 250
	ccontroller = CollisionController(WIDTH, HEIGHT)
	c = colors.color("slategray")
	fill(c)
	stroke(c)
	strokewidth(0.5)
	k = 0.8
	lineheight(k)
	align(LEFT)
	for b in books:
		fontsize(14)
		y = HEIGHT - 2*BORDER_TOP
		t = to_t(b.year())
		x = b.author.x
		w, hh = textmetrics(b.name, width=wmax)
		fontsize(9)
		h = textheight("a")
		ls = h * k / (1 + k) 
		w2, h2 = textmetrics(b.author.name)
		while ccontroller.overlap(int(x), int(y), int(w), int(hh + h2)):
			y +=5
		ccontroller.add_object(x, y, w, hh + h2)
		#line(x, y, x + w, y + 2)
		util.circle(x, y, 5)
		fontsize(15)
		text(b.name, x, y, width=wmax)
		fontsize(9)
		push()
		skew(x=10)
		text(b.author.name, x + w/4, y + hh - 2*ls)
		pop()
		
		
		


#
#
#
def draw_events(river_path, col):
    """ Draw events. """
    
    if not ALL and not DRAW_EVENTS:
    	return
   
    col = c
    col.alpha = 250
    align(LEFT)
    fill(col)
    stroke(col)
    strokewidth(0.5)
    font("Arial")
    fontsize(11)
    side = -1
    cpt = 0
    lineheight(0.9)
    for e in events:
        align(LEFT)
        font("Helvetica-Bold")
        year = "(%i)" % e.y1
        yw, yh= textmetrics(year)
        font("Helvetica")
        tw, th = textmetrics(e.name, width=150)
        fill(col)
        t = to_t(e.y1)
        # TODO if y2 > y1 --> period
        pt = river_path.point(t)
        e.x = pt.x
        e.y = pt.y
        star(e.x, e.y, 7, 5, 3)
        d = 250
        if cpt % 2 == 0:
        	d = d + th
        	to_x, to_y = e.x, e.y - d
        else:
        	to_x, to_y = e.x, e.y + d
        
        push()
        translate(to_x, to_y)
        col2 = colors.color(233,238,247, range=255)
        fill(col2)
        rect(-tw/2, -yh/2, tw, th + yh/2, roundness=0.3)
        fill(col)
        text(e.name, -tw/2, yh/2 + 3, width=150)
        font("Helvetica-Bold")
        text(year, -yw/2 , 0, width=yw+10)
        stroke(col)
        pop()
        if cpt % 2 == 0:
        	delta = th
        else: delta = -yh/2
        line(e.x, e.y, to_x, to_y + delta)
        c.alpha= 250
        side = side * -1
        cpt +=1
        cc.add_object(to_x, to_y - yh, tw, th + yh)   
    font("Helvetica")


############################
#  
#   LOAD DATA
#
# ###########################
        
#
def load_data():
    """ Load data. """
   
    global periods_dict, philosophers, centuries, theories, schools, schools_dict, events, books

    # periods
    periods_dict = domain.load(2, domain.Period)
    
    # schools & theories
    schools_dict = domain.load(4, domain.School)
    schools = [s for (i, s) in schools_dict.iteritems()]    

    # philosophers
    philosophers_dict = domain.load(0, domain.Philosopher, schools_dict)
    philosophers = [p for (i,p) in philosophers_dict.iteritems()  if p.importance >= 4 and p.y2 <> 0 and p.name <> '' and p. haslivedin(FR, TO)]
    philosophers.sort(key=lambda obj:obj.y1)
    
    # books
    books = domain.load(5, domain.Book, philosophers_dict)
    books = domain.get_list(books)
    books.sort(key = lambda b: b.year)

    
    schools.sort(key=lambda obj:obj.year)

    # centuries
    centuries = domain.load(3, domain.Century)
    
    # events
    events_dict = domain.load(1, domain.Event)
    events = [e for (i, e) in events_dict.iteritems() if e.y1 > FR]
    events.sort(key=lambda obj:obj.y1)


############################
#  
#   COLOR ASSIGNATIONS
#
# ###########################

#
def assign_colors():
    """ Assign colors. """
    
    # periods
    periods_dict[1].color = c2
    periods_dict[2].color = c3
    periods_dict[3].color = c4
    periods_dict[4].color = c5
    periods_dict[7].color = c6
    periods_dict[8].color = c7
    periods_dict[9].color = c8
    periods_dict[11].color = c9
    periods = [p for (i,p) in periods_dict.iteritems() if p.color]
    periods.sort()

    # philosophers
    for p in philosophers:
        philosopher_periods = p.contemporaries(periods)
        if philosopher_periods:
            if philosopher_periods[0].color <> None:
                p.color = philosopher_periods[0].color
        if p.color == None: p.color = c # default    

############################
#  
#  MAIN
#
# ###########################

def __main__():
    
    __setup__()
        
    load_data()
    
    assign_colors()
    
    # get river path
    path = get_river_path()

    # fraw legend
    draw_title()

    # draw background
    draw_background(path)

    # draw density
    draw_courbe(path, philosophers, colors.color("slategray"))

    # draw periods
    p = periods_dict[1] # presocratiques di=1
    draw_period(p.name, p.color, p.y1, p.y2, path)
    p = periods_dict[2] # classique id = 2
    draw_period(p.name, p.color, p.y1, p.y2, path)
    p = periods_dict[3] # hellenisme id = 3
    draw_period(p.name, p.color,p.y1, p.y2,path)
    p = periods_dict[4] # antiquite tardive id = 4
    draw_period(p.name, p.color, p.y1, p.y2, path)
    p = periods_dict[7] # philosophie medievale id = 7
    draw_period(p.name, p.color, p.y1, p.y2, path)
    p = periods_dict[8] # renaissance id = 8
    draw_period(p.name, p.color, p.y1, p.y2, path)
    p = periods_dict[9] #lumieres id = 9
    draw_period(p.name, p.color, p.y1, p.y2, path)
    p = periods_dict[11]# contemporain id = 11
    draw_period(p.name, p.color, p.y1, p.y2, path)
   
    #
    draw_riverarea(path, philosophers)
    
    # draw river
    draw_river(path)

    # draw centuries
    draw_centuries(path)

    colormode(RGB, range=255)
    
    # draw philosophers
    D = 20
    delta = 35
    k = -1
    util.noshadow()
    cpt = 0
    for p in philosophers:
        if p.image:
        	 cpt += 1
        draw_philosopher(p, path, cpt, D)
        D += delta
        if D == 0: D += delta
        if D >= 150:
	   D = -150 - (k+1)*delta/4
	   k = -1 * k

    # draw events
    draw_events(path, colors.named_color("royalblue"))


    # draw schools and theories
    draw_schools(path, schools)
    draw_schools_wiki(schools)
        
    # draw books
    draw_books(path)
   
    


if __name__ == '__main__':
	main()

__main__()

#canvas.save("philo8.png")

