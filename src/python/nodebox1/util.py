"""
  Author:       Gilbert Perrin <gilbert.perrin@gmail.com>
  Project:      POSTER PHILO
  Date:         2007-2008
  Description:  Program generation of a philosophy poster.
"""
__version__ = "1"

# standards
from math import radians, degrees, atan2, pow, pi, sqrt, sin, cos
from datetime import datetime
from time import time
from Numeric import zeros
from copy import deepcopy
import traceback

# nodebox
from nodebox.graphics import *
from AppKit import *
import colors
import web
import svg


def wikipedia(slug, lang='fr'):
  """wikipedia
  """
  article = web.wikipedia.search(slug, language=lang, light=False, cached=True)
  if article.paragraphs:
      paragraph = article.paragraphs[0]
      return paragraph[0]  # first text block
  return ""


def xmin_ymin(path, limit=0):
  """xmin_ymin
  """
  xmin = min(p.x for p in path.points())
  ymin = min(p.y for p in path.points())
  return xmin, ymin


def xmax_ymax(path):
  """xmax_ymax
  """
  xmax = max(p.x for p in path.points())
  ymax = max(p.y for p in path.points())
  return xmax, ymax


def tangent(path, t, dt=0.01):
  """tangent
  """
  o1 = path.point(t)
  o2 = path.point(t + dt)
  a =  (o2.y - o1.y) / (o2.x-o1.x)  # pente tangente
  b = o1.y - a*o1.x
  return a,b


def normal(path, t, dt=0.01):
  """normal
  """
  o1 = path.point(t)
  o2 = path.point(t + dt)
  a =  (o2.y - o1.y) / (o2.x - o1.x)  # pente tangente
  b = o1.y - a * o1.x
  an = - 1 / a
  bn = b + o1.x * (a + 1 / a)
  return an, bn


def sub_path(path, t1, t2, dt=0.01):
  """sub_path
  """
  t = t1
  o = path.point(t)
  x1, y1 = o.x, o.y
  _ctx.autoclosepath(close=False)
  _ctx.beginpath()
  _ctx.moveto(x1, y1)
  while t <= t2:
      t += 10 * dt
      if t >= t2:
          break
      o = path.point(t)
      x2, y2 = o.x, o.y
      _ctx.lineto(x2, y2)
      x, y = x2, y2
      _ctx.moveto(x, y)
  path = _ctx.endpath(False)
  return path


def get_parallel_path(path, t1, t2, d, dt=0.01):
  """get_parallel_path
  """
  C = -abs(d) / d
  t = t1
  o = path.point(t)
  x1, y1 = o.x, o.y
  a, b = normal(path, t, dt)
  x = x1 + C * sqrt(pow(d, 2) / (1 + pow(a, 2)))
  y = a * x + b
  di0 = direction(path, t, dt)
  _ctx.beginpath()
  _ctx.moveto(x,y)
  _ctx.autoclosepath(close=False)
  while t <= t2:
      t = t + 10 * dt
      if t >= t2:
          break
      o = path.point(t)
      a, b = normal(path, t, dt)
      di = direction(path, t, dt)
      # dans certain cas, si d trop grand et virage trop serre, les normales se coupent et il y a retour en arriere-> diminuer d
      if di == 1 and di0 == 4:
          pass
      elif (di <> di0) :
          C = C * -1
      x2 = o.x + float(C * sqrt(pow(d, 2) / (1 + pow(a, 2))))
      y2 = a * x2 + b
      _ctx.lineto(x2, y2)
      x, y = x2, y2
      di0 = di
      _ctx.moveto(x, y)
  path = _ctx.endpath(False)
  return path


def direction(path, t, dt=0.01):
  """direction"""
  p1 = path.point(t)
  p2 = path.point(t + dt)
  deltax = p2.x - p1.x
  deltay = p2.y - p1.y
  if deltax > 0 and deltay > 0:
      return 1
  if deltax > 0 and deltay < 0:
      return 2
  if deltax < 0 and deltay < 0:
      return 3
  if deltax < 0 and deltay > 0:
      return 4


class shadow(Grob):
  """shadow
  """
  
  def __init__(self, x=10, y=10, alpha=1, blur=4.0):
      Grob.__init__(self, _ctx)
      self._shadow = NSShadow.alloc().init()
      self._shadow.setShadowOffset_((x, -y))
      self._shadow.setShadowColor_(_ctx.color(0, 0, 0, alpha)._rgb)
      self._shadow.setShadowBlurRadius_(blur)
      self.draw()
  
  def _draw(self):
      self._shadow.set()


def noshadow():
  """noshadow
  """
  shadow(alpha=0)


def linedash(x1, y1, x2, y2, segment=10, gap=5):
  """linedash
  """
  p = _ctx.line(x1, y1, x2, y2, draw=False)
  p. _nsBezierPath.setLineDash_count_phase_([segment, gap], 2, 0)
  _ctx.drawpath(p)


def link(x1, y1, x2, y2, direct=True, mode=1, segment=10, gap=5):
  """link
  """
  if direct:
      linedash(x1, y1, x2, y2, segment, gap)
  else:
      if mode == 1:
          x11 = x1
          y11 = y1 + (y2 - y1) / 2
          x22 = x2
          y22 = y11
      else:
          x11 = x1 + (x2 - x1) / 2
          y11 = y1
          x22 = x11
          y22 = y2
      linedash(x1, y1, x11, y11, segment, gap)
      linedash(x11, y11, x22, y22, segment, gap)
      linedash(x22, y22, x2, y2, segment, gap)


