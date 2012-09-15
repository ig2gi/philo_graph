from math import sqrt, atan, degrees

web = ximport("web")
reload(web)

domain = ximport("domain")
reload(domain)

util = ximport("util")
reload(util)

coreimage = ximport("coreimage")
reload(coreimage)

#graph = ximport("graph")
#reload(graph)

size(2820,2100)
#size(7009,4450)






colormode(RGB, range=255)
background(255,255,255)




''' show flags constants
'''
SHOW_PHILOSOPHERS = 1
SHOW_EVENTS = 1


''' time constants
'''
FR = -700 # from date (year)
TO = 2000 # to date (year)
dt = 1/float(TO-FR) # time unit
scale = 50  # graduation unit

''' river
'''
RS = 400 # river size 
RC = Color(114, 104, 0, 30)
RCT = Color(50,0, 200, 255)
RFS = 17 # river font size

''' categories colors
'''
C1 = Color(132,138,215, 200)
C4 = Color(169, 63,55)
C5 = Color(114,104,255)

''' fonts
'''
F1 = "Ayuthaya" # title
FS1 = 70 # title font size
F2 = "Skia" # legend
FS2 = 50 # legend font size

''' categories
''' 
IS = 12 # icon size

t0 = 0 # philosopher
t1 = 1 # religious/christianism
t2 = 2 # religious/jewish
t3 = 3 # religious/muslim
t4 = 4 # war
t5 = 5 # religious/bhudism
t6 = 6 # politic


# misc
#
img_dir = "images/"
philosophers_file = "data/philo.txt"
events_file = "data/events.txt"
BORDER = 10

centuries = ["-VIIe", "-VIe","-Ve","-IVe","-IIIe","-IIe","-Ie", "Ie", "IIe", "IIIe" , "IVe", "Ve", "VIe", "VIIe", "VIIIe", "IXe", "Xe", "XIe","XIIe", "XIIIe","XIVe","XVe","XVIe","XVIIe","XVIIIe","XIXe","XXe"]


'''

'''    
def draw_event_image(p):
    nofill()
    strokewidth(2)
    if p.image != "":
        file = img_dir + p.image
        w, h = imagesize(file)
        image(file, p.x , p.y + 3)
        rect(p.x, p.y  + 3, w, h)


'''
 
 
'''
def draw_event(e, path, direction = 1) :
    
    fontsize(8 + e.importance)
    fill(e.color)
    stroke(e.color)
    
    pt1 = path.point(to_t(e.d1 + float(e.d2 - e.d1)/2)) 
    e.x = pt1.x
    e.y = pt1.y
    d = 4 * e.importance
    
    oval(pt1.x-d/2, pt1.y-d/2, d, d)
    txt = e.years_as_string()
    txt +=  ":\n" + e.name
    h = textheight(txt, 120)
    strokewidth(1)
    if direction == 1:
        line(pt1.x, pt1.y + d/2,pt1.x,  pt1.y + lineheight() + h + 2)
        text(txt, pt1.x + 4 , pt1.y + d + 5, 100)
    else:
        line(pt1.x, pt1.y - d/2,pt1.x,  pt1.y - d - h - 2)
        text(txt, pt1.x + 4 , pt1.y- 2 - h, 100)
    nofill()
    #draw_icon(pt1.x + d  , pt1.y + 5  , self.type, self.color)
    draw_event_image(e)

        
'''


'''    
def draw_philosopher(p, path, D) :
    fs = 10 + p.importance
    fontsize(fs)
    fill(p.color)
    stroke(p.color)
    
    t1 = to_t(p.d1)
    t2 = to_t(p.d2)
    orig = path.point(t1)
    p.x = orig.x
    p.y = orig.y
           
    pth = util.get_parallel_path(path, t1, t2, D, dt)
    
    p.color.alpha = 60
    stroke(p.color)
    strokewidth(15)
    drawpath(pth)
    p.color.alpha = 255
    
    #print self

    w = textwidth(p.name)
    h = textheight(p.name)
    
    n = len(p.name)     
    ti = 0
    #print str(direc) + self.name
    for c in range(n):
        ti = float(c) / float( n) 
        direc = util.direction(pth, ti) 
        pti = pth.point(ti+ dt)
        a,b = util.tangent(pth, ti)
        angle = degrees(atan(a))
        push()
        rotate(-angle)
        if direc == 3 or direc == 4:
            c = n - c - 1
        text(p.name[c], pti.x, pti.y)
        pop()
            
    #p.draw_image()

