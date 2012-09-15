class Point:
  def __init__(self, x, y):
    """docstring for __init__"""
    self.x = x
    self.y = y
    
l = [Point(34,4),Point(34,2),Point(3,50),Point(6,78),Point(3,40)]
print min(p.x for p in l)