"""
  Author:       Gilbert Perrin <gilbert.perrin@gmail.com>
  Project:      POSTER PHILO
  Date:         2007-2008
  Description:  Program generation of a philosophy poster.
"""
__version__ = "1"

var ("DRAW_BACKGROUND", BOOLEAN, default=False)
var ("DRAW_RIVER", BOOLEAN, default=False)
var ("DRAW_PERIODS", BOOLEAN, default=False)
var ("DRAW_EVENTS", BOOLEAN, default=False)
var ("DRAW_SCHOOLS", BOOLEAN, default=False)
var ("DRAW_CENTURIES", BOOLEAN, default=False)
var ("DRAW_PHILOSOPHERS", BOOLEAN, default=False)
var ("DRAW_BOOKS", BOOLEAN, default=False)
var ("DRAW_DENSITY", BOOLEAN, default=False)
var ("ALL", BOOLEAN, default=True)


############################
#
#   IMPORTS
#
############################

# pyhon core libraries
from math import sqrt, atan, degrees
from nodebox.graphics import *
from AppKit import *
from time import time

# nodebox libraries
coreimage = _ctx.ximport("coreimage")
reload(coreimage)
supershape = _ctx.ximport("supershape")
reload(supershape)
colors = ximport("colors")
reload(colors)
svg = ximport("svg")
reload(svg)

# philo libraries 
util = ximport("util")
reload(util)
from domain import *


############################
#
#   CONSTANTS & SETUP
#
############################

size(6600, 2700)

CC = util.CollisionController(WIDTH, HEIGHT)
FR, TO = -700, 1950

BORDER_TOP, BORDER_DOWN = 400, 400
BORDER_LEFT, BORDER_RIGHT = 600, 600

IMG_DIR = "images/"

c = colors.rgb(132, 162, 212, a = 100, range=255)

title = "  LA RIVIERE PHILOSOPHIQUE  "

colormode(RGB, range=255)

############################
#
#   CONSTANT STYLES
#
############################

titlestyle = util.Style(
            fillcolor = None, 
            strokecolor = colors.color("slategray"), 
            fontsize = 65, 
            font = "Arial Bold", 
            align = CENTER, 
            strokewidth = 5)
                
bgdstyle = util.Style(
            fillcolor = colors.color("slategray"), 
            strokecolor = colors.color("slategray"), 
            fontsize = 20, 
            font = "Arial Bold", 
            align = CENTER, 
            strokewidth = 0.5)

riverstyle = util.Style(
            fillcolor = None, 
            strokecolor = c, 
            fontsize = 11, 
            font = "Arial Bold", 
            align = CENTER, 
            strokewidth = 3)
                
courbestyle = util.Style(
            fillcolor = colors.color("slategray"), 
            strokecolor = colors.color("slategray"),
            fontsize = 11, 
            font = "Arial", 
            align = CENTER, 
            strokewidth = 0.8)
                
periodstyle = util.Style(
            strokecolor = None, 
            fontsize = 20, 
            font = "Arial")


############################
#
#   DRAW FUNCTIONS
#
# ###########################

def draw_title(style = titlestyle):
	"""draw title
	"""
 	style.apply()
	w = textwidth(title)
	rect(10, 10 , WIDTH - 20, HEIGHT - 20)
	style.fillcolor = style.strokecolor
	style.apply()
	text(title, WIDTH / 2 - w / 2, 80)

@util.logtime
def draw_background(style = bgdstyle):
  """Draw the background
  """
  if not ALL and not DRAW_BACKGROUND:
  	return
  style.apply()
  for year in range(FR, TO, 100):
  	x = river.point(year).x
  	util.linedash(x, BORDER_TOP, x, HEIGHT - BORDER_DOWN)
  	util.linedash(x, BORDER_TOP - 300, x, BORDER_TOP - 80)
  	util.linedash(x, HEIGHT - BORDER_DOWN + 300, x, HEIGHT - BORDER_DOWN +80)
  	w, h = textmetrics(str(year))
  	text(str(year), x - w / 2, BORDER_TOP + 20)
  	text(str(year), x - w / 2, BORDER_TOP - 270)
  	text(str(year), x - w / 2, HEIGHT - BORDER_DOWN - 20)

@util.logtime
def draw_river(style = riverstyle):
  """draw river
  """
  if not ALL and not DRAW_RIVER:
  	return
  style.apply()
  drawpath(river.path)
  style.fillcolor = style.strokecolor
  style.strokecolor = None
  D = 30
  d = 10
  for year in range(FR, TO, 100):
      p = river.point(year)
      style.apply()
      util.circle(p.x, p.y, D)
      w,h = textmetrics(str(year))
      fill(1)
      text(str(year), p.x - w / 2, p.y + 2.5)
  
  draw_riverarea()
  