def circle(x, y, D):
  """define an oval that draws from the centre.
  """
  return _ctx.oval(x - D / 2, y - D / 2, D, D)


def rectround(x, y, w, h, clr=colors.rgb(0, 0 , 0), txt='', draw=True, clr2=colors.rgb(1, 1, 1)):
  """rectround
  """
  p = _ctx.rect(x, y, w, h, roundness=1)
  if txt != '':
      _ctx.fill(clr2)
      wt, ht = _ctx.textmetrics(txt)
      _ctx.text(txt, x + w / 2 - wt / 2, y + h - ht / 4)
      _ctx.fill(clr)
  return p


def angle(x0, y0, x1, y1):
  """The angle between two points.
  """
  a = degrees(atan2(y1 - y0, x1 - x0))
  return a


def distance(x0, y0, x1, y1):
  """The distance between two points.
  """
  return sqrt(pow(x1 - x0, 2) + pow(y1 - y0, 2))


def coordinates(x0, y0, distance, angle):
  """The location of a point based on angle and distance.
  """
  x1 = x0 + cos(radians(angle)) * distance
  y1 = y0 + sin(radians(angle)) * distance
  return x1, y1


def reflect(x0, y0, x1, y1, d=1.0, a=180):
  """The reflection of a point through an origin point.
  """
  d *= distance(x0, y0, x1, y1)
  a += angle(x0, y0, x1, y1)
  x, y = coordinates(x0, y0, d, a)
  return x, y


class CollisionController:
  """CollisionController
  """
  
  def __init__(self, width, height):
      self.width = width
      self.height = height
      self.matrix = zeros([width, height])
  
  def add_object(self, x, y, w, h):
      xmax = min(x + w, self.width - 1)
      ymax = min(y + h, self.height - 1)
      for i in range(x, xmax):
          for j in range(y, ymax):
              self.matrix[i][j] = 1
  
  def overlap(self, x, y, w, h):
      x = int(x)
      y = int(y)
      w = int(w)
      h = int(h)
      xmax = min(x + w, self.width - 1)
      ymax = min(y + h, self.height - 1)
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


class River:
  """River
  """
  
  def __init__(self, svgfile, fr, to, x0, y0):
    self.fr = fr
    self.to = to
    data = open(svgfile).read()
    paths = svg.parse(data)
    self.path = paths[0]
    self.path.fit(x = x0, y = y0)
    self.dt = 1 / float(to - fr) # time unit
  
  def t(self, year):
    """t(year) -> t in [0,1] with year in [fr,to]"""
    return float(year - self.fr) / float(self.to - self.fr)
  
  def year(self, t):
    """year(t) -> year with t in [0,1] and year in [fr,to]"""
    return int (self.fr + t * (self.to - self.fr))
  
  def xy(self, year):
    """xy(year) -> (x, y)"""
    pt = self.point(year)
    return pt.x, pt.y
  
  def point(self, year):
    """point(year) -> point (nodebox path point)"""
    return self.path.point(self.t(year))
  
  def parallelpath(self, fromyear, toyear, D):
    """parallelpath"""
    return get_parallel_path(self.path, self.t(fromyear), self.t(toyear), D, self.dt)


class Style:
  """ Style
  """
  
  black = colors.color("black")
  
  def  __init__ (self, fillcolor=None, strokecolor=None, strokewidth=1, font="Arial", fontsize=10, align=None, lineheight=1.2):
    self.fillcolor = fillcolor
    self.strokecolor = strokecolor
    self.strokewidth = strokewidth
    self.font = font
    self.fontsize = fontsize
    self.lineheight = lineheight
    self.align = align
  
  def apply(self):
    """apply"""
    if self.fillcolor:
      _ctx.fill(self.fillcolor)
    else: _ctx.nofill()
    if self.strokecolor:
      _ctx.stroke(self.strokecolor)
    else: _ctx.nostroke()
    _ctx.strokewidth(self.strokewidth)
    _ctx.font(self.font)
    _ctx.fontsize(self.fontsize)
    _ctx.lineheight(self.lineheight)
    if not self.align:
      _ctx.align(LEFT)
    else: _ctx.align(self.align)
    
  def copy(self):
    style = Style()
    if self.fillcolor:
      style.fillcolor=self.fillcolor.copy()
    if self.strokecolor:
      style.strokecolor=self.strokecolor.copy()
    style.font = self.font
    style.fontsize = self.fontsize
    style.strokewidth = self.strokewidth
    return style

def log(message):
  """log function: to be replaced by logging API
  """
  now = datetime.now()
  now = now.strftime("%Y-%m-%d %H:%M:%S")
  print "%s : %s" % (now, message)


def logtime(func):
  """log time function decorator
  """
  def wrapper(*__args, **__kw):
    t1 = time()
    try:
      return func(*__args,**__kw)
    finally:
      t2 = time()
      msg = "%s (%.2fs)" % (func.__name__, (t2 - t1))
      log(msg)
  return wrapper

    
  
    

  
  
  
  