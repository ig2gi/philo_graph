
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
    
    size(3200, 2400)

    FR = -700
    TO = 1950
    
    cc = CollisionController(WIDTH, HEIGHT)
    
    BORDER_TOP = 400
    BORDER_LEFT, BORDER_RIGHT = 400, 400
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
    

    data = open("river2.svg").read()
    paths = svg.parse(data)
    path = paths[0]
    path.fit(x=BORDER_LEFT, y=BORDER_TOP)
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
def draw_background():
    """ Draw the background"""
    if not ALL and not DRAW_BACKGROUND:
    	return
    
    pass
 
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
def draw_period(txt, c, year1,year2, path, location, xmin=0,ymin=0,xmax=0,ymax=0, pas=40):
    """ Draw the period. """
    
    if not ALL and not DRAW_PERIODS:
    	return
    
    c.alpha=1
    w=40
    fill(c)
    nostroke()
    fontsize(17)
    p1=path.point(to_t(year1))
    p2=path.point(to_t(year2))
    x1 = p1.x
    y1 = p1.y
    x2 = p2.x
    y2 = p2.y
    if(xmin>0):
        x1 = xmin - w
    if(xmax>0):
        x2 = xmax + w
    if(ymin>0):
        y1 =ymin -w 
    if(ymax>0):
        y2 =ymax + w
        
    strokewidth(0.8)
    c.alpha = 0.7
    stroke(c)
    
    if location == 'N':
        text(txt, x1 + (x2-x1)/2 - textwidth(txt)/2, BORDER_TOP -w -1+ textheight(txt)/1.5)
        line(x1, BORDER_TOP - w, x2, BORDER_TOP - w)

    if location == 'E':
        line(WIDTH - BORDER_RIGHT + w, y1, WIDTH - BORDER_RIGHT + w, y2)
          
    if location == 'O':
       line(BORDER_LEFT - w, y1, BORDER_LEFT - w, y2)
           
    if location == 'S':
        line(x1, HEIGHT - BORDER_DOWN +w, x2, HEIGHT - BORDER_DOWN + w) 
        text(txt, x1 + (x2-x1)/2 - textwidth(txt)/2, HEIGHT-BORDER_DOWN + 4 + textheight(txt))
      
#
#
#
def draw_zone(path, y1, y2, col, txt='', D = 50, content=False):
    """ Draw a zone. """
        	
    t1= to_t(y1)
    t2= to_t(y2)
    p1 = util.get_parallel_path(path, t1, t2, D, dt)
    p2 = util.get_parallel_path(path, t1, t2, -D, dt)
    col.alpha=255
    stroke(col)
    fill(col)
    strokewidth(1)
    if content == True:
        for t in range(101):
            pt1 = p1.point(0.01*t)
            pt2 = p2.point(0.01*t)
            line(pt1.x,pt1.y,pt2.x,pt2.y)
    pt1 = path.point(t1)
    pt2 = path.point(t2)
    x = (pt1.x + pt2.x)/2
    y = (pt1.y + pt2.y)/2
    fontsize(30)
    col.alpha = 0.25
    fill(col)
    font("Cochin")
    fontsize(85)
    strokewidth(1)
    text(txt, x - textwidth(txt)/2, y -D/2)

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
    font("Courier New Bold")
    fontsize(14)
    
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
        pos = 0 # 0: top 1: down
        if p.y1 < 300:
        	y = BORDER_TOP - 70 - h
        	pos = 0
        if p.y1 > 300 and p.y1 < 900:
        	y = BORDER_TOP - 140 - h
        	pos = 0
        if p.y1 > 900:
        	y = HEIGHT - BORDER_DOWN + 70 
        	pos = 1
        if cpt % 2 == 0:
        	if pos == 0:
        	   y += -h -20
        	else: y += h + 20
        x = x - w/2
        image(file, x , y)
        c = colors.color("slategray")
        c.alpha = 100
        stroke(c)
        rect(x, y, w, h)
        strokewidth(0.5)
        wtext, htext = textmetrics(p.name)
        toy = y + h + htext
        if pos == 1:
        	toy = y - htext
        line(p.x, p.y, x + w/2, toy)
        #fill(p.color)
        c.alpha = 200
        fill(c)
        align(CENTER)
        if pos == 1:
        	toy = y - 3
        else: toy = y + h + 10 
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
    	  else: col = colors.color("peru")
    	  cpt += 1
    	  t = to_t(s.year)
    	  pt = river_path.point(t)
    	  a,b = util.normal(river_path, t)
    	  angle = degrees(atan(a))
    	  sig = -1 + 2*(cpt%2)
    	  print "%s %i" % (s.name, sig)
    	  delta = random(70)
    	  fill(col)
    	  N = len(s.philosophers) 
    	  FS = 13
    	  if N == 1:
   	  	FS = 13
   	  elif N==2: 
   	  	FS = 15
   	  else: FS = 17
   	  fontsize(9)
   	  hest = len(s.philosophers) * textheight("A")
   	  fontsize(FS) 
    	  w, h = textmetrics(s.name)
    	  s.x, s.y = util.coordinates(pt.x, pt.y, (200 + delta) * sig, angle)
    	  stroke(0)
       	  while cc.overlap(int(s.x), int(s.y), int(w), int(h+hest)):
    	  	s.x += random(-150, 150)
    	  	s.y += random(-150, 150)
           
 	  cc.add_object(int(s.x), int(s.y), int(w), int(h+hest))
    	  col.alpha= 20
    	  stroke(col)
    	  for p in s.philosophers:
    	  	line(s.x + w/2, s.y, p.x, p.y)
    	  col.alpha = 100
    	  stroke(col)
    	  text(s.name, s.x, s.y)
    	  line(s.x, s.y, s.x + w, s.y)    	  
        	  # philosophers
	  fontsize(9)
	  align(RIGHT)
    	  yp = s.y + h/2
    	  col.alpha = 200
    	  fill(col)
    	  l = s.philosophers
    	  l.sort(key=lambda p: p.y1)
    	  for p in s.philosophers:
    	  	txt = "%s  %i" % (p.name, p.y1)
    	  	text(txt, s.x - w, yp, width = 2*w)
    	  	yp += textheight(txt) + 2
       	  col.alpha = 50
    	  fill(col)
    	  push()
    	  transform(CORNER)
    	  translate(s.x + w - 10, yp )
    	  rotate(-90)
    	  arrow( 0,  0, yp-s.y)
    	  pop()
  
    	  
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
    for e in events:
        fill(col)
        t = to_t(e.y1)
        # TODO if y2 > y1 --> period
        pt = river_path.point(t)
        e.x = pt.x
        e.y = pt.y
        star(e.x, e.y, 7, 5, 3)
        a,b = util.normal(river_path, t)
        angle = degrees(atan(a))
        d = 170
        if cpt % 2 == 0:
        	to_x, to_y = util.coordinates(e.x, e.y, d, angle)
        	to_x2, to_y2 = util.coordinates(e.x, e.y, d-15, angle)
        else:
          to_x, to_y = util.coordinates(e.x, e.y, -d, angle)
          to_x2, to_y2 = util.coordinates(e.x, e.y, -d +15, angle)
        line(e.x, e.y, to_x2, to_y2)
        push()
        translate(to_x, to_y)
        align(LEFT)
        font("Helvetica-Bold")
        year = "%i" % e.y1
        yw, yh= textmetrics(year)
        text(year, 0 , 0, width=yw+10)
        font("Helvetica")
        text(e.name, 3, yh, width=100)
        stroke(col)
        tw, th = textmetrics(e.name, width=100)
        col.alpha = 20
        fill(col)
        rect(-2, -yh, tw, th + yh + 10)
        pop()
        c.alpha= 250
        side = side * -1
        cpt +=1
        cc.add_object(to_x, to_y - yh, tw, th + yh)   