def draw_riverarea():
  """draw river area
  """
  nostroke()
  c.alpha = 0.2
  fill(c)
  autoclosepath(True)
  x0, y0 = river.xy(FR)
  x1, y1 = x0, y0
  reverse = []
  beginpath(x0, y0)
  for year in range(FR, TO-1, 30):
  	ct = 1.2 * db.count(year)
  	t = river.t(year)
  	a, b = util.normal(river.path, t)
  	angle = degrees(atan(a))
  	pt = river.point(year)
  	theta = angle
  	if angle < 0:
  		theta = angle + 180
  	x, y = util.coordinates(pt.x, pt.y, ct, theta)
  	k, v = random(10), random(-5, +5)
  	if x > x1:
  		curveto(x1 + k, y1 + v, x - k, y - v, x, y)
  		x1, y1 = x, y
  	if angle < 0:
  		theta = angle
  	else: theta = angle - 180
  	reverse.append((util.coordinates(pt.x, pt.y, ct, theta)))
  reverse.reverse()
  x0, y0 = reverse[0]
  x1, y1 = (x + x0) / 2 + 50, (y + y0) / 2
  curveto(x + 20, y, x1, y1 + 20, x1, y1)
  curveto(x1, y1 - 20, x0 + 20, y0, x0, y0)
  x1, y1 = x0, y0
  for x,y in reverse:
  	k, v = random(-10), random(-5, +5)
  	if x < x1:
  		curveto(x1 + k, y1 + v, x - k, y - v, x, y)
  		x1, y1 = x, y
  p = endpath(draw = True)


@util.logtime
def draw_courbe(style = courbestyle):
  """draw courbe density
  """
  if not ALL and not DRAW_DENSITY:
    	return
  style.apply()
  x0, y0 = river.point(FR).x, HEIGHT - BORDER_DOWN + 200
  xmax = river.point(TO).x
  line(x0, y0, xmax, y0)
  c = 8
  x1, y1 = x0, y0
  autoclosepath(True)
  beginpath(x0, y0)
  ymax = y0
  for year in range(FR, TO - 1, 100):
      d = db.density(year , year + 1)
      x, y = river.point(year).x, y0 - d * c
      curveto(x1 + 20, y1, x - 20, y, x, y)
      x1, y1 = x, y
      #util.circle(x, y, 0.5)
      if year % 100 == 0:
      	 w, h = textmetrics(str(year))
      	 text(str(year), x - w / 2, y0 + h)
      #line(x, y0, x, y)
  lineto(xmax, y0)
  p = endpath(draw=False)
  colors.gradientfill(p, colors.color("white"), style.fillcolor, type = "linear")

@util.logtime
def draw_periods():
  """Draw the period.
  """
  if not ALL and not DRAW_PERIODS:
  	return
  w = 40
  for p in db.periods:
    p.style.apply()
    p1 = river.point(p.y1)
    p2 = river.point(p.y2)
    x1 = p1.x
    x2 = p2.x
    h = textheight(p.name)
    # top
    ytop = BORDER_TOP - w
    util.rectround(x1, ytop, x2 - x1 - 6, h, clr = p.style.fillcolor, txt = p.name)
    # down
    ydown = HEIGHT - BORDER_DOWN + w
    util.rectround(x1, ydown, x2 - x1 - 6, h, clr = p.style.fillcolor, txt = p.name)


@util.logtime
def draw_centuries():
  """Draw centuries.
  """
  if not ALL and not DRAW_CENTURIES:
  	return
  D = 50
  for cent in db.centuries:
      txt = cent.name
      util.shadow(blur = 40.0)
      pt1 = river.point(cent.y1)
      pt2 = river.point(cent.y2)
      x = (pt1.x + pt2.x) / 2
      y = HEIGHT - BORDER_DOWN - 60
      cent.style.apply()
      text(txt, x - textwidth(txt) / 2, y - D / 2)
      y = BORDER_TOP + 60
      text(txt, x - textwidth(txt) / 2, y + D / 2)

@util.logtime
def draw_philosophers() :
  """Draw philosophers.
  """
  if not ALL and not DRAW_PHILOSOPHERS:
  	return
  D = 20
  delta = 35
  k = -1
  util.noshadow()
  cpt = 0
  for p in db.philosophers:
    if p.image:
      cpt += 1
    
    pth = river.parallelpath(p.y1, p.y2, D)
    p.x = pth.point(0).x
    p.y = pth.point(0).y
    
    draw_lifeline(pth, p)
    
    stroke(p.color)
    
    # draw image if any
    draw_image(p, cpt, D)
    D += delta
    if D == 0: D += delta
    if D >= 150:
      D = -150 - (k + 1) * delta / 4
      k = -1 * k
      

