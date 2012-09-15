size(800, 800)
align(JUSTIFY)
fill(0)
fontsize(15)
x, y =  WIDTH/2, HEIGHT/2
translate(x, y)
rect(0, 0, 50, 50)
fill(0.9, 0 , 0)
k = 0.8
lineheight(k)
txt = "ajsfgddsgfjhdsgfdgdhdgssgdfsdfkgsddfgsdgfh" 
w, hh = textmetrics(txt, width=200)
h = textheight("a")
ls = h * k / (1 + k) 
lh = h - ls
print lh
text(txt, 0, 0, width=200, height=None)
fill(0, 0.8,0)
rect(0, hh, 10, 10)
fontsize(10)
skew(x=20)
text("dasdas", w/2, hh - ls, width=200)
