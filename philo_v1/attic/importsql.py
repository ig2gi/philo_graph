#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Gilbert Perrin on 2008-02-07.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import domain
import MySQLdb
import sys
import os


def main():
  db = MySQLdb.connect(user="home", passwd="home",db="home")
  c = db.cursor()
  
  # EVENT TYPES
  c.execute("INSERT INTO `home`.`philo_eventtype` (id,name) VALUES (1,'CENTURY')")
  c.execute("INSERT INTO `home`.`philo_eventtype` (id,name) VALUES (2,'PERIOD')")
  c.execute("INSERT INTO `home`.`philo_eventtype` (id,name) VALUES (3,'HISTORICAL')")
  
  # SCHOOLS
  schools_dict = domain.load(4, domain.School)
  schools = domain.get_list(schools_dict)
  for s in schools:
    typ = 'E'
    if s.type == "theory":
      typ = 'D'
    query = '''INSERT INTO philo_school (id, name, school_type) VALUES (%i, "%s", "%s")''' % (s.id, s.name, typ)
    c.execute(query)
    print "OK" + query
    
  # CENTURIES
  centuries = domain.load(3, domain.Century)
  centuries = domain.get_list(centuries)
  for cent in centuries:
    query = '''INSERT INTO `home`.`philo_event` (id, name, from_year, to_year, event_type_id) VALUES (%i, "%s", %i, %i, %i)''' % (cent.id, cent.name, cent.y1, cent.y2, 1)
    c.execute(query)
    print "OK" + query
    
  # PERIODS
  periods = domain.load(2, domain.Period)
  periods = domain.get_list(periods)
  periods.sort(key = lambda p: p.parentid)
  for p in periods:
    query = '''INSERT INTO `home`.`philo_event` (name, from_year, to_year, event_type_id) VALUES ("%s", %i, %i, %i)''' % (p.name, p.y1, p.y2, 2)
    c.execute(query)
    print "OK" + query
    
  # PHILOSOPHERS
  philosophers = domain.load(0, domain.Philosopher, schools_dict)
  philosophers = domain.get_list(philosophers)
  for p in philosophers:
    query = '''INSERT INTO `home`.`philo_philosopher` (id, name, from_year, to_year, importance, image) VALUES (%i, "%s", %i, %i, %i, "%s")''' % (p.id, p.name, p.y1, p.y2, p.importance, p.image)
    c.execute(query)
    print "OK" + query
  
  for s in schools:
    if s.philosophers:
      for p in s.philosophers:
        query = '''INSERT INTO `home`.`philo_school_philosophers` (school_id, philosopher_id) VALUES (%i, %i);''' % (s.id, p.id)  
        c.execute(query)
        print "OK" + query
    
  # HISTORICAL EVENTS
  events = domain.load(1, domain.Event)
  events = domain.get_list(events)
  for e in events:
    query = '''INSERT INTO `home`.`philo_event` (name, from_year, to_year, event_type_id) VALUES ("%s", %i, %i, %i)''' % (e.name, e.y1, e.y2, 3)
    c.execute(query)
    print "OK" + query
  
  
  db.commit()
  
if __name__ == '__main__':
  main()