def draw_river():
    nofill()
        
    path = get_river_path()

    copyOfPath = [pt for pt in path]
    strokewidth(RS)
    stroke(RC)
    #drawpath(path)
            
    for k in range(0, 150, 10):
            strokewidth(k)
            stroke(114, 104, 255, k/10)
            drawpath(copyOfPath)
    
    nofill
    stroke(RCT)
    strokewidth(1)
    #drawpath(copyOfPath)
               
    RC.alpha = 30    
    strokewidth(1)
    i = FR
    fontsize(RFS)
    pas = 10
    
    '''
     draw philosophy density
    '''
    for pt in path.points(int((TO-FR)/pas+1)):
        t1 = to_t(i)
        n = count_philosophers(phs, i-pas/2, i+pas/2) 
        i += pas
        d =float(n) *10
        x1 = path.point(t1).x
        y1 = path.point(t1).y
        nostroke()
        RCT.alpha = 40
        fill(RCT)
        oval(x1-d/2, y1-d/2,  d, d )           
        
    '''
     draw centuries
    '''
    D = 150
    col = color(0,0,220)
    alpha = 5
    c = 0
    for y in range (FR, TO , 100):
        draw_zone(path, y + 1, y + 99, centuries[c], D, col, alpha)
        c = c + 1
        if c >= len(centuries):
            break;
    '''
     draw periodes
    '''
    draw_zone(path, -700, -500, "Presocratique",content=False, c=color(0, 255, 0), a=100, D=160)
    draw_zone(path, -500, -400, "Classique",content=False, c=color(0, 255, 0), a=100, D=150)
    draw_zone(path, -400, -0, "Hellenistique",content=False, c=color(0, 255, 0), a=100, D=160)
    draw_zone(path, 0, 500, "Antiquite Tardive",content=False, c=color(0, 255, 0), a=100, D=150)
    draw_area(path, -700, 550, "Philosophie Antique", outline=True)
    
   
    draw_area(path, 500, 1000, "Philosophie Medievale", c=color(255, 0 , 0), outline=True)
    draw_zone(path,500, 1400, "Philosophie Medievale",content=False, c=color(255, 0, 0), a=100, D=130)
    draw_area(path, 1000, 1400, "Philosophie Medievale", c=color(255, 0 , 0), outline=True)
    
    draw_zone(path, 1650, 1770, "Lumieres",content=False, c=color(0, 0, 0), a=100, D=140)
    draw_zone(path, 1400, 1640, "Renaissance",content=False, c=color(0, 0, 0), a=100, D=150)
    draw_area(path, 1390, 1760, "Philosophie Moderne", c=color(0, 0 , 0), outline=True)
      
    draw_zone(path, 1800, 2000, "Philosophie Contemporaine",content=False, c=color(255, 255, 0), a=100, D=150)
    draw_area(path, 1800, 2000, "Philosophie Contemporaine", c=color(255, 255 ,0), outline=True)
    
     
    return path



'''
colormode(HSB)
g = graph.create(500, 500, 1000, 1000, style="default")
n1 = g.add_node("Aristote")
n1.type = "dark"
n2 = g.add_node("Platon")
n3 = g.add_node("O")
n3.type = "dark"
n1.type = "light"
g.add_edge(n1.id, n2.id)
g.add_edge(n1.id, n3.id)
g.trim()
g.solve(k=10)
g.center()
g.draw(orphans=False, centroid=True, clusters=True)
'''


