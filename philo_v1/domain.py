#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""  
  Author:       Gilbert Perrin <gilbert.perrin@gmail.com>
  Project:      POSTER PHILO
  Date:         2007-2008
  Description:  Program generation of a philosophy poster.
"""
__version__ = "1"

import sys
import os
import xlrd
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
    parentid = None
    if row[4].ctype != xlrd.XL_CELL_EMPTY:
       parentid = int(row[4].value)
    return Period(int(row[0].value), str(row[3].value), int(row[1].value), int(row[2].value), parentid)
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
    return Event(int(row[0].value), str(row[1].value), int(row[2].value), int(row[3].value), 0, int(row[6].value), importance = int(row[4].value))
  create = staticmethod(create)


class Book:
  """docstring for Book
  """
  
  def __init__(self, id, name, description):
    self.id = id
    self.name = name
    self.description = description
    
  def create(row, dict_philosophers):
    p = dict_philosophers.get(int(row[3].value))
    b = Book(int(row[0].value), str(row[1].value), str(row[2].value))
    p.addbook(b)
    return b
  create = staticmethod(create)
  
  def __str__(self):
    return "%s (%s)" % (self.name, self.author.name) 
  
  def year(self):
    """docstring for year"""
    return int((self.author.y1 + self.author.y2) / 2)
    

class Philosopher(Event):
  """Philosopher
  """
  
  def __init__(self, id, name, y1, y2, type, schools, color = None,  importance = 1, image="") :
      Event.__init__(self, id, name, y1, y2, 0, color, importance, image)
      self.schools = schools
      self.books = []
  
  def addbook(self, book):
    """docstring for addbook"""
    self.books.append(book)
    book.author = self
    
  
  def __str__(self):
    return "%s: %s" % (self.name, "-".join(str(s) for s in self.schools))
  
  def create(row, dict_schools):
    schoolids = str(row[7].value)
    schools = ()
    if schoolids:
      schools = [dict_schools.get(int(float(s))) for s in schoolids.split(",")]
    p = Philosopher(int(row[0].value), str(row[1].value), int(row[2].value), int(row[3].value), 0, schools, importance = int(row[4].value), image = str(row[5].value))
    for sc in schools:
      sc.add_philosopher(p)
    return p
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
    return School(int(row[0].value), str(row[1].value), str(row[2].value))
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
    return Century(int(row[0].value), str(row[3].value), int(row[1].value), int(row[2].value), 0)
  create = staticmethod(create)


def get_list(d):
  """get_list
  """
  return [v for k,v in d.iteritems()]


def load(sheetindex, clazz, dict = None):
  """load
  """
  dic = {}
  book = xlrd.open_workbook("data/philo-db.xls")
  sheet = book.sheet_by_index(sheetindex)
  for i in range(1, sheet.nrows): # skip first row (header)
   row = sheet.row(i)
   if dict:
     obj = clazz.create(row, dict)
   else: obj = clazz.create(row)
   if obj:
     dic[obj.id] = obj
  return dic

def towikidot(file, db):
  f = open('/Users/gperrin/Desktop/' + file, 'w')
  f.write("++ philodb %s\n" % strftime("%a, %d %b %Y %Hh", gmtime()))
  f.write("**Philosophers**: %i\n" % len(db.philosophers))
  f.write("**Schools**: %i\n" % len(db.schools))
  f.write("**Books**: %i\n\n" % len(db.books))
  
  content = "\n".join(["%s" % wikidot(p, db) for p in db.philosophers])
  f.write(content)
  
def wikidot(philosopher, db):
  name = philosopher.name.strip()
  name = name.replace(" ", "_")
  name = name.replace("'", "_")
  years = "%i:%i" % (philosopher.y1, philosopher.y2)
  schools = " _\n".join(s.name for s in philosopher.schools)
  if schools == "":
    schools = " "
  centuries = "/".join(c.name for c in  philosopher.contemporaries(db.centuries))
  books = " _\n".join(b.name for b in philosopher.books)
  imp = " "
  if philosopher.importance >= 4:
    imp = "X"
  if books == "":
     books = " "
  return "||{{%s}}||[wikipedia:%s %s] ^^(%s)^^||%s||%s||%s||" % (centuries, name.replace(" ", "_"), philosopher.name,years, schools, books, imp)


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
     # periods
    periods_dict = load(2, Period)
    self.periods = [e for (i, e) in periods_dict.iteritems() if e.parentid <> None]
    # schools & theories
    schools_dict = load(4, School)
    self.schools = get_list(schools_dict)  
    self.schools.sort(key=lambda obj:obj.year) 
    # philosophers
    philosophers_dict = load(0, Philosopher, schools_dict)
    self.philosophers = [p for (i,p) in philosophers_dict.iteritems()  if p.importance >= self.imp and p.y2 <> 0 and p.name <> '' and p.haslivedin(self.fr, self.to)]
    self.philosophers.sort(key=lambda obj:obj.y1)
    # books
    books = load(5, Book, philosophers_dict)
    self.books = get_list(books)
    self.books.sort(key = lambda b: b.year)
    # centuries
    centuries_dict = load(3, Century)
    self.centuries = get_list(centuries_dict)
    # events
    events_dict = load(1, Event)
    self.events = [e for (i, e) in events_dict.iteritems() if e.y1 > self.fr]
    self.events.sort(key=lambda obj:obj.y1)


def main():
  db = PhiloDb(-700, 1900, imp=1)
  db.load()
  for s in db.schools:
    if s.name == "Atomisme":
      print "\n".join(str(p) for p in s.philosophers)
      print s.dates()
  print time()
  print "---------- Schools: -------------"
  print "\n".join("%s -- %s" % (str(p.dates()), str(p)) for p in db.schools)
  print "------------ Books: -------------"
  print "\n".join("%s" % str(b) for b in db.books)
  print "------------ Periods: -------------"
  print "\n".join("%s" % str(b) for b in db.periods)
  print "----------- Philosophers: ---------------"
  print "\n".join("%s %i" % (str(p), p.y1) for p in db.philosophers)
  print ",".join(["%s" % p for p in db.philosophers[0].contemporaries(db.centuries)])
  print "----------- WIKIDOT: ---------------"
  towikidot("philodb.txt", db)
  


if __name__ == '__main__':
  print DatedObject.__doc__
  main()