def draw_lifeline(path, philosopher):
    """Draw a philosopher:
      - path: philosopher path
      - philosopher: philosopher object
    """
    dt = 0.001
   
    # get philosopher name
    name = philosopher.name
    philosopher.style.apply()
    
    # draw first part
    util.circle(philosopher.x, philosopher.y, 6)
    
    # compute letters coordinates
    n = len(name)
    ti = 0
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
    p = util.sub_path(path, 0, 1, dt = dt)
    drawpath(p)
    
    # draw letters
    for k in range(len(tp)):
        pk = tp[k]
        push()
        rotate(-pk[3])
        translate(0, textheight(pk[0]) / 4)
        text(pk[0], pk[1], pk[2])
        pop()
    
    
def draw_image(p, cpt, D=0):
  """Draw philosopher image.
  """
  if not p.image:
      pass
  
  nofill()
  fontsize(9)
  font("Arial")
  strokewidth(2)
  x, y = p.x, p.y
  if p.image != "":
      file = IMG_DIR + p.image
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
      line(p.x, p.y, x + w / 2, toy)
      #fill(p.color)
      c.alpha = 200
      fill(c)
      align(CENTER)
      toy = y + h + 10
      text(p.name, x + w / 2 - wtext / 2, toy)


@util.logtime
def draw_schools():
  """Draw schools.
  """
  if not ALL and not DRAW_SCHOOLS:
  	return
  cpt = 0
  for school in db.schools:
  	if school.philosophers:
  	  cpt += 1
  	  sig = -1 + 2 * (cpt % 2)
  	  delta = random(70)
  	  fromyear, toyear = school.dates()
  	  fromx, fromy = river.xy(fromyear)
  	  tox, toy = river.xy(toyear)
  	  school.style.fillcolor.alpha = 255
  	  school.style.apply()
  	  w, h = textmetrics(school.name)
  	  school.x, school.y = fromx, fromy + 600
  	  k = -40
  	  while CC.overlap(school.x, school.y, tox - fromx, h + 10):
  	    school.y +=  k
  	  
  	  CC.add_object(school.x, school.y, tox - fromx, h + 10)
  	  text(school.name, school.x + (tox - fromx) / 2 - w / 2, school.y + h/2 - 5)
  	  school.style.fillcolor.alpha = 200
  	  school.style.apply()
  	  nostroke()
  	  rect(school.x, school.y, tox - fromx, 5, roundness = 0.9)
  	  nofill()
  	  #rect(school.x, school.y, tox - fromx, h + 10)
  	  
  	  fontsize(10)
  	  font("Arial")
  	  school.style.fillcolor.alpha = 200
  	  fill(school.style.fillcolor)
  	  for p in  school.philosophers:
  	    txt = "%s" % (p.name)
  	    w, h = textmetrics(p.name)
  	    text(txt, p.x - w / 2 , school.y + h)
  	    util.circle(p.x, school.y + 5, 7)
	    
  draw_schools_wiki()


def draw_schools_wiki():
  """schools wikipedia
  """
  # sort by name
  textw = 200
  db.schools.sort()
  y = BORDER_TOP / 2
  x = (BORDER_LEFT - textw) / 2
  align(JUSTIFY)
  for school in db.schools:
    # wiki text
    txt = util.wikipedia(school.name)
    if txt and school.philosophers:
      if school.type == "theory":
    	  col = colors.color("chocolate")
      else: col = colors.color("peru")
      fontsize(9)
      H = textheight(txt, width= textw)
      h = textheight(school.name)
      if y > HEIGHT - BORDER_TOP / 2 :
      	y = BORDER_TOP / 2
      	x = WIDTH - (BORDER_RIGHT - textw) / 2 - textw
      fill(col)
      text(school.name, x, y, width= textw)
      fill(colors.color("dimgray"))
      text(txt, x, y + h, width= textw)
      y += H + h + 15


@util.logtime
def draw_books():
  """draw books
  """
  if not ALL and not DRAW_BOOKS:
    return
  wmax = 250
  ccontroller = util.CollisionController(WIDTH, HEIGHT)
  c = colors.color("slategray")
  fill(c)
  stroke(c)
  strokewidth(0.5)
  k = 0.8
  lineheight(k)
  align(LEFT)
  for book in db.books:
  	print book
  	print book.author
  	fontsize(14)
  	y = HEIGHT - 2*BORDER_TOP
  	x = book.author.x
  	w, hh = textmetrics(book.name, width=wmax)
  	fontsize(9)
  	h = textheight("a")
  	ls = h * k / (1 + k)
  	w2, h2 = textmetrics(book.author.name)
  	while ccontroller.overlap(int(x), int(y), int(w), int(hh + h2)):
  		y +=5
  	ccontroller.add_object(x, y, w, hh + h2)
  	#line(x, y, x + w, y + 2)
  	util.circle(x, y, 5)
  	fontsize(15)
  	text(book.name, x, y, width=wmax)
  	fontsize(9)
  	push()
  	skew(x=10)
  	text(book.author.name, x + w/4, y + hh - 2*ls)
  	pop()