def draw_title(x, y):
        
    stroke(color(0,0,0,150))
    strokewidth(1)
    fill(color(0,0,0,100))
    fontsize(50)
    text("Histoire de la \n Philosophie", x, y)
           
    
def load_philophers_fron_wikipedia():
    philo = []
    a = web.wikipedia.search("Liste_de_philosophes_par_année_de_naissance", language="fr", light=False, cached=True)
    fontsize(10)
    for paragraph in a.paragraphs:    
        if paragraph.depth == 2 or paragraph.depth == 3:
            s = str(paragraph)
            s = unicode(s.strip(), 'utf-8', errors='errors')
            for textblock in paragraph:
                for l in textblock.splitlines():
                    l = l.strip()
                    if l <> '' and l.startswith("*"):
                        philo.append(l)

    return philo

#
# to_t Function
#
def to_t(year):
    return float(year - FR)  / float(TO - FR)



'''
draw zone
'''
def draw_zone(path, y1, y2, txt='', D = 150, c=color(0,0,220), a=5, content=True):
    t1= to_t(y1)
    t2= to_t(y2)
    
    p1 = util.get_parallel_path(path, t1, t2, D, dt)
    p2 = util.get_parallel_path(path, t1, t2, -D, dt)

    c.alpha = a
    stroke(c)
    strokewidth(10)
    if content == True:
        for t in range(101):
            pt1 = p1.point(0.01*t)
            pt2 = p2.point(0.01*t)
            line(pt1.x,pt1.y,pt2.x,pt2.y)
    
    if content == False:
        drawpath(p1)
        drawpath(p2)    
    
    pt1 = path.point(t1)
    pt2 = path.point(t2)
    x = (pt1.x + pt2.x)/2
    y = (pt1.y + pt2.y)/2
    fontsize(40)
    c.alpha = 150
    fill(c)
    font("Arial")
    strokewidth(1)
    text(txt, x - textwidth(txt)/2, y - D/2)


    

    
'''
 draw area
'''
def draw_area(path, y1, y2, txt="", c=color(0, 255, 0), D=150, sw = 1, outline=False):
    c.alpha = 255
    t1= to_t(y1)
    t2= to_t(y2)
    p = util.sub_path(path, t1, t2, dt)
    
    xmin, ymin = util.xmin_ymin(p, 1)
    xmax, ymax = util.xmax_ymax(p)
    
    ymin = ymin -D
    xmin = xmin
    xmax = xmax
    
    if xmin < BORDER:
        xmin = BORDER    +1
    if xmax > WIDTH-BORDER:
        xmax = WIDTH - BORDER - 1
    if ymin < BORDER:
        ymin = BORDER + 1
        
    w = xmax - xmin
    h = ymax - ymin
    nofill()
    stroke(c)
    strokewidth(sw)
    rect(xmin,ymin ,w,h + D)
    font("Arial")
    fontsize(30)
    fill(c)
    if ymin < 0:
        ymin = 0
    strokewidth(sw)
    text(txt,xmin + w/2 - textwidth(txt)/2, ymin + textheight(txt) + 5, outline=outline)
    nofill()
    

    
#
# draw_background Function
#
def draw_background():
    canvas = coreimage.canvas(WIDTH, HEIGHT)
    l = canvas.layer("images/raffael.jpg")
    l.blend(40)
    w,h = l.size()
    print str(w) + " " + str(h)
    dw = WIDTH - w
    dh = (HEIGHT - h)/2
    print(str(dh) + " " + str(dw))
    l.scale(0.9,1.1)
    canvas.draw()
    nofill()
    strokewidth(BORDER)
    stroke(color(0,0,0,200))
    rect(0,0,WIDTH, HEIGHT)
    draw_title(10, 600)
    
    return draw_river()
   