############################
#  
#   LOAD DATA
#
# ###########################
        
#
def load_data():
    """ Load data. """
   
    global periods_dict, philosophers, centuries, theories, schools, schools_dict, events

    # periods
    periods_dict = domain.load(2, domain.Period)
    
    # schools & theories
    schools_dict = domain.load(4, domain.School)
    schools = [s for (i, s) in schools_dict.iteritems()]
    

    # philosophers
    philosophers_dict = domain.load(0, domain.Philosopher, schools_dict)
    philosophers = [p for (i,p) in philosophers_dict.iteritems()  if p.importance > 4 and p.y2 <> 0 and p.name <> '' and p. in_range(FR, TO)]
    philosophers.sort(key=lambda obj:obj.y1)
    
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
    draw_background()

    # draw periods
    p = periods_dict[1] # presocratiques di=1
    draw_period(p.name, p.color, p.y1, p.y2, path, location='N', xmin=BORDER_LEFT)
    draw_period("", p.color, -680, -510, path, location='O', ymin=BORDER_TOP)
    p = periods_dict[2] # classique id = 2
    draw_period(p.name, p.color, p.y1, p.y2, path, location='N')
    p = periods_dict[3] # hellenisme id = 3
    draw_period(p.name, p.color,-400,0,path, location='N')
    p = periods_dict[4] # antiquite tardive id = 4
    draw_period(p.name, p.color, 0, 121, path,  location='N', xmax=WIDTH-BORDER_RIGHT)
    draw_period("", p.color, 120, 390, path, location='E', ymin=BORDER_TOP)
    p = periods_dict[7] # philosophie medievale id = 7
    draw_period("", p.color, 600, 1150, path, location='O', ymax=HEIGHT-BORDER_DOWN)
    draw_period(p.name, p.color,1120,1400,path, location='S', xmin = BORDER_LEFT)
    p = periods_dict[8] # renaissance id = 8
    draw_period(p.name, p.color, p.y1, p.y2, path, location='S')
    p = periods_dict[9] #lumieres id = 9
    draw_period(p.name, p.color, p.y1, p.y2, path, location='S')
    p = periods_dict[11]# contemporain id = 11
    draw_period(p.name, p.color, 1800, 1950, path, location='S',xmax=WIDTH-BORDER_RIGHT)
    draw_period("", p.color,1850,1950, path, location='E', ymax=HEIGHT-BORDER_DOWN)

    # draw river
    draw_river(path)

    # draw centuries
    draw_centuries(path)

    colormode(RGB, range=255)
    
    # draw philosophers
    D = 20
    delta = 30
    k = -1
    util.noshadow()
    cpt = 0
    for p in philosophers:
        if p.image:
        	 cpt += 1
        draw_philosopher(p, path, cpt, D)
        D += delta
        if D == 0: D += delta
        if D >= 120:
	   D = -120 - (k+1)*delta/4
	   k = -1 * k

    # draw events
    draw_events(path, colors.named_color("royalblue"))


    # draw schools and theories
    draw_schools(path, schools)
    draw_schools_wiki(schools)
        
   
    


if __name__ == '__main__':
	main()

__main__()

#canvas.save("philo8.png")

