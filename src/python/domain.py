#!/usr/local/bin/python2.6
# encoding: utf-8

"""  
  Author:       Gilbert Perrin <gilbert.perrin@gmail.com>
  Project:      POSTER PHILO
  Date:         2007-2008
  Description:  Program generation of a philosophy poster.
"""
__version__ = "1"

import sys
import os
from time import time, strftime, gmtime


class DatedObject:
  """DatedObject.
  """
    
  def __init__(self, y1, y2) :
      self.y1 = y1
      self.y2 = y2
  
  def years(self) :
    """years"""
    return self.y2 - self.y1
  
  def in_range(self, y1, y2):
    """in range"""
    if self.y2 == 0:
        return self.y1 >= y1
    return self.y1 >= y1 and self.y2 <= y2
  
  def __cmp__(self, other):
    return cmp(self.y1, other.y1)
  
  def iscontemporary(self, other):
    """is contemporary"""
    yo1, yo2 = other.y1, other.y2
    return self.haslivedin(yo1, yo2)
    
  def years_in(self, other):
    years = self.y2 - self.y1
    if other.y1 >= self.y1:
      years = years - (other.y1 - self.y1)
    if self.y2 >= other.y2:
      years = years - (self.y2 - other.y2)
    return years

  
  def haslivedin(self, yo1, yo2):
    """docstring for haslivedin"""
    y1, y2 = self.y1, self.y2
    a = y1 >= yo1 and y2 <= yo2
    b = y1 <= yo2 and y2 >= yo2 #and (y2 - yo2) < 50
    c = y1 <= yo1 and y2 >= yo1 #and (yo1 - y1) < 50
    d = y1 <= yo1 and y2 >= yo2
    return a or b or c or d
  
  def contemporaries(self, datedobjects):
    """contemporaries"""
    return [o for o in datedobjects if self.iscontemporary(o)]
  
  def years_as_string(self):
    """yearas string"""
    txt = str(self.y1)
    if self.y1 != self.y2:
        txt +=  "..." + str(self.y2)
    return txt


class Period(DatedObject):
  """Period
  """
  
  def __init__(self, id, name, y1, y2, parentid, col = None) :
      self.id =  id
      self.name = name
      self.color = col
      DatedObject.__init__(self, y1, y2)
      self.parentid = parentid
  
  def __str__(self):
    return "%s [%i,%i]" % (self.name, self.y1, self.y2)
  
  def create(row):
    return
  create = staticmethod(create)


class Category:
  """Category
  """
    
  def __init__(self, id, name, col = None) :
      self.id =  id
      self.name = name
      self.color = col


class Event(DatedObject):
  """Event
  """
  
  def __init__(self, id, name, y1, y2, type, color = None,  importance=1, image="") :
      self.id = id
      self.name = name
      DatedObject.__init__(self, y1, y2)
      self.importance = int(importance)
      self.image = image
      if image == 'x':
          self.image = ""
      self.type = int(type)
      self.color = color
      
  def __str__(self) :
      return "%s (%i / %i)" % (self.name, self.y1, self.y2)
  
  def create(row):
    return
  create = staticmethod(create)


class Book:
  """docstring for Book
  """
  
  def __init__(self, id, name, description):
    self.id = id
    self.name = name
    self.description = description
    
  def create(row, dict_philosophers):
    return
  create = staticmethod(create)
  
  def __str__(self):
    return "%s (%s)" % (self.name, self.author.name) 
  
  def year(self):
    """docstring for year"""
    return int((self.author.y1 + self.author.y2) / 2)
    

class Philosopher(Event):
  """Philosopher
  """
  
  def __init__(self, id, name, y1, y2, type, schools=None, color = None,  importance = 1, image="") :
      Event.__init__(self, id, name, y1, y2, 0, color, importance, image)
      self.schools = schools
      self.books = []
  
  def addbook(self, book):
    """docstring for addbook"""
    self.books.append(book)
    book.author = self
    
  
  def __str__(self):
    if self.schools:
      return "%s: %s" % (self.name, "-".join(str(s) for s in self.schools))
    return self.name
  
  def create(row, dict_schools):
    return
  create = staticmethod(create)


class School:
  """School
  """
  
  def __init__(self, id, name, type):
    self.id = id
    self.name = name
    self.type = type
    self.philosophers = []
    self.year = 0

  def add_philosopher (self, philosopher):
    """add_philosopher"""
    self.philosophers.append(philosopher)
    self.year = sum(p.y1 for p in self.philosophers) / len(self.philosophers)
  
  def __str__(self):
    return "%s (%s) %i" % (self.name, self.type, len(self.philosophers))
  
  def __cmp__(self, other):
    return cmp(self.name.lower(), other.name.lower())
    
  def dates(self):
    """docstring for dates"""
    if self.philosophers:
      fromYear = min(p.y1 for p in self.philosophers)
      toYear = max(p.y2 for p in self.philosophers)
      return fromYear, toYear

  def create(row):
    return
  create = staticmethod(create)


class Century(DatedObject):
  """Century
  """
  
  def __init__(self, id, name, y1, y2, color = None):
    self.id = id
    self.name = name
    self.color = color
    DatedObject.__init__(self, y1, y2)
  
  def __str__(self):
    return "%s [%i,%i]" % (self.name, self.y1, self.y2)
  
  def create(row):
    return
  create = staticmethod(create)


def get_list(d):
  """get_list
  """
  return [v for k,v in d.iteritems()]


class PhiloDb:
  """docstring for PhiloDb
  """
  
  def __init__(self, fr=-700, to=1900, imp=4):
    self.fr = fr
    self.to = to
    self.imp = imp 
    
  def count(self, year):
    """ count"""
    return len([p for p in self.philosophers if p.y1 <= year])
        
  def density(self, fr, to):
    """density"""
    return len([p for p in self.philosophers if p.haslivedin(fr, to)])
   
  def load(self):
    """docstring for load"""
    

def main():
  
  db = PhiloDb(-700, 1900, imp=1)
  db.load()
  print time()
  print "---------- Schools: -------------"
  #print "\n".join("%s -- %s" % (str(p.dates()), str(p)) for p in db.schools)
  print "------------ Books: -------------"
  #print "\n".join("%s" % str(b) for b in db.books)
  print "------------ Periods: -------------"
  #print "\n".join("%s" % str(b) for b in db.periods)
  print "----------- Philosophers: ---------------"
  #print "\n".join("%s %i" % (str(p), p.y1) for p in db.philosophers)
  #print ",".join(["%s" % p for p in db.philosophers[0].contemporaries(db.centuries)])

  


if __name__ == '__main__':
  print DatedObject.__doc__
  main()