#
# load Data Function
#
def load(file, d, log=False):
    txt = open(file).readlines()
    list = []
    for l in txt:
        if l.startswith('!!'):
            continue
        s = l.split('|')
        if log:
            print(s[0] + " " + s[1] + " " + s[2]+ " " + s[3]+ " " + s[4])
        n = unicode(s[0].strip(), 'utf-8', errors='strict')
        y1 = s[1].strip()
        y2 = s[2].strip()
        i = s[3].strip()
        img = s[4].strip()
        t = s[5].strip()
        if d == 0:
            list.append(domain.Philosopher(n, y1, y2, 0, C5, i, img ))
        else:
           list.append(domain.Event(n, y1, y2, t, C4, i, img))
    return list
    
        
        
'''

'''
class PhilosopherLoader:
    
    list = []
    
    def record(self, r):
        self.list.append(domain.Philosopher(r[0], r[1], r[2], 0, C5, r[3],r[4]  ))
        
    def get_list(self):
        return self.list
        
'''

'''
class EventLoader:
    
    list = []
    
    def record(self, r):
        self.list.append(domain. Event(r[0], r[1], r[2], r[5], C4, r[3],r[4]  ))
        
    def get_list(self):
        return self.list



def get_river_path():
    autoclosepath(close=False)
    beginpath(-20, 40)
    curveto(150, 140, 200, 110, 300, 210)
    curveto(450, 350, 700, 800, 1000, 490)
    curveto(1200, 300, 1250, 220, 1400, 180)
    curveto(1500, 150, 1600, 160, 1800, 300)
    curveto(1950, 400, 1960, 450, 2300, 350)
    curveto(3000, 180, 2700, 1000, 2000, 880)
    curveto(1700, 850, 1600, 720, 1300, 780)
    curveto(800, 900, 700, 900, 500, 1200)
    curveto(430, 1300, 400, 1850, 1000, 1400)
    curveto(1100, 1330, 1250, 1220, 1400, 1300)   
    curveto(1600, 1400, 2000, 1760, 2200, 1500)   
    curveto(2400, 1200, 2500, 1300, 3000, 1400)   
    path = endpath(False)
    return path
 
        
def count_philosophers(phs, y1, y2):
    count = 0
    for p in phs:
        if p.exists(y1, y2):
                count += 1
    return count

def count_philosophers_until(phs, year):
    count = 0
    for p in phs:
        if p.d1 <= year:
                count += 1
    return count

def draw_graphic(philosophers):
    strokewidth(1)
    stroke(100)
    y = HEIGHT - 100
    xoffset = BORDER + 10
    len = WIDTH - 2 * xoffset
    line(xoffset, y, xoffset + len, y)
    rect(xoffset, y-250, len, 300)
    fill(100)
     
    k = 0
    pas = 100
    fontsize(15)
    for year in range(FR, TO, pas):
        x = xoffset + len * (year-FR)/(TO-FR)
        line(x, y-5, x, y+5)
        w,h = textmetrics(str(year))
        text(centuries[k], x - w/2 + pas /2 , y + h, outline=True)
    
    RCT.alpha = 100
    fill(RCT)
    stroke(RCT)
    
    
    for year in range(FR, TO, 2):
        x = xoffset + len * (year-FR)/(TO-FR)
        c = count_philosophers_until(philosophers, year)
        n = count_philosophers(philosophers, year-2, year+2)
        oval(x, y +4*n, 1, 1)
        line(x,y,x,y-4*c)
        
    


# load data
philosophers = load(philosophers_file, 0)
pl = PhilosopherLoader()
#philosophers = util.load(philosophers_file, pl, 5)

el = EventLoader()
events = load(events_file,1)
phs = [p for p in philosophers  if p.importance > 2 and p.d2 <> 0 and p.name <> '' and p. in_range(FR, TO)]

# 
river_path = draw_background()
def draw():
    if SHOW_PHILOSOPHERS == 1:
        D = 50
        c = 1
        for p in phs:
            draw_philosopher(p, river_path, c * D)
            D += 20
            if D >= 180:
                D = 50
            c = c * -1
        
          
    if SHOW_EVENTS == 1:
        d = 0;
        for e in events:
            if d == 2: d = 0
            draw_event(e, river_path,d)    
            d += 1
            
    draw_graphic(phs)

            
draw()