@util.logtime
def draw_events(col):
  """Draw events.
  """
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
  for event in db.events:
      align(LEFT)
      font("Helvetica-Bold")
      year = "(%i)" % event.y1
      yw, yh= textmetrics(year)
      font("Helvetica")
      tw, th = textmetrics(event.name, width=150)
      fill(col)
      # TODO if y2 > y1 --> period
      event.x, event.y = river.xy(event.y1)
      star(event.x, event.y, 7, 5, 3)
      d = 250
      if cpt % 2 == 0:
      	d = d + th
      	to_x, to_y = event.x, event.y - d
      else:
      	to_x, to_y = event.x, event.y + d
      
      push()
      translate(to_x, to_y)
      col2 = colors.color(233,238,247, range=255)
      fill(col2)
      rect(-tw / 2, -yh / 2, tw, th + yh / 2, roundness=0.3)
      fill(col)
      text(event.name, -tw / 2, yh / 2 + 3, width=150)
      font("Helvetica-Bold")
      text(year, -yw / 2 , 0, width=yw+10)
      stroke(col)
      pop()
      if cpt % 2 == 0:
      	delta = th
      else: delta = -yh / 2
      line(event.x, event.y, to_x, to_y + delta)
      c.alpha = 250
      side = side * -1
      cpt += 1
      CC.add_object(to_x, to_y - yh, tw, th + yh)
  font("Helvetica")


############################
#
#   STYLE ASSIGNATIONS
#
# ###########################

@util.logtime
def assign_styles():
  """Assign styles.
  """
    
  # periods
  c2 = colors.rgb(175,201,81, a=100, range=255)
  c3 = colors.rgb(195,203,65,a=100, range=255)
  c4 = colors.rgb(204,183,64, a=100, range=255)
  c5 = colors.rgb(204,156,64, a=100, range=255)
  c6 = colors.rgb(203,109,113, a=100, range=255)
  c7 = colors.rgb(100,158,178, a=100, range=255)
  c8 = colors.rgb(137,128,201, a=100, range=255)
  c9 = colors.rgb(201,128,170, a=100, range=255)
  clrs = colors.list(c2, c3, c4, c5, c6, c7, c8, c9, "periods")
  i = 0
  for p in db.periods:
    p.style = periodstyle.copy()
    p.style.fillcolor = clrs[i]
    i += 1
    
  # centuries
  fcol = c.copy()
  fcol.alpha = 0.25
  style = util.Style(fillcolor = fcol, strokecolor = None, fontsize = 65, font = "Cochin")
  for cent in db.centuries:
    cent.style = style
  
  # philosophers
  for p in db.philosophers:
      philosopher_periods = p.contemporaries(db.periods)
      col = c
      if philosopher_periods:
          if philosopher_periods[0].color <> None:
              col = philosopher_periods[0].color
      p.style = util.Style(fillcolor=colors.color("slategray"), strokecolor=col, fontsize=16, font="Courier New", strokewidth=5)
  
  # schools  
  for s in db.schools:
    if s.philosophers:
      N = len(s.philosophers)
      fs = 13
      if N == 2:
        fs = 15
      elif N >= 3: fs = 17
      if s.type == "theory":
        col = colors.color("chocolate")
      else: col = colors.color("cadetblue")
      col.alpha = 0.2
      style = util.Style(fillcolor=col, strokecolor=col, font="Arial", fontsize=fs, strokewidth=0.8, align=LEFT)
      s.style = style
  

############################
#
#  MAIN
#
# ###########################

@util.logtime
def __main__():
	   
    util.log("Start")
    
    global db
    db = PhiloDb(fr=-700, to=1900)
    db.load()
    util.log("Load Philo DB Ok")
    
    global river
    river = util.River("data/river.svg", FR, TO, BORDER_LEFT, 2 * BORDER_TOP)
    util.log("Load River Ok")
        
    assign_styles()
    
    draw_title()
    
    draw_background()
    
    draw_courbe()
    
    draw_periods()
    
    draw_river()
    
    colormode(RGB, range=255)
    
    draw_centuries()
    
    draw_philosophers()
    
    draw_events(colors.named_color("royalblue"))
    
    draw_schools()
    
    draw_books()


if __name__ == '__main__':
	main()

__main__()

#canvas.save("philo8.png")

